import unittest
from datetime import time

from app.services.heat_burden import HeatWindow, calculate_burden, critical_window, risk_for_time, risk_label, schedule_burden


class HeatBurdenTests(unittest.TestCase):
    timeline = [HeatWindow(time(9), time(12), "moderate"), HeatWindow(time(12), time(15), "very high"), HeatWindow(time(15), time(17), "high")]

    def test_calculation_is_deterministic_and_transparent(self):
        result = calculate_burden(risk_level="high", intensity="high", duration_minutes=120, ventilation="poor")
        self.assertEqual(result.score, 1404.0)
        self.assertEqual(result.factors["heat_risk"], 3)

    def test_timeline_lookup_and_critical_window(self):
        self.assertEqual(risk_for_time(time(13), self.timeline), ("very high", 4))
        self.assertEqual(critical_window(self.timeline).risk_level, "very high")

    def test_schedule_uses_midpoint_risk(self):
        result = schedule_burden(start=time(13), end=time(15), intensity="high", ventilation="poor", timeline=self.timeline)
        self.assertEqual(result.score, 1872.0)
        self.assertEqual(risk_label(result.score), "very high")


if __name__ == "__main__":
    unittest.main()
