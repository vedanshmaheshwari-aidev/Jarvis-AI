"""
column_detector.py
------------------

Detects which DataFrame columns the user is referring to
in a natural-language request.
"""

import re

import pandas as pd


class ColumnDetector:
    def detect(self, df: pd.DataFrame, request: str) -> list[str]:
        """
        Detect columns mentioned in the user's request.

        Returns:
            A list of matching DataFrame column names.
        """
        request = request.lower().strip()

        words = set(
            re.findall(
                r"\b[a-zA-Z_][a-zA-Z0-9_]*\b",
                request,
            )
        )

        matches = []

        for column in df.columns:
            column_text = str(column).lower().strip()

            aliases = self._build_aliases(column_text)

            if any(alias in words for alias in aliases):
                matches.append(str(column))

        return matches

    def _build_aliases(self, column: str) -> set[str]:
        """
        Build simple semantic aliases for a column name.
        """
        aliases = {column}

        semantic_aliases = {
            "salary": {"salary", "pay", "income", "wage", "earnings"},
            "age": {"age", "ages"},
            "department": {
                "department",
                "departments",
                "dept",
                "division",
                "category",
            },
            "name": {"name", "names", "employee", "employees", "person"},
            "sales": {"sales", "sale", "revenue"},
        }

        for key, values in semantic_aliases.items():
            if column == key:
                aliases.update(values)

        return aliases


column_detector = ColumnDetector()