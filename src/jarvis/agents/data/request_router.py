"""
request_router.py
-----------
Determines which type of data analysis the user is requesting.
"""

class DataRequestRouter:
    """
    Routes natural-language data requests to the appropriate data analysis service.
    """

    def route(self, text: str) -> str:

        text = text.lower().strip()

        # ----------------------------------------------
        # Outlier Analysis
        # ----------------------------------------------

        if any(
            keyword in text for keyword in[
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

# ======================================================
# Singleton
# ======================================================

data_request_router = DataRequestRouter()