#!/usr/bin/env python3
"""
Script to run the Real-Time Scheduling Simulator.
Starts both FastAPI backend and Reflex frontend.
"""

import os
import socket
import subprocess
import sys
import time

def find_free_port(start=8000, end=8100):
    for port in range(start, end):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    raise RuntimeError("No free port found")


def run_backend(port):
    print(f"Starting FastAPI backend on port {port}...")
    return subprocess.Popen([sys.executable, "-m", "uvicorn", "api.main:app", "--port", str(port)])

def run_frontend(api_base_url):
    print("Starting Reflex frontend...")
    env = os.environ.copy()
    env["API_BASE_URL"] = api_base_url
    return subprocess.Popen([sys.executable, "-m", "reflex", "run"], env=env)

if __name__ == "__main__":
    backend_port = find_free_port(8000, 8100)
    backend = run_backend(backend_port)
    time.sleep(2)  # wait for backend to start
    frontend = run_frontend(f"http://127.0.0.1:{backend_port}")

    try:
        backend.wait()
        frontend.wait()
    except KeyboardInterrupt:
        print("Shutting down...")
        backend.terminate()
        frontend.terminate()