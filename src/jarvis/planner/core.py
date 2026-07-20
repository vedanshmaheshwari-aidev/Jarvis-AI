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

        agents = intent.detect(question)

        tasks: list[Task] = []

        for agent in agents:

            task = Task(
                agent=agent.name,
                action=question,
                priority=agent.priority,
                requires_llm=agent.requires_llm,
            )

            tasks.append(task)

        return scheduler.schedule(tasks)


# Singleton
planner = Planner()