from dataclasses import dataclass


@dataclass
class Config:
    # ==========================================================
    # Application
    # ==========================================================

    APP_NAME: str = "Jarvis AI OS"
    VERSION: str = "0.2.0"

    # ==========================================================
    # Ollama
    # ==========================================================

    OLLAMA_HOST: str = "http://localhost:11434"

    # ==========================================================
    # Models
    # ==========================================================

    FAST_MODEL: str = "qwen2.5:3b"
    REASONING_MODEL: str = "qwen3:8b"

    # ==========================================================
    # Planner
    # ==========================================================

    # Agents within 80% of the highest score
    # will be selected by the Planner.
    PLANNER_MATCH_THRESHOLD: float = 0.80

    # Ignore agents whose score is below this.
    PLANNER_MIN_SCORE: int = 5

    # ==========================================================
    # Memory
    # ==========================================================

    MEMORY_LIMIT: int = 30

    # ==========================================================
    # Agent Execution
    # ==========================================================

    MAX_PARALLEL_AGENTS: int = 3

    # ==========================================================
    # Output
    # ==========================================================

    ENABLE_STREAMING: bool = True

    SHOW_RESPONSE_TIME: bool = True

    DEBUG: bool = False


config = Config()