"""
query.py
--------

Handles simple column-specific data queries.
"""

import pandas as pd


class QueryAnalyzer:
    """
    Performs simple queries on dataset columns.
    """

    def analyze(self, df: pd.DataFrame, request: str) -> list[str]:
        lines: list[str] = []

        request_lower = request.lower()

        # --------------------------------------------------
        # Find column mentioned in request
        # --------------------------------------------------

        column = self._find_column(df, request_lower)

        if column is None:
            return [
                "❌ I couldn't identify which column "
                "you want to analyze."
            ]

        series = df[column].dropna()

        if series.empty:
            return [
                f"❌ Column '{column}' contains no usable values."
            ]

        # --------------------------------------------------
        # Average / Mean
        # --------------------------------------------------

        if (
            "average" in request_lower
            or "mean" in request_lower
        ):
            if not pd.api.types.is_numeric_dtype(series):
                return [
                    f"❌ '{column}' is not a numeric column."
                ]

            lines.append("📊 Query Result")
            lines.append("=" * 40)
            lines.append("")
            lines.append(f"Column : {column}")
            lines.append(f"Average: {series.mean():.2f}")

            return lines

        # --------------------------------------------------
        # Maximum / Highest
        # --------------------------------------------------

        if (
            "maximum" in request_lower
            or "highest" in request_lower
            or "max" in request_lower
        ):
            if not pd.api.types.is_numeric_dtype(series):
                return [
                    f"❌ '{column}' is not a numeric column."
                ]

            lines.append("📊 Query Result")
            lines.append("=" * 40)
            lines.append("")
            lines.append(f"Column : {column}")
            lines.append(f"Maximum: {series.max()}")

            return lines

        # --------------------------------------------------
        # Minimum / Lowest
        # --------------------------------------------------

        if (
            "minimum" in request_lower
            or "lowest" in request_lower
            or "min" in request_lower
        ):
            if not pd.api.types.is_numeric_dtype(series):
                return [
                    f"❌ '{column}' is not a numeric column."
                ]

            lines.append("📊 Query Result")
            lines.append("=" * 40)
            lines.append("")
            lines.append(f"Column : {column}")
            lines.append(f"Minimum: {series.min()}")

            return lines

        # --------------------------------------------------
        # Count
        # --------------------------------------------------

        if "count" in request_lower:
            lines.append("📊 Query Result")
            lines.append("=" * 40)
            lines.append("")
            lines.append(f"Column : {column}")
            lines.append(f"Count  : {series.count()}")

            return lines

        # --------------------------------------------------
        # Unique Values
        # --------------------------------------------------

        if (
            "unique" in request_lower
            or "distinct" in request_lower
        ):
            lines.append("📊 Query Result")
            lines.append("=" * 40)
            lines.append("")
            lines.append(f"Column : {column}")
            lines.append(f"Unique : {series.nunique()}")

            return lines

        # --------------------------------------------------
        # No recognized query
        # --------------------------------------------------

        return [
            f"❌ I understand the column '{column}', "
            "but I don't understand the requested operation."
        ]

    # ------------------------------------------------------

    def _find_column(
        self,
        df: pd.DataFrame,
        request: str,
    ) -> str | None:
        """
        Finds a dataset column mentioned in the request.
        """

        for column in df.columns:
            if str(column).lower() in request:
                return str(column)

        return None


query_analyzer = QueryAnalyzer()