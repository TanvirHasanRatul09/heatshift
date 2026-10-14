from datetime import time

from sqlalchemy import Boolean, Float, ForeignKey, Integer, String, Time
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Workplace(Base):
    __tablename__ = "workplaces"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    location: Mapped[str] = mapped_column(String(120))
    is_simulated: Mapped[bool] = mapped_column(Boolean, default=True)


class Zone(Base):
    __tablename__ = "zones"
    id: Mapped[int] = mapped_column(primary_key=True)
    workplace_id: Mapped[int] = mapped_column(ForeignKey("workplaces.id"))
    name: Mapped[str] = mapped_column(String(120))
    ventilation: Mapped[str] = mapped_column(String(20))
    cooling_area: Mapped[bool] = mapped_column(Boolean, default=False)
    cooling_capacity: Mapped[int] = mapped_column(Integer, default=0)


class Worker(Base):
    __tablename__ = "workers"
    id: Mapped[int] = mapped_column(primary_key=True)
    workplace_id: Mapped[int] = mapped_column(ForeignKey("workplaces.id"))
    name: Mapped[str] = mapped_column(String(80))
    skill: Mapped[str] = mapped_column(String(80))
    available_from: Mapped[time] = mapped_column(Time)
    available_until: Mapped[time] = mapped_column(Time)
    is_simulated: Mapped[bool] = mapped_column(Boolean, default=True)


class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    workplace_id: Mapped[int] = mapped_column(ForeignKey("workplaces.id"))
    name: Mapped[str] = mapped_column(String(120))
    intensity: Mapped[str] = mapped_column(String(20))
    duration_minutes: Mapped[int] = mapped_column(Integer)
    required_skill: Mapped[str] = mapped_column(String(80))
    dependency: Mapped[str] = mapped_column(String(120), nullable=True)


class HeatCondition(Base):
    __tablename__ = "heat_conditions"
    id: Mapped[int] = mapped_column(primary_key=True)
    workplace_id: Mapped[int] = mapped_column(ForeignKey("workplaces.id"))
    start_time: Mapped[time] = mapped_column(Time)
    end_time: Mapped[time] = mapped_column(Time)
    risk_level: Mapped[str] = mapped_column(String(20))
    risk_score: Mapped[int] = mapped_column(Integer)


class ScheduleItem(Base):
    __tablename__ = "schedule_items"
    id: Mapped[int] = mapped_column(primary_key=True)
    workplace_id: Mapped[int] = mapped_column(ForeignKey("workplaces.id"))
    task_name: Mapped[str] = mapped_column(String(120))
    worker_name: Mapped[str] = mapped_column(String(80))
    zone_name: Mapped[str] = mapped_column(String(120))
    start_time: Mapped[time] = mapped_column(Time)
    end_time: Mapped[time] = mapped_column(Time)
    is_original: Mapped[bool] = mapped_column(Boolean, default=True)
