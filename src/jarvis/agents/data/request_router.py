"""
request_router.py
-----------------

Determines which type of data analysis
the user is requesting.
"""


class DataRequestRouter:
    """
    Routes natural-language data requests
    to the appropriate analysis service.
    """

    def route(self, text: str) -> str:

        text = text.lower().strip()

        # ----------------------------------------------
        # Outlier Analysis
        # ----------------------------------------------

        if any(
            keyword in text
            for keyword in [
                "outlier",
                "outliers",
                "unusual values",
                "anomalies",
            ]
        ):
            return "outlier"

        # ----------------------------------------------
        # Correlation Analysis
        # ----------------------------------------------

        if any(
            keyword in text
            for keyword in [
                "correlation",
                "correlations",
                "relationship",
                "relationships",
            ]
        ):
            return "correlation"

        # ----------------------------------------------
        # Query Analysis
        # ----------------------------------------------

        if self._is_query_request(text):
            return "query"

        # ----------------------------------------------
        # Categorical Analysis
        # ----------------------------------------------

        if any(
            keyword in text
            for keyword in [
                "categorical",
                "category",
                "categories",
                "department",
                "departments",
                "distribution",
            ]
        ):
            return "categorical"

        # ----------------------------------------------
        # Numeric Analysis
        # ----------------------------------------------

        if any(
            keyword in text
            for keyword in [
                "statistics",
                "statistic",
                "average",
                "mean",
                "median",
                "minimum",
                "maximum",
                "min",
                "max",
                "variance",
                "standard deviation",
                "std",
                "sum",
            ]
        ):
            return "numeric"

        # ----------------------------------------------
        # Data Quality
        # ----------------------------------------------

        if any(
            keyword in text
            for keyword in [
                "quality",
                "missing values",
                "duplicates",
                "duplicate",
                "data quality",
            ]
        ):
            return "quality"

        # ----------------------------------------------
        # Full Analysis
        # ----------------------------------------------

        if any(
            keyword in text
            for keyword in [
                "analyze",
                "analyse",
                "full analysis",
                "complete analysis",
                "eda",
                "exploratory",
            ]
        ):
            return "full"

        # ----------------------------------------------
        # Unknown
        # ----------------------------------------------

        return "unknown"

    # ==================================================
    # Query Detection
    # ==================================================

    def _is_query_request(self, text: str) -> bool:

        # ----------------------------------------------
        # Average / Mean
        # ----------------------------------------------

        if any(
            keyword in text
            for keyword in [
                "what is the average",
                "what's the average",
                "what is the mean",
                "what's the mean",
                "average salary",
                "average age",
                "average by",
                "average department",
                "average departments",
                "average category",
                "average categories",
            ]
        ):
            return True

        # ----------------------------------------------
        # Highest / Lowest / Ranking
        # ----------------------------------------------

        if any(
            keyword in text
            for keyword in [
                "what is the maximum",
                "what's the maximum",
                "what is the highest",
                "what's the highest",
                "what is the minimum",
                "what's the minimum",
                "what is the lowest",
                "what's the lowest",
                "highest paid",
                "lowest paid",
                "highest salary",
                "lowest salary",
                "highest average",
                "lowest average",
                "top",
                "bottom",
            ]
        ):
            return True

        # ----------------------------------------------
        # Count
        # ----------------------------------------------

        if any(
            keyword in text
            for keyword in [
                "how many",
                "how much",
                "number of",
                "count",
            ]
        ):
            return True

        # ----------------------------------------------
        # Sum
        # ----------------------------------------------

        if any(
            keyword in text
            for keyword in [
                "what is the sum",
                "what's the sum",
                "total salary",
                "total salaries",
                "total income",
                "total pay",
            ]
        ):
            return True

        # ----------------------------------------------
        # Filtering
        # ----------------------------------------------

        if any(
            keyword in text
            for keyword in [
                "above",
                "below",
                "greater than",
                "less than",
                "more than",
                "under",
                "over",
                "equal to",
            ]
        ):
            return True

        # ----------------------------------------------
        # Row Lookup
        # ----------------------------------------------

        if any(
            keyword in text
            for keyword in [
                "who is the oldest",
                "who's the oldest",
                "who is oldest",
                "who's oldest",
                "oldest employee",
                "oldest person",
                "who is the youngest",
                "who's the youngest",
                "who is youngest",
                "who's youngest",
                "youngest employee",
                "youngest person",
            ]
        ):
            return True

        return False


# ======================================================
# Singleton
# ======================================================

data_request_router = DataRequestRouter()