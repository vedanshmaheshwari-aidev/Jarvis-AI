"""
analyzer.py
-----------

Coordinates all dataset analyzers.
"""

import pandas as pd

from jarvis.agents.data.analyzers.basic import basic_analyzer
from jarvis.agents.data.analyzers.quality import quality_analyzer
from jarvis.agents.data.analyzers.numeric import numeric_analyzer
from jarvis.agents.data.analyzers.correlation import correlation_analyzer


class DataAnalyzer:
    """
    Coordinates multiple analyzers.
    """

    def analyze(self, df: pd.DataFrame) -> str:

        report: list[str] = []

        report.extend(
            basic_analyzer.analyze(df)
        )

        report.extend(
            quality_analyzer.analyze(df)
        )

        report.extend(
            numeric_analyzer.analyze(df)
        )
        report.extend(
            correlation_analyzer.analyze(df)
        )
        return "\n".join(report)


# ======================================================
# Singleton
# ======================================================

data_analyzer = DataAnalyzer()