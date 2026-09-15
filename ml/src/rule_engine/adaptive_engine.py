"""
MINDCARE NER — Rule-Based Adaptive Difficulty Engine
SIH26003: Cognitive Support Platform

NOTE: The performance score and difficulty transitions represent task-specific
engagement heuristics. They are NOT clinical diagnostic measures or cognitive health percentages.
"""

from dataclasses import dataclass
from enum import Enum


class DifficultyAction(str, Enum):
    INCREASE = "INCREASE"
    MAINTAIN = "MAINTAIN"
    DECREASE = "DECREASE"


@dataclass
class SessionMetrics:
    accuracy: float  # 0.0 to 1.0
    duration_seconds: float  # >= 0.0
    hints_used: int  # >= 0
    max_hints_allowed: int = 3
    target_duration_seconds: float = 60.0


@dataclass
class AdaptiveRecommendation:
    current_difficulty: int
    recommended_difficulty: int
    performance_score: float
    action: DifficultyAction
    reason: str


class AdaptiveDifficultyEngine:
    """
    Computes performance score and recommends difficulty adjustments based on:
    performance_score = 0.5 * accuracy_norm + 0.3 * speed_score + 0.2 * hint_efficiency
    """

    MIN_DIFFICULTY = 1
    MAX_DIFFICULTY = 5

    THRESHOLD_INCREASE = 0.75
    THRESHOLD_DECREASE = 0.40

    @staticmethod
    def calculate_performance_score(metrics: SessionMetrics) -> float:
        """
        Calculate composite task performance score bounded between 0.0 and 1.0.
        """
        # Validate and clamp accuracy
        if metrics.accuracy < 0.0 or metrics.accuracy > 1.0:
            raise ValueError(f"Accuracy must be between 0.0 and 1.0, got {metrics.accuracy}")
        accuracy_norm = max(0.0, min(1.0, metrics.accuracy))

        # Speed score calculation: faster than or equal to target gives 1.0, degrades smoothly
        if metrics.duration_seconds < 0.0:
            raise ValueError(f"Duration cannot be negative, got {metrics.duration_seconds}")

        if metrics.duration_seconds == 0.0:
            # Avoid division by zero, instant completion
            speed_score = 1.0
        else:
            # Score is ratio of target duration to actual duration, capped at 1.0
            # If actual duration is twice target, score is 0.5
            ratio = metrics.target_duration_seconds / metrics.duration_seconds
            speed_score = max(0.0, min(1.0, ratio))

        # Hint efficiency calculation: 0 hints used gives 1.0; max hints gives 0.0
        if metrics.hints_used < 0:
            raise ValueError(f"Hints used cannot be negative, got {metrics.hints_used}")

        if metrics.max_hints_allowed <= 0:
            hint_efficiency = 1.0
        else:
            used = min(metrics.hints_used, metrics.max_hints_allowed)
            hint_efficiency = max(0.0, 1.0 - (used / metrics.max_hints_allowed))

        # Composite score
        score = (0.5 * accuracy_norm) + (0.3 * speed_score) + (0.2 * hint_efficiency)
        return round(max(0.0, min(1.0, score)), 4)

    def evaluate_session(
        self,
        current_difficulty: int,
        metrics: SessionMetrics,
        recent_scores: list[float] | None = None,
    ) -> AdaptiveRecommendation:
        """
        Evaluates a session and recommends the next difficulty level.
        Considers recent session history when available.
        """
        if current_difficulty < self.MIN_DIFFICULTY or current_difficulty > self.MAX_DIFFICULTY:
            raise ValueError(
                f"Difficulty must be between {self.MIN_DIFFICULTY} and {self.MAX_DIFFICULTY}"
            )

        current_score = self.calculate_performance_score(metrics)

        # Cold start handling (first session) vs historical trend
        if recent_scores is None or len(recent_scores) == 0:
            effective_score = current_score
        else:
            # 50% weight to current session, 50% to moving average of last sessions
            history_avg = sum(recent_scores) / len(recent_scores)
            effective_score = 0.5 * current_score + 0.5 * history_avg

        if effective_score >= self.THRESHOLD_INCREASE:
            if current_difficulty < self.MAX_DIFFICULTY:
                action = DifficultyAction.INCREASE
                new_diff = current_difficulty + 1
                reason = "Consistently high engagement and performance on recent tasks."
            else:
                action = DifficultyAction.MAINTAIN
                new_diff = self.MAX_DIFFICULTY
                reason = "High performance maintained at maximum difficulty level."
        elif effective_score <= self.THRESHOLD_DECREASE:
            if current_difficulty > self.MIN_DIFFICULTY:
                action = DifficultyAction.DECREASE
                new_diff = current_difficulty - 1
                reason = "Adjusting task difficulty to support user comfort and reduce cognitive fatigue."
            else:
                action = DifficultyAction.MAINTAIN
                new_diff = self.MIN_DIFFICULTY
                reason = "Maintained at foundational level to encourage positive participation."
        else:
            action = DifficultyAction.MAINTAIN
            new_diff = current_difficulty
            reason = "Performance stable within expected baseline parameters."

        return AdaptiveRecommendation(
            current_difficulty=current_difficulty,
            recommended_difficulty=new_diff,
            performance_score=current_score,
            action=action,
            reason=reason,
        )
