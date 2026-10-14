from dataclasses import dataclass
from datetime import time

RISK_SCORES = {"low": 1, "moderate": 2, "high": 3, "very high": 4}
INTENSITY_SCORES = {"low": 1, "medium": 2, "high": 3}
VENTILATION_MULTIPLIERS = {"good": 0.8, "normal": 1.0, "poor": 1.3}


@dataclass(frozen=True)
class HeatWindow:
    start: time
    end: time
    risk_level: str


@dataclass(frozen=True)
class BurdenResult:
    score: float
    risk_level: str
    factors: dict[str, float | str]


def _minutes(value: time) -> int:
    return value.hour * 60 + value.minute


def risk_for_time(at: time, timeline: list[HeatWindow]) -> tuple[str, int]:
    minute = _minutes(at)
    for window in timeline:
        if _minutes(window.start) <= minute < _minutes(window.end):
            return window.risk_level, RISK_SCORES[window.risk_level]
    return "low", RISK_SCORES["low"]


def calculate_burden(*, risk_level: str, intensity: str, duration_minutes: int, ventilation: str) -> BurdenResult:
    if risk_level not in RISK_SCORES:
        raise ValueError(f"Unknown risk level: {risk_level}")
    if intensity not in INTENSITY_SCORES:
        raise ValueError(f"Unknown intensity: {intensity}")
    if ventilation not in VENTILATION_MULTIPLIERS:
        raise ValueError(f"Unknown ventilation: {ventilation}")
    if duration_minutes <= 0:
        raise ValueError("Duration must be positive")
    score = RISK_SCORES[risk_level] * INTENSITY_SCORES[intensity] * duration_minutes * VENTILATION_MULTIPLIERS[ventilation]
    return BurdenResult(round(score, 2), risk_level, {"heat_risk": RISK_SCORES[risk_level], "task_intensity": INTENSITY_SCORES[intensity], "duration_minutes": duration_minutes, "zone_multiplier": VENTILATION_MULTIPLIERS[ventilation]})


def schedule_burden(*, start: time, end: time, intensity: str, ventilation: str, timeline: list[HeatWindow]) -> BurdenResult:
    duration = _minutes(end) - _minutes(start)
    if duration <= 0:
        raise ValueError("Schedule end must be after start")
    midpoint = time((_minutes(start) + duration // 2) // 60, (_minutes(start) + duration // 2) % 60)
    risk_level, _ = risk_for_time(midpoint, timeline)
    return calculate_burden(risk_level=risk_level, intensity=intensity, duration_minutes=duration, ventilation=ventilation)


def risk_label(score: float) -> str:
    if score >= 1000:
        return "very high"
    if score >= 500:
        return "high"
    if score >= 200:
        return "moderate"
    return "low"


def critical_window(timeline: list[HeatWindow]) -> HeatWindow:
    return max(timeline, key=lambda window: RISK_SCORES[window.risk_level])
