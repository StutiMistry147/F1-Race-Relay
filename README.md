# F1 Race Relay

A Formula 1 race analytics platform that transforms FastF1 timing data
into driver comparisons and race visualizations across three interfaces —
a Flask-powered web dashboard, a PySide6 desktop GUI, and a terminal CLI.
<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/bc3b8b27-fcd8-4ffc-b7c0-36014b864400" />

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
```
| Endpoint | Parameters | Description |
|---|---|---|
| `GET /race` | `year`, `track` | Full race classification |
| `GET /compare` | `year`, `track`, `d1`, `d2` | Head-to-head stats |
| `GET /visuals` | `year`, `track` | Generate all plot files |
| `GET /health` | — | API status and config |
| `GET /seasons` | — | Available years |
```
----
## Data and Outputs

Works with any FastF1-supported season. Tested across 2021–2024 at
Monaco, Bahrain, Silverstone, Spa, Monza, Suzuka, and more. First load
per race downloads and caches data locally in `data_cache/` — subsequent
loads are instant.

Visualizations are saved to `modern_plots/`, `interactive_plots/`,
`podium_plots/`, and `dashboards/`.
