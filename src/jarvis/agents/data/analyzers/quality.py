"""
quality.py
----------

Dataset quality analysis.
"""

import pandas as pd


class QualityAnalyzer:
    """
    Performs dataset quality analysis.
    """

    def analyze(self, df: pd.DataFrame) -> list[str]:

        lines: list[str] = []

        # ======================================================
        # Missing Values
        # ======================================================

        lines.append("❌ Missing Values")

        missing = df.isnull().sum()

        if missing.sum() == 0:
            lines.append(" No missing values found.")
        else:
            for column, count in missing.items():
                if count > 0:
                    lines.append(f" • {column}: {count}")

        lines.append("")

        # ======================================================
        # Duplicate Rows
        # ======================================================

        lines.append("📑 Duplicate Rows")

        duplicates = df.duplicated().sum()

        lines.append(f" {duplicates} duplicate row(s) found.")

        lines.append("")

        # ======================================================
        # Memory Usage
        # ======================================================

        lines.append("💾 Memory Usage")

        memory = df.memory_usage(deep=True).sum()

        lines.append(f" {memory:,} bytes")

        lines.append("")

        # ======================================================
        # Column Categories
        # ======================================================

        lines.append("📂 Column Categories")

        numeric = df.select_dtypes(include="number").columns
        categorical = df.select_dtypes(exclude="number").columns

        lines.append(f" Numeric Columns: {len(numeric)}")
        lines.append(f" Categorical Columns: {len(categorical)}")

        lines.append("")

        # ======================================================
        # Data Quality Score
        # ======================================================

        lines.append("✅ Data Quality")

        score = 100

        score -= duplicates * 5
        score -= int(missing.sum())

        score = max(score, 0)

        lines.append(f" Quality Score: {score}/100")

        lines.append("")

        return lines


# ======================================================
# Singleton
# ======================================================

quality_analyzer = QualityAnalyzer()