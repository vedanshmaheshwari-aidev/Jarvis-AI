"""
basic.py
--------

Basic dataset information.
"""

import pandas as pd


class BasicAnalyzer:
    """
    Performs basic exploratory analysis
    on a pandas DataFrame.
    """

    def analyze(self, df: pd.DataFrame) -> list[str]:

        lines: list[str] = []

        # ======================================================
        # Shape
        # ======================================================

        rows, columns = df.shape

        lines.append("📊 Dataset Analysis")
        lines.append("=" * 40)

        lines.append(f"Rows: {rows}")
        lines.append(f"Columns: {columns}")
        lines.append("")

        # ======================================================
        # Column Names
        # ======================================================

        lines.append("📋 Column Names")

        for column in df.columns:
            lines.append(f" • {column}")

        lines.append("")

        # ======================================================
        # Data Types
        # ======================================================

        lines.append("🔢 Data Types")

        for column, dtype in df.dtypes.items():
            lines.append(f" • {column}: {dtype}")

        lines.append("")

        return lines


# ======================================================
# Singleton
# ======================================================

basic_analyzer = BasicAnalyzer()