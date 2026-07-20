"""
task_result.py
--------------

Represents the outcome of Task execution.

Every AGent Returns a TaskResult.
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class TaskResult:
    """
    Standard result returned after executing a task.
    """

   # ---------------------------------------------------------
    # Task Information
    # ---------------------------------------------------------

    # ID of the executed task

    task_id: str


         # ---------------------------------------------------------
    # Execution Status
    # ---------------------------------------------------------

    # Was the task successful?
    success:bool

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