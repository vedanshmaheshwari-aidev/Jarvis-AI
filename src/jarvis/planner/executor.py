"""
executor.py
-----------

Executes an ordered list of Planner Tasks.

The Executor is responsible only for dispatching
Tasks to the appropriate Agent handler and
collecting TaskResults.
"""

from jarvis.planner.task import Task
from jarvis.planner.task_result import TaskResult


class TaskExecutor:
    """
    Executes an ordered list of Planner Tasks.

    The Executor dispatches each Task to the
    appropriate Agent handler and collects
    TaskResults.
    """

    def execute(self, tasks: list[Task]) -> list[TaskResult]:
        """
        Execute Tasks in order.

        Returns:
            list[TaskResult]: Results produced by the executed tasks.
        """

        results: list[TaskResult] = []

        for task in tasks:

            handler = task.agent.handler

            # -------------------------------------------------
            # No handler registered
            # -------------------------------------------------

            if handler is None:
                results.append(
                    TaskResult(
                        task_id=task.id,
                        agent_name=task.agent.name,
                        success=False,
                        error=f"No handler registered for '{task.agent.name}'.",
                    )
                )
                continue

            # -------------------------------------------------
            # Execute Task
            # -------------------------------------------------

            try:
                result = handler.execute(task)

            except Exception as exc:
                result = TaskResult(
                    task_id=task.id,
                    agent_name=task.agent.name,
                    success=False,
                    error=str(exc),
                )

            results.append(result)

        return results


# ---------------------------------------------------------
# Singleton
# ---------------------------------------------------------

executor = TaskExecutor()