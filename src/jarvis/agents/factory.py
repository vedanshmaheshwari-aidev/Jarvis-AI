"""
factory.py
----------

Creates and manages Agent instances.

The Planner Registry stores metadata only.
Actual Agent objects are created here.
"""

from jarvis.agents.chat import ChatAgent
from jarvis.planner.registry import CHAT


class AgentFactory:
    """
    Creates and manages Agent instances.
    """

    def __init__(self):
        self._agents: dict[str, object] = {}

        # Register built-in Agents
        self.register(CHAT, ChatAgent())

    # ======================================================
    # Registration
    # ======================================================

    def register(self, name: str, agent: object) -> None:
        """
        Register an Agent instance.
        """
        self._agents[name] = agent

    def unregister(self, name: str) -> None:
        """
        Remove an Agent from the Factory.
        """
        self._agents.pop(name, None)

    # ======================================================
    # Lookup
    # ======================================================

    def get(self, name: str):
        """
        Return an Agent instance.

        Returns None if the Agent
        is not registered.
        """
        return self._agents.get(name)

    def exists(self, name: str) -> bool:
        """
        Check whether an Agent exists.
        """
        return name in self._agents

    def all(self) -> dict[str, object]:
        """
        Return all registered Agents.
        """
        return self._agents.copy()


# ======================================================
# Singleton
# ======================================================

agent_factory = AgentFactory()