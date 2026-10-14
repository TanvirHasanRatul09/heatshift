from datetime import time

from .database import Base, SessionLocal, engine
from .models import HeatCondition, ScheduleItem, Task, Workplace, Worker, Zone


def seed_database(reset: bool = True) -> None:
    Base.metadata.create_all(engine)
    db = SessionLocal()
    try:
        if reset:
            for model in (ScheduleItem, HeatCondition, Task, Worker, Zone, Workplace):
                db.query(model).delete()

        workplace = Workplace(name="Dhaka Garment Factory — Demo", location="Dhaka, Bangladesh", is_simulated=True)
        db.add(workplace)
        db.flush()
        zones = [
            Zone(workplace_id=workplace.id, name="Production Floor", ventilation="normal"),
            Zone(workplace_id=workplace.id, name="Loading Area", ventilation="poor"),
            Zone(workplace_id=workplace.id, name="Cooling / Recovery Area", ventilation="good", cooling_area=True, cooling_capacity=4),
        ]
        db.add_all(zones)
        db.add_all([
            Worker(workplace_id=workplace.id, name="Worker A", skill="material handling", available_from=time(9), available_until=time(17)),
            Worker(workplace_id=workplace.id, name="Worker B", skill="quality and inventory", available_from=time(9), available_until=time(17)),
        ])
        db.add_all([
            Task(workplace_id=workplace.id, name="Fabric-roll transfer", intensity="high", duration_minutes=120, required_skill="material handling"),
            Task(workplace_id=workplace.id, name="Quality tagging", intensity="medium", duration_minutes=120, required_skill="quality and inventory"),
            Task(workplace_id=workplace.id, name="Packing preparation", intensity="medium", duration_minutes=60, required_skill="material handling", dependency="Fabric-roll transfer"),
            Task(workplace_id=workplace.id, name="Cooling / recovery", intensity="low", duration_minutes=60, required_skill="any"),
            Task(workplace_id=workplace.id, name="Inventory update", intensity="low", duration_minutes=120, required_skill="quality and inventory", dependency="Quality tagging"),
        ])
        db.add_all([
            HeatCondition(workplace_id=workplace.id, start_time=time(9), end_time=time(12), risk_level="moderate", risk_score=2),
            HeatCondition(workplace_id=workplace.id, start_time=time(12), end_time=time(15), risk_level="very high", risk_score=4),
            HeatCondition(workplace_id=workplace.id, start_time=time(15), end_time=time(17), risk_level="high", risk_score=3),
        ])
        db.add_all([
            ScheduleItem(workplace_id=workplace.id, task_name="Fabric-roll transfer", worker_name="Worker A", zone_name="Loading Area", start_time=time(13), end_time=time(15), is_original=True),
            ScheduleItem(workplace_id=workplace.id, task_name="Quality tagging", worker_name="Worker B", zone_name="Production Floor", start_time=time(9), end_time=time(11), is_original=True),
            ScheduleItem(workplace_id=workplace.id, task_name="Packing preparation", worker_name="Worker A", zone_name="Production Floor", start_time=time(15), end_time=time(16), is_original=True),
            ScheduleItem(workplace_id=workplace.id, task_name="Inventory update", worker_name="Worker B", zone_name="Production Floor", start_time=time(15), end_time=time(17), is_original=True),
        ])
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
    print("Seeded simulated HEATSHIFT database.")
