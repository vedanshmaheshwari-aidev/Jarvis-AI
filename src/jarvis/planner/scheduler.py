"""
scheduler.py
------------

Determines the execution orfder of tasks.

The scheduler does not exercute the tasks.
It simply returns them in the correct order.

"""

from jarvis.planner.task import Task

class TaskScheduler:
    """
    Orders tasks for execution
    """

    def schedule(self, tasks: list[Task]) -> list[Task]:
        """
        Returns Tasks ordered by prioroity.
        
        Higher priority tasks are schedueled first
        """

        return sorted (
            tasks,
            key=lambda task: task.priority,
            reverse= True,
        )
    

    # Singleton
scheduler = TaskScheduler()    