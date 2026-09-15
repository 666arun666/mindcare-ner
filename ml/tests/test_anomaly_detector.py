from ml.src.anomaly_detection.anomaly_detector import PerformanceAnomalyDetector


def test_anomaly_detector_cold_start():
    detector = PerformanceAnomalyDetector()
    # Less than 5 samples -> cold start
    detector.fit([[0.8, 45.0, 1, 0.82]])
    res = detector.detect([0.85, 40.0, 0, 0.90])
    assert not res.is_unusual
    assert "Insufficient historical sessions" in res.description


def test_anomaly_detector_trained_normal_and_outlier():
    detector = PerformanceAnomalyDetector(contamination=0.1, random_state=42)

    # Historical normal cluster (high accuracy ~0.8-0.9, duration ~30-40s, 0-1 hints, score ~0.85)
    history = [
        [0.85, 35.0, 0, 0.88],
        [0.82, 38.0, 1, 0.81],
        [0.90, 32.0, 0, 0.93],
        [0.87, 36.0, 1, 0.84],
        [0.83, 40.0, 1, 0.80],
        [0.88, 33.0, 0, 0.91],
        [0.86, 34.0, 0, 0.89],
        [0.84, 37.0, 1, 0.82],
    ]
    detector.fit(history)

    # Normal session similar to baseline
    normal_res = detector.detect([0.85, 36.0, 0, 0.88])
    assert not normal_res.is_unusual

    # Extreme outlier (drastic drop: 0.1 accuracy, 250s duration, 8 hints, score 0.15)
    outlier_res = detector.detect([0.10, 250.0, 8, 0.15])
    assert outlier_res.is_unusual
    assert "Unusual performance change" in outlier_res.status_label
    assert "Caregiver attention recommended" in outlier_res.description

    # Strict check: NEVER contain clinical diagnosis terms
    assert "dementia" not in outlier_res.description.lower()
    assert "alzheimer" not in outlier_res.description.lower()
