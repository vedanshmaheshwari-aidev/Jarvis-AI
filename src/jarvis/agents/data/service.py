"""
service.py
----------

Business logic for the Data Agent.

The DataService coordinates all data-related
operations such as:

    • locating files
    • reading datasets
    • analyzing data
    • maintaining dataset context
    • cleaning data (future)
    • visualizations (future)

The Agent itself remains lightweight.
"""

import re
from pathlib import Path

from jarvis.agents.data.analyzer import data_analyzer
from jarvis.agents.data.reader import data_reader
from jarvis.agents.data.request_router import data_request_router

from jarvis.agents.data.analyzers.numeric import numeric_analyzer
from jarvis.agents.data.analyzers.outlier import outlier_analyzer
from jarvis.agents.data.analyzers.categorical import categorical_analyzer
from jarvis.agents.data.analyzers.correlation import correlation_analyzer
from jarvis.agents.data.analyzers.quality import quality_analyzer

from jarvis.planner.task import Task
from jarvis.tools.file_resolver import file_resolver


class DataService:
    """
    Service layer for the Data Agent.
    """

    def __init__(self):
        # Currently loaded dataset
        self.current_path: Path | None = None
        self.current_df = None

    # ======================================================
    # Public API
    # ======================================================

    def execute(self, task: Task) -> str:
        """
        Execute a data-related task.
        """

        file_path = self._extract_file_path(task.action)

        # --------------------------------------------------
        # Case 1: A new file was provided
        # --------------------------------------------------

        if file_path is not None:

            path = file_resolver.resolve(file_path)

            # Read dataset
            df = data_reader.read(path)

            # Store dataset context
            self.current_path = path
            self.current_df = df

        # --------------------------------------------------
        # Case 2: No file, use current dataset
        # --------------------------------------------------

        elif self.current_df is not None:

            df = self.current_df

        # --------------------------------------------------
        # Case 3: No file and no dataset
        # --------------------------------------------------

        else:

            return (
                "I don't have a dataset loaded yet.\n\n"
                "Please provide a CSV or Excel file.\n\n"
                "Example:\n"
                "Analyze D:\\Data\\sales.csv"
            )

        # --------------------------------------------------
        # Determine requested analysis
        # --------------------------------------------------

        request_type = data_request_router.route(
            task.action
        )

        # --------------------------------------------------
        # Route the request
        # --------------------------------------------------

        if request_type == "full":
            return data_analyzer.analyze(df)

        if request_type == "numeric":
            return "\n".join(
                numeric_analyzer.analyze(df)
            )

        if request_type == "outlier":
            return "\n".join(
                outlier_analyzer.analyze(df)
            )

        if request_type == "categorical":
            return "\n".join(
                categorical_analyzer.analyze(df)
            )

        if request_type == "correlation":
            return "\n".join(
                correlation_analyzer.analyze(df)
            )

        if request_type == "quality":
            return "\n".join(
                quality_analyzer.analyze(df)
            )

        # --------------------------------------------------
        # Unknown request
        # --------------------------------------------------

        return (
            "I understand that you're asking about "
            "the dataset, but I couldn't determine "
            "which analysis you want.\n\n"
            "Try:\n"
            "• Show salary statistics\n"
            "• Find outliers\n"
            "• Show correlations\n"
            "• Analyze departments\n"
            "• Check data quality\n"
            "• Perform full analysis"
        )

    # ======================================================
    # Helpers
    # ======================================================

    def _extract_file_path(
        self,
        text: str
    ) -> str | None:
        """
        Extract a CSV or Excel path
        from the user's request.
        """

        pattern = (
            r'([A-Za-z]:\\[^"\']+\.(?:csv|xlsx|xls))'
        )

        match = re.search(pattern, text)

        if match:
            return match.group(1)

        return None


# ======================================================
# Singleton
# ======================================================

data_service = DataService()