#!/usr/bin/env python3
"""
Script to run the Real-Time Scheduling Simulator.
Starts both FastAPI backend and Reflex frontend.
"""

import subprocess
import sys
import time

def run_backend():
    print("Starting FastAPI backend...")
    return subprocess.Popen([sys.executable, "-m", "uvicorn", "api.main:app", "--reload", "--port", "8000"])

def run_frontend():
    print("Starting Reflex frontend...")
    return subprocess.Popen([sys.executable, "-m", "reflex", "run"])

if __name__ == "__main__":
    backend = run_backend()
    time.sleep(2)  # wait for backend to start
    frontend = run_frontend()

    try:
        backend.wait()
        frontend.wait()
    except KeyboardInterrupt:
        print("Shutting down...")
        backend.terminate()
        frontend.terminate()