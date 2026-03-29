# Real-Time Scheduling Algorithm Simulator

Build a simulator for real-time scheduling algorithms such as Rate Monotonic and Earliest Deadline First. The tool visualizes task execution, deadlines, preemption, and missed deadlines, helping users understand real-time constraints and scheduling behavior.

## Features

- Simulate Rate Monotonic (RM) and Earliest Deadline First (EDF) scheduling algorithms
- Interactive web interface built with Reflex
- REST API built with FastAPI
- Visualization of task execution timeline, preemption, and missed deadlines

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Karam2006-dev/Real-Time-Scheduling-Algorithm-Simulator.git
   cd Real-Time-Scheduling-Algorithm-Simulator
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the FastAPI backend:
   ```bash
   uvicorn api.main:app --reload --port 8000
   ```

2. In another terminal, start the Reflex frontend:
   ```bash
   reflex run
   ```

3. Open your browser to `http://localhost:3000` to access the simulator.

## API Endpoints

- `POST /simulate/rm`: Simulate Rate Monotonic scheduling
- `POST /simulate/edf`: Simulate Earliest Deadline First scheduling

Send a JSON array of tasks with fields: id, name, period, execution_time, deadline (optional).
