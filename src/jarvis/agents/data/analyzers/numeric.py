"""
numeric.py
----------

Performs numerical analysis on datasets.
"""

import pandas as pd

class NumericAnalyzer:
    """
    Perform statistical analysis
    on numeric columns.
    """

    def analyze(self, df: pd.DataFrame) -> list[str]:

        lines: list[str] = []

        # ======================================================
        # Find Numeric Columns
        # ======================================================

        numeric_columns = df.select_dtypes(include="number")

        if numeric_columns.empty:
            return lines

        lines.append("📈 Numeric Analysis")
        lines.append("=" *40)
        lines.append("")   

         # ======================================================
        # Analyze each numeric column
        # ======================================================
        
        for column in numeric_columns.columns:

            series = numeric_columns[column]

            lines.append(f"📊 {column}")
            lines.append("-" * 25)

            lines.append(f"Count  : {series.count()}")

            lines.append(f"Mean   : {series.mean():.2f}")

            lines.append(f"Median : {series.median():.2f}")

            mode = series.mode()

            if len(mode) == len(series):
                lines.append("Mode      : No unique mode")

            else:
                lines.append(f"Mode     : {mode.iloc[0]}")

            lines.append(f"Minimum   : {series.min()}")

            lines.append(f"Maximum   : {series.max()}")

            lines.append(f"Std Dev   : {series.std():.2f}")

            lines.append(f"Variance  : {series.var():.2f}")

            lines.append(f"Sum       : {series.sum()}")

            lines.append("")

        return lines




# ======================================================
# Singleton
# ======================================================

numeric_analyzer = NumericAnalyzer()