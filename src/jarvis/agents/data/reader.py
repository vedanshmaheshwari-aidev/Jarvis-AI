"""
reader.py

Handles loading datasets into mempory

Supported formats(v.0.1.0)
    • CSV
    • Excel

Future:
    • JSON
    • Parquet
    • SQL  
"""

from pathlib import Path

import pandas as pd

class DataReader:
    """
    reads datasets from disk
    """

    # ======================================================
    # Public API
    # ======================================================

    def read(self, path: str | Path) -> pd.DataFrame:
        """
        Automatically read a supported dataset.
        """
        path = Path(path)

        suffix = path.suffix.lower()

        if suffix == ".csv":
            return self.read_csv(path)

        if suffix in (".xlsx", "xls"):
            return self.read_excel(path)

        raise ValueError(f"Unsupported file format: {suffix}")


    # ======================================================
    # CSV
    # ======================================================
    def read_csv(self, path: str | Path) -> pd.DataFrame:
        """
        Load a CSV file.
        """
        return pd.read_csv(path)

    # ======================================================
    # Excel
    # ======================================================
    def read_excel(self, path:str | Path) -> pd.DataFrame:
        """
        Load an excel file.
        """
        return pd.read_excel(path)



# ======================================================
# Singleton
# ======================================================

data_reader = DataReader()