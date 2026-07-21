"""
base.py
-------

Base class for every agent in Jarvis AI OS.

All agents inherti from BaseAgent.

Agents should only implement _run().

The execution lifecycle is managed here.
"""


from abc import ABC, abstractmethod

from jarvis.planner.task import Task
from jarvis.planner.task_result import TaskResult


class BaseAgent(ABC):
    """
    Base class for all Jarvis Agents.
    """

    def __init__(self, name: str):
        self.name = name


    # ======================================================
    # Public Execution API
    # ======================================================

    def execute(self, task: Task) -> TaskResult:
        """
        Executes a Task.
        
        This method should never be overriden.
        """

        try:
            self.before_execute(task)

            result = self._run(task)

            self.after_execute(task, result)

            return result
        
        except Exception as exc:
            return self.on_error(task, exc)
        


     # ======================================================
    # Hooks
    # ======================================================

    def before_execute(self, task: Task) ->None:
        """
        Runs before task execution.
        
        Child Agents may override if needed.
        """
        pass

    def after_execute(
           self,
           task: Task,
           result: TaskResult, 
    ) -> None:
        """
        Runs after successful execution.
        
        Child Agents may override if needed.
        """

        pass


      # ======================================================
    # Error Handler
    # ======================================================

    def on_error(
        self,
        task: Task,
        error: Exception
    ) -> TaskResult:
        """
        Converts exception into TaskResults.
        """
        return TaskResult(
            task_id= task.id,
            success= False,
            message="",
            error= str(error),
        )
    # ======================================================
    # Agent Logic
    # ======================================================
    @abstractmethod
    def _run(self, task: Task) -> TaskResult:
        """
        Every agent must implement this.
        
        This is where the actual work will happens.
        """
        raise NotImplementedError