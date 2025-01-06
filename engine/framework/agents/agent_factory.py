from ...configuration.config_loader import (
    ConfigLoader, Agent, ModelChat
)
from ...common.logger import log
from typing import Union
# from .standard_agent import StandardAgent
from .langgraph_agent import LanggraphAgent
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama

class AgentFactory:
    @staticmethod
    def get_agent() -> Union[LanggraphAgent]:
        """
        Get the appropriate agent based on the model configuration.

        Returns:
            Union[DummyAgent, OpenAiAgent, OllamaAgent]: The agent instance.

        Raises:
            ValueError: If the model configuration is not supported.
        """
        model_chat = None
        match ConfigLoader().model_config.model_chat:
            case ModelChat.OLLAMA:
                model_chat= ChatOllama(
                model=ConfigLoader().model_config.model_name,
                temperature=ConfigLoader().model_config.temperature,
                verbose= ConfigLoader().model_config.verbose,
                base_url=ConfigLoader().model_config.url
            )
            case ModelChat.OPENAI:
                model_chat= ChatOpenAI(
                model_name=ConfigLoader().model_config.model_name,
                openai_api_key=ConfigLoader().openai_api_key,
                temperature=ConfigLoader().model_config.temperature,
                verbose=ConfigLoader().model_config.verbose,
            )
            case _:
                raise ValueError("Unsupported model type, check configuration")
             
        match ConfigLoader().agent:
            case Agent.LANGGRAPH:
                log.debug(f"Choosing Langgraph Agent with model {model_chat}")
                return LanggraphAgent(model_chat)
            case _:
                raise ValueError("Unsupported agent type, check configuration")