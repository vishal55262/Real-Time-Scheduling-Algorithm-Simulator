from typing import List, Dict, Optional
from models import Task, ScheduleEvent, SimulationResult
import heapq

class Scheduler:
    def __init__(self, tasks: List[Task]):
        self.tasks = tasks
        self.total_time = 100  # default simulation time

    def simulate_rm(self) -> SimulationResult:
        """Simulate Rate Monotonic Scheduling"""
        return self._simulate(priority_type='rm')

    def simulate_edf(self) -> SimulationResult:
        """Simulate Earliest Deadline First Scheduling"""
        return self._simulate(priority_type='edf')

    def _simulate(self, priority_type: str) -> SimulationResult:
        events = []
        missed_deadlines = []
        current_time = 0
        running_task: Optional[Task] = None
        remaining_time: Dict[int, int] = {}  # task_id -> remaining execution time
        deadlines: Dict[int, int] = {}  # task_id -> absolute deadline
        next_release: Dict[int, int] = {task.id: 0 for task in self.tasks}

        while current_time < self.total_time:
            # Release new tasks
            for task in self.tasks:
                if next_release[task.id] == current_time:
                    remaining_time[task.id] = task.execution_time
                    deadlines[task.id] = current_time + task.effective_deadline
                    next_release[task.id] += task.period
                    events.append(ScheduleEvent(time=current_time, task_id=task.id, action='release'))

            # Check for missed deadlines
            for task_id, deadline in list(deadlines.items()):
                if current_time >= deadline and remaining_time.get(task_id, 0) > 0:
                    missed_deadlines.append(task_id)
                    del deadlines[task_id]
                    del remaining_time[task_id]
                    events.append(ScheduleEvent(time=current_time, task_id=task_id, action='missed'))

            # Select task to run
            ready_tasks = [task for task in self.tasks if task.id in remaining_time and remaining_time[task.id] > 0]
            if ready_tasks:
                if priority_type == 'rm':
                    selected_task = min(ready_tasks, key=lambda t: t.priority_rm)
                elif priority_type == 'edf':
                    selected_task = min(ready_tasks, key=lambda t: deadlines[t.id])
                else:
                    selected_task = ready_tasks[0]

                if running_task != selected_task:
                    if running_task:
                        events.append(ScheduleEvent(time=current_time, task_id=running_task.id, action='preempt'))
                    events.append(ScheduleEvent(time=current_time, task_id=selected_task.id, action='start'))
                    running_task = selected_task

                # Execute for one time unit
                remaining_time[selected_task.id] -= 1
                if remaining_time[selected_task.id] == 0:
                    events.append(ScheduleEvent(time=current_time + 1, task_id=selected_task.id, action='complete'))
                    del remaining_time[selected_task.id]
                    del deadlines[selected_task.id]
                    running_task = None
            else:
                running_task = None

            current_time += 1

        return SimulationResult(events=events, total_time=self.total_time, missed_deadlines=list(set(missed_deadlines)))