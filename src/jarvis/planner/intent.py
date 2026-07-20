"""
intent.py
---------

Determines which Agent(s)
should handle the user's request.
"""

from jarvis.config import config
from jarvis.planner.registry import DEFAULT_AGENT
from jarvis.planner.scorer import scorer


class IntentDetector:
    """
    Detects the best Agent(s) for a user request.
    """

    def detect(self, question: str):
        """
        Returns a list of AgentRule objects.
        """

        results = scorer.score(question)

        # No matching agents
        if not results:
            return [DEFAULT_AGENT]

        highest_score = results[0].score

        selected_agents = []

        for result in results:

            if result.score >= highest_score * config.PLANNER_MATCH_THRESHOLD:
                selected_agents.append(result.agent)

        return selected_agents


# Singleton
intent = IntentDetector()