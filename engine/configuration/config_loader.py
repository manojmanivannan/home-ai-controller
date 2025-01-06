import yaml
import os
from ..common.logger import log
from pydantic import BaseModel, ConfigDict,ValidationError
from typing import Optional, Union
import os.path
from enum import Enum

class Agent(Enum):
    STANDARD = "standard"
    LANGGRAPH = "langgraph"

class ModelChat(Enum):
    OLLAMA = "ollama"
    OPENAI = "openai"

class ConversationHistoryType(Enum):
    MEMORY = "memory"
    POSTGRES = "postgres"

class ModelConfig(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    model_name: str
    model_chat: ModelChat
    url: Optional[str] = None
    model_type: Optional[str] = None
    temperature: Optional[float] = None
    verbose: Optional[bool]=False
    prompt: Optional[str] = "You are a helpful assistant. You need to use tools to get information and provide the final answer" # Default system prompt

class ToolsConfig(BaseModel):
    home_automation_url: str

class EngineConfig(BaseModel):
    ask_model_config: ModelConfig
    ask_tools_config: ToolsConfig
    ask_agent: Agent
    ask_conversation_history_type: ConversationHistoryType

class ChromaConfig(BaseModel):
    host: str
    port: int
    embedding_model: str
    collection: str
    chunk_size: int
    chunk_overlap: int
    client_only: bool
    score_threshold: float

class ConfigLoader:
    _instance = None
    _default_config_file_path = os.getenv(
        "ENGINE_CONFIG_FILE_PATH", "/configuration/rules/configuration.yml"
    )
    _engine_config: EngineConfig = None
    _chroma_config: ChromaConfig = None

    def __new__(cls, config_file_path=None, *args, **kwargs):
        """
        Create and return a new instance of the ConfigLoader class.

        Parameters:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            ConfigLoader: The newly created instance of the ConfigLoader class.
        """
        if not cls._instance:
            cls._instance = super(ConfigLoader, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialize(config_file_path or cls._default_config_file_path)
        return cls._instance

    def _initialize(self, config_file_path):
        """
        Initializes the configuration loader by loading the configuration from a YAML file.

        This method reads the configuration from a YAML file located at '/configuration/rules/configuration.yml'.
        If the file is not found or an error occurs while reading the file, the method logs a warning and
        sets the configuration to a default configuration.

        The method also sets the values of various configuration parameters based on the loaded configuration.
        If a parameter is not found in the configuration, a default value is used.
        """

        log.debug(f"Loading configurations from {config_file_path}")

        try:
            with open(config_file_path, "r") as f:
                    full_engine_config = yaml.safe_load(f.read())
                    
        except Exception as e:
            log.error(f"Unable to load configuration file: {e}")
            raise e

        selected_model = full_engine_config.get("engine").get("model")

        try:
            self._engine_config = EngineConfig(
                ask_model_config=full_engine_config.get("models").get(selected_model),
                ask_tools_config=full_engine_config.get("engine").get("tools_config"),
                ask_agent=Agent.STANDARD if not full_engine_config.get("engine").get("agent") else Agent(full_engine_config.get("engine").get("agent")),
                ask_conversation_history_type=ConversationHistoryType.MEMORY if not full_engine_config.get("engine").get("history") else ConversationHistoryType(full_engine_config.get("engine").get("history")),
            )

            self._chroma_config = ChromaConfig(
                host=full_engine_config.get("chroma").get("host"),
                port=full_engine_config.get("chroma").get("port"),
                collection=full_engine_config.get("chroma").get("collection"),
                chunk_size=full_engine_config.get("chroma").get("chunk_size"),
                chunk_overlap=full_engine_config.get("chroma").get("chunk_overlap"),
                client_only=full_engine_config.get("chroma").get("client_only", True),
                embedding_model=full_engine_config.get("chroma").get("embedding_model"),
                score_threshold=full_engine_config.get("chroma").get("score_threshold", 0.5),
            )
            
        except ValidationError as exc:
            log.error("""An error occurred while validating the configuration: {}""".format(exc))
            raise exc

        log.debug(f"Selected model: {self._engine_config.ask_model_config} and agent: {self._engine_config.ask_agent}")

    @classmethod
    def reset_instance(cls):
        log.debug("Resetting ConfigLoader instance")
        cls._instance = None

    @property
    def model_config(self) -> ModelConfig:
        return self._engine_config.ask_model_config

    @property
    def tools_config(self) -> ToolsConfig:
        return self._engine_config.ask_tools_config

    @property
    def agent(self) -> Agent:
        return self._engine_config.ask_agent
    
    @property
    def conversation_history_type(self) -> ConversationHistoryType:
        return self._engine_config.ask_conversation_history_type

    @property
    def chroma_config(self) -> ChromaConfig:
        return self._chroma_config
    
    @property
    def openai_api_key(self):
        return os.getenv("OPENAI_API_KEY") or "NO_OPENAI_API_KEY_FOUND"

    @property
    def home_automation_url(self):
        return self._engine_config.ask_tools_config.home_automation_url
    
    @property
    def log_level(self):
        return os.getenv("LOG_LEVEL")