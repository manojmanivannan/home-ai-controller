from langchain_core.messages import (
    BaseMessage,
    AIMessage,
    HumanMessage)
from langchain_core.chat_history import BaseChatMessageHistory
from ...common.logger import log

class Utils:
    def _init_(self):
        pass

    @staticmethod
    def convert_chat_history_to_list_msg(chat_history: BaseChatMessageHistory) -> list:
        """
        Function to convert the BaseChatMessageHistory and extract the message from the json stored as text
        :param chat_history: BaseChatMessageHistory
        :return: str
        """
        messages=[]
        for message in chat_history.messages:
            # log.debug(f"DEBUG chat history Message: {message} | class:{type(message)} | msg.type: {message.type} | attrs: {dir(message)}")
            message_content = message.content
            if message.type == "human":
                messages.append(('human',message_content))
            elif message.type == "ai":
                messages.append(('assistant', message_content))
            else:
                messages.append(f'{message_content}') #BaseMessage(content=message_content))
                
        return messages
