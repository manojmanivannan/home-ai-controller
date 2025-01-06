import time
from typing import Dict, Tuple
from ...configuration.config_loader import ConfigLoader
from ...common.logger import log
from ...framework.history.interface import ConversationHistoryInterface
from langchain_community.chat_message_histories import ChatMessageHistory


class WithMetadataChatMessageHistory(ChatMessageHistory):
    created: float

class StoreKey(object):

    id: str

    def __init__(self, id) -> None:
        super().__init__()
        self.id = id
    
    def __hash__(self) -> int:
        return hash((self.id))
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, StoreKey):
            return False
        return self.id == other.id


class InMemoryConversationHistory(ConversationHistoryInterface):
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(InMemoryConversationHistory, cls).__new__(cls)
            cls.stores: Dict[str, Dict[StoreKey, WithMetadataChatMessageHistory]] = {}
        return cls.instance
    
    def create_conversation(self, id: str) -> WithMetadataChatMessageHistory:
        store_key = StoreKey(id)
        if store_key not in self.stores:
            self.stores[store_key] = WithMetadataChatMessageHistory(created=time.time())
        return self.stores[store_key]
    
    def get_conversation(self, id: str) -> WithMetadataChatMessageHistory:
        store_key = StoreKey(id)
        return self.stores.get(store_key)

    def get_conversations(self, organization: str, owner: str) -> Dict[str, WithMetadataChatMessageHistory]:
        result = dict()
        if organization in self.stores:
            for k, v in self.stores.get(organization, {}).items():
                if owner == k.owner:
                    result[k.id] = v
        return result

    def update_conversation(self, id: str) -> WithMetadataChatMessageHistory:
        chat_history = self.get_conversation(id)
        return chat_history

    def delete_conversation(self, id: str) -> None:
        store = self.stores.get({})
        conversation_key = StoreKey(id)
        if conversation_key in store:
            del store[conversation_key]