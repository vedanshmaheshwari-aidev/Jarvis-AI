"""
text.py
========

Text processing utilities for the Planner.

Every user request should be normalized before
intent detection and scoring.
"""

import re


# ==========================================================
# Text Normalization
# ==========================================================

def normalize(text: str) -> str:
    """
    Normalize user input.

    Example:
        "  Power BI!!!  "
            ↓
        "power bi"
    """

    text = text.lower().strip()

    # Replace punctuation with spaces
    text = re.sub(r"[^\w\s]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text


# ==========================================================
# Tokenization
# ==========================================================

def tokenize(text: str) -> list[str]:
    """
    Split text into individual words.

    Example:
        "clean csv file"

    Returns:
        ["clean", "csv", "file"]
    """

    return normalize(text).split()


# ==========================================================
# Keyword Matching
# ==========================================================

def contains_keyword(question: str, keyword: str) -> bool:
    """
    Check whether a keyword exists in a question.

    Supports:
        - Single words
        - Multi-word phrases

    Examples:
        contains_keyword("Open Excel", "excel")
            -> True

        contains_keyword("Build a Power BI dashboard", "power bi")
            -> True

        contains_keyword("Launch Task Manager", "task manager")
            -> True
    """

    question = normalize(question)
    keyword = normalize(keyword)

    # Multi-word phrase
    if " " in keyword:
        return keyword in question

    # Single word
    return keyword in tokenize(question)