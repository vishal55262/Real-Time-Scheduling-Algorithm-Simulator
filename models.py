from pydantic import BaseModel
from typing import List, Optional

class Task(BaseModel):
    id: int
    name: str
    period: int  # in time units
    execution_time: int  # in time units
    deadline: Optional[int] = None  # if None, deadline = period

    @property
    def priority_rm(self) -> float:
        """Rate Monotonic priority: higher for shorter period"""
        return 1.0 / self.period

    @property
    def effective_deadline(self) -> int:
        return self.deadline if self.deadline is not None else self.period

class ScheduleEvent(BaseModel):
    time: int
    task_id: int
    action: str  # 'start', 'preempt', 'complete', 'missed'

class SimulationResult(BaseModel):
    events: List[ScheduleEvent]
    total_time: int
    missed_deadlines: List[int]  # task ids that missed deadlines