"""
task.py
-------

Represents a unit of work created by the Planner.

Every task is assigned to exactly one Agent.
"""

from dataclasses import dataclass, field
from typing import Any
from jarvis.planner.registry import AgentRule
import uuid


@dataclass
class Task:

    # ---------------------------------------------------------
    # Assignment (Required)
    # ---------------------------------------------------------

    agent: AgentRule

    action: str

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])

    # ---------------------------------------------------------
    # Scheduling
    # ---------------------------------------------------------

    priority: int = 1

    status: str = "pending"

    dependencies: list[str] = field(default_factory=list)

    # ---------------------------------------------------------
    # Execution
    # ---------------------------------------------------------

    requires_llm: bool = False

    payload: dict[str, Any] = field(default_factory=dict)

    result: Any = None