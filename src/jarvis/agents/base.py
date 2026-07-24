"""
base.py
-------

Base class for every Agent in Jarvis AI OS.

All Agents inherit from BaseAgent.

Agents should only implement:

- _validate()
- _run()

The execution lifecycle is managed here.
"""

from abc import ABC, abstractmethod
from typing import Any

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
        Execute a Task.

        This method defines the execution lifecycle and
        should never be overridden by child Agents.
        """

        try:
            # ---------------------------------------------
            # Pre-execution hook
            # ---------------------------------------------

            self.before_execute(task)

            # ---------------------------------------------
            # Validation
            # ---------------------------------------------

            self._validate(task)

            # ---------------------------------------------
            # Execute Agent logic
            # ---------------------------------------------

            data = self._run(task)

            # ---------------------------------------------
            # Wrap into TaskResult
            # ---------------------------------------------

            result = TaskResult(
                task_id=task.id,
                success=True,
                message="Task completed successfully.",
                data=data,
                agent_name=self.name,
            )

            # ---------------------------------------------
            # Post-execution hook
            # ---------------------------------------------

            self.after_execute(task, result)

            return result

        except Exception as exc:
            return self.on_error(task, exc)

    # ======================================================
    # Hooks
    # ======================================================

    def before_execute(self, task: Task) -> None:
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
    # Validation
    # ======================================================

    def _validate(self, task: Task) -> None:
        """
        Validate the Task before execution.

        Child Agents may override this method to perform
        custom validation.

        Raise an exception if validation fails.
        """
        pass

    # ======================================================
    # Agent Logic
    # ======================================================

    @abstractmethod
    def _run(self, task: Task) -> Any:
        """
        Execute the Agent's business logic.

        Returns:
            Any:
                The business result produced by the Agent.

        BaseAgent automatically wraps the returned value
        inside a TaskResult.
        """
        raise NotImplementedError

    # ======================================================
    # Error Handling
    # ======================================================

    def on_error(
        self,
        task: Task,
        error: Exception,
    ) -> TaskResult:
        """
        Convert an exception into a TaskResult.
        """

        return TaskResult(
            task_id=task.id,
            success=False,
            message="Task execution failed.",
            error=str(error),
            agent_name=self.name,
        )