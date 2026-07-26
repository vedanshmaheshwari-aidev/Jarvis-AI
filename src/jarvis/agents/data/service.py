"""
service.py
----------

Business logic for the Data Agent.

The DataService coordinates all data-related
operations such as:

    • locating files
    • reading datasets
    • analyzing data
    • cleaning data (future)
    • visualizations (future)

The Agent itself remains lightweight.
"""

from pathlib import Path
import re

from jarvis.agents.data.analyzer import data_analyzer
from jarvis.agents.data.reader import data_reader
from jarvis.planner.task import Task
from jarvis.tools.file_resolver import file_resolver


class DataService:
    """
    Service layer for the Data Agent.
    """

    # ======================================================
    # Public API
    # ======================================================

    def execute(self, task: Task) -> str:
        """
        Execute a data-related task.
        """

        file_path = self._extract_file_path(task.action)

        if file_path is None:
            return (
                "I couldn't find a CSV or Excel file in your request.\n\n"
                "Example:\n"
                "Analyze D:\\Data\\sales.csv"
            )

        # Resolve the path
        path = file_resolver.resolve(file_path)

        # Read dataset
        df = data_reader.read(path)

        # Analyze dataset
        return data_analyzer.analyze(df)

    # ======================================================
    # Helpers
    # ======================================================

    def _extract_file_path(self, text: str) -> str | None:
        """
        Extract a CSV or Excel path from the user's request.
        """

        pattern = r'([A-Za-z]:\\[^"\']+\.(?:csv|xlsx|xls))'

        match = re.search(pattern, text)

        if match:
            return match.group(1)

        return None


# ======================================================
# Singleton
# ======================================================

data_service = DataService()