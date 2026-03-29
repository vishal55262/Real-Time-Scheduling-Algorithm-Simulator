from fastapi import FastAPI, HTTPException
from typing import List
from models import Task, SimulationResult
from scheduler import Scheduler

app = FastAPI(title="RT Scheduler API")

@app.get("/")
def read_root():
    return {"message": "Real-Time Scheduling API"}

@app.post("/simulate/rm", response_model=SimulationResult)
def simulate_rm(tasks: List[Task]):
    if not tasks:
        raise HTTPException(status_code=400, detail="No tasks provided")
    scheduler = Scheduler(tasks)
    return scheduler.simulate_rm()

@app.post("/simulate/edf", response_model=SimulationResult)
def simulate_edf(tasks: List[Task]):
    if not tasks:
        raise HTTPException(status_code=400, detail="No tasks provided")
    scheduler = Scheduler(tasks)
    return scheduler.simulate_edf()