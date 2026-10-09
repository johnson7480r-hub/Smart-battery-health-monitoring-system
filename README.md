# Smart Battery Health Monitoring System

A GitHub-ready starter project for monitoring battery condition through a lightweight Flask dashboard. It includes simulated live telemetry, estimated State of Charge (SoC), estimated State of Health (SoH), temperature/voltage warnings, and CSV logging.

> **Prototype note:** The included data source is simulated so the project runs without hardware. SoH is a demo estimate based on configured nominal capacity and a simple degradation model, not a certified battery diagnostic. For real batteries, use a suitable BMS/sensor interface and follow the battery manufacturer's safety guidance.

## Features

- Live dashboard with voltage, current, temperature, SoC, and estimated SoH
- Status indicators for normal, warning, and critical readings
- Recent telemetry table and downloadable CSV log
- Configurable battery thresholds
- Responsive browser UI
- Simple modular structure to replace simulated readings with a real sensor/BMS source

## Requirements

- Python 3.10+
- pip

## Run locally

```bash
# 1. Create and activate a virtual environment (recommended)
python -m venv .venv

# Windows PowerShell:
.venv\Scripts\Activate.ps1

# macOS/Linux:
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the app
python app.py
```

Open http://127.0.0.1:5000 in your browser.

## Configuration

Edit `config.py` to change nominal capacity and alert thresholds. Values are demo defaults for a generic low-voltage battery and must be adapted to your actual battery chemistry and pack specifications.

## Project structure

```text
smart-battery-health-monitor/
├── app.py
├── config.py
├── battery_monitor.py
├── requirements.txt
├── .gitignore
├── LICENSE
├── README.md
├── templates/
│   └── index.html
└── static/
    ├── css/style.css
    └── js/dashboard.js
```

## Connect real hardware

Replace `SimulatedBatterySource.read()` in `battery_monitor.py` with a data adapter for your battery management system (BMS), microcontroller, or sensor gateway. Keep the same dictionary fields:

- `voltage_v`
- `current_a` (positive = discharge in this demo)
- `temperature_c`
- `soc_pct`
- `soh_pct`
- `timestamp`

Do not connect a GPIO/I²C/serial adapter until the pinout, voltage levels, isolation, and sensor limits have been verified for your hardware.

## API endpoints

- `GET /api/telemetry` — latest reading and alert state
- `GET /api/history?limit=20` — recent readings
- `GET /api/export.csv` — download logged readings

## GitHub upload

```bash
git init
git add .
git commit -m "Initial commit: smart battery health monitoring system"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/smart-battery-health-monitor.git
git push -u origin main
```

Create an empty repository on GitHub first. Do not commit `.venv/`, secrets, or real user data.
