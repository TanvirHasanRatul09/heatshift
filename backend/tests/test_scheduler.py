import unittest
from datetime import time

from app.services.heat_burden import HeatWindow
from app.services.scheduler import recommend_schedule


class SchedulerTests(unittest.TestCase):
    timeline = [HeatWindow(time(9), time(12), "moderate"), HeatWindow(time(12), time(15), "very high"), HeatWindow(time(15), time(17), "high")]

    def test_recommendation_is_feasible_and_lower_burden(self):
        result = recommend_schedule(transfer_locked=False, timeline=self.timeline)
        self.assertEqual(result["status"], "feasible")
        self.assertEqual(result["total_burden"], 2328.0)
        self.assertEqual(result["schedule"][0]["start"], "09:00")

    def test_locked_transfer_returns_no_safe_schedule(self):
        result = recommend_schedule(transfer_locked=True, timeline=self.timeline)
        self.assertEqual(result["status"], "no-safe-schedule")


if __name__ == "__main__":
    unittest.main()
