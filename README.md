# F1 Race Relay

A multi-interface Formula 1 race analytics platform that transforms
FastF1 timing data into interactive dashboards, driver comparisons,
and broadcast-style visualizations across three separate interfaces.

---

## Interfaces

**Web Dashboard** — Browser-based terminal interface powered by a Flask
REST API. Features real-time loading states, live clock, API health
monitoring, driver comparison, and visualization triggers.

**Desktop GUI** — PySide6 Qt6 application with tabbed layout, threaded
data loading, medal-highlighted results table, and head-to-head driver
comparison cards.

**Terminal CLI** — Fully colored ANSI terminal interface for race
classification, fastest laps, head-to-head comparison, and tyre stint
summaries.

---

## Architecture
```
FastF1 API
    │
    ▼
api.py (Flask REST)          ◄──  index.html (Web Dashboard)
    │
    ├── /race                →  Full race classification + fastest lap
    ├── /compare             →  Head-to-head driver statistics  
    ├── /visuals             →  Triggers modern_plots.py
    └── /health              →  API status and configuration

modern_plots.py              ◄──  api.py / modern_gui.py / launch.py
    ├── Lap time comparison chart (PNG)
    ├── Interactive race replay (HTML)
    ├── Podium visualization (PNG)
    └── Full race dashboard (PNG)

modern_gui.py                →  PySide6 desktop application
main.py                      →  Terminal CLI
launch.py                    →  Unified project launcher
```

---

## Tech Stack

| Component | Technology |
|---|---|
| Data Source | FastF1 |
| REST API | Flask, Flask-CORS |
| Web Frontend | HTML, CSS, JavaScript |
| Desktop GUI | PySide6 (Qt6) |
| Static Plots | Matplotlib |
| Interactive Plots | Plotly |
| Data Processing | Pandas, NumPy |
| Caching | FastF1 local disk cache |

---

## Getting Started

### Install
```bash
git clone https://github.com/StutiMistry147/F1-Race-Relay.git
cd F1-Race-Relay
pip install -r requirements.txt
```

### Option 1 — Web Dashboard (recommended)
```bash
# Terminal 1
python api.py

# Terminal 2 — open in browser
open index.html
# or navigate to http://localhost:5000
```

### Option 2 — Desktop GUI
```bash
python modern_gui.py
```

### Option 3 — Terminal CLI
```bash
python main.py
```

### Option 4 — Unified Launcher
```bash
python launch.py
```

---

## API Reference

| Endpoint | Parameters | Description |
|---|---|---|
| `GET /race` | `year`, `track` | Full race classification |
| `GET /compare` | `year`, `track`, `d1`, `d2` | Head-to-head stats |
| `GET /visuals` | `year`, `track` | Generate all plot files |
| `GET /health` | — | API status and config |
| `GET /seasons` | — | Available years |
```bash
# Examples
curl "http://localhost:5000/race?year=2023&track=Monaco"
curl "http://localhost:5000/compare?year=2023&track=Monaco&d1=HAM&d2=VER"
```

---

## Generated Outputs

Visualization files are saved to local folders:
```
modern_plots/        →  Lap time comparison (PNG, 180 DPI)
interactive_plots/   →  Race replay dashboard (HTML)
podium_plots/        →  Podium visualization (PNG)
dashboards/          →  Full race dashboard (PNG)
```

---

## Supported Races

Works with any FastF1-supported season. Tested with 2021 — 2024
across Monaco, Bahrain, Silverstone, Spa, Monza, Hungaroring,
Suzuka, Imola, Zandvoort, and Singapore.

First load per race downloads and caches data locally in
`data_cache/`. Subsequent loads are instant.

---

## Project Structure
```
f1-race-relay/
├── api.py               # Flask REST backend
├── index.html           # Web dashboard frontend
├── modern_gui.py        # PySide6 desktop application
├── modern_plots.py      # Visualization generation engine
├── main.py              # Terminal CLI
├── launch.py            # Unified project launcher
├── requirements.txt     # Dependencies
├── data_cache/          # FastF1 local cache (auto-created)
├── modern_plots/        # PNG outputs (auto-created)
├── interactive_plots/   # HTML outputs (auto-created)
├── podium_plots/        # PNG outputs (auto-created)
├── dashboards/          # PNG outputs (auto-created)
└── README.md
```

---
