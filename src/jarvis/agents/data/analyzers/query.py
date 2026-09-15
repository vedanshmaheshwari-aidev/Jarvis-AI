"""
query.py
--------

Handles natural-language queries on a pandas DataFrame.
"""

import re
import pandas as pd


class QueryAnalyzer:

    # ======================================================
    # Main Entry Point
    # ======================================================

    def analyze(self, df: pd.DataFrame, request: str) -> list[str]:

        request_lower = request.lower().strip()

        # --------------------------------------------------
        # Employee Count
        # --------------------------------------------------

        if self._is_employee_count_request(request_lower):
            return self._count_rows(df)

        # --------------------------------------------------
        # Unique Category Count
        # --------------------------------------------------

        if self._is_unique_count_request(request_lower):

            column = self._find_column(df, request_lower)

            if column is None:
                column = self._find_semantic_column(
                    df,
                    request_lower,
                    prefer_numeric=False,
                )

            if column is not None:
                return self._unique_count(df, column)

        # --------------------------------------------------
        # Grouped Average
        # IMPORTANT: Must happen before normal ranking
        # --------------------------------------------------

        if self._is_grouped_average_request(request_lower):
            return self._grouped_average(df, request_lower)

        # --------------------------------------------------
        # Filtering
        # --------------------------------------------------

        if self._is_filter_request(request_lower):
            return self._filter_data(df, request_lower)

        # --------------------------------------------------
        # Ranking
        # --------------------------------------------------

        if self._is_ranking_request(request_lower):
            return self._rank_data(df, request_lower)

        # --------------------------------------------------
        # Age Queries
        # --------------------------------------------------

        if "oldest" in request_lower or "youngest" in request_lower:
            return self._age_query(df, request_lower)

        # --------------------------------------------------
        # Normal Column Queries
        # --------------------------------------------------

        column = self._find_column(df, request_lower)

        if column is None:
            column = self._find_semantic_column(
                df,
                request_lower,
                prefer_numeric=True,
            )

        if column is None:
            return [
                "❌ I couldn't identify which column you want to analyze."
            ]

        series = df[column].dropna()

        if series.empty:
            return [
                f"❌ Column '{column}' contains no usable values."
            ]

        # --------------------------------------------------
        # Average / Mean
        # --------------------------------------------------

        if "average" in request_lower or "mean" in request_lower:

            if not pd.api.types.is_numeric_dtype(series):
                return [
                    f"❌ '{column}' is not a numeric column."
                ]

            return [
                "📊 Query Result",
                "=" * 40,
                "",
                f"Column : {column}",
                f"Average: {series.mean():.2f}",
            ]

        # --------------------------------------------------
        # Maximum
        # --------------------------------------------------

        if (
            "maximum" in request_lower
            or "highest" in request_lower
            or re.search(r"\bmax\b", request_lower)
        ):

            if not pd.api.types.is_numeric_dtype(series):
                return [
                    f"❌ '{column}' is not a numeric column."
                ]

            return [
                "📊 Query Result",
                "=" * 40,
                "",
                f"Column  : {column}",
                f"Maximum : {series.max()}",
            ]

        # --------------------------------------------------
        # Minimum
        # --------------------------------------------------

        if (
            "minimum" in request_lower
            or "lowest" in request_lower
            or re.search(r"\bmin\b", request_lower)
        ):

            if not pd.api.types.is_numeric_dtype(series):
                return [
                    f"❌ '{column}' is not a numeric column."
                ]

            return [
                "📊 Query Result",
                "=" * 40,
                "",
                f"Column  : {column}",
                f"Minimum : {series.min()}",
            ]

        # --------------------------------------------------
        # Count
        # --------------------------------------------------

        if "count" in request_lower:

            return [
                "📊 Query Result",
                "=" * 40,
                "",
                f"Column : {column}",
                f"Count  : {series.count()}",
            ]

        # --------------------------------------------------
        # Unique
        # --------------------------------------------------

        if (
            "unique" in request_lower
            or "distinct" in request_lower
        ):

            return [
                "📊 Query Result",
                "=" * 40,
                "",
                f"Column : {column}",
                f"Unique : {series.nunique()}",
            ]

        return [
            f"❌ I understand the column '{column}', "
            "but I don't understand the requested operation."
        ]

    # ======================================================
    # Employee Count
    # ======================================================

    def _is_employee_count_request(
        self,
        request: str,
    ) -> bool:

        return any(
            phrase in request
            for phrase in [
                "how many employees",
                "number of employees",
                "count employees",
                "how many people",
            ]
        )

    def _count_rows(
        self,
        df: pd.DataFrame,
    ) -> list[str]:

        return [
            "📊 Query Result",
            "=" * 40,
            "",
            f"Employees: {len(df)}",
        ]

    # ======================================================
    # Unique Category Count
    # ======================================================

    def _is_unique_count_request(
        self,
        request: str,
    ) -> bool:

        return any(
            phrase in request
            for phrase in [
                "how many departments",
                "number of departments",
                "count departments",
                "how many categories",
                "number of categories",
            ]
        )

    def _unique_count(
        self,
        df: pd.DataFrame,
        column: str,
    ) -> list[str]:

        count = df[column].dropna().nunique()

        return [
            "📊 Query Result",
            "=" * 40,
            "",
            f"Column : {column}",
            f"Unique : {count}",
        ]

    # ======================================================
    # Filtering
    # ======================================================

    def _is_filter_request(
        self,
        request: str,
    ) -> bool:

        keywords = [
            "above",
            "below",
            "greater than",
            "less than",
            "more than",
            "under",
            "over",
            "equal to",
        ]

        return any(
            keyword in request
            for keyword in keywords
        )

    def _filter_data(
        self,
        df: pd.DataFrame,
        request: str,
    ) -> list[str]:

        # --------------------------------------------------
        # IMPORTANT:
        # For filters, prefer numeric columns.
        # This prevents "employees" from selecting Name.
        # --------------------------------------------------

        column = self._find_numeric_column(
            df,
            request,
        )

        if column is None:
            return [
                "❌ I couldn't identify a numeric column "
                "to filter."
            ]

        number_match = re.search(
            r"[-+]?\d+(?:\.\d+)?",
            request,
        )

        if not number_match:
            return [
                "❌ I couldn't identify the value "
                "to filter by."
            ]

        value = float(number_match.group())

        # --------------------------------------------------
        # Greater Than
        # --------------------------------------------------

        if (
            "above" in request
            or "greater than" in request
            or "more than" in request
            or "over" in request
        ):

            result = df[df[column] > value]
            operator = ">"

        # --------------------------------------------------
        # Less Than
        # --------------------------------------------------

        elif (
            "below" in request
            or "less than" in request
            or "under" in request
        ):

            result = df[df[column] < value]
            operator = "<"

        # --------------------------------------------------
        # Equal To
        # --------------------------------------------------

        elif "equal to" in request:

            result = df[df[column] == value]
            operator = "="

        else:

            return [
                "❌ I couldn't determine "
                "the filter condition."
            ]

        return self._format_dataframe_result(
            result,
            f"{column} {operator} {value:g}",
        )

    # ======================================================
    # Ranking
    # ======================================================

    def _is_ranking_request(
        self,
        request: str,
    ) -> bool:

        return any(
            keyword in request
            for keyword in [
                "top",
                "bottom",
                "highest",
                "lowest",
            ]
        )

    def _rank_data(
        self,
        df: pd.DataFrame,
        request: str,
    ) -> list[str]:

        # --------------------------------------------------
        # Always prefer a numeric column for ranking
        # --------------------------------------------------

        column = self._find_numeric_column(
            df,
            request,
        )

        if column is None:
            return [
                "❌ I couldn't identify a numeric "
                "column to rank."
            ]

        # --------------------------------------------------
        # Determine number of records
        # --------------------------------------------------

        number_match = re.search(
            r"\b(?:top|bottom)\s+(\d+)\b",
            request,
        )

        if number_match:
            count = int(number_match.group(1))
        else:
            count = 1

        if count <= 0:
            return [
                "❌ Ranking count must be greater than zero."
            ]

        count = min(
            count,
            len(df),
        )

        # --------------------------------------------------
        # Lowest / Bottom
        # --------------------------------------------------

        if (
            "bottom" in request
            or "lowest" in request
        ):

            result = (
                df.nsmallest(
                    count,
                    column,
                )
                .sort_values(
                    by=column,
                    ascending=True,
                )
            )

            title = f"Bottom {count} {column}"

        # --------------------------------------------------
        # Highest / Top
        # --------------------------------------------------

        else:

            result = (
                df.nlargest(
                    count,
                    column,
                )
                .sort_values(
                    by=column,
                    ascending=False,
                )
            )

            title = f"Top {count} {column}"

        return self._format_dataframe_result(
            result,
            title,
        )

    # ======================================================
    # Age Query
    # ======================================================

    def _age_query(
        self,
        df: pd.DataFrame,
        request: str,
    ) -> list[str]:

        age_column = self._find_age_column(df)

        if age_column is None:
            return [
                "❌ I couldn't find an age column."
            ]

        if "oldest" in request:

            row = df.loc[
                df[age_column].idxmax()
            ]

            title = "Oldest employee"

        else:

            row = df.loc[
                df[age_column].idxmin()
            ]

            title = "Youngest employee"

        lines = [
            "📊 Query Result",
            "=" * 40,
            "",
            f"{title}:",
        ]

        for column in df.columns:

            lines.append(
                f"  {column}: {row[column]}"
            )

        return lines

    # ======================================================
    # Grouped Average
    # ======================================================

    def _is_grouped_average_request(
        self,
        request: str,
    ) -> bool:

        has_average = any(
            word in request
            for word in [
                "average",
                "mean",
            ]
        )

        has_grouping = any(
            word in request
            for word in [
                "department",
                "departments",
                "category",
                "categories",
                "group",
                "by",
            ]
        )

        return (
            has_average
            and has_grouping
        )

    def _grouped_average(
        self,
        df: pd.DataFrame,
        request: str,
    ) -> list[str]:

        group_column = self._find_group_column(
            df,
            request,
        )

        numeric_column = self._find_numeric_column(
            df,
            request,
        )

        if group_column is None:
            return [
                "❌ I couldn't identify "
                "the grouping column."
            ]

        if numeric_column is None:
            return [
                "❌ I couldn't identify "
                "the numeric column."
            ]

        grouped = (
            df.groupby(
                group_column
            )[numeric_column]
            .mean()
            .sort_values(
                ascending=False
            )
        )

        lines = [
            "📊 Query Result",
            "=" * 40,
            "",
            f"Grouped By : {group_column}",
            f"Metric     : {numeric_column}",
            "",
            "Average by group:",
        ]

        for group, value in grouped.items():

            lines.append(
                f" • {group}: {value:.2f}"
            )

        if not grouped.empty:

            highest_group = grouped.idxmax()
            highest_value = grouped.max()

            lines.extend(
                [
                    "",
                    (
                        f"🏆 Highest Average: "
                        f"{highest_group} "
                        f"({highest_value:.2f})"
                    ),
                ]
            )

        return lines

    # ======================================================
    # Column Detection
    # ======================================================

    def _find_column(
        self,
        df: pd.DataFrame,
        request: str,
    ) -> str | None:

        words = set(
            re.findall(
                r"\b[a-zA-Z_][a-zA-Z0-9_]*\b",
                request.lower(),
            )
        )

        for column in df.columns:

            column_name = str(column).lower()

            if column_name in words:
                return str(column)

        return None

    # ======================================================
    # Semantic Column Detection
    # ======================================================

    def _find_semantic_column(
        self,
        df: pd.DataFrame,
        request: str,
        prefer_numeric: bool = False,
    ) -> str | None:

        semantic_map = {
            "salary": [
                "salary",
                "salaries",
                "pay",
                "income",
                "wage",
                "wages",
                "earning",
                "earnings",
            ],

            "age": [
                "age",
                "old",
                "young",
                "oldest",
                "youngest",
            ],

            "department": [
                "department",
                "departments",
                "team",
                "division",
                "category",
                "categories",
            ],

            "name": [
                "name",
                "employee",
                "employees",
                "person",
                "people",
            ],
        }

        # --------------------------------------------------
        # IMPORTANT FIX:
        # Use whole words instead of substring matching.
        #
        # Previously:
        #
        #     "age" in "average"
        #
        # returned True.
        #
        # Now "age" only matches when "age" is actually
        # a separate word in the request.
        # --------------------------------------------------

        words = set(
            re.findall(
                r"\b[a-zA-Z_][a-zA-Z0-9_]*\b",
                request.lower(),
            )
        )

        # --------------------------------------------------
        # First pass:
        # Numeric columns when numeric data is expected
        # --------------------------------------------------

        if prefer_numeric:

            for column in df.columns:

                column_name = str(column).lower()

                if not pd.api.types.is_numeric_dtype(
                    df[column]
                ):
                    continue

                aliases = semantic_map.get(
                    column_name,
                    [],
                )

                if any(
                    alias in words
                    for alias in aliases
                ):
                    return str(column)

        # --------------------------------------------------
        # Second pass:
        # Normal semantic detection
        # --------------------------------------------------

        for column in df.columns:

            column_name = str(column).lower()

            aliases = semantic_map.get(
                column_name,
                [],
            )

            if any(
                alias in words
                for alias in aliases
            ):
                return str(column)

        return None

    # ======================================================
    # Numeric Column Detection
    # ======================================================

    def _find_numeric_column(
        self,
        df: pd.DataFrame,
        request: str,
    ) -> str | None:

        numeric_columns = df.select_dtypes(
            include="number"
        ).columns

        if len(numeric_columns) == 0:
            return None

        # --------------------------------------------------
        # Exact column name
        # --------------------------------------------------

        column = self._find_column(
            df,
            request,
        )

        if (
            column is not None
            and pd.api.types.is_numeric_dtype(
                df[column]
            )
        ):
            return column

        # --------------------------------------------------
        # Semantic numeric detection
        # --------------------------------------------------

        column = self._find_semantic_column(
            df,
            request,
            prefer_numeric=True,
        )

        if column is not None:
            return column

        # --------------------------------------------------
        # Common natural-language hints
        # --------------------------------------------------

        if any(
            word in request
            for word in [
                "salary",
                "salaries",
                "pay",
                "income",
                "wage",
                "wages",
                "earning",
                "earnings",
            ]
        ):

            for candidate in numeric_columns:

                if (
                    str(candidate).lower()
                    == "salary"
                ):
                    return str(candidate)

        # --------------------------------------------------
        # If only one numeric column exists,
        # safely use it.
        # --------------------------------------------------

        if len(numeric_columns) == 1:
            return str(numeric_columns[0])

        return None

    # ======================================================
    # Age Column
    # ======================================================

    def _find_age_column(
        self,
        df: pd.DataFrame,
    ) -> str | None:

        for column in df.columns:

            if str(column).lower() == "age":
                return str(column)

        return None

    # ======================================================
    # Group Column
    # ======================================================

    def _find_group_column(
        self,
        df: pd.DataFrame,
        request: str,
    ) -> str | None:

        # --------------------------------------------------
        # Explicit department/category detection
        # --------------------------------------------------

        for column in df.columns:

            column_name = str(column).lower()

            if column_name == "department":

                if (
                    "department" in request
                    or "departments" in request
                ):
                    return str(column)

            if column_name == "category":

                if (
                    "category" in request
                    or "categories" in request
                ):
                    return str(column)

        # --------------------------------------------------
        # Normal column detection
        # --------------------------------------------------

        column = self._find_column(
            df,
            request,
        )

        if column is not None:

            if not pd.api.types.is_numeric_dtype(
                df[column]
            ):
                return column

        # --------------------------------------------------
        # Semantic fallback
        # --------------------------------------------------

        return self._find_semantic_column(
            df,
            request,
            prefer_numeric=False,
        )

    # ======================================================
    # Format DataFrame
    # ======================================================

    def _format_dataframe_result(
        self,
        df: pd.DataFrame,
        title: str,
    ) -> list[str]:

        lines = [
            "📊 Query Result",
            "=" * 40,
            "",
            f"{title}:",
            "",
        ]

        if df.empty:

            lines.append(
                "No matching records found."
            )

            return lines

        for _, row in df.iterrows():

            values = []

            for column in df.columns:

                values.append(
                    f"{column}={row[column]}"
                )

            lines.append(
                " • " + ", ".join(values)
            )

        lines.extend(
            [
                "",
                f"Total records: {len(df)}",
            ]
        )

        return lines


# ======================================================
# Singleton
# ======================================================

query_analyzer = QueryAnalyzer()