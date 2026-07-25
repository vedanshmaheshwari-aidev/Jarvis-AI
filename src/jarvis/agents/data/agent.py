"""
agent.py
---------

Data Agent For Jarvis AI OS.

Handles data Analysis tasks.

(Currentlt placeholder implmentation.)
"""

from jarvis.agents.base import BaseAgent
from jarvis.planner.registry import DATA
from jarvis.planner.task import Task
from jarvis.agents.data.service import data_service


class DataAgent(BaseAgent):
    """
    Handles Data Analysis Tasks.
    """

    def __init__(self):
        super().__init__(DATA)


    # ======================================================
    # Validation
    # ======================================================

    def _validate(self, task: Task) -> None:
        if not task.action.strip():
            raise ValueError("Task action cannot be empty.")



    # ======================================================
    # Agent Logic
    # ======================================================
    def _run(self, task: Task) -> str:
        """
        Delegate execution to the Data Service
        """
        return data_service.execute(task)