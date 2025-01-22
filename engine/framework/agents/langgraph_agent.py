from langchain.agents import AgentExecutor
from ...common.logger import log
from langchain_community.chat_message_histories import ChatMessageHistory
import json

from .base_agent import BaseAgent

# from ...generated.models.conversation import Message
# from ...generated.models.message_content_inner import MessageContentInner
from datetime import datetime
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableConfig
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.messages.tool import ToolMessage

from langgraph.graph import END, StateGraph, START
from typing import Annotated
from langgraph.errors import GraphRecursionError
from typing_extensions import TypedDict

from langgraph.graph.message import AnyMessage, add_messages
from langchain_core.messages.human import HumanMessage
from langgraph.prebuilt import ToolNode
from langchain.chat_models.base import BaseChatModel
from .utils import Utils
from ...configuration.config_loader import ConfigLoader
from langchain_core.prompts import MessagesPlaceholder


class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    chat_history: list[AnyMessage]
    current_date_time: str
    mediation_doc: str


class Assistant:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def __call__(self, state: State, config: RunnableConfig):
        print("#### DEBUG: Assistant called with state: ", state)
        while True:
            result = self.runnable.invoke(state)

            # If the LLM happens to return an empty response, we will re-prompt it
            # for an actual response.
            if not result.tool_calls and (
                not result.content
                or isinstance(result.content, list)
                and not result.content[0].get("text")
            ):
                messages = state["messages"] + [("user", "Respond with a real output.")]
                state = {**state, "messages": messages}
            else:
                break
        return {"messages": result}


class LanggraphAgent(BaseAgent):
    _llm: BaseChatModel = None
    _agent_executor = None

    def __init__(self, llm: BaseChatModel):
        self._llm = llm
        super().__init__()
        
    def should_continue(self, state):
        if isinstance(state, list):
            ai_message = state[-1]
        elif messages := state.get("messages", []):
            ai_message = messages[-1]
        else:
            raise ValueError(f"No messages found in input state to tool_edge: {state}")
        if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
            value = str(
                ai_message.tool_calls[0]["args"].get("is_chart", "false")
            ).lower()
            if value == "true":
                return "final"
            return "tools"
        return END

    def check_for_error(self, state):
        if isinstance(state, list):
            ai_message = state[-1]
        elif messages := state.get("messages", []):
            ai_message = messages[-1]
        else:
            raise ValueError(f"No messages found in input state to tool_edge: {state}")

        if (
            hasattr(ai_message, "tool_call_id")
            and hasattr(ai_message, "status")
            and ai_message.status == "error"
        ):
            log.debug(f"Exiting from chart node due to agent state: {state}")
            return "error"

        return "no_error"

    def init_workflow(self):
        tools = self.get_tools()

        primary_assistant_prompt = self.prompt
        # log.debug(f"Primary Assistant Prompt: {primary_assistant_prompt}")
        
        
        runnable = primary_assistant_prompt | self._llm.bind_tools(tools)

        workflow = StateGraph(State)

        workflow.add_node("assistant", Assistant(runnable))
        workflow.add_node("tools", ToolNode(tools))
        workflow.add_node("final", ToolNode(tools))
        # Define edges: these determine how the control flow moves
        workflow.add_edge(START, "assistant")
        workflow.add_conditional_edges(
            "assistant",
            self.should_continue,
            {
                "tools": "tools",
                "final": "final",
                END: END,
            },
        )
        # Add a new conditional edge to check for errors and choose the appropriate node for charts
        workflow.add_conditional_edges(
            "final",
            # Assess agent decision
            self.check_for_error,
            {
                "error": "assistant",
                "no_error": END,
            },
        )

        workflow.add_edge("tools", "assistant")
        workflow.add_edge("final", END)

        self._agent_executor = workflow.compile()
    
    def get_agent_executor(self) -> AgentExecutor:
        #Lazy loading to support LLM mock injection in tests
        if self._agent_executor is None:
            self.init_workflow()
        return self._agent_executor

    @property
    def prompt(self):
        tools = self.get_tools()
        return ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    f"{ConfigLoader().model_config.prompt}"
                    f"\nTools available for you to use are {[t.name for t in tools]}"
                    # "\nYou have this context: {mediation_doc}."
                    "\nCurrent datetime: {current_date_time}."
                ),
                MessagesPlaceholder("chat_history"),
                MessagesPlaceholder("messages"),
            ]
        )

    def get_response(
        self, chat_history: ChatMessageHistory, user_prompt: HumanMessage
    ) -> AIMessage:
        return super().get_response(chat_history, user_prompt)

    def _get_response_from_agent_invoke(
        self,
        user_prompt: str,
        agent_executor: AgentExecutor,
        chat_history: ChatMessageHistory,
        token: str = None
    ):
        try:
            # mediation_doc = "\n".join([s.page_content for s in self.vector_store.query_rag(user_prompt)])
            # if not mediation_doc:
            #     mediation_doc = "None"
            messages = agent_executor.invoke(
                {
                    "messages": HumanMessage(content=user_prompt),
                    "chat_history": Utils.convert_chat_history_to_list_msg(chat_history),
                    # "mediation_doc": mediation_doc,
                    "current_date_time": datetime.now().isoformat(timespec="seconds"),
                },
                config=RunnableConfig(recursion_limit=20, token=token),
            )
            log.debug(f"Return from llm: {messages}")
            log.debug(f"Chat history messages list {Utils.convert_chat_history_to_list_msg(chat_history)}")
            # Capture tool calls 
            tool_called = [m.tool_calls for m in messages["messages"] if isinstance(m, AIMessage) and hasattr(m, "tool_calls")]
            # tool called is of the format [[{'name':'tool-name','args':{}}],[{'name':'tool-name','args':{}}],[]]
            log.debug(f"Tool called into chat history: {tool_called}")

        except GraphRecursionError:
            log.error("Agent stopped due to recursion limit.")
            return "I was not able to help with your request after exhausting all tools, please try again..", []
        except Exception as e:
            log.error("Unexpected exception caught:" + str(e))
            return f"I was not able to help with your request, due to {e} please try again..", []

        return messages["messages"][-1].content, [{'name': t[0].get('name'),'args':t[0].get('args')} for t in tool_called if t]