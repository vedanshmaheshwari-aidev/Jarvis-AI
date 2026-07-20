"""
scorer.py
---------

Scores every registered Agent based on the user's request.
"""

from dataclasses import dataclass

from jarvis.config import config
from jarvis.planner.registry import REGISTERED_AGENTS
from jarvis.planner.text import contains_keyword


# ==========================================================
# Score Result
# ==========================================================

@dataclass(slots=True)
class ScoreResult:
    """Stores the score assigned to an Agent."""

    agent: object
    score: int


# ==========================================================
# Agent Scorer
# ==========================================================

class AgentScorer:
    """Calculates scores for all registered Agents."""

    def score(self, question: str) -> list[ScoreResult]:
        """
        Returns all matching agents sorted by score.
        """

        question = question.lower().strip()

        results = []

        for agent in REGISTERED_AGENTS:

            if not agent.enabled:
                continue

            score = self._calculate_score(
                question,
                agent.keyword_weights,
            )

            # Ignore weak matches
            if score < config.PLANNER_MIN_SCORE:
                continue

            results.append(
                ScoreResult(
                    agent=agent,
                    score=score,
                )
            )

        results.sort(
            key=lambda result: result.score,
            reverse=True,
        )

        return results

    # ------------------------------------------------------

    def _calculate_score(
        self,
        question: str,
        keyword_weights: dict[str, int],
    ) -> int:
        """
        Calculates the weighted keyword score for one Agent.
        """

        score = 0

        for keyword, weight in keyword_weights.items():
            if contains_keyword(question, keyword):
                score += weight

        return score


# ==========================================================
# Singleton
# ==========================================================

scorer = AgentScorer()