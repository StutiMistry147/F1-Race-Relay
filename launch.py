"""
launch.py  —  F1 Race Relay  ·  Project Launcher
Run:  python launch.py
"""

import os
import sys
import subprocess
from datetime import datetime

# ── ANSI helpers ─────────────────────────────────────────────────────────────
RST  = "\033[0m"; BOLD = "\033[1m"; DIM = "\033[2m"
BLUE = "\033[38;2;53;88;114m"
LB   = "\033[38;2;122;170;206m"
SKY  = "\033[38;2;156;213;255m"
GRN  = "\033[38;2;76;175;130m"
RED  = "\033[38;2;224;82;82m"

def clr(t, *c): return "".join(c) + str(t) + RST
def ok(m):  print(clr(f"  ✓  {m}", GRN))
def err(m): print(clr(f"  ✗  {m}", RED))
def info(m):print(clr(f"  ·  {m}", DIM))

BANNER = f"""{BLUE}{BOLD}
  ╔══════════════════════════════════════════════════════════╗
  ║                                                          ║
  ║   F1  RACE  RELAY                                        ║
  ║   Professional Formula 1 Analytics                      ║
  ║                                                          ║
  ╚══════════════════════════════════════════════════════════╝{RST}"""

REQUIRED = ["fastf1", "pandas", "matplotlib", "seaborn",
            "plotly", "flask", "flask_cors"]

GUI_REQUIRED = ["PySide6"]


def check_dependencies(packages=REQUIRED):
    print(clr("\n  Checking dependencies…", DIM))
    ok_all = True
    for pkg in packages:
        try:
            __import__(pkg.replace("-", "_"))
            ok(pkg)
        except ImportError:
            print(clr(f"  ✗  {pkg} — installing…", RED))
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install",
                     pkg.replace("_", "-"), "-q"],
                    stdout=subprocess.DEVNULL,
                )
                ok(f"{pkg} installed")
            except Exception:
                err(f"Failed to install {pkg}")
                ok_all = False
    return ok_all


def create_project_structure():
    folders = ["modern_plots", "interactive_plots", "podium_plots",
               "dashboards", "exports", "data_cache"]
    print(clr("\n  Creating project structure…", DIM))
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        status = "exists" if os.path.exists(folder) else "created"
        info(f"{folder}/  [{status}]")


def run_api():
    api_path = os.path.join(os.path.dirname(__file__), "api.py")
    if not os.path.exists(api_path):
        err("api.py not found in project folder")
        return
    print(clr("\n  Starting Flask API on http://localhost:5000 …", LB))
    print(clr("  Open index.html in your browser to use the web dashboard.", DIM))
    print(clr("  Press Ctrl+C to stop.\n", DIM))
    try:
        subprocess.run([sys.executable, "api.py"])
    except KeyboardInterrupt:
        print(clr("\n  API stopped.\n", DIM))


def open_browser():
    index = os.path.join(os.path.dirname(__file__), "index.html")
    if not os.path.exists(index):
        err("index.html not found")
        return
    print(clr("  Opening index.html …", LB))
    if sys.platform == "win32":
        os.startfile(index)
    elif sys.platform == "darwin":
        subprocess.run(["open", index])
    else:
        subprocess.run(["xdg-open", index])


def run_gui():
    gui_path = os.path.join(os.path.dirname(__file__), "modern_gui.py")
    if not os.path.exists(gui_path):
        err("modern_gui.py not found")
        return
    if not check_dependencies(GUI_REQUIRED):
        err("PySide6 is required for the desktop GUI")
        return
    print(clr("\n  Launching Desktop GUI …\n", LB))
    subprocess.run([sys.executable, "modern_gui.py"])


def run_terminal():
    main_path = os.path.join(os.path.dirname(__file__), "main.py")
    if not os.path.exists(main_path):
        err("main.py not found")
        return
    print(clr("\n  Launching Terminal CLI …\n", LB))
    subprocess.run([sys.executable, "main.py"])


def run_visuals():
    plots_path = os.path.join(os.path.dirname(__file__), "modern_plots.py")
    if not os.path.exists(plots_path):
        err("modern_plots.py not found")
        return
    year  = input(clr("  Year  (e.g. 2023) ▸ ", LB)).strip() or "2023"
    track = input(clr("  Track (e.g. Monaco) ▸ ", LB)).strip() or "Monaco"
    print(clr(f"\n  Generating visuals for {year} {track} …\n", DIM))
    try:
        import modern_plots
        modern_plots.generate_all_visuals(int(year), track)
    except Exception as e:
        err(f"Error: {e}")


def test_connection():
    print(clr("\n  Testing FastF1 connection …", DIM))
    try:
        import fastf1
        fastf1.Cache.enable_cache("data_cache")
        s = fastf1.get_session(2023, "Monaco", "R")
        s.load(telemetry=False, weather=False)
        ok(f"FastF1 OK  ·  {len(s.laps)} laps loaded  ·  {len(s.results)} drivers")
        ok(f"Event: {s.event.get('EventName', 'Monaco')}")
    except Exception as e:
        err(f"Connection failed: {e}")
        info("Tip: check your internet connection and try again")


def main_menu():
    OPTS = [
        ("Start Web Dashboard (API + browser)",  run_api),
        ("Open index.html in browser",           open_browser),
        ("Launch Desktop GUI (PySide6)",          run_gui),
        ("Launch Terminal CLI",                   run_terminal),
        ("Generate Visualizations",               run_visuals),
        ("Test FastF1 Connection",                test_connection),
        ("Check & Install Dependencies",          lambda: check_dependencies()),
        ("Exit",                                  None),
    ]

    while True:
        print(f"\n  {clr('═'*54, BLUE)}")
        print(f"  {clr('F1 RACE RELAY  ·  LAUNCHER', BOLD, LB)}")
        print(f"  {clr('═'*54, BLUE)}")
        for i, (label, _) in enumerate(OPTS, 1):
            print(f"  {clr(i, BOLD, LB)}.  {label}")
        print(f"  {clr('═'*54, BLUE)}")

        choice = input(clr("\n  Select option ▸ ", LB)).strip()
        if not choice.isdigit() or not (1 <= int(choice) <= len(OPTS)):
            err("Invalid choice."); continue

        label, action = OPTS[int(choice) - 1]
        if action is None:
            print(clr("\n  Goodbye! 🏁\n", BOLD, LB))
            break
        action()


if __name__ == "__main__":
    print(BANNER)
    print(clr(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ·  Python {sys.version.split()[0]}", DIM))
    create_project_structure()
    check_dependencies()
    main_menu()
