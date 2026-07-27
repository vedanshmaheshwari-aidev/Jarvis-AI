"""
correlation.py
--------------

Performs correlation analysis on numeric columns.
"""

import pandas as pd


class CorrelationAnalyzer:
    """
    Performs correlation analysis.
    """

    def analyze(self, df: pd.DataFrame) -> list[str]:

        lines: list[str] = []

        numeric = df.select_dtypes(include="number")

        # Need at least two numeric columns
        if numeric.shape[1] < 2:
            return lines

        lines.append("📈 Correlation Analysis")
        lines.append("=" * 40)
        lines.append("")

        correlation = numeric.corr(numeric_only=True)

        lines.append(correlation.round(2).to_string())

        lines.append("")

        lines.append("🔍 Relationships")

        columns = correlation.columns

        found = False

        for i in range(len(columns)):
            for j in range(i + 1, len(columns)):

                value = correlation.iloc[i, j]

                strength = ""

                abs_value = abs(value)

                if abs_value >= 0.80:
                    strength = "Very Strong"

                elif abs_value >= 0.60:
                    strength = "Strong"

                elif abs_value >= 0.40:
                    strength = "Moderate"

                elif abs_value >= 0.20:
                    strength = "Weak"

                else:
                    strength = "Very Weak"

                direction = (
                    "Positive"
                    if value >= 0
                    else "Negative"
                )

                lines.append(
                    f" • {columns[i]} ↔ {columns[j]} : "
                    f"{value:.2f} ({strength} {direction})"
                )

                found = True

        if not found:
            lines.append(" No correlations found.")

        lines.append("")

        return lines


# ======================================================
# Singleton
# ======================================================

correlation_analyzer = CorrelationAnalyzer()