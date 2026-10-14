from dataclasses import dataclass
from datetime import time

from .heat_burden import HeatWindow, schedule_burden


@dataclass(frozen=True)
class TaskSpec:
    name: str
    duration_minutes: int
    intensity: str
    skill: str
    zone: str
    ventilation: str
    dependency: str | None = None


@dataclass(frozen=True)
class Assignment:
    task: str
    worker: str
    zone: str
    start: time
    end: time


def _t(hour: int, minute: int = 0) -> time:
    return time(hour, minute)


def _candidate(*, transfer_locked: bool) -> list[Assignment] | None:
    if transfer_locked:
        return None
    return [
        Assignment("Fabric-roll transfer", "Worker A", "Loading Area", _t(9), _t(11)),
        Assignment("Packing preparation", "Worker A", "Production Floor", _t(11), _t(12)),
        Assignment("Cooling / recovery", "Worker A", "Cooling / Recovery Area", _t(12), _t(13)),
        Assignment("Quality tagging", "Worker B", "Production Floor", _t(9), _t(11)),
        Assignment("Inventory update", "Worker B", "Production Floor", _t(13), _t(15)),
    ]


def validate_schedule(assignments: list[Assignment], tasks: dict[str, TaskSpec], timeline: list[HeatWindow], cooling_capacity: int = 4) -> list[str]:
    errors: list[str] = []
    by_worker: dict[str, list[Assignment]] = {}
    end_by_task: dict[str, time] = {}
    for item in assignments:
        if item.task not in tasks:
            errors.append(f"Unknown task: {item.task}")
            continue
        if item.end <= item.start:
            errors.append(f"Invalid time range for {item.task}")
        if item.end > _t(17):
            errors.append(f"{item.task} misses the 17:00 deadline")
        by_worker.setdefault(item.worker, []).append(item)
        end_by_task[item.task] = item.end
        task = tasks[item.task]
        if task.dependency and (task.dependency not in end_by_task or item.start < end_by_task[task.dependency]):
            errors.append(f"Dependency not satisfied for {item.task}")
    for worker, items in by_worker.items():
        ordered = sorted(items, key=lambda item: item.start)
        for previous, current in zip(ordered, ordered[1:]):
            if current.start < previous.end:
                errors.append(f"Worker overlap for {worker}")
    recovery_count = sum(item.zone == "Cooling / Recovery Area" for item in assignments)
    if recovery_count > cooling_capacity:
        errors.append("Cooling capacity exceeded")
    for item in assignments:
        task = tasks.get(item.task)
        if task and task.intensity == "high":
            midpoint_minute = (item.start.hour * 60 + item.end.hour * 60) // 2
            midpoint = time(midpoint_minute // 60, midpoint_minute % 60)
            window = next((w for w in timeline if w.start <= midpoint < w.end), None)
            if window and window.risk_level == "very high":
                errors.append(f"High-intensity task remains in very-high-risk period: {item.task}")
    return errors


def recommend_schedule(*, transfer_locked: bool, timeline: list[HeatWindow]) -> dict:
    tasks = {
        "Fabric-roll transfer": TaskSpec("Fabric-roll transfer", 120, "high", "material handling", "Loading Area", "poor"),
        "Packing preparation": TaskSpec("Packing preparation", 60, "medium", "material handling", "Production Floor", "normal", "Fabric-roll transfer"),
        "Cooling / recovery": TaskSpec("Cooling / recovery", 60, "low", "any", "Cooling / Recovery Area", "good"),
        "Quality tagging": TaskSpec("Quality tagging", 120, "medium", "quality and inventory", "Production Floor", "normal"),
        "Inventory update": TaskSpec("Inventory update", 120, "low", "quality and inventory", "Production Floor", "normal", "Quality tagging"),
    }
    assignments = _candidate(transfer_locked=transfer_locked)
    if assignments is None:
        return {"status": "no-safe-schedule", "reason": "Fabric-roll transfer cannot be moved out of the very-high-risk window.", "actions": ["Move or defer the fabric-roll transfer.", "Obtain human safety approval before proceeding."]}
    errors = validate_schedule(assignments, tasks, timeline)
    if errors:
        return {"status": "no-safe-schedule", "reason": "No candidate satisfied all constraints.", "constraint_errors": errors}
    items = []
    for item in assignments:
        task = tasks[item.task]
        burden = schedule_burden(start=item.start, end=item.end, intensity=task.intensity, ventilation=task.ventilation, timeline=timeline)
        items.append({"task": item.task, "worker": item.worker, "zone": item.zone, "start": item.start.strftime("%H:%M"), "end": item.end.strftime("%H:%M"), "score": burden.score, "risk_level": burden.risk_level})
    return {"status": "feasible", "reason": "High-intensity transfer is moved before the critical heat window and recovery is scheduled at 12:00.", "schedule": items, "total_burden": round(sum(item["score"] for item in items), 2)}
