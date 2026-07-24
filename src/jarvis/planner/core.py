"""
core.py
-------

Planner orchestration.

Converts a user request into
an ordered list of Tasks.
"""

from jarvis.planner.intent import intent
from jarvis.planner.scheduler import scheduler
from jarvis.planner.task import Task


class Planner:
    """
    Main Planner.
    """

    def plan(self, question: str) -> list[Task]:
        """
        Build an execution plan for a user request.
        """
     # -----------------------------------------------------
        # Detect which Agents should handle the request
        # -----------------------------------------------------

        agents = intent.detect(question)

        tasks: list[Task] = []
        # -----------------------------------------------------
        # Create Tasks
        # -----------------------------------------------------

        for agent in agents:
            tasks.append(
                Task(
                agent=agent,
                action=question,
                priority=agent.priority,
                requires_llm=agent.requires_llm,
            )
        )

         # -----------------------------------------------------
        # Schedule Tasks
        # -----------------------------------------------------

        return scheduler.schedule(tasks)


# Singleton
planner = Planner()