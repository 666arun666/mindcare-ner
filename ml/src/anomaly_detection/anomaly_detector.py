"""
MINDCARE NER — Isolation Forest Anomaly Detection Interface
SIH26003: Cognitive Support Platform

NOTE: This module detects statistical outliers/unusual shifts in task performance metrics.
It NEVER outputs a clinical diagnosis (e.g. Alzheimer's, Dementia).
Allowed terminology: "Unusual performance change" or "Caregiver attention recommended".
"""

from dataclasses import dataclass

import numpy as np
from sklearn.ensemble import IsolationForest


@dataclass
class AnomalyDetectionResult:
    is_unusual: bool
    status_label: str
    anomaly_score: float
    description: str


class PerformanceAnomalyDetector:
    """
    Detects unusual performance shifts across recent sessions using Isolation Forest.
    """

    TERMINOLOGY_ALERT = "Unusual performance change detected"
    TERMINOLOGY_NORMAL = "Performance consistent with historical baseline"
    TERMINOLOGY_ATTENTION = "Caregiver attention recommended"

    def __init__(self, contamination: float = 0.1, random_state: int = 42):
        self.contamination = contamination
        self.random_state = random_state
        self.model: IsolationForest | None = None

    def fit(self, historical_features: list[list[float]]) -> None:
        """
        Fit IsolationForest on historical feature matrix:
        Features per row: [accuracy, duration_seconds, hints_used, performance_score]
        """
        if len(historical_features) < 5:
            # Insufficient historical baseline data for cold start
            self.model = None
            return

        X = np.array(historical_features)
        self.model = IsolationForest(
            contamination=self.contamination,
            random_state=self.random_state,
        )
        self.model.fit(X)

    def detect(self, current_features: list[float]) -> AnomalyDetectionResult:
        """
        Assess current session metrics for unusual variance.
        """
        if len(current_features) != 4:
            raise ValueError("Expected 4 features: [accuracy, duration, hints, performance_score]")

        if self.model is None:
            # Baseline not established yet (cold start)
            return AnomalyDetectionResult(
                is_unusual=False,
                status_label=self.TERMINOLOGY_NORMAL,
                anomaly_score=0.0,
                description="Insufficient historical sessions to establish baseline profile.",
            )

        X_curr = np.array([current_features])
        prediction = self.model.predict(X_curr)[0]  # -1 = anomaly, 1 = normal
        raw_score = float(self.model.score_samples(X_curr)[0])

        is_unusual = prediction == -1
        if is_unusual:
            label = self.TERMINOLOGY_ALERT
            description = (
                f"{self.TERMINOLOGY_ATTENTION}: Current session shows a statistical divergence "
                "from historical task patterns. Please observe user fatigue or comfort."
            )
        else:
            label = self.TERMINOLOGY_NORMAL
            description = "Activity completion matches existing individual performance history."

        return AnomalyDetectionResult(
            is_unusual=is_unusual,
            status_label=label,
            anomaly_score=round(raw_score, 4),
            description=description,
        )
