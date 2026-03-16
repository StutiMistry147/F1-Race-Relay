"""
main.py  —  F1 Race Relay  ·  Terminal Analysis CLI
Run:  python main.py
"""

import os
import sys
from datetime import datetime
import fastf1
import pandas as pd

# ── ANSI colour helpers ─────────────────────────────────────────────────────
RST   = "\033[0m";  BOLD  = "\033[1m";  DIM   = "\033[2m"
BLUE  = "\033[38;2;53;88;114m"
LBLUE = "\033[38;2;122;170;206m"
SKY   = "\033[38;2;156;213;255m"
GOLD  = "\033[38;2;212;168;67m"
GREEN = "\033[38;2;76;175;130m"
RED   = "\033[38;2;224;82;82m"

def c(*codes): return "".join(codes)
def clr(text, *codes): return c(*codes) + str(text) + RST

def div(ch="─", w=72, color=BLUE): return clr(ch * w, color)
def header(t):
    print(); print(div("═")); print(clr(f"  {t}", BOLD, LBLUE)); print(div("═"))
def subheader(t):
    print(); print(clr(f"  ▸  {t}", BOLD, SKY)); print(div())
def ok(m):   print(clr(f"  ✓  {m}", GREEN))
def err(m):  print(clr(f"  ✗  {m}", RED))
def info(m): print(clr(f"  ·  {m}", DIM))

# ── Cache ────────────────────────────────────────────────────────────────────
CACHE = os.path.join(os.path.dirname(__file__), "data_cache")

def setup_cache():
    os.makedirs(CACHE, exist_ok=True)
    fastf1.Cache.enable_cache(CACHE)
    info(f"Cache → {CACHE}")

# ── Formatting ───────────────────────────────────────────────────────────────
def fmt_td(td):
    try:
        if pd.isna(td): return "DNF"
        t = td.total_seconds()
        if t < 0: return "DNF"
        return f"{int(t//60)}:{t%60:06.3f}"
    except Exception:
        return str(td)[:12]

def safe(val, n=30):
    if val is None: return "—"
    try:
        if pd.isna(val): return "—"
    except Exception:
        pass
    return str(val)[:n]

# ── Session loader ────────────────────────────────────────────────────────────
def load_session(year, track, telemetry=False):
    info(f"Loading {year} {track} [session R] …")
    s = fastf1.get_session(int(year), track, "R")
    s.load(telemetry=telemetry, weather=False)
    ok(f"Loaded  {len(s.laps)} laps  ·  {len(s.results)} drivers")
    return s

# ── Analyses ──────────────────────────────────────────────────────────────────
def show_race_results(session):
    subheader("Race Classification")
    R = session.results
    COL = (4, 5, 24, 24, 14)
    hdr_fmt = f"  {{:<{COL[0]}}}  {{:<{COL[1]}}}  {{:<{COL[2]}}}  {{:<{COL[3]}}}  {{}}"
    print(clr(hdr_fmt.format("POS", "CODE", "DRIVER", "TEAM", "TIME"), BOLD, BLUE))
    print(div())
    medal_fg = [GOLD, SKY, c(DIM)]
    for i, (_, row) in enumerate(R.iterrows()):
        pos  = i + 1
        code = safe(row.get("Abbreviation"), 5)
        name = safe(row.get("FullName"),     22)
        team = safe(row.get("TeamName"),     22)
        time = fmt_td(row.get("Time"))
        line = hdr_fmt.format(pos, code, name, team, time)
        col  = medal_fg[pos - 1] if pos <= 3 else RST
        print(clr(line, col))
    print(div())
    try:
        fl = session.laps.pick_fastest()
        print(clr(f"\n  Fastest Lap :  {fmt_td(fl.get('LapTime'))}  ({safe(fl.get('Driver'))})", GREEN))
    except Exception:
        pass


def show_fastest_laps(session, top=10):
    subheader(f"Fastest Laps  (top {top})")
    data = []
    for code in session.results["Abbreviation"]:
        laps = session.laps.pick_driver(code)
        if laps.empty: continue
        fl = laps.pick_fastest()
        if fl is None or pd.isna(fl.get("LapTime")): continue
        data.append({"code": code, "time": fl["LapTime"], "lap": int(fl["LapNumber"])})
    data.sort(key=lambda x: x["time"].total_seconds())
    print(clr(f"  {'#':<4}  {'DRV':<5}  {'LAP TIME':<13}  LAP #", BOLD, BLUE))
    print(div())
    for rank, d in enumerate(data[:top], 1):
        col = SKY if rank == 1 else (LBLUE if rank <= 3 else RST)
        print(clr(f"  {rank:<4}  {d['code']:<5}  {fmt_td(d['time']):<13}  {d['lap']}", col))
    print(div())


def show_comparison(session, d1, d2):
    subheader(f"Head-to-Head  ·  {d1}  vs  {d2}")

    def stats(code):
        laps = session.laps.pick_driver(code)
        if laps.empty: return None
        fl  = laps.pick_fastest()
        avg = laps["LapTime"].mean()
        rr  = session.results[session.results["Abbreviation"] == code]
        pos  = int(rr.iloc[0].get("Position") or 0) if not rr.empty else 0
        team = safe(rr.iloc[0].get("TeamName")) if not rr.empty else "—"
        return dict(team=team, pos=pos,
                    fastest=fl["LapTime"], fastestNo=int(fl["LapNumber"]),
                    avg=avg, laps=len(laps))

    s1, s2 = stats(d1), stats(d2)
    if not s1 or not s2:
        err("No data for one or both drivers."); return

    W = 26
    print(clr(f"  {'METRIC':<18}  {d1:<{W}}  {d2:<{W}}", BOLD, BLUE))
    print(div())
    rows = [
        ("Team",          safe(s1["team"]),        safe(s2["team"])),
        ("Finishing Pos", f"P{s1['pos']}",          f"P{s2['pos']}"),
        ("Fastest Lap",   fmt_td(s1["fastest"]),    fmt_td(s2["fastest"])),
        ("Fastest Lap #", str(s1["fastestNo"]),     str(s2["fastestNo"])),
        ("Average Lap",   fmt_td(s1["avg"]),        fmt_td(s2["avg"])),
        ("Total Laps",    str(s1["laps"]),          str(s2["laps"])),
    ]
    for label, v1, v2 in rows:
        print(f"  {clr(label+':',BOLD):<24}  "
              f"{clr(v1,LBLUE):<{W+8}}  {clr(v2,SKY):<{W+8}}")
    delta  = abs(s1["fastest"].total_seconds() - s2["fastest"].total_seconds())
    faster = d1 if s1["fastest"] < s2["fastest"] else d2
    print(div())
    print(clr(f"\n  ⚡  {faster} is faster by {delta:.3f}s on best lap\n", BOLD, SKY))


def show_stint_summary(session):
    subheader("Stint & Compound Summary")
    if "Compound" not in session.laps.columns:
        info("No compound data available."); return
    cmap = {
        "SOFT":"[38;2;220;60;60m", "MEDIUM":"[38;2;255;210;0m",
        "HARD":"[37m", "INTERMEDIATE":"[38;2;0;180;80m", "WET":"[38;2;0;100;200m",
    }
    print(clr(f"  {'DRV':<6}  {'STINT':<6}  {'COMPOUND':<14}  LAPS", BOLD, BLUE))
    print(div())
    for code in session.results["Abbreviation"]:
        laps = session.laps.pick_driver(code)
        if laps.empty: continue
        for stint_no, stint in laps.groupby("Stint"):
            compound = safe(stint["Compound"].iloc[0]) if "Compound" in stint else "?"
            col = "\033" + cmap.get(compound.upper(), "[0m")
            print(f"  {clr(code,LBLUE):<14}  {stint_no:<6}  {col}{compound:<14}{RST}  {len(stint)}")
    print(div())


def show_overview(session):
    subheader("Race Overview")
    w = session.results.iloc[0]
    rows = [
        ("Event",        safe(session.event.get("EventName"))),
        ("Circuit",      safe(session.event.get("Location"))),
        ("Date",         str(session.event.get("EventDate", ""))[:10]),
        ("Winner",       safe(w.get("FullName"))),
        ("Winning Team", safe(w.get("TeamName"))),
        ("Total Laps",   safe(getattr(session, "total_laps", "—"))),
        ("Finishers",    str(len(session.results))),
    ]
    for label, val in rows:
        print(f"  {clr(label+':',DIM):<26}  {clr(val,LBLUE)}")
    try:
        fl = session.laps.pick_fastest()
        print(f"  {clr('Fastest Lap:',DIM):<26}  "
              f"{clr(fmt_td(fl.get('LapTime')),GREEN)}  ({safe(fl.get('Driver'))})")
    except Exception:
        pass
    print(div())


# ── Interactive menu ──────────────────────────────────────────────────────────
def analysis_menu(session):
    year  = str(session.event["EventDate"].year)
    track = safe(session.event.get("Location"))
    OPTIONS = [
        ("Race Classification",   lambda: show_race_results(session)),
        ("Fastest Laps",          lambda: show_fastest_laps(session)),
        ("Driver Head-to-Head",   None),
        ("Stint / Tyre Summary",  lambda: show_stint_summary(session)),
        ("Race Overview Stats",   lambda: show_overview(session)),
        ("Load a different race", "reload"),
        ("Exit",                  "exit"),
    ]
    while True:
        header(f"F1 RACE RELAY  ·  {year}  {track}")
        for i, (label, _) in enumerate(OPTIONS, 1):
            print(f"{clr(f'  {i}.', BOLD, LBLUE)}  {label}")
        print()
        choice = input(clr("  Select option  ▸  ", LBLUE)).strip()
        if not choice.isdigit() or not (1 <= int(choice) <= len(OPTIONS)):
            err("Invalid choice."); continue
        _, action = OPTIONS[int(choice) - 1]
        if action == "exit":
            print(clr("\n  Thanks for using F1 Race Relay!\n", BOLD, LBLUE))
            sys.exit(0)
        if action == "reload":
            return "reload"
        if action is None:
            drivers = list(session.results["Abbreviation"])
            print(clr(f"\n  Drivers:  {', '.join(drivers)}", DIM))
            d1 = input(clr("  Driver 1  ▸  ", LBLUE)).strip().upper()
            d2 = input(clr("  Driver 2  ▸  ", LBLUE)).strip().upper()
            show_comparison(session, d1, d2)
        else:
            action()
        input(clr("\n  Press Enter to continue …", DIM))


def prompt_session():
    print()
    print(clr("  Examples:  2024 Monaco  ·  2023 Bahrain  ·  2022 Silverstone", DIM))
    year  = input(clr("  Year   ▸  ", LBLUE)).strip()
    track = input(clr("  Track  ▸  ", LBLUE)).strip()
    return year, track


def main():
    print(clr("""
  ╔══════════════════════════════════════════════════════╗
  ║   F1 RACE RELAY  ·  Terminal Analysis v2.0           ║
  ╚══════════════════════════════════════════════════════╝""", BOLD, BLUE))
    print(clr(f"  Python {sys.version.split()[0]}  ·  {datetime.now().strftime('%Y-%m-%d %H:%M')}\n", DIM))
    setup_cache()
    while True:
        year, track = prompt_session()
        try:
            session = load_session(year, track)
        except Exception as e:
            err(f"Could not load: {e}")
            info("Try:  2023 Monaco  /  2023 Bahrain  /  2022 Silverstone")
            continue
        if analysis_menu(session) != "reload":
            break


if __name__ == "__main__":
    main()
