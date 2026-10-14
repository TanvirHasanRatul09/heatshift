from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import HeatCondition, ScheduleItem, Task, Workplace, Worker, Zone
from ..services.heat_burden import HeatWindow, critical_window, schedule_burden

router = APIRouter(prefix="/api/demo", tags=["demo"])


def as_time(value):
    return value.strftime("%H:%M")


@router.get("/scenario")
def scenario(db: Session = Depends(get_db)):
    workplace = db.query(Workplace).first()
    if workplace is None:
        raise HTTPException(status_code=404, detail="Demo scenario is not seeded. Run python -m app.seed.")
    return {
        "data_status": "simulated/demo data",
        "workplace": {"id": workplace.id, "name": workplace.name, "location": workplace.location},
        "shift": {"start": "09:00", "end": "17:00", "deadline": "17:00"},
        "zones": [{"name": z.name, "ventilation": z.ventilation, "cooling_area": z.cooling_area, "cooling_capacity": z.cooling_capacity} for z in db.query(Zone).filter_by(workplace_id=workplace.id)],
        "workers": [{"name": w.name, "skill": w.skill, "available_from": as_time(w.available_from), "available_until": as_time(w.available_until)} for w in db.query(Worker).filter_by(workplace_id=workplace.id)],
        "tasks": [{"name": t.name, "intensity": t.intensity, "duration_minutes": t.duration_minutes, "required_skill": t.required_skill, "dependency": t.dependency} for t in db.query(Task).filter_by(workplace_id=workplace.id)],
        "heat_conditions": [{"start": as_time(h.start_time), "end": as_time(h.end_time), "risk_level": h.risk_level, "risk_score": h.risk_score} for h in db.query(HeatCondition).filter_by(workplace_id=workplace.id)],
        "original_schedule": [{"task": s.task_name, "worker": s.worker_name, "zone": s.zone_name, "start": as_time(s.start_time), "end": as_time(s.end_time)} for s in db.query(ScheduleItem).filter_by(workplace_id=workplace.id, is_original=True)],
    }


@router.get("/heat-burden")
def heat_burden(db: Session = Depends(get_db)):
    workplace = db.query(Workplace).first()
    if workplace is None:
        raise HTTPException(status_code=404, detail="Demo scenario is not seeded. Run python -m app.seed.")
    conditions = db.query(HeatCondition).filter_by(workplace_id=workplace.id).all()
    timeline = [HeatWindow(h.start_time, h.end_time, h.risk_level) for h in conditions]
    schedule = db.query(ScheduleItem).filter_by(workplace_id=workplace.id, is_original=True).all()
    tasks = {task.name: task for task in db.query(Task).filter_by(workplace_id=workplace.id)}
    zones = {zone.name: zone for zone in db.query(Zone).filter_by(workplace_id=workplace.id)}
    items = []
    for item in schedule:
        task = tasks[item.task_name]
        zone = zones[item.zone_name]
        result = schedule_burden(start=item.start_time, end=item.end_time, intensity=task.intensity, ventilation=zone.ventilation, timeline=timeline)
        items.append({"task": item.task_name, "start": as_time(item.start_time), "end": as_time(item.end_time), "score": result.score, "risk_level": result.risk_level, "factors": result.factors})
    return {"disclaimer": "Estimated occupational heat exposure — simulated comparison, not medical guidance.", "critical_window": {"start": as_time(critical_window(timeline).start), "end": as_time(critical_window(timeline).end), "risk_level": critical_window(timeline).risk_level}, "original_schedule": items, "total_burden": round(sum(item["score"] for item in items), 2)}
