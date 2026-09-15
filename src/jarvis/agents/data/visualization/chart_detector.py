"""
chart_detector.py
-----------------

Detects the type of chart requested
by the user.
"""


class ChartDetector:
    """
    Determines which chart type best matches
    a natural-language request.
    """

    # ======================================================
    # Main Entry Point
    # ======================================================

    def detect(self, request: str) -> str:
        """
        Detect the requested chart type.

        Returns:
            str: chart type
        """

        request = request.lower().strip()

        # --------------------------------------------------
        # Scatter Plot
        # --------------------------------------------------

        if any(
            keyword in request
            for keyword in [
                "scatter",
                "scatter plot",
                "relationship between",
                "relationship of",
                "correlation plot",
                "x vs y",
                " vs ",
            ]
        ):
            return "scatter"

        # --------------------------------------------------
        # Histogram
        # --------------------------------------------------

        if any(
            keyword in request
            for keyword in [
                "histogram",
                "distribution",
                "frequency distribution",
            ]
        ):
            return "histogram"

        # --------------------------------------------------
        # Line Chart
        # --------------------------------------------------

        if any(
            keyword in request
            for keyword in [
                "line chart",
                "line graph",
                "line plot",
                "trend",
                "over time",
                "time series",
            ]
        ):
            return "line"

        # --------------------------------------------------
        # Pie Chart
        # --------------------------------------------------

        if any(
            keyword in request
            for keyword in [
                "pie chart",
                "pie graph",
                "pie",
                "proportion",
                "percentage breakdown",
                "share of",
            ]
        ):
            return "pie"

        # --------------------------------------------------
        # Bar Chart
        # --------------------------------------------------

        if any(
            keyword in request
            for keyword in [
                "bar chart",
                "bar graph",
                "bar plot",
                "compare",
                "comparison",
                "by department",
                "by category",
            ]
        ):
            return "bar"

        # --------------------------------------------------
        # Default
        # --------------------------------------------------

        return "unknown"


# ======================================================
# Singleton
# ======================================================

chart_detector = ChartDetector()