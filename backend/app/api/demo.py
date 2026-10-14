from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import HeatCondition, ScheduleItem, Workplace
from ..schemas import WhatIfRequest
from ..services.heat_burden import HeatWindow
from ..services.scheduler import recommend_schedule

router = APIRouter(prefix="/api/demo", tags=["demo workflow"])
DISCLAIMER = "Estimated occupational heat exposure — simulated comparison, not medical guidance."


def _timeline(db: Session, workplace_id: int):
    return db.query(HeatCondition).filter_by(workplace_id=workplace_id).order_by(HeatCondition.start_time).all()


def _workplace_or_404(db: Session):
    workplace = db.query(Workplace).first()
    if workplace is None:
        raise HTTPException(status_code=404, detail="Demo scenario is not seeded. Run python -m app.seed.")
    return workplace


@router.get("/original-schedule")
def original_schedule(db: Session = Depends(get_db)):
    workplace = _workplace_or_404(db)
    items = db.query(ScheduleItem).filter_by(workplace_id=workplace.id, is_original=True).order_by(ScheduleItem.start_time).all()
    return {"data_status": "simulated/demo data", "disclaimer": DISCLAIMER, "schedule": [{"task": x.task_name, "worker": x.worker_name, "zone": x.zone_name, "start": x.start_time.strftime("%H:%M"), "end": x.end_time.strftime("%H:%M")} for x in items]}


@router.get("/heat-timeline")
def heat_timeline(db: Session = Depends(get_db)):
    workplace = _workplace_or_404(db)
    conditions = _timeline(db, workplace.id)
    return {"data_status": "simulated/demo data", "disclaimer": DISCLAIMER, "timeline": [{"start": x.start_time.strftime("%H:%M"), "end": x.end_time.strftime("%H:%M"), "risk_level": x.risk_level, "risk_score": x.risk_score} for x in conditions]}


@router.post("/what-if")
def what_if(request: WhatIfRequest, db: Session = Depends(get_db)):
    workplace = _workplace_or_404(db)
    conditions = _timeline(db, workplace.id)
    timeline = [HeatWindow(x.start_time, x.end_time, x.risk_level) for x in conditions]
    result = recommend_schedule(transfer_locked=request.transfer_locked, timeline=timeline)
    return {"data_status": "simulated/demo data", "disclaimer": DISCLAIMER, "scenario": {"transfer_locked": request.transfer_locked}, **result}
