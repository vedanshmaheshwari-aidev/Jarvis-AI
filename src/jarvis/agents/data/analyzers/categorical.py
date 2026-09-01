"""
categorical.py
-----------
Analyzes categorical columns in a pandas DataFrame.
"""

import pandas as pd

from jarvis.agents.data.analyzers import categorical

class CategoricalAnalyzer:
    """
    Performs categoerical analysis on a pandas DataFrame.
    """
    def analyze(self, df: pd.DataFrame) -> list[str]:

        lines: list[str] = []

        categorical = df.select_dtypes(include=["object", "category", "string"])
    
        if categorical.empty:
            return lines

        lines.append("📂 Categorical Analysis")
        lines.append("=" * 40)
        lines.append("")

        for column in categorical.columns:

            series = categorical[column].dropna()

            if series.empty:
                continue

            counts = series.value_counts()
            percentages = series.value_counts(normalize=True) * 100

            lines.append(f"📊 {column}")
            lines.append("-" * 25)

            lines.append(
                f"Unique Values : {series.nunique()}"
            )

            top_value = counts.index[0]
            top_count = counts.iloc[0]
            top_percent = percentages.iloc[0]

            lines.append(
                f"Most Common : "
                f"{top_value}"
                f"({top_count},{top_percent:.2f}%)"
            )

            lines.append("")
            lines.append("Value Distribution")

            for value, count in counts.items():

                percentage = percentages.loc[value]

                lines.append(
                    f" • {value}: "
                    f"{count} "
                    f"({percentage:.2f}%)"
                )

            lines.append("")

        return lines


# ======================================================
# Singleton
# ======================================================

categorical_analyzer = CategoricalAnalyzer()