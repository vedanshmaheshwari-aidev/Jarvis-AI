"""
chart_service.py
----------------

Generates charts from pandas DataFrames
based on the user's natural-language request.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import re

from jarvis.agents.data.visualization.chart_detector import chart_detector
from jarvis.agents.data.visualization.column_detector import column_detector


class ChartService:
    def __init__(self):
        self.output_dir = Path("assets/output")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def create_chart(self, df: pd.DataFrame, request: str) -> str:
        """
        Create a chart based on the user's request.
        """

        chart_type = chart_detector.detect(request)

        if chart_type == "unknown":
            return (
                "❌ I couldn't determine which chart "
                "you want.\n\n"
                "Try:\n"
                "• Show a bar chart of salary\n"
                "• Show salary distribution\n"
                "• Show a scatter plot of age vs salary\n"
                "• Show a line chart of sales over time\n"
                "• Show a pie chart of departments"
            )

        if df.empty:
            return "❌ The dataset is empty."

        columns = column_detector.detect(df, request)

        # If the user explicitly names a column that was not
        # detected, don't silently chart an unrelated column.
        if not columns:
            requested_field = re.search(
                r"\b(?:of|by)\s+([a-zA-Z_][a-zA-Z0-9_]*)",
                request,
                re.IGNORECASE,
            )

            if requested_field:
                field = requested_field.group(1)
                available = ", ".join(
                    str(column) for column in df.columns
                )

                return (
                    f"❌ I couldn't find a column matching "
                    f"'{field}'.\n\n"
                    f"Available columns: {available}"
                )
                
        if chart_type == "bar":
            return self._create_bar_chart(df, columns)

        if chart_type == "histogram":
            return self._create_histogram(df, columns)

        if chart_type == "scatter":
            return self._create_scatter_chart(df, columns)

        if chart_type == "line":
            return self._create_line_chart(df, columns, request)

        if chart_type == "pie":
            return self._create_pie_chart(df, columns)

        return f"❌ Unsupported chart type: {chart_type}"

    def _create_bar_chart(
        self,
        df: pd.DataFrame,
        columns: list[str],
    ) -> str:
        """
        Create a bar chart using the detected column.
        """

        if columns:
            column = columns[0]
        else:
            numeric_columns = df.select_dtypes(
                include="number"
            ).columns

            if len(numeric_columns) == 0:
                return (
                    "❌ No numeric columns available "
                    "for a bar chart."
                )

            column = numeric_columns[0]

        plt.figure(figsize=(8, 5))

        plt.bar(
            range(len(df[column])),
            df[column],
        )

        plt.xlabel("Records")
        plt.ylabel(column)
        plt.title(f"{column} - Bar Chart")

        return self._save_chart(f"bar_{column}")

    def _create_histogram(
        self,
        df: pd.DataFrame,
        columns: list[str],
    ) -> str:
        """
        Create a histogram using the detected numeric column.
        """

        if columns:
            column = columns[0]

            if not pd.api.types.is_numeric_dtype(
                df[column]
            ):
                return (
                    f"❌ '{column}' is not a numeric "
                    "column suitable for a histogram."
                )

        else:
            numeric_columns = df.select_dtypes(
                include="number"
            ).columns

            if len(numeric_columns) == 0:
                return (
                    "❌ No numeric columns available "
                    "for a histogram."
                )

            column = numeric_columns[0]

        plt.figure(figsize=(8, 5))

        plt.hist(
            df[column].dropna(),
            bins=10,
        )

        plt.xlabel(column)
        plt.ylabel("Frequency")
        plt.title(f"{column} - Distribution")

        return self._save_chart(f"histogram_{column}")

    def _create_scatter_chart(
        self,
        df: pd.DataFrame,
        columns: list[str],
    ) -> str:
        """
        Create a scatter plot using two detected
        numeric columns.
        """

        if len(columns) >= 2:
            x_column = columns[0]
            y_column = columns[1]

        else:
            numeric_columns = df.select_dtypes(
                include="number"
            ).columns

            if len(numeric_columns) < 2:
                return (
                    "❌ A scatter plot requires "
                    "at least two numeric columns."
                )

            x_column = numeric_columns[0]
            y_column = numeric_columns[1]

        if not pd.api.types.is_numeric_dtype(
            df[x_column]
        ) or not pd.api.types.is_numeric_dtype(
            df[y_column]
        ):
            return (
                "❌ Scatter plots require "
                "numeric columns."
            )

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

    
    def _create_line_chart(
        self,
        df: pd.DataFrame,
        columns: list[str],
        request: str,
    ) -> str:
        """Create a line chart, using dates when available."""

        # Select the requested numeric column.
        column = next(
            (
                col for col in columns
                if pd.api.types.is_numeric_dtype(df[col])
            ),
            None,
        )

        if column is None:
            numeric_columns = df.select_dtypes(
                include="number"
            ).columns

            if len(numeric_columns) == 0:
                return (
                    "❌ No numeric columns available "
                    "for a line chart."
                )

            column = numeric_columns[0]

        # Look for a column that appears to contain dates.
        date_column = next(
            (
                col for col in df.columns
                if any(
                    word in str(col).lower()
                    for word in ("date", "time", "timestamp")
                )
            ),
            None,
        )

        plt.figure(figsize=(9, 5))

        if date_column is not None:
            try:
                dates = pd.to_datetime(
                    df[date_column],
                    errors="coerce",
                    dayfirst=True,
                    format="mixed",
                )
            except (TypeError, ValueError):
                dates = pd.to_datetime(
                    df[date_column],
                    errors="coerce",
                    dayfirst=True,
                )

            valid = pd.DataFrame({
                "date": dates,
                "value": df[column],
            }).dropna()

            if len(valid) >= 2:
                # Aggregate multiple records on the same date.
                daily = (
                    valid.groupby("date")["value"]
                    .sum()
                    .sort_index()
                )

                plt.plot(
                    daily.index,
                    daily.values,
                    marker="o",
                )

                plt.xlabel(str(date_column))
                plt.ylabel(f"Total {column}")
                plt.title(f"{column} Over Time")
                plt.xticks(rotation=45)

                return self._save_chart(
                    f"line_{column}_over_{date_column}"
                )

        # Fall back to record order when usable dates
        # aren't available.
        plt.plot(df[column], marker="o")
        plt.xlabel("Records")
        plt.ylabel(column)
        plt.title(f"{column} - Line Chart")

        return self._save_chart(f"line_{column}")


    def _create_pie_chart(
        self,
        df: pd.DataFrame,
        columns: list[str],
    ) -> str:
        """
        Create a pie chart using the detected
        categorical column.
        """

        if columns:
            column = columns[0]

            if not (
                pd.api.types.is_object_dtype(df[column])
                or pd.api.types.is_categorical_dtype(df[column])
                or pd.api.types.is_string_dtype(df[column])
            ):
                return (
                    f"❌ '{column}' is not a "
                    "categorical column suitable "
                    "for a pie chart."
                )

        else:
            categorical_columns = df.select_dtypes(
                include=[
                    "object",
                    "category",
                    "string",
                ]
            ).columns

            if len(categorical_columns) == 0:
                return (
                    "❌ No categorical columns "
                    "available for a pie chart."
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

    def _save_chart(self, filename: str) -> str:
        """
        Save the generated chart as a PNG file.
        """

        path = self.output_dir / f"{filename}.png"

        plt.tight_layout()
        plt.savefig(path)
        plt.close()

        return (
            "📊 Chart created successfully.\n"
            f"Saved to: {path}"
        )


chart_service = ChartService()