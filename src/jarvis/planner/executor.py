"""
executor.py
-----------

Executes Tasks produced by the Planner

The Executor does not know How an Agent works.

It simply dispatches each task to the 
registered Agent handler.
"""

from jarvis.planner.task import Task
from jarvis.planner.task_result import TaskResult


class TaskExecutor:
    """
    Executes Planner Tasks.
    """

    def execute(self, tasks: list[Task]) -> list[TaskResult]:
        """Execute Tasks in order.
        
        Returns a list of TaskResults.
        """

        results: list[TaskResult] = []

        for task in tasks:

            handler = task.agent.handler

            if handler is None:
                results.append(
                    TaskResult(
                        task_id=task.id,
                        success= False,
                        error= f"No handler registered for '{task.agent.name}'.",
                    )
                )
                continue

            result = handler.execute(task)

            results.append(result)


        return results




#Singleton
executor = TaskExecutor()        