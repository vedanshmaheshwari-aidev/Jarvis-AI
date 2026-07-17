from dataclasses import dataclass


@dataclass
class Config:
    APP_NAME: str = "Jarvis AI OS"
    VERSION: str = "0.2.0"

    OLLAMA_HOST: str = "http://localhost:11434"

    FAST_MODEL: str = "qwen2.5:3b"
    REASONING_MODEL: str = "qwen3:8b"


config = Config()