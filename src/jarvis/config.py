from dataclasses import dataclass

@dataclass
class Config:
    APP_NAME: str = "Jarvis-AI"
    VERSION: str = "0.1.0"
    MODEL: str = "qwen3:8b"
    OLLAMA_HOST: str = "http://localhost:11434"

config = Config() 