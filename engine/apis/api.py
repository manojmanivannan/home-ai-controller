from fastapi import HTTPException
from ..common.logger import log
from .opts.schemas import ConversationResponse
from typing import ClassVar, Dict, List, Tuple
from ..framework.agents.base_agent import BaseAgent
from ..framework.agents.agent_factory import AgentFactory
from langchain_core.chat_history import BaseChatMessageHistory
from ..framework.history.interface import ConversationHistoryInterface
from ..framework.history.factory import ConversationHistoryFactory
from langchain_core.messages import HumanMessage

class BaseEngineChatApi:
    subsclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseEngineChatApi.subsclasses = BaseEngineChatApi.subsclasses + (cls,)
    
    # def create_conversation(self):
    #     ...

    def make_user_prompt(
            self,
            question: str,
    ) -> ConversationResponse:
        """ make a conversation """
        ...

class EngineChatApi(BaseEngineChatApi):
    def __init__(self, conversation_id: str):
        self._agent: BaseAgent = AgentFactory.get_agent()
        self._history: ConversationHistoryInterface = ConversationHistoryFactory.get_history()
        if not self._history.get_conversation(conversation_id):
            log.info(f"Creating new conversation with id {conversation_id}")
            self._history.create_conversation(conversation_id)
        super().__init__()

    # def create_conversation(self):
    #     chat_history = self._history.create_conversation("12345", "Test conversation")
    #     return chat_history.id

    def make_user_prompt(self, question: str, conversation_id: str):
        log.debug(f"Asking agent with question {question} in conversation {conversation_id}")
        response = self._agent.get_response(chat_history=self._history.get_conversation(conversation_id), user_prompt=HumanMessage(content=question))
        return ConversationResponse(answer=response.content)
