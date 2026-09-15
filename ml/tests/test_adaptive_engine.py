import pytest
from ml.src.rule_engine.adaptive_engine import (
    AdaptiveDifficultyEngine,
    DifficultyAction,
    SessionMetrics,
)


def test_performance_score_formula_calculation():
    # 0.5 * 1.0 (accuracy) + 0.3 * 1.0 (speed) + 0.2 * 1.0 (hints) = 1.0
    metrics = SessionMetrics(
        accuracy=1.0,
        duration_seconds=30.0,
        hints_used=0,
        target_duration_seconds=60.0,
    )
    score = AdaptiveDifficultyEngine.calculate_performance_score(metrics)
    assert score == 1.0


def test_performance_score_zero_hints():
    metrics = SessionMetrics(
        accuracy=0.8,
        duration_seconds=60.0,
        hints_used=0,
        max_hints_allowed=3,
        target_duration_seconds=60.0,
    )
    # accuracy: 0.5 * 0.8 = 0.40
    # speed: 0.3 * 1.0 = 0.30
    # hints: 0.2 * 1.0 = 0.20
    # total = 0.90
    score = AdaptiveDifficultyEngine.calculate_performance_score(metrics)
    assert score == 0.90


def test_performance_score_maximum_hints():
    metrics = SessionMetrics(
        accuracy=0.8,
        duration_seconds=60.0,
        hints_used=3,
        max_hints_allowed=3,
        target_duration_seconds=60.0,
    )
    # accuracy: 0.40
    # speed: 0.30
    # hints: 0.2 * 0.0 = 0.0
    # total = 0.70
    score = AdaptiveDifficultyEngine.calculate_performance_score(metrics)
    assert score == 0.70


def test_very_fast_response_capped():
    metrics = SessionMetrics(
        accuracy=1.0,
        duration_seconds=5.0,
        hints_used=0,
        target_duration_seconds=60.0,
    )
    score = AdaptiveDifficultyEngine.calculate_performance_score(metrics)
    assert score == 1.0


def test_very_slow_response():
    metrics = SessionMetrics(
        accuracy=0.5,
        duration_seconds=600.0,
        hints_used=2,
        target_duration_seconds=60.0,
    )
    score = AdaptiveDifficultyEngine.calculate_performance_score(metrics)
    assert score < 0.40


def test_zero_duration_edge_case():
    metrics = SessionMetrics(
        accuracy=1.0,
        duration_seconds=0.0,
        hints_used=0,
    )
    score = AdaptiveDifficultyEngine.calculate_performance_score(metrics)
    assert score == 1.0


def test_invalid_input_boundaries():
    with pytest.raises(ValueError, match="Accuracy must be between 0.0 and 1.0"):
        AdaptiveDifficultyEngine.calculate_performance_score(
            SessionMetrics(accuracy=1.5, duration_seconds=30.0, hints_used=0)
        )

    with pytest.raises(ValueError, match="Duration cannot be negative"):
        AdaptiveDifficultyEngine.calculate_performance_score(
            SessionMetrics(accuracy=0.8, duration_seconds=-10.0, hints_used=0)
        )

    with pytest.raises(ValueError, match="Hints used cannot be negative"):
        AdaptiveDifficultyEngine.calculate_performance_score(
            SessionMetrics(accuracy=0.8, duration_seconds=30.0, hints_used=-1)
        )


def test_adaptive_difficulty_increase():
    engine = AdaptiveDifficultyEngine()
    metrics = SessionMetrics(
        accuracy=1.0,
        duration_seconds=30.0,
        hints_used=0,
    )
    rec = engine.evaluate_session(current_difficulty=2, metrics=metrics)
    assert rec.action == DifficultyAction.INCREASE
    assert rec.recommended_difficulty == 3


def test_adaptive_difficulty_decrease():
    engine = AdaptiveDifficultyEngine()
    metrics = SessionMetrics(
        accuracy=0.2,
        duration_seconds=180.0,
        hints_used=3,
        max_hints_allowed=3,
    )
    rec = engine.evaluate_session(current_difficulty=3, metrics=metrics)
    assert rec.action == DifficultyAction.DECREASE
    assert rec.recommended_difficulty == 2


def test_boundary_difficulty_levels():
    engine = AdaptiveDifficultyEngine()
    # At max difficulty (5), cannot increase further
    rec = engine.evaluate_session(
        current_difficulty=5,
        metrics=SessionMetrics(accuracy=1.0, duration_seconds=30.0, hints_used=0),
    )
    assert rec.recommended_difficulty == 5
    assert rec.action == DifficultyAction.MAINTAIN

    # At min difficulty (1), cannot decrease further
    rec = engine.evaluate_session(
        current_difficulty=1,
        metrics=SessionMetrics(accuracy=0.1, duration_seconds=300.0, hints_used=5),
    )
    assert rec.recommended_difficulty == 1
    assert rec.action == DifficultyAction.MAINTAIN


def test_cold_start_vs_consecutive_sessions():
    engine = AdaptiveDifficultyEngine()
    metrics = SessionMetrics(accuracy=0.9, duration_seconds=40.0, hints_used=0)

    # Cold start (no history)
    cold_rec = engine.evaluate_session(current_difficulty=2, metrics=metrics, recent_scores=[])
    assert cold_rec.action == DifficultyAction.INCREASE

    # Consecutive low scores dampen a single spike
    damped_rec = engine.evaluate_session(
        current_difficulty=2,
        metrics=metrics,
        recent_scores=[0.3, 0.35, 0.3],
    )
    assert damped_rec.action == DifficultyAction.MAINTAIN
