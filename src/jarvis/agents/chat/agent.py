"""
agent.py
--------

Chat Agent for Jarvis AI OS.

Handles general conversation by communicatingb
with the configured LLM.
"""

from jarvis.agents.base import BaseAgent
from jarvis.ollama_client import ollama_client
from jarvis.planner.registry import CHAT
from jarvis.planner.task import Task


class ChatAgent(BaseAgent):
    """
    general conversation Agent.
    """
    def __init__(self,):
        super().__init__(CHAT)

     # ======================================================
    # Validation
    # ======================================================
    def _validate(self, task: Task) -> None:
        """
        Ensure the task contains a prompt.
        """
        if not task.action.strip():
            raise ValueError("Task action connot be empty.")
    
    # ---------------------------------------------------------
    # Agent Logic
    # ---------------------------------------------------------

    def _run(self, task: Task) -> str:

        """
        Execute a chat Task by sending the user's
        request to the configured LLM.
        """
        model = task.payload["model"]
        
        return ollama_client.chat(
            model=model,
            prompt=task.action,
        )