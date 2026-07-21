"""
factory.py
----------

Creates and manages Agent instances.

The Planner Registry stores metadata only.
Actual Agent objects are created here.
"""

from jarvis.agents.chat import ChatAgent


class AgentFactory:
    """
    Create Agent Instances.
    """

    def __init__(self):
        self._agents ={
            "chat": ChatAgent(),
        }

    def get(self, name: str):
        """
        Return the Agent instance by name.
        """    
        return self._agents.get(name)
    


# ---------------------------------------------------------
# Singleton
# ---------------------------------------------------------

agent_factory = AgentFactory()    
