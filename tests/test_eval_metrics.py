import unittest

from src.evaluation.metrics import timeline_event_metrics


class TestEvalMetrics(unittest.TestCase):
    def test_timeline_basic(self) -> None:
        gt = [
            {
                "start": "00:01.00",
                "end": "00:03.00",
                "event_type": "near_miss",
                "severity": "high",
            }
        ]
        pred = [
            {
                "start": "00:02.00",
                "end": "00:04.00",
                "event_type": "near_miss",
                "severity": "high",
            }
        ]
        m = timeline_event_metrics(pred, gt, tol_s=2.0)
        self.assertGreaterEqual(m["f1"], 0.99)


if __name__ == "__main__":
    unittest.main()
