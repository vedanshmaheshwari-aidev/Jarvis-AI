"""
task.py
-------

Represents a unit of work created by the Planner.

Every task is assigned to exactly one Agent.
"""

from dataclasses import dataclass, field
from typing import Any
import uuid


@dataclass
class Task:
    """
    Represents a task created by the Planner.

    A Task contains everything an Agent needs
    to perform one unit of work.
    """

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    # Unique task identifier
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])

    # ---------------------------------------------------------
    # Assignment
    # ---------------------------------------------------------

    # Which Agent should execute this task?
    agent: str = ""

    # What should the Agent do?
    action: str = ""

    # ---------------------------------------------------------
    # Scheduling
    # ---------------------------------------------------------

    # Higher number = higher priority
    priority: int = 1

    # Current task status
    # pending | running | completed | failed
    status: str = "pending"

    # Task IDs that must finish before this task
    dependencies: list[str] = field(default_factory=list)

    # ---------------------------------------------------------
    # Execution
    # ---------------------------------------------------------

    # Whether this task requires an LLM
    requires_llm: bool = False

    # Additional information for the Agent
    payload: dict[str, Any] = field(default_factory=dict)

    # Result produced after execution
    result: Any = None