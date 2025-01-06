from ...configuration.config_loader import ConfigLoader, ConversationHistoryType
from ...framework.history.interface import ConversationHistoryInterface
from ...framework.history.memory import InMemoryConversationHistory



class ConversationHistoryFactory:
    @staticmethod
    def get_history() -> ConversationHistoryInterface:
        match ConfigLoader().conversation_history_type:
            case ConversationHistoryType.MEMORY:
                return InMemoryConversationHistory()
            case _:
                raise ValueError("Unsupported agent type, check configuration")