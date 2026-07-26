"""
file_resolver.py
----------------

Utility for locating files on disk.
"""

from pathlib import Path

class FileResolver:
    """
    Resolve file paths.
    """

    def resolve(self, path: str | Path) -> Path:
        """
        Resolve a file path.
        
        Raises:
            FileNotFoundError
        """

        file_path = Path(path).expanduser().resolve()

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        return file_path


# ======================================================
# Singleton
# ======================================================

file_resolver = FileResolver()
