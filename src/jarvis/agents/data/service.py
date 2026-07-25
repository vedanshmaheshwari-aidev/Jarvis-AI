"""
service.py
----------
Business logic for the Data Agent

The DataService coordinates all the data-related
operations such as reading files, analyzing data,
cleaning data, and generationg visuals

The Agent itself remains lightweight
"""

from jarvis.agents.data.reader import data_reader
from jarvis.planner.task import Task


class DataService:
    """
    Service layer for the Data Agent.
    """
    def execute(self, task: Task) -> str:
        """
        Execute a data-related task.

        This is currently a placeholder.

        Future workflow:

            Detect file type
                    ↓
             Read dataset
                    ↓
            Analyze dataset
                    ↓
            Clean if requested
                    ↓
          Generate visualizations
                    ↓
            Return final result
        """
        text = task.action.lower()

        if "csv" in text:
            return "CSV analysis requested."

        if "excel" in text:
            return "Excel Analysis. requested."

            
        return (
            "Data Agent received the task successfullhy.\n"
            f"Task: {task.action}"
        )


# ======================================================
# Singleton
# ======================================================

data_service = DataService()
