"""
modern_plots.py  —  F1 Race Relay  ·  Visualization Generator
Generates PNG + HTML plots via Matplotlib & Plotly.
Run standalone:  python modern_plots.py
Called by:       api.py  /  modern_gui.py  /  launch.py
"""

import os
import fastf1
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")          # headless — no display required
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Design tokens ──────────────────────────────────────────────────────────
BG      = "#0F1621"
BG2     = "#1A2332"
PRIMARY = "#355872"
A1      = "#7AAACE"
A2      = "#9CD5FF"
WARM    = "#F3E3D0"
BORDER  = "#D2C4B4"
GOLD    = "#D4A843"
SILVER  = "#9BA8B0"
BRONZE  = "#B07D52"

DRIVER_COLORS = [
    "#FF1801","#00D2BE","#FFFFFF","#FF8700","#0090FF",
    "#9B0000","#FFD700","#C0C0C0","#B07D52","#00A550",
    "#FF69B4","#006F62","#FFF500","#DC0000","#2B4562",
    "#0082FA","#B6BABD","#900000","#005AFF","#52E252",
]

plt.rcParams.update({
    "figure.facecolor":  BG,
    "axes.facecolor":    BG2,
    "text.color":        WARM,
    "axes.labelcolor":   WARM,
    "xtick.color":       BORDER,
    "ytick.color":       BORDER,
    "axes.edgecolor":    "#2A3A4A",
    "grid.color":        "#1E2D3A",
    "grid.linestyle":    "--",
    "grid.alpha":        0.4,
    "legend.facecolor":  BG2,
    "legend.edgecolor":  PRIMARY,
    "font.family":       "monospace",
})

CACHE_DIR = os.path.join(os.path.dirname(__file__), "data_cache")
os.makedirs(CACHE_DIR, exist_ok=True)
fastf1.Cache.enable_cache(CACHE_DIR)

for d in ["modern_plots", "interactive_plots", "podium_plots", "dashboards"]:
    os.makedirs(d, exist_ok=True)


# ── Helpers ────────────────────────────────────────────────────────────────
def fmt_td(td):
    try:
        if pd.isna(td): return "—"
        t = td.total_seconds()
        return f"{int(t//60)}:{t%60:06.3f}"
    except Exception:
        return "—"

def load(year, track, telemetry=False):
    session = fastf1.get_session(year, track, "R")
    session.load(telemetry=telemetry, weather=False)
    return session

def watermark(fig, text="F1 RACE RELAY"):
    fig.text(0.5, 0.978, text, fontsize=18, fontweight="bold",
             color=A1, ha="center", va="top", fontfamily="monospace",
             alpha=0.9)

def save(fig, path):
    fig.savefig(path, dpi=180, facecolor=BG, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✓  {path}")
    return path


# ── 1. Lap time comparison ─────────────────────────────────────────────────
def create_modern_lap_comparison(year, track, driver_count=6):
    try:
        session = load(year, track)
        top_drivers = list(session.results["Abbreviation"].head(driver_count))
        if not top_drivers:
            print(f"  ✗  No drivers found for {year} {track}")
            return None

        fig, axes = plt.subplots(1, 2, figsize=(18, 7))
        fig.suptitle(f"{year} {track} Grand Prix",
                     fontsize=20, fontweight="bold", color=A2,
                     y=0.96, fontfamily="monospace")

        ax_line, ax_bar = axes

        # ── Line chart: lap times
        for idx, drv in enumerate(top_drivers):
            laps = session.laps.pick_driver(drv)
            if laps.empty: continue
            valid = laps.dropna(subset=["LapTime"])
            if valid.empty: continue
            times = valid["LapTime"].dt.total_seconds()
            ax_line.plot(valid["LapNumber"], times,
                         label=drv, linewidth=2,
                         color=DRIVER_COLORS[idx % len(DRIVER_COLORS)],
                         marker="o", markersize=3, alpha=0.85)

        ax_line.set_xlabel("Lap Number", fontsize=11)
        ax_line.set_ylabel("Lap Time (s)", fontsize=11)
        ax_line.set_title("Lap Time Progression", fontsize=13, color=A1)
        ax_line.legend(loc="upper right", fontsize=9)
        ax_line.grid(True)

        # ── Bar chart: fastest laps
        bests, labels = [], []
        for drv in top_drivers:
            laps = session.laps.pick_driver(drv)
            if laps.empty: continue
            fl = laps.pick_fastest()
            if fl is None or pd.isna(fl.get("LapTime")): continue
            bests.append(fl["LapTime"].total_seconds())
            labels.append(drv)

        if bests:
            cols = [DRIVER_COLORS[top_drivers.index(l) % len(DRIVER_COLORS)]
                    for l in labels]
            bars = ax_bar.bar(labels, bests, color=cols, width=0.6, alpha=0.9,
                              edgecolor=BG, linewidth=1.5)
            ax_bar.set_title("Fastest Lap by Driver", fontsize=13, color=A1)
            ax_bar.set_ylabel("Time (s)", fontsize=11)
            ax_bar.grid(axis="y")
            for bar, t in zip(bars, bests):
                ax_bar.text(bar.get_x() + bar.get_width() / 2,
                            bar.get_height() + 0.05,
                            f"{t:.3f}", ha="center", va="bottom",
                            fontsize=8, color=WARM)

        watermark(fig)
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        path = f"modern_plots/{year}_{track}_lap_comparison.png"
        return save(fig, path)

    except Exception as e:
        print(f"  ✗  Lap comparison failed: {e}")
        return None


# ── 2. Interactive race replay (Plotly HTML) ───────────────────────────────
def create_interactive_race_replay(year, track, top_n=8):
    try:
        session = load(year, track)
        top_drivers = list(session.results["Abbreviation"].head(top_n))
        if not top_drivers:
            return None

        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=("Race Position Timeline", "Fastest Lap Comparison",
                            "Position Changes Heatmap", "Lap Count by Driver"),
            vertical_spacing=0.14, horizontal_spacing=0.12,
        )

        # Position timeline
        for idx, drv in enumerate(top_drivers[:6]):
            laps = session.laps.pick_driver(drv)
            if laps.empty: continue
            fig.add_trace(go.Scatter(
                x=laps["LapNumber"], y=laps["Position"],
                name=drv, mode="lines+markers",
                line=dict(width=2.5, color=DRIVER_COLORS[idx]),
                marker=dict(size=4),
            ), row=1, col=1)

        # Fastest lap bar
        bests, labels = [], []
        for drv in top_drivers:
            laps = session.laps.pick_driver(drv)
            if laps.empty: continue
            fl = laps.pick_fastest()
            if fl is None or pd.isna(fl.get("LapTime")): continue
            bests.append(fl["LapTime"].total_seconds())
            labels.append(drv)
        if bests:
            fig.add_trace(go.Bar(
                x=labels, y=bests,
                marker_color=DRIVER_COLORS[:len(labels)],
                name="Fastest Lap",
                text=[f"{t:.3f}s" for t in bests],
                textposition="outside",
            ), row=1, col=2)

        # Position heatmap
        pos_matrix, hm_labels = [], []
        for drv in top_drivers:
            laps = session.laps.pick_driver(drv)
            if laps.empty or len(laps) < 5: continue
            pos_matrix.append(laps["Position"].values[:30].tolist())
            hm_labels.append(drv)
        if pos_matrix:
            fig.add_trace(go.Heatmap(
                z=pos_matrix, x=list(range(1, 31)),
                y=hm_labels, colorscale="Plasma",
                reversescale=True, showscale=False,
            ), row=2, col=1)

        # Lap counts
        lap_counts = []
        lap_labels = []
        for drv in top_drivers:
            laps = session.laps.pick_driver(drv)
            if laps.empty: continue
            lap_counts.append(len(laps))
            lap_labels.append(drv)
        if lap_counts:
            fig.add_trace(go.Bar(
                x=lap_labels, y=lap_counts,
                marker_color=DRIVER_COLORS[:len(lap_labels)],
                name="Laps Completed",
            ), row=2, col=2)

        fig.update_layout(
            title=dict(
                text=f"{year} {track} Grand Prix — Interactive Analysis",
                font=dict(size=22, color=A2, family="Courier New"),
            ),
            plot_bgcolor="#0A0F1A",
            paper_bgcolor="#0F1621",
            font=dict(color=WARM),
            showlegend=True,
            height=800,
            hovermode="x unified",
        )
        fig.update_yaxes(autorange="reversed", row=1, col=1)
        fig.update_xaxes(gridcolor="#1E2D3A")
        fig.update_yaxes(gridcolor="#1E2D3A")

        path = f"interactive_plots/{year}_{track}_interactive.html"
        fig.write_html(path)
        print(f"  ✓  {path}")
        return path

    except Exception as e:
        print(f"  ✗  Interactive replay failed: {e}")
        return None


# ── 3. Podium visualization ────────────────────────────────────────────────
def create_podium_visualization(year, track):
    try:
        session = load(year, track)
        top3 = session.results.head(3)
        if len(top3) < 3:
            print(f"  ✗  Not enough finishers for podium")
            return None

        fig, ax = plt.subplots(figsize=(12, 8))

        heights = [3.0, 2.0, 1.5]   # P1, P2, P3
        x_pos   = [0,  -1.1, 1.1]
        colors  = [GOLD, SILVER, BRONZE]
        bg_cols = ["#2A2000", "#1A1A1A", "#1A1000"]

        for i in range(3):
            drv  = top3.iloc[i]
            name = str(drv.get("FullName", "?"))
            team = str(drv.get("TeamName", "?"))
            time = str(drv.get("Time", ""))
            abbr = str(drv.get("Abbreviation", "?"))

            # Podium block
            ax.add_patch(FancyBboxPatch(
                (x_pos[i] - 0.45, 0), 0.9, heights[i],
                boxstyle="round,pad=0.02",
                facecolor=bg_cols[i], edgecolor=colors[i], linewidth=2.5,
            ))
            # Position number inside block
            ax.text(x_pos[i], heights[i] * 0.5, str(i + 1),
                    ha="center", va="center",
                    fontsize=48, fontweight="bold", color=colors[i],
                    fontfamily="monospace", alpha=0.35)

            # Driver abbreviation above
            ax.text(x_pos[i], heights[i] + 0.12, abbr,
                    ha="center", va="bottom",
                    fontsize=22, fontweight="bold", color=colors[i],
                    fontfamily="monospace")
            # Full name
            display = (name[:12] + "…") if len(name) > 13 else name
            ax.text(x_pos[i], heights[i] + 0.46, display,
                    ha="center", va="bottom",
                    fontsize=11, color=WARM, fontfamily="monospace")
            # Team
            tm = (team[:14] + "…") if len(team) > 15 else team
            ax.text(x_pos[i], heights[i] + 0.70, tm,
                    ha="center", va="bottom",
                    fontsize=9, color=BORDER, fontfamily="monospace")
            # Time
            if time and time.strip() and time != "None":
                t_disp = time[:14] if len(time) > 14 else time
                ax.text(x_pos[i], -0.18, t_disp,
                        ha="center", va="top",
                        fontsize=9, color=BORDER, fontfamily="monospace")

        ax.set_xlim(-2, 2)
        ax.set_ylim(-0.45, 4.6)
        ax.axis("off")
        ax.set_facecolor(BG)

        ax.text(0, 4.4, f"{year} {track.upper()} GRAND PRIX",
                ha="center", va="top", fontsize=18, fontweight="bold",
                color=A2, fontfamily="monospace")
        ax.text(0, 4.15, "PODIUM FINISHERS",
                ha="center", va="top", fontsize=12, color=WARM,
                fontfamily="monospace")
        ax.text(0, -0.38, "F1 RACE RELAY",
                ha="center", va="top", fontsize=13, fontweight="bold",
                color=A1, fontfamily="monospace")

        plt.tight_layout()
        path = f"podium_plots/{year}_{track}_podium.png"
        return save(fig, path)

    except Exception as e:
        print(f"  ✗  Podium failed: {e}")
        return None


# ── 4. Race dashboard ──────────────────────────────────────────────────────
def create_dashboard(year, track):
    try:
        session = load(year, track)
        fig = plt.figure(figsize=(22, 12))
        fig.suptitle(f"F1 RACE RELAY  ·  {year} {track} Grand Prix",
                     fontsize=24, fontweight="bold",
                     color=A2, y=0.98, fontfamily="monospace")

        gs = fig.add_gridspec(3, 3, hspace=0.45, wspace=0.3)

        # ── Panel 1: Results table
        ax1 = fig.add_subplot(gs[0, :2])
        ax1.axis("off")
        ax1.set_facecolor(BG)
        n = min(10, len(session.results))
        tdata = []
        for i in range(n):
            row = session.results.iloc[i]
            name = str(row.get("FullName", "?"))[:20]
            team = str(row.get("TeamName", "?"))[:18]
            tdata.append([
                i + 1,
                str(row.get("Abbreviation", "?")),
                name, team,
                fmt_td(row.get("Time")),
            ])
        tbl = ax1.table(
            cellText=tdata,
            colLabels=["POS", "CODE", "DRIVER", "TEAM", "TIME"],
            cellLoc="center", loc="center",
            colColours=[PRIMARY] * 5,
        )
        tbl.auto_set_font_size(False)
        tbl.set_fontsize(9)
        tbl.scale(1, 1.8)
        for (r, c), cell in tbl.get_celld().items():
            cell.set_facecolor(BG2 if r > 0 else PRIMARY)
            cell.set_text_props(color=WARM if r > 0 else "#FFFFFF")
            cell.set_edgecolor("#2A3A4A")
            if r in (1, 2, 3) and c == 0:
                cell.set_text_props(
                    color=[GOLD, SILVER, BRONZE][r - 1], fontweight="bold")
        ax1.set_title("Race Classification", color=A1, fontsize=13,
                      pad=12, fontfamily="monospace")

        # ── Panel 2: Fastest lap bars
        ax2 = fig.add_subplot(gs[0, 2])
        ax2.set_facecolor(BG2)
        bests, labels = [], []
        for drv in list(session.results["Abbreviation"].head(8)):
            laps = session.laps.pick_driver(drv)
            if laps.empty: continue
            fl = laps.pick_fastest()
            if fl is None or pd.isna(fl.get("LapTime")): continue
            bests.append(fl["LapTime"].total_seconds())
            labels.append(drv)
        if bests:
            colors = DRIVER_COLORS[:len(labels)]
            ax2.barh(labels, bests, color=colors, alpha=0.9, edgecolor=BG)
            ax2.set_title("Fastest Laps", color=A1, fontsize=12,
                          fontfamily="monospace")
            ax2.set_xlabel("Time (s)", fontsize=9)
            ax2.grid(axis="x")
            for i, (bar, t) in enumerate(
                    zip(ax2.patches, bests)):
                ax2.text(t + 0.05, bar.get_y() + bar.get_height() / 2,
                         f"{t:.3f}", va="center", fontsize=8, color=WARM)

        # ── Panel 3: Position heatmap
        ax3 = fig.add_subplot(gs[1, :])
        ax3.set_facecolor(BG2)
        pdata, pdrvs = [], []
        for drv in list(session.results["Abbreviation"].head(10)):
            laps = session.laps.pick_driver(drv)
            if laps.empty or len(laps) < 5: continue
            pdata.append(laps["Position"].values[:40].tolist())
            pdrvs.append(drv)
        if pdata:
            im = ax3.imshow(pdata, cmap="plasma_r", aspect="auto",
                            interpolation="nearest")
            ax3.set_title("Position Changes — First 40 Laps",
                          color=A1, fontsize=12, fontfamily="monospace")
            ax3.set_xlabel("Lap", fontsize=9)
            ax3.set_yticks(range(len(pdrvs)))
            ax3.set_yticklabels(pdrvs, fontsize=9)
            plt.colorbar(im, ax=ax3, fraction=0.015, pad=0.01)
        else:
            ax3.text(0.5, 0.5, "No position data", ha="center",
                     va="center", color=WARM, fontsize=12,
                     transform=ax3.transAxes)

        # ── Panel 4: Stats text
        ax4 = fig.add_subplot(gs[2, :])
        ax4.axis("off")
        ax4.set_facecolor(BG)
        winner = session.results.iloc[0]
        lines = [
            f"Event       :  {session.event.get('EventName', track)}",
            f"Circuit     :  {session.event.get('Location', track)}",
            f"Date        :  {str(session.event.get('EventDate', year))[:10]}",
            f"Winner      :  {winner.get('FullName', '?')}  ({winner.get('TeamName', '?')})",
            f"Total Laps  :  {getattr(session, 'total_laps', '—')}",
            f"Finishers   :  {len(session.results)}",
        ]
        try:
            fl = session.laps.pick_fastest()
            lines.append(
                f"Fastest Lap :  {fmt_td(fl.get('LapTime'))}  ({fl.get('Driver', '?')})")
        except Exception:
            pass

        for i, line in enumerate(lines):
            ax4.text(0.02, 0.9 - i * 0.14, line,
                     transform=ax4.transAxes,
                     fontsize=11, color=WARM,
                     fontfamily="monospace", va="top")

        path = f"dashboards/{year}_{track}_dashboard.png"
        return save(fig, path)

    except Exception as e:
        print(f"  ✗  Dashboard failed: {e}")
        return None


# ── Public entry point ─────────────────────────────────────────────────────
def generate_all_visuals(year, track):
    print(f"\n{'='*56}")
    print(f"  GENERATING VISUALS  ·  {year} {track}")
    print(f"{'='*56}")

    # Verify session exists first (light load)
    try:
        s = fastf1.get_session(int(year), track, "R")
        s.load(telemetry=False, weather=False)
    except Exception as e:
        print(f"  ✗  Cannot load session: {e}")
        print(f"     Try:  2023 Monaco  /  2023 Bahrain  /  2022 Silverstone")
        return

    files = []
    print("\n  [1/4] Lap comparison…")
    f = create_modern_lap_comparison(int(year), track)
    if f: files.append(f)

    print("  [2/4] Interactive replay…")
    f = create_interactive_race_replay(int(year), track)
    if f: files.append(f)

    print("  [3/4] Podium…")
    f = create_podium_visualization(int(year), track)
    if f: files.append(f)

    print("  [4/4] Dashboard…")
    f = create_dashboard(int(year), track)
    if f: files.append(f)

    print(f"\n{'='*56}")
    print(f"  {len(files)}/4 visuals saved")
    print(f"{'='*56}\n")
    return files


def generate_visuals_for_gui(year, track):
    """Thin wrapper called by modern_gui.py and api.py."""
    try:
        generate_all_visuals(int(year), track)
        return True
    except Exception as e:
        print(f"  ✗  generate_visuals_for_gui error: {e}")
        return False


# ── Standalone usage ────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("F1 Race Relay — Visualization Generator")
    print("=" * 44)
    print("  1.  2023 Monaco (recommended)")
    print("  2.  2023 Bahrain")
    print("  3.  Custom year & track")
    choice = input("Choice: ").strip()
    if choice == "1":
        generate_all_visuals(2023, "Monaco")
    elif choice == "2":
        generate_all_visuals(2023, "Bahrain")
    else:
        y = input("Year:  ").strip()
        t = input("Track: ").strip()
        generate_all_visuals(int(y), t)
