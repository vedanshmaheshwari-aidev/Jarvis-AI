
"""
service.py
-----------

Business logic for the Data Agent.

Coordinates dataset loading, analysis, and visualization
while maintaining the currently loaded dataset.
"""

import re
from pathlib import Path

from jarvis.agents.data.analyzer import data_analyzer
from jarvis.agents.data.reader import data_reader
from jarvis.agents.data.request_router import data_request_router

from jarvis.agents.data.analyzers.query import query_analyzer
from jarvis.agents.data.analyzers.numeric import numeric_analyzer
from jarvis.agents.data.analyzers.outlier import outlier_analyzer
from jarvis.agents.data.analyzers.categorical import categorical_analyzer
from jarvis.agents.data.analyzers.correlation import correlation_analyzer
from jarvis.agents.data.analyzers.quality import quality_analyzer

from jarvis.agents.data.visualization.chart_detector import chart_detector
from jarvis.agents.data.visualization.chart_service import chart_service

from jarvis.planner.task import Task
from jarvis.tools.file_resolver import file_resolver


class DataService:
    """Service layer for the Data Agent."""

    def __init__(self):
        self.current_path: Path | None = None
        self.current_df = None

    def execute(self, task: Task) -> str:
        """Execute a data-related task."""

        file_path = self._extract_file_path(task.action)

        # Load a new dataset when a path is supplied.
        if file_path is not None:
            path = file_resolver.resolve(file_path)
            df = data_reader.read(path)

            self.current_path = path
            self.current_df = df

        # Otherwise, reuse the previously loaded dataset.
        elif self.current_df is not None:
            df = self.current_df

        else:
            return (
                "I don't have a dataset loaded yet.\n\n"
                "Please provide a CSV or Excel file.\n\n"
                "Example:\n"
                r"Analyze D:\Data\sales.csv"
            )

        # --------------------------------------------------
        # Route visualization requests first.
        # --------------------------------------------------

        chart_type = chart_detector.detect(task.action)

        if chart_type != "unknown":
            return chart_service.create_chart(df, task.action)

        # --------------------------------------------------
        # Route regular data-analysis requests.
        # --------------------------------------------------

        request_type = data_request_router.route(task.action)

        if request_type == "full":
            return data_analyzer.analyze(df)

        if request_type == "query":
            return "\n".join(
                query_analyzer.analyze(df, task.action)
            )

        if request_type == "numeric":
            return "\n".join(numeric_analyzer.analyze(df))

        if request_type == "outlier":
            return "\n".join(outlier_analyzer.analyze(df))

        if request_type == "categorical":
            return "\n".join(categorical_analyzer.analyze(df))

        if request_type == "correlation":
            return "\n".join(correlation_analyzer.analyze(df))

        if request_type == "quality":
            return "\n".join(quality_analyzer.analyze(df))

        return (
            "I understand that you're asking about the dataset, "
            "but I couldn't determine which analysis you want.\n\n"
            "Try:\n"
            "• Show salary statistics\n"
            "• Find outliers\n"
            "• Show correlations\n"
            "• Analyze departments\n"
            "• Check data quality\n"
            "• Perform full analysis\n"
            "• Show a bar chart of salary"
        )

    def _extract_file_path(self, text: str) -> str | None:
        """Extract a CSV or Excel file path from a request."""

        pattern = r'([A-Za-z]:\\[^"\r\n]+?\.(?:csv|xlsx|xls))'
        match = re.search(pattern, text)

        if match:
            return match.group(1)

        return None


data_service = DataService()
