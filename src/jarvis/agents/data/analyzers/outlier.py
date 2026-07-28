"""
outlier.py
----------

Detects outliers using the IQR method.
"""

import pandas as pd

class OutlierAnalyzer:
    """
    Detects outliers in numeric columns.
    """
    def analyze(self, df: pd.DataFrame) -> list[str]:

        lines: list[str] = []  

        numeric = df.select_dtypes(include="number")

        if numeric.empty:
            return lines

        lines.append("🚨 Outlier Analysis")
        lines.append("=" *40)
        lines.append("")

        found_any = False

        for column in numeric.columns:

            series = numeric[column]

            q1 = series.quantile(0.25) 
            q3 = series.quantile(0.75)

            iqr = q3 - q1

            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr

            outliers = series[
                (series < lower) |
                (series > upper)
            ]

            lines.append(f"📊 {column}")
            lines.append("-" * 25)

            lines.append(f"Q1          : {q1:.2f}")
            lines.append(f"Q3          : {q3:.2f}")
            lines.append(f"IQR         : {iqr:.2f}")
            lines.append(f"Lower Limit : {lower:.2f}")
            lines.append(f"Upper Limit : {upper:.2f}")

            if outliers.empty:

                lines.append("Outliers    : None")

            else:

                found_any = True

                lines.append("Outliers")

                for value in outliers:
                    lines.append(f" • {value}")

            lines.append("")

        if not found_any:
            lines.append("✅ No outliers detected.")
            lines.append("")

        return lines


# ======================================================
# Singleton
# ======================================================

outlier_analyzer = OutlierAnalyzer()