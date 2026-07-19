from jarvis.config import config

# Keywords that require deeper reasoning
COMPLEX_KEYWORDS = {
    "build",
    "create",
    "design",
    "architecture",
    "debug",
    "optimize",
    "algorithm",
    "project",
    "agent",
    "system",
    "workflow",
    "api",
    "database",
    "sql",
    "integration",
}


def is_complex(question: str) -> bool:
    """
    Returns True if the question requires the reasoning model.
    """
    question = question.lower()

    words = question.lower().split()
    return any(keyword in words for keyword in COMPLEX_KEYWORDS)


class Brain:
    """
    Decides which AI model should answer the user's question.
    """

    def choose_model(self, question: str) -> str:
        if is_complex(question):
            return config.REASONING_MODEL

        return config.FAST_MODEL


brain = Brain()