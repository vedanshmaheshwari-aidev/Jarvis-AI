"""
brain.py
--------

Central orchestration engine for Jarvis AI OS.

The Brain is responsible for:

- Choosing the appropriate LLM
- Creating an execution plan
- Injecting runtime information into Tasks
- Executing the plan
"""

from jarvis.config import config
from jarvis.planner.core import planner
from jarvis.planner.executor import executor
from jarvis.planner.task import Task
from jarvis.planner.task_result import TaskResult


# ======================================================
# Model Routing
# ======================================================

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
    Returns True if the question requires
    the reasoning model.
    """

    words = question.lower().split()

    return any(
        keyword in words
        for keyword in COMPLEX_KEYWORDS
    )


# ======================================================
# Brain
# ======================================================

class Brain:
    """
    Central orchestration engine for Jarvis AI OS.
    """

    # --------------------------------------------------
    # Model Selection
    # --------------------------------------------------

    def choose_model(self, question: str) -> str:
        """
        Decide which LLM should answer.
        """

        if is_complex(question):
            return config.REASONING_MODEL

        return config.FAST_MODEL

    # --------------------------------------------------
    # Planning
    # --------------------------------------------------

    def create_plan(self, question: str) -> list[Task]:
        """
        Ask the Planner to build Tasks.
        """

        return planner.plan(question)

    # --------------------------------------------------
    # Execution
    # --------------------------------------------------

    def execute_plan(self, tasks: list[Task]) -> list[TaskResult]:
        """
        Execute Planner Tasks.
        """

        return executor.execute(tasks)

    # --------------------------------------------------
    # Complete AI Pipeline
    # --------------------------------------------------

    def think(self, question: str) -> list[TaskResult]:
        """
        Complete AI execution pipeline.

        Question
            ↓
        Choose Model
            ↓
        Planner
            ↓
        Inject Runtime Data
            ↓
        Executor
            ↓
        TaskResults
        """

        # Select the model once
        model = self.choose_model(question)

        # Build the execution plan
        tasks = self.create_plan(question)

        # Inject runtime information into every Task
        for task in tasks:
            task.payload["model"] = model

        # Execute the plan
        results = self.execute_plan(tasks)

        return results


# ======================================================
# Singleton
# ======================================================

brain = Brain()