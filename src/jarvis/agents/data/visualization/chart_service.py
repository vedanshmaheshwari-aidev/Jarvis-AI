"""
chat_service.py
-----------------

Generates charts from pandas DataFrames based on the user's natural-language request.
"""

from pathlib import Path

import matplotlib.pyplot as plt  # pyright: ignore[reportMissingModuleSource]
import pandas as pd

from jarvis.agents.data.visualization.chart_detector import chart_detector

class ChatService:
    """
    Handles chart generation for the Data Agents
    """

    def __init__(self):
        self.output_dir = Path("assets/output")
        self.output_dir.mkdir(parents=True, exist_ok=True,)


    # ======================================================
    # Public API
    # ======================================================

    def create_chart(self, df: pd.DataFrame, request: str) -> str:
        """
        Create a chart from the DataFrame.
        
        Returns:
            str: Path to the generated chart.
            """    

        chart_type = chart_detector.detect(request)

        if chart_type == "unknown":
            return ("❌ I couldn't determine which chart "
                "you want.\n\n"
                "Try:\n"
                "• Show a bar chart of salary\n"
                "• Show salary distribution\n"
                "• Show a scatter plot of age vs salary\n"
                "• Show a line chart of sales over time\n"
                "• Show a pie chart of departments")

        if df.empty:
            return "❌ The dataset is empty."


        # --------------------------------------------------
        # Create chart
        # --------------------------------------------------

        if chart_type == "bar":
            return self._create_bar_chart(df)

        if chart_type == "histogram":
            return self._create_histogram_chart(df)
    
        if chart_type == "scatter":
            return self._create_scatter_chart(df)

        if chart_type == "line":
            return self._create_line_chart(df)

        if chart_type == "pie":
            return self._create_pie_chart(df)

        return f"❌ Unsupported chart type: {chart_type}"

    # ======================================================
    # Bar Chart
    # ======================================================
    
    def _create_bar_chart(self, df: pd.DataFrame) -> str:

        numeric_columns = df.select_dtypes(include="number").columns

        if len(numeric_columns) ==0:
            return "❌ No numeric columns available for a bar chart."

        column = numeric_columns[0]

        plt.figure(figsize =(8,5))

        plt.bar(range(len(df[column])) , df[column])

        plt.xlabel("Records")
        plt.ylabel(column)
        plt.title(f"{column} - Bar Chart")

        return self._save_chart(f"bar_{column}")

    # ======================================================
    # Histogram
    # ======================================================

    def _create_histogram_chart(self, df: pd.DataFrame) -> str:

        numeric_columns = df.select_dtypes(include="number").columns

        if len(numeric_columns) == 0:
            return "❌ No numeric columns available for a histogram."

        column = numeric_columns[0]

        plt.figure(figsize =(8,5))
        # plt.hist(df[column], bins=30)
        # plt.xlabel(column)
        # plt.ylabel("Frequency")
        # plt.title(f"{column} - Histogram")

        # return self._save_chart(f"histogram_{column}")
        plt.ylabel("Frequency")
        plt.title(f"{column} - Distribution")

        return self._save_chart(
            f"histogram_{column}")

    # ======================================================
    # Scatter Chart
    # ======================================================

    def _create_scatter_chart(self, df: pd.DataFrame) -> str:

        numeric_columns = df.select_dtypes(
            include="number"
        ).columns

        if len(numeric_columns) < 2:
            return (
                "❌ A scatter plot requires at least "
                "two numeric columns."
            )

        x_column = numeric_columns[0]
        y_column = numeric_columns[1]

        plt.figure(figsize=(8, 5))

        plt.scatter(
            df[x_column],
            df[y_column],
        )

        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.title(
            f"{x_column} vs {y_column}"
        )

        return self._save_chart(
            f"scatter_{x_column}_vs_{y_column}"
        )

    # ======================================================
    # Line Chart
    # ======================================================

    def _create_line_chart(
        self,
        df: pd.DataFrame,
    ) -> str:

        numeric_columns = df.select_dtypes(
            include="number"
        ).columns

        if len(numeric_columns) == 0:
            return "❌ No numeric columns available for a line chart."

        column = numeric_columns[0]

        plt.figure(figsize=(8, 5))

        plt.plot(
            df[column],
            marker="o",
        )

        plt.xlabel("Records")
        plt.ylabel(column)
        plt.title(f"{column} - Line Chart")

        return self._save_chart(
            f"line_{column}"
        )

    # ======================================================
    # Pie Chart
    # ======================================================

    def _create_pie_chart(
        self,
        df: pd.DataFrame,
    ) -> str:

        categorical_columns = df.select_dtypes(
            include=["object", "category", "string"]
        ).columns

        if len(categorical_columns) == 0:
            return (
                "❌ No categorical columns available "
                "for a pie chart."
            )

        column = categorical_columns[0]

        counts = df[column].value_counts()

        plt.figure(figsize=(7, 7))

        plt.pie(
            counts.values,
            labels=counts.index,
            autopct="%1.1f%%",
        )

        plt.title(
            f"{column} - Distribution"
        )

        return self._save_chart(
            f"pie_{column}"
        )

    # ======================================================
    # Save Chart
    # ======================================================

    def _save_chart(
        self,
        filename: str,
    ) -> str:

        path = self.output_dir / f"{filename}.png"

        plt.tight_layout()
        plt.savefig(path)
        plt.close()

        return (
            "📊 Chart created successfully.\n"
            f"Saved to: {path}"
        )


# ======================================================
# Singleton
# ======================================================

chart_service = ChatService()
