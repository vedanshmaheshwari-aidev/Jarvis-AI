
"""
column_detector.py
------------------

Detects DataFrame columns mentioned in natural-language requests.
Supports underscores, spaces, and basic semantic aliases.
"""

import re

import pandas as pd


class ColumnDetector:
    def detect(self, df: pd.DataFrame, request: str) -> list[str]:
        """
        Return matching DataFrame columns in the order they
        appear in the user's request.
        """
        normalized_request = self._normalize(request)
        matches = []

        for column in df.columns:
            column_name = str(column)
            aliases = self._build_aliases(
                self._normalize(column_name)
            )

            earliest_position = None
            longest_match = 0

            for alias in aliases:
                pattern = self._alias_pattern(alias)
                match = re.search(pattern, normalized_request)

                if match:
                    position = match.start()

                    if (
                        earliest_position is None
                        or position < earliest_position
                    ):
                        earliest_position = position
                        longest_match = len(alias)
                    elif position == earliest_position:
                        longest_match = max(
                            longest_match, len(alias)
                        )

            if earliest_position is not None:
                matches.append(
                    (earliest_position, -longest_match, column_name)
                )

        matches.sort(key=lambda item: (item[0], item[1]))

        return [column for _, _, column in matches]

    def _normalize(self, text: str) -> str:
        """Normalize underscores, hyphens, and whitespace."""
        text = text.lower().strip()
        text = re.sub(r"[_\-]+", " ", text)
        return re.sub(r"\s+", " ", text)

    def _alias_pattern(self, alias: str) -> str:
        """Match a complete alias, not a partial word."""
        parts = alias.split()
        alias_regex = r"\s+".join(
            re.escape(part) for part in parts
        )
        return rf"(?<!\w){alias_regex}(?!\w)"

    def _build_aliases(self, column: str) -> set[str]:
        """Build aliases for common column names."""
        aliases = {column}

        semantic_aliases = {
            "salary": {
                "salary", "pay", "income", "wage", "earnings"
            },
            "age": {"age", "ages"},
            "department": {
                "department", "departments", "dept", "division"
            },
            "name": {
                "name", "names", "employee", "employees", "person"
            },
            "sales": {"sales", "sale", "revenue"},
        }

        aliases.update(semantic_aliases.get(column, set()))
        return aliases


column_detector = ColumnDetector()
