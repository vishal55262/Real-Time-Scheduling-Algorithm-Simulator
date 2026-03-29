import reflex as rx
from typing import List
import httpx
from models import Task, ScheduleEvent

class State(rx.State):
    tasks: List[Task] = []
    algorithm: str = "rm"
    simulation_result: dict = {}
    task_name: str = ""
    task_period: str = ""
    task_execution: str = ""
    task_deadline: str = ""

    def add_task(self):
        if self.task_name and self.task_period and self.task_execution:
            try:
                period = int(self.task_period)
                execution = int(self.task_execution)
                deadline = int(self.task_deadline) if self.task_deadline else None
                new_task = Task(
                    id=len(self.tasks) + 1,
                    name=self.task_name,
                    period=period,
                    execution_time=execution,
                    deadline=deadline
                )
                self.tasks.append(new_task)
                self.task_name = ""
                self.task_period = ""
                self.task_execution = ""
                self.task_deadline = ""
            except ValueError:
                pass  # handle error

    def remove_task(self, task_id: int):
        self.tasks = [t for t in self.tasks if t.id != task_id]

    async def run_simulation(self):
        if not self.tasks:
            return
        endpoint = f"/simulate/{self.algorithm}"
        async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
            try:
                response = await client.post(endpoint, json=[t.dict() for t in self.tasks])
                self.simulation_result = response.json()
            except:
                self.simulation_result = {"error": "Failed to run simulation"}

def task_input():
    return rx.vstack(
        rx.heading("Add Task", size="md"),
        rx.input(placeholder="Task Name", value=State.task_name, on_change=State.set_task_name),
        rx.input(placeholder="Period", value=State.task_period, on_change=State.set_task_period),
        rx.input(placeholder="Execution Time", value=State.task_execution, on_change=State.set_task_execution),
        rx.input(placeholder="Deadline (optional)", value=State.task_deadline, on_change=State.set_task_deadline),
        rx.button("Add Task", on_click=State.add_task),
        spacing="2",
    )

def task_list():
    return rx.vstack(
        rx.heading("Tasks", size="md"),
        rx.foreach(
            State.tasks,
            lambda task: rx.hstack(
                rx.text(f"{task.name}: P={task.period}, C={task.execution_time}, D={task.deadline or task.period}"),
                rx.button("Remove", on_click=lambda: State.remove_task(task.id)),
                spacing="2",
            )
        ),
        spacing="2",
    )

def simulation_controls():
    return rx.vstack(
        rx.heading("Simulation", size="md"),
        rx.select(["rm", "edf"], value=State.algorithm, on_change=State.set_algorithm),
        rx.button("Run Simulation", on_click=State.run_simulation),
        spacing="2",
    )

def results_display():
    return rx.cond(
        State.simulation_result,
        rx.vstack(
            rx.heading("Results", size="md"),
            rx.text(f"Missed Deadlines: {State.simulation_result.get('missed_deadlines', [])}"),
            rx.text("Execution Timeline:"),
            rx.table(
                rx.thead(
                    rx.tr(
                        rx.th("Time"),
                        rx.th("Task"),
                        rx.th("Action"),
                    )
                ),
                rx.tbody(
                    rx.foreach(
                        State.simulation_result.get("events", []),
                        lambda event: rx.tr(
                            rx.td(event['time']),
                            rx.td(f"Task {event['task_id']}"),
                            rx.td(event['action']),
                        )
                    )
                ),
            ),
            spacing="2",
        ),
        rx.text("No results yet")
    )

def index():
    return rx.center(
        rx.vstack(
            rx.heading("Real-Time Scheduling Algorithm Simulator", size="lg"),
            rx.hstack(
                task_input(),
                task_list(),
                simulation_controls(),
                spacing="4",
            ),
            results_display(),
            spacing="4",
        ),
        height="100vh",
    )

app = rx.App(state=State)
app.add_page(index, route="/")