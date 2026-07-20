from dataclasses import dataclass, field
from typing import Any


@dataclass
class Task:
    """
    Represents a task created by the Planner 
    Every task is assigned to an Agent
    """

    # Which agent should execute this task?
    agent: str

    # WHat should the agent do?
    action: str

    # Priority (Higher = more important)
    priority: int = 1

    # Does it require an LLMN?
    requires_llm: bool = False


    # Additional information required by the agent
    payload: dict[str, Any] = field(default_factory=dict)