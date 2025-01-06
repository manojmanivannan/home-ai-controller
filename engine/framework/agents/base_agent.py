from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from ...configuration.config_loader import ConfigLoader

# from ...generated.models.conversation import Message
from abc import abstractmethod, ABC

from ..tools.rooms import RoomsListTool
from ..tools.devices import DevicesListTool
from ..tools.toogle_device import ToggleDeviceTool

from langchain.agents import AgentExecutor

from .utils import Utils
from ...common.logger import log
from datetime import datetime
import json


class BaseAgent(ABC):
    @abstractmethod

    def get_agent_executor(self) -> AgentExecutor:
        raise NotImplementedError()
     
    def __init__(self) -> None:
        # embeddings_initializer = EmbeddingsInitializer(ConfigLoader())
        # embeddings = embeddings_initializer.initialize_embeddings()
        # self.vector_store = ChromaDB(embeddings)
        pass

    def get_tools(self) -> list:
        """
        Returns a list of tools used by the agent.

        :param token: An optional authentication token.
        :type token: str
        :return: A list of Tool objects.
        :rtype: List[Tool]
        """

        return [
            RoomsListTool(),
            DevicesListTool(),
            ToggleDeviceTool()

        ]

    def get_response(
        self, chat_history: BaseChatMessageHistory, user_prompt: HumanMessage
    ) -> AIMessage:
        """
        Get the response from the agent based on the given chat history, token, and user prompt.

        Args:
            chat_history (BaseChatMessageHistory): The chat history object.
            token (str): The token.
            user_prompt (Message): The user prompt.

        Returns:
            Message: The response message.
        """
        response_type = "text"
        response, tool_called = self._get_response_from_agent_invoke(
            user_prompt.content,
            self.get_agent_executor(),
            chat_history
        )

        log.debug(f"Response from agent: {response}")
        
        if isinstance(response, dict) or "options" in str(response):
            response_type = "chart"

        chat_history.add_user_message(user_prompt)
        
        reply = AIMessage(
            # timestamp=datetime.now().isoformat(),
            content=self._get_response_str(response)
                )

        # Add past tool calls to conversation history as AI message
        if tool_called:
            chat_history.add_ai_message(
                AIMessage(
                    # timestamp=reply.timestamp, # set the timestamp to the same as the reply
                    content="Past tool call:" + self._get_response_str(tool_called)
                        )
            )


        chat_history.add_ai_message(reply)

        return reply

    def _get_response_from_agent_invoke(
        self,
        user_prompt: str,
        agent_executor: AgentExecutor,
        chat_history: BaseChatMessageHistory,
    ):
        """
        Function to invoke the Agent/LLM Model

        Args:
            user_prompt (str): The user prompt to be sent to the LLM model
            agent_executor (AgentExecutor): The agent executor object
            chat_history (BaseChatMessageHistory): The chat history object

        Returns:
            str: The response from the LLM model.
        """
        try:
            invoke = agent_executor.invoke(
                {
                    "input": user_prompt,
                    "chat_history": Utils.convert_chat_history_to_list_msg(
                        chat_history
                    ),
                    # "mediation_doc": "\n".join([s.page_content for s in self.vector_store.query_rag(user_prompt)]),
                    "current_date_time": datetime.now().isoformat(),
                },
                config=RunnableConfig()
            )
        except Exception as e:
            log.error(f"Agent stopped due to error: {e}")
            return "I was not able to properly find an answer for your question, please try again.."

        log.debug(f"Return from llm: {invoke}")

        return invoke["output"], []

    def _get_response_str(self, response) -> str:
        """
        Converts the given response to a string.

        Args:
            response (Any): The response to be converted.

        Returns:
            str: The response as a string.
        """
        if isinstance(response, dict):
            return json.dumps(response)
        return str(response)