from fastapi import FastAPI

app = FastAPI(title="RT Scheduler API")

@app.get("/")
def read_root():
    return {"message": "Real-Time Scheduling API"}