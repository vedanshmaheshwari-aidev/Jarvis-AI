COMPLEX_KEYWORDS ={
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
    "integration"

}

def is_complex(question: str) -> bool:
    question = question.lower()

    return any(word in question for word in COMPLEX_KEYWORDS)