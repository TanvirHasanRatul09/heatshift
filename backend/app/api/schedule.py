from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import HeatCondition
from ..services.heat_burden import HeatWindow
from ..services.scheduler import recommend_schedule

router = APIRouter(prefix="/api/schedule", tags=["schedule"])


class RecommendationRequest(BaseModel):
    transfer_locked: bool = False


@router.post("/recommend")
def recommend(request: RecommendationRequest, db: Session = Depends(get_db)):
    conditions = db.query(HeatCondition).order_by(HeatCondition.start_time).all()
    timeline = [HeatWindow(item.start_time, item.end_time, item.risk_level) for item in conditions]
    result = recommend_schedule(transfer_locked=request.transfer_locked, timeline=timeline)
    return {"disclaimer": "Estimated occupational heat exposure — simulated comparison, not medical guidance.", **result}
