"""
agent.py
--------

Chat Agent for Jarvis AI OS.

Handles general conversation by communicatingb
with the configured LLM.
"""

from jarvis.agents.base import BaseAgent
from jarvis.ollama_client import ollama_client
from jarvis.planner.task import Task
from jarvis.planner.task_result import TaskResult


class ChatAgent(BaseAgent):
    """
    general conversation Agent.
    """
    def __init__(self,):
        super().__init__("chat")

    
    # ---------------------------------------------------------
    # Agent Logic
    # ---------------------------------------------------------

    def _run(self, task: Task) -> TaskResult:

        """
        Execute a chat Task.
        """
        response = ollama_client.chat(task.action)


        return TaskResult(
            task_id= task.id,
            agent_name= self.name,
            success= True,
            message= response,
        )    