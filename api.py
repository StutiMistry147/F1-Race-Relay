"""
api.py  —  F1 Race Relay  ·  Flask REST backend
Connects index.html  →  FastF1  →  modern_plots  →  main analysis helpers
Run:  python api.py
"""

import os
import sys
import json
import math
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import fastf1
import pandas as pd

# ── optional: import your own modules ──────────────────────────────────────
try:
    import modern_plots
    HAS_PLOTS = True
except ImportError:
    HAS_PLOTS = False

# ───────────────────────────────────────────────────────────────────────────
app = Flask(__name__, static_folder=".", static_url_path="")
CORS(app)

CACHE_DIR = os.path.join(os.path.dirname(__file__), "data_cache")
os.makedirs(CACHE_DIR, exist_ok=True)
fastf1.Cache.enable_cache(CACHE_DIR)

OUTPUT_DIRS = ["modern_plots", "interactive_plots", "podium_plots", "dashboards"]
for d in OUTPUT_DIRS:
    os.makedirs(d, exist_ok=True)


# ── helpers ─────────────────────────────────────────────────────────────────
def safe_str(val, maxlen=40):
    if val is None or (isinstance(val, float) and math.isnan(val)):
        return "N/A"
    return str(val)[:maxlen]


def td_to_str(td):
    """Convert a Timedelta to a readable string."""
    try:
        if pd.isna(td):
            return "DNF"
        total = td.total_seconds()
        if total < 0:
            return "DNF"
        mins = int(total // 60)
        secs = total % 60
        return f"{mins}:{secs:06.3f}"
    except Exception:
        return str(td)[:12]


def td_to_sec(td):
    try:
        if pd.isna(td):
            return None
        return td.total_seconds()
    except Exception:
        return None


def load_session(year, track, telemetry=False):
    session = fastf1.get_session(int(year), track, "R")
    session.load(telemetry=telemetry, weather=False)
    return session


# ── serve index.html at / ──────────────────────────────────────────────────
@app.route("/")
def index():
    index_path = os.path.join(os.path.dirname(__file__), "index.html")
    if os.path.exists(index_path):
        return send_from_directory(os.path.dirname(__file__), "index.html")
    return "<h2>F1 Race Relay API is running. Place index.html in the same folder.</h2>"


# ── GET /race?year=2023&track=Monaco ──────────────────────────────────────
@app.route("/race")
def race():
    year  = request.args.get("year",  "2023")
    track = request.args.get("track", "Monaco")

    try:
        session = load_session(year, track)
        results = session.results

        rows = []
        leader_secs = None

        for i, (_, row) in enumerate(results.iterrows()):
            time_td = row.get("Time")
            time_str = td_to_str(time_td)

            # gap from leader
            if i == 0:
                leader_secs = td_to_sec(time_td)
                gap_str = "WINNER"
            else:
                secs = td_to_sec(time_td)
                if secs and leader_secs:
                    diff = secs - leader_secs
                    gap_str = f"+{diff:.3f}s"
                else:
                    gap_str = "—"

            rows.append({
                "pos":    i + 1,
                "code":   safe_str(row.get("Abbreviation")),
                "driver": safe_str(row.get("FullName"), 25),
                "team":   safe_str(row.get("TeamName"), 25),
                "time":   time_str,
                "gap":    gap_str,
            })

        # fastest lap
        fastest_info = {"driver": "—", "time": "—", "lap": "—", "tire": "—"}
        try:
            if not session.laps.empty:
                fl = session.laps.pick_fastest()
                fastest_info = {
                    "driver": safe_str(fl.get("Driver")),
                    "time":   td_to_str(fl.get("LapTime")),
                    "lap":    int(fl.get("LapNumber", 0)),
                    "tire":   safe_str(fl.get("Compound", "—")),
                }
        except Exception:
            pass

        # event meta
        event_name = safe_str(session.event.get("EventName",  track))
        event_date = safe_str(session.event.get("EventDate",  year))[:10]
        total_laps = safe_str(getattr(session, "total_laps", "—"))

        return jsonify({
            "ok":         True,
            "year":       year,
            "track":      track,
            "eventName":  event_name,
            "eventDate":  event_date,
            "totalLaps":  total_laps,
            "winner":     rows[0]["driver"] if rows else "—",
            "winnerCode": rows[0]["code"]   if rows else "—",
            "winnerTeam": rows[0]["team"]   if rows else "—",
            "finishers":  len(rows),
            "fastestLap": fastest_info,
            "results":    rows,
        })

    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


# ── GET /compare?year=2023&track=Monaco&d1=HAM&d2=VER ─────────────────────
@app.route("/compare")
def compare():
    year  = request.args.get("year",  "2023")
    track = request.args.get("track", "Monaco")
    d1    = request.args.get("d1",    "HAM").upper()
    d2    = request.args.get("d2",    "VER").upper()

    if d1 == d2:
        return jsonify({"ok": False, "error": "Choose two different drivers"}), 400

    try:
        session = load_session(year, track, telemetry=False)

        def driver_stats(code):
            laps = session.laps.pick_driver(code)
            if laps.empty:
                raise ValueError(f"No laps found for {code}")
            fl   = laps.pick_fastest()
            rrow = session.results[session.results["Abbreviation"] == code]
            pos  = int(rrow.iloc[0].get("Position", 0) or 0) if not rrow.empty else 0
            team = safe_str(rrow.iloc[0].get("TeamName")) if not rrow.empty else "—"
            return {
                "code":     code,
                "team":     team,
                "fastest":  td_to_str(fl.get("LapTime")),
                "fastestS": td_to_sec(fl.get("LapTime")),
                "fastLap":  int(fl.get("LapNumber", 0)),
                "avgLap":   td_to_str(laps["LapTime"].mean()),
                "totalLaps": len(laps),
                "position": pos,
            }

        s1 = driver_stats(d1)
        s2 = driver_stats(d2)

        delta  = None
        faster = None
        if s1["fastestS"] and s2["fastestS"]:
            delta  = round(abs(s1["fastestS"] - s2["fastestS"]), 3)
            faster = d1 if s1["fastestS"] < s2["fastestS"] else d2

        return jsonify({
            "ok":     True,
            "year":   year,
            "track":  track,
            "d1":     s1,
            "d2":     s2,
            "delta":  delta,
            "faster": faster,
        })

    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


# ── GET /visuals?year=2023&track=Monaco ───────────────────────────────────
@app.route("/visuals")
def visuals():
    year  = request.args.get("year",  "2023")
    track = request.args.get("track", "Monaco")

    if not HAS_PLOTS:
        return jsonify({"ok": False, "error": "modern_plots.py not found"}), 500

    try:
        modern_plots.generate_all_visuals(int(year), track)
        files = [
            f"modern_plots/{year}_{track}_lap_comparison.png",
            f"interactive_plots/{year}_{track}_interactive.html",
            f"podium_plots/{year}_{track}_podium.png",
            f"dashboards/{year}_{track}_dashboard.png",
        ]
        return jsonify({
            "ok":      True,
            "message": f"All visuals generated for {year} {track}",
            "files":   files,
        })
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


# ── GET /seasons  (available years) ───────────────────────────────────────
@app.route("/seasons")
def seasons():
    return jsonify({"ok": True, "years": ["2024", "2023", "2022", "2021"]})


# ── health check ──────────────────────────────────────────────────────────
@app.route("/health")
def health():
    return jsonify({
        "ok":         True,
        "status":     "F1 Race Relay API running",
        "cache":      CACHE_DIR,
        "hasPlots":   HAS_PLOTS,
    })


# ───────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n" + "═" * 52)
    print("  F1 Race Relay  ·  API Server")
    print("═" * 52)
    print(f"  http://localhost:5000/")
    print(f"  http://localhost:5000/health")
    print(f"  Cache  →  {CACHE_DIR}")
    print(f"  Plots  →  {'enabled' if HAS_PLOTS else 'modern_plots.py not found'}")
    print("═" * 52 + "\n")
    app.run(host="0.0.0.0", port=5000, debug=True)
