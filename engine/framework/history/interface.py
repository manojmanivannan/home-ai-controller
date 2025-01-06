from abc import abstractmethod, ABC
from typing import Dict
from langchain_core.chat_history import BaseChatMessageHistory


class ConversationHistoryInterface(ABC):
    @abstractmethod
    def create_conversation(self, id: str) -> BaseChatMessageHistory:
        """Create a new conversation"""
        pass

    @abstractmethod
    def get_conversation(self, id: str) -> BaseChatMessageHistory:
        """Get a single conversation by ID"""
        pass

    @abstractmethod
    def get_conversations(self) -> Dict[str, BaseChatMessageHistory]:
        """Get a list of all conversations"""
        pass

    @abstractmethod
    def update_conversation(self, id: str) -> BaseChatMessageHistory:
        """Update a single conversation"""
        pass

    @abstractmethod
    def delete_conversation(self, id: str) -> None:
        """Delete a single conversation by ID"""
        pass