# F1 Race Relay

A Formula 1 race visualization and analytics platform built with Python.
Transforms raw FastF1 timing data into broadcast-style dashboards,
interactive charts, and driver comparison tools through a desktop GUI.

---

## Features

- **Race Results** — Full finishing order with fastest lap and gap times
- **Lap Time Analysis** — Multi-driver lap time comparison across full race distance
- **Driver Comparison** — Head-to-head fastest lap, finishing position, and delta
- **Position Heatmap** — Visual grid showing position changes across first 30 laps
- **Podium Visualization** — Styled podium graphic with driver and team info
- **Interactive Dashboard** — Plotly-based HTML export with hover telemetry
- **Desktop GUI** — Dark-mode PySide6 interface with real-time loading feedback

---

## Tech Stack

| Component | Technology |
|---|---|
| GUI | PySide6 (Qt6) |
| Data Source | FastF1 API |
| Data Processing | Pandas, NumPy |
| Static Plots | Matplotlib, Seaborn |
| Interactive Plots | Plotly |

---

## Getting Started
```bash
git clone https://github.com/StutiMistry147/F1-Race-Relay.git
cd F1-Race-Relay
pip install -r requirements.txt
python launch.py
```

## Running Options
```bash
# Recommended — launcher with menu
python launch.py

# Direct GUI
python modern_gui.py

# Generate visualizations only (no GUI)
python modern_plots.py
```

---

## Output

Generated files are saved to:
- `modern_plots/` — Lap time and fastest lap charts (PNG, 300 DPI)
- `interactive_plots/` — Race replay dashboard (HTML)
- `podium_plots/` — Podium visualization (PNG)
- `dashboards/` — Full race dashboard (PNG)

---

## Supported Races

Works with any FastF1-supported season and circuit. Tested with:
- 2023 Monaco, Bahrain, Silverstone
- 2022 Spa, Monza, Suzuka
- 2021 Hungaroring, Abu Dhabi

---

## Project Structure
```
f1-race-relay/
├── launch.py          # Entry point and launcher menu
├── modern_gui.py      # PySide6 desktop application
├── modern_plots.py    # Visualization generation engine
├── requirements.txt   # Dependencies
└── README.md
```

---
