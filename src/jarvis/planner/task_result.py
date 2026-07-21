"""
task_result.py
--------------

Represents the outcome of a Task execution.

Every Agent returns a TaskResult.
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class TaskResult:
    """
    Standard result returned after executing a Task.
    """

    # ---------------------------------------------------------
    # Task Information
    # ---------------------------------------------------------

    # ID of the executed task
    task_id: str

    # Name of the Agent that executed the task
    agent_name: str

    # ---------------------------------------------------------
    # Execution Status
    # ---------------------------------------------------------

    # Was the task successful?
    success: bool

    # ---------------------------------------------------------
    # Human-readable message
    # ---------------------------------------------------------

    message: str = ""

    # ---------------------------------------------------------
    # Result Data
    # ---------------------------------------------------------

    # Output produced by the task
    data: Any = None

    # ---------------------------------------------------------
    # Error Information
    # ---------------------------------------------------------

    # Error message if execution failed
    error: str | None = None