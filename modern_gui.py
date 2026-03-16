import sys
import os
from datetime import datetime
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QComboBox, QFrame, QTabWidget, QGridLayout,
    QProgressBar, QLineEdit, QFileDialog, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QScrollArea, QSizePolicy, QSpacerItem,
    QGraphicsDropShadowEffect
)
from PySide6.QtCore import (
    Qt, QTimer, QPropertyAnimation, QEasingCurve, QThread, Signal, QSize,
    QRect, QPoint
)
from PySide6.QtGui import (
    QFont, QColor, QPainter, QPainterPath, QLinearGradient, QBrush, QPen,
    QPixmap, QFontDatabase, QIcon, QPolygon, QPalette
)
import fastf1
import pandas as pd

# ─────────────────────────────────────────────────────────────────────────────
#  Design Tokens
# ─────────────────────────────────────────────────────────────────────────────
PRIMARY    = "#355872"
ACCENT1    = "#7AAACE"
ACCENT2    = "#9CD5FF"
BG         = "#F7F8F0"
SECONDARY  = "#81A6C6"
MUTED      = "#AACDDC"
WARM       = "#F3E3D0"
BORDER     = "#D2C4B4"
TEXT_DARK  = "#1E2D3A"
TEXT_MID   = "#4A6278"
TEXT_LIGHT = "#7A95A8"
WHITE      = "#FFFFFF"

GOLD   = "#D4A843"
SILVER = "#9BA8B0"
BRONZE = "#B07D52"

# ─────────────────────────────────────────────────────────────────────────────
#  Worker Thread
# ─────────────────────────────────────────────────────────────────────────────
class DataWorker(QThread):
    progress = Signal(int, str)
    result   = Signal(object)
    error    = Signal(str)

    def __init__(self, year, track, mode="race", driver1=None, driver2=None):
        super().__init__()
        self.year = year; self.track = track; self.mode = mode
        self.driver1 = driver1; self.driver2 = driver2

    def run(self):
        try:
            self.progress.emit(15, f"Connecting to FastF1…")
            session = fastf1.get_session(int(self.year), self.track, 'R')

            self.progress.emit(40, "Downloading race data…")
            full_tele = (self.mode == "compare")
            session.load(telemetry=full_tele, weather=False)

            self.progress.emit(80, "Processing results…")
            self.result.emit(session)
            self.progress.emit(100, "Done")
        except Exception as e:
            self.error.emit(str(e))
class VizWorker(QThread):
    progress = Signal(int, str)
    result   = Signal(object)
    error    = Signal(str)

    def __init__(self, year, track):
        super().__init__()
        self.year  = year
        self.track = track

    def run(self):
        try:
            self.progress.emit(30, "Loading session data…")
            import modern_plots
            self.progress.emit(60, "Generating visualizations…")
            files = modern_plots.generate_all_visuals(self.year, self.track)
            self.progress.emit(100, "Done")
            self.result.emit(files or [])
        except Exception as e:
            self.error.emit(str(e))
# ─────────────────────────────────────────────────────────────────────────────
#  Custom Widgets
# ─────────────────────────────────────────────────────────────────────────────
class StatusBadge(QWidget):
    """Animated status indicator."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(10, 10)
        self._color = QColor(BORDER)
        self._pulse = 0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)

    def _tick(self):
        self._pulse = (self._pulse + 8) % 360
        self.update()

    def set_state(self, state):
        colors = {"idle": BORDER, "loading": ACCENT2, "ok": "#4CAF82", "error": "#E05252"}
        self._color = QColor(colors.get(state, BORDER))
        if state == "loading":
            self._timer.start(30)
        else:
            self._timer.stop()
            self._pulse = 0
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        if self._pulse:
            glow = QColor(self._color)
            glow.setAlpha(40)
            p.setBrush(QBrush(glow))
            p.setPen(Qt.NoPen)
            p.drawEllipse(0, 0, 10, 10)
        p.setBrush(QBrush(self._color))
        p.setPen(Qt.NoPen)
        p.drawEllipse(2, 2, 6, 6)


class SlimProgress(QProgressBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(3)
        self.setTextVisible(False)
        self.setStyleSheet(f"""
            QProgressBar {{
                background: {BORDER};
                border: none;
                border-radius: 1px;
            }}
            QProgressBar::chunk {{
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 {ACCENT1}, stop:1 {ACCENT2}
                );
                border-radius: 1px;
            }}
        """)
        self._anim = QPropertyAnimation(self, b"value")
        self._anim.setDuration(350)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)

    def animate_to(self, value):
        self._anim.stop()
        self._anim.setStartValue(self.value())
        self._anim.setEndValue(value)
        self._anim.start()


class Card(QFrame):
    """Elevated card with optional accent bar."""
    def __init__(self, accent_color=None, parent=None):
        super().__init__(parent)
        self._accent = accent_color
        self.setStyleSheet(f"""
            Card {{
                background-color: {WHITE};
                border: 1px solid {BORDER};
                border-radius: 12px;
            }}
        """)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(16)
        shadow.setOffset(0, 2)
        shadow.setColor(QColor(0, 0, 0, 18))
        self.setGraphicsEffect(shadow)

    def paintEvent(self, event):
        super().paintEvent(event)
        if self._accent:
            p = QPainter(self)
            p.setRenderHint(QPainter.Antialiasing)
            p.setBrush(QBrush(QColor(self._accent)))
            p.setPen(Qt.NoPen)
            path = QPainterPath()
            path.moveTo(12, 0)
            path.lineTo(80, 0)
            path.lineTo(80, 4)
            path.lineTo(12, 4)
            path.quadTo(0, 4, 0, 12)
            path.lineTo(0, 4)
            path.quadTo(0, 0, 12, 0)
            p.drawPath(path)


class TagButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCheckable(True)
        self.setCursor(Qt.PointingHandCursor)
        self._refresh_style()
        self.toggled.connect(lambda: self._refresh_style())

    def _refresh_style(self):
        if self.isChecked():
            self.setStyleSheet(f"""
                QPushButton {{
                    background: {PRIMARY};
                    color: {WHITE};
                    border: none;
                    border-radius: 16px;
                    padding: 6px 18px;
                    font-size: 11px;
                    font-weight: 600;
                    letter-spacing: 0.5px;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    background: {WARM};
                    color: {TEXT_MID};
                    border: 1px solid {BORDER};
                    border-radius: 16px;
                    padding: 6px 18px;
                    font-size: 11px;
                }}
                QPushButton:hover {{
                    background: {MUTED};
                    color: {PRIMARY};
                    border-color: {ACCENT1};
                }}
            """)


class StatItem(QWidget):
    def __init__(self, label, value="—", parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 10, 0, 10)

        self._label_w = QLabel(label.upper())
        self._label_w.setStyleSheet(f"color:{TEXT_LIGHT}; font-size:10px; letter-spacing:1px;")

        self._value_w = QLabel(value)
        self._value_w.setStyleSheet(f"""
            color:{TEXT_DARK}; font-family:'JetBrains Mono','Courier New',monospace;
            font-size:12px; font-weight:600;
        """)
        self._value_w.setAlignment(Qt.AlignRight)

        layout.addWidget(self._label_w)
        layout.addStretch()
        layout.addWidget(self._value_w)

        separator = QFrame(self)
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet(f"color:{BORDER};")

    def set_value(self, v):
        self._value_w.setText(str(v))


def make_button(text, primary=True, small=False):
    btn = QPushButton(text)
    btn.setCursor(Qt.PointingHandCursor)
    h = "34px" if small else "40px"
    px = "16px" if small else "22px"
    fs = "11px" if small else "12px"
    if primary:
        btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                    stop:0 {ACCENT1}, stop:1 {PRIMARY});
                color: {WHITE};
                border: none;
                border-radius: 8px;
                height: {h};
                padding: 0 {px};
                font-size: {fs};
                font-weight: 600;
                letter-spacing: 0.8px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                    stop:0 {ACCENT2}, stop:1 {ACCENT1});
            }}
            QPushButton:disabled {{
                background: {MUTED};
                color: {TEXT_LIGHT};
            }}
            QPushButton:pressed {{
                background: {PRIMARY};
            }}
        """)
    else:
        btn.setStyleSheet(f"""
            QPushButton {{
                background: {WARM};
                color: {PRIMARY};
                border: 1px solid {BORDER};
                border-radius: 8px;
                height: {h};
                padding: 0 {px};
                font-size: {fs};
                font-weight: 500;
            }}
            QPushButton:hover {{
                background: {MUTED};
                border-color: {ACCENT1};
            }}
        """)
    return btn


def make_combo(items, width=None):
    cb = QComboBox()
    cb.addItems(items)
    if width:
        cb.setFixedWidth(width)
    cb.setStyleSheet(f"""
        QComboBox {{
            background: {BG};
            border: 1.5px solid {BORDER};
            border-radius: 8px;
            padding: 8px 12px;
            color: {TEXT_DARK};
            font-size: 12px;
            min-height: 36px;
        }}
        QComboBox:hover {{ border-color: {ACCENT1}; }}
        QComboBox:focus {{ border-color: {PRIMARY}; }}
        QComboBox::drop-down {{
            border: none; width: 24px;
        }}
        QComboBox::down-arrow {{
            border-left: 4px solid transparent;
            border-right: 4px solid transparent;
            border-top: 5px solid {PRIMARY};
            width: 0; height: 0;
        }}
        QComboBox QAbstractItemView {{
            background: {WHITE};
            border: 1px solid {BORDER};
            selection-background-color: {MUTED};
            selection-color: {PRIMARY};
            outline: none;
        }}
    """)
    return cb


def section_label(text):
    lbl = QLabel(text.upper())
    lbl.setStyleSheet(f"""
        color: {PRIMARY};
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 2px;
    """)
    return lbl


def mini_label(text):
    lbl = QLabel(text)
    lbl.setStyleSheet(f"color:{TEXT_LIGHT}; font-size:10px; letter-spacing:1px;")
    return lbl

# ─────────────────────────────────────────────────────────────────────────────
#  Main Window
# ─────────────────────────────────────────────────────────────────────────────
class F1App(QMainWindow):
    YEARS  = ["2024", "2023", "2022", "2021"]
    TRACKS = ["Bahrain", "Monaco", "Silverstone", "Spa", "Monza",
              "Hungaroring", "Suzuka", "Imola", "Zandvoort", "Singapore"]
    DRIVERS = ["VER", "HAM", "LEC", "NOR", "SAI", "RUS",
               "PER", "ALO", "STR", "GAS"]

    def __init__(self):
        super().__init__()
        self.setWindowTitle("F1 Race Relay")
        self.setMinimumSize(1280, 820)
        self._session = None
        self._worker  = None
        self._setup_ui()

    # ── Top-level layout ────────────────────────────────────────────────────
    def _setup_ui(self):
        self.setStyleSheet(f"QMainWindow {{ background: {BG}; }}")

        root = QWidget()
        self.setCentralWidget(root)
        vbox = QVBoxLayout(root)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)

        vbox.addWidget(self._build_topbar())
        vbox.addWidget(self._build_tabs())
        vbox.addWidget(self._build_statusbar())

        self.progress = SlimProgress()
        self.progress.setVisible(False)
        vbox.addWidget(self.progress)

    # ── Top bar ─────────────────────────────────────────────────────────────
    def _build_topbar(self):
        bar = QFrame()
        bar.setFixedHeight(60)
        bar.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 {PRIMARY}, stop:1 #2A4A62);
                border-bottom: 1px solid #1E3347;
            }}
        """)
        h = QHBoxLayout(bar)
        h.setContentsMargins(28, 0, 28, 0)

        # Wordmark
        mark = QLabel("F1  RACE  RELAY")
        mark.setStyleSheet(f"""
            color: {WHITE};
            font-size: 15px;
            font-weight: 700;
            letter-spacing: 5px;
            font-family: 'DM Mono', 'JetBrains Mono', 'Courier New', monospace;
        """)

        # Nav pills
        nav = QHBoxLayout()
        nav.setSpacing(4)
        for name in ["Overview", "Analysis", "Compare", "Export"]:
            pill = QPushButton(name)
            pill.setCursor(Qt.PointingHandCursor)
            pill.setStyleSheet(f"""
                QPushButton {{
                    color: rgba(255,255,255,0.6);
                    background: transparent;
                    border: none;
                    padding: 6px 14px;
                    font-size: 12px;
                    border-radius: 6px;
                }}
                QPushButton:hover {{
                    color: {WHITE};
                    background: rgba(255,255,255,0.12);
                }}
            """)
            nav.addWidget(pill)

        # Status cluster
        status_box = QWidget()
        sh = QHBoxLayout(status_box)
        sh.setContentsMargins(0, 0, 0, 0)
        sh.setSpacing(6)
        self._badge = StatusBadge()
        self._badge.set_state("idle")
        self._conn_label = QLabel("Idle")
        self._conn_label.setStyleSheet(f"color:rgba(255,255,255,0.65); font-size:11px;")
        sh.addWidget(self._badge)
        sh.addWidget(self._conn_label)

        h.addWidget(mark)
        h.addSpacing(24)
        h.addLayout(nav)
        h.addStretch()
        h.addWidget(status_box)
        return bar

    # ── Tab widget ───────────────────────────────────────────────────────────
    def _build_tabs(self):
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: none;
                background: {BG};
                padding: 28px 32px;
            }}
            QTabBar::tab {{
                background: transparent;
                color: {TEXT_LIGHT};
                padding: 14px 26px;
                font-size: 11px;
                letter-spacing: 1.5px;
                font-weight: 500;
                border: none;
                text-transform: uppercase;
            }}
            QTabBar::tab:hover {{ color: {ACCENT1}; }}
            QTabBar::tab:selected {{
                color: {PRIMARY};
                font-weight: 700;
                border-bottom: 2.5px solid {PRIMARY};
            }}
            QTabWidget::tab-bar {{
                background: {WHITE};
                border-bottom: 1px solid {BORDER};
            }}
        """)
        self.tabs.addTab(self._tab_results(),    "Race Results")
        self.tabs.addTab(self._tab_compare(),    "Driver Compare")
        self.tabs.addTab(self._tab_visuals(),    "Visualizations")
        self.tabs.addTab(self._tab_settings(),   "Settings")
        return self.tabs

    # ── Tab 1 – Race Results ────────────────────────────────────────────────
    def _tab_results(self):
        w = QWidget()
        v = QVBoxLayout(w)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(20)

        # ── Selector card
        sel_card = Card(accent_color=ACCENT2)
        sel_card.setFixedHeight(88)
        sh = QHBoxLayout(sel_card)
        sh.setContentsMargins(20, 16, 20, 16)
        sh.setSpacing(12)

        sh.addWidget(section_label("Load Race"))
        sh.addSpacing(8)

        self.r_year  = make_combo(self.YEARS, 110)
        self.r_track = make_combo(self.TRACKS, 200)
        self.r_load  = make_button("Load Race")
        self.r_load.clicked.connect(self._do_load_race)

        sh.addWidget(self.r_year)
        sh.addWidget(self.r_track)
        sh.addWidget(self.r_load)
        sh.addStretch()

        v.addWidget(sel_card)

        # ── KPI strip
        kpi_row = QHBoxLayout()
        kpi_row.setSpacing(14)

        self.kpi_winner = self._kpi_card("Winner", "—", PRIMARY)
        self.kpi_fast   = self._kpi_card("Fastest Lap", "—", ACCENT1)
        self.kpi_laps   = self._kpi_card("Total Laps", "—", SECONDARY)
        self.kpi_dnf    = self._kpi_card("DNFs", "—", "#C97E5A")

        for k in [self.kpi_winner, self.kpi_fast, self.kpi_laps, self.kpi_dnf]:
            kpi_row.addWidget(k)

        v.addLayout(kpi_row)

        # ── Results table
        tbl_label = section_label("Classification")
        v.addWidget(tbl_label)

        self.results_table = QTableWidget()
        self.results_table.setColumnCount(6)
        self.results_table.setHorizontalHeaderLabels(
            ["POS", "DRIVER", "TEAM", "TIME", "GAP", "FASTEST LAP"])
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.results_table.setAlternatingRowColors(True)
        self.results_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.results_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.results_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.results_table.verticalHeader().setVisible(False)
        self.results_table.setShowGrid(False)
        self.results_table.setStyleSheet(f"""
            QTableWidget {{
                background: {WHITE};
                alternate-background-color: {BG};
                border: 1px solid {BORDER};
                border-radius: 10px;
                gridline-color: transparent;
                font-size: 12px;
                color: {TEXT_DARK};
                outline: none;
            }}
            QTableWidget::item {{
                padding: 12px 16px;
                border-bottom: 1px solid {BORDER};
            }}
            QTableWidget::item:selected {{
                background: {MUTED};
                color: {PRIMARY};
            }}
            QHeaderView::section {{
                background: {WARM};
                color: {TEXT_MID};
                padding: 10px 16px;
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 1.5px;
                border: none;
                border-bottom: 1.5px solid {BORDER};
            }}
        """)
        v.addWidget(self.results_table)
        return w

    def _kpi_card(self, title, value, color):
        card = Card()
        h = QHBoxLayout(card)
        h.setContentsMargins(18, 14, 18, 14)

        accent = QFrame()
        accent.setFixedWidth(3)
        accent.setStyleSheet(f"background:{color}; border-radius:2px;")

        meta = QVBoxLayout()
        meta.setSpacing(4)
        t = QLabel(title.upper())
        t.setStyleSheet(f"color:{TEXT_LIGHT}; font-size:9px; letter-spacing:1.5px; font-weight:600;")
        v_lbl = QLabel(value)
        v_lbl.setStyleSheet(f"""
            color:{color}; font-size:16px; font-weight:700;
            font-family:'JetBrains Mono','Courier New',monospace;
        """)
        meta.addWidget(t)
        meta.addWidget(v_lbl)

        h.addWidget(accent)
        h.addSpacing(10)
        h.addLayout(meta)
        h.addStretch()

        card._value_lbl = v_lbl
        return card

    # ── Tab 2 – Driver Compare ───────────────────────────────────────────────
    def _tab_compare(self):
        w = QWidget()
        v = QVBoxLayout(w)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(20)

        # Controls
        ctrl = Card()
        ctrl.setFixedHeight(88)
        ch = QHBoxLayout(ctrl)
        ch.setContentsMargins(20, 16, 20, 16)
        ch.setSpacing(12)

        ch.addWidget(section_label("Compare"))
        ch.addSpacing(8)

        self.c_d1    = make_combo(self.DRIVERS, 100)
        self.c_d2    = make_combo(self.DRIVERS, 100)
        self.c_d2.setCurrentIndex(1)
        self.c_year  = make_combo(self.YEARS, 110)
        self.c_track = make_combo(self.TRACKS, 200)
        self.c_btn   = make_button("Compare")
        self.c_btn.clicked.connect(self._do_compare)

        ch.addWidget(mini_label("Driver A"))
        ch.addWidget(self.c_d1)
        ch.addWidget(mini_label("vs"))
        ch.addWidget(self.c_d2)
        ch.addSpacing(8)
        ch.addWidget(self.c_year)
        ch.addWidget(self.c_track)
        ch.addWidget(self.c_btn)
        ch.addStretch()

        v.addWidget(ctrl)

        # Delta banner
        self.delta_banner = QFrame()
        self.delta_banner.setFixedHeight(52)
        self.delta_banner.setStyleSheet(f"""
            background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                stop:0 {WARM}, stop:1 {BG});
            border: 1px solid {BORDER};
            border-radius: 10px;
        """)
        dh = QHBoxLayout(self.delta_banner)
        self.delta_text = QLabel("Select two drivers and click Compare")
        self.delta_text.setAlignment(Qt.AlignCenter)
        self.delta_text.setStyleSheet(f"""
            color:{TEXT_MID}; font-size:13px; font-weight:500;
            font-family:'JetBrains Mono','Courier New',monospace;
        """)
        dh.addWidget(self.delta_text)
        v.addWidget(self.delta_banner)

        # Driver cards
        cards_row = QHBoxLayout()
        cards_row.setSpacing(16)
        self.card_d1 = self._driver_card_widget()
        self.card_d2 = self._driver_card_widget()
        cards_row.addWidget(self.card_d1)
        cards_row.addWidget(self.card_d2)
        v.addLayout(cards_row)
        return w

    def _driver_card_widget(self):
        card = Card(accent_color=ACCENT1)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(0)

        top = QHBoxLayout()
        top.setSpacing(12)
        code_lbl = QLabel("—")
        code_lbl.setStyleSheet(f"""
            color:{PRIMARY}; font-size:36px; font-weight:800;
            font-family:'JetBrains Mono','Courier New',monospace;
            letter-spacing:2px;
        """)
        team_lbl = QLabel("—")
        team_lbl.setStyleSheet(f"color:{TEXT_LIGHT}; font-size:11px; margin-top:8px;")
        top.addWidget(code_lbl)
        top.addWidget(team_lbl, alignment=Qt.AlignBottom)
        top.addStretch()
        layout.addLayout(top)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setFixedHeight(1)
        sep.setStyleSheet(f"background:{BORDER}; margin: 12px 0;")
        layout.addWidget(sep)

        stat_keys = ["Fastest Lap", "Average Lap", "Total Laps", "Finishing Position"]
        card.stat_items = {}
        for key in stat_keys:
            si = StatItem(key)
            sep2 = QFrame()
            sep2.setFrameShape(QFrame.HLine)
            sep2.setStyleSheet(f"color:{BORDER};")
            card.stat_items[key] = si
            layout.addWidget(si)
            layout.addWidget(sep2)

        card.code_lbl = code_lbl
        card.team_lbl = team_lbl
        return card

    # ── Tab 3 – Visualizations ──────────────────────────────────────────────
    def _tab_visuals(self):
        w = QWidget()
        v = QVBoxLayout(w)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(20)

        ctrl = Card()
        ctrl.setFixedHeight(88)
        ch = QHBoxLayout(ctrl)
        ch.setContentsMargins(20, 16, 20, 16)
        ch.setSpacing(12)

        self.v_year  = make_combo(self.YEARS, 110)
        self.v_track = make_combo(self.TRACKS, 200)
        self.v_gen   = make_button("Generate All")
        self.v_gen.clicked.connect(self._do_generate)

        ch.addWidget(self.v_year)
        ch.addWidget(self.v_track)
        ch.addSpacing(8)
        ch.addWidget(self.v_gen)
        ch.addStretch()

        v.addWidget(ctrl)

        # Type selector
        pills_row = QHBoxLayout()
        pills_row.setSpacing(8)
        self.viz_pills = []
        for name in ["Lap Chart", "Podium", "Dashboard", "Interactive"]:
            pill = TagButton(name)
            pill.toggled.connect(self._pill_mutex)
            pills_row.addWidget(pill)
            self.viz_pills.append(pill)
        self.viz_pills[0].setChecked(True)
        pills_row.addStretch()
        v.addLayout(pills_row)

        # Output canvas
        canvas = Card()
        canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        canvas_layout = QVBoxLayout(canvas)

        self.viz_status = QLabel("Select a race and click Generate All")
        self.viz_status.setAlignment(Qt.AlignCenter)
        self.viz_status.setStyleSheet(f"color:{TEXT_LIGHT}; font-size:13px;")
        canvas_layout.addWidget(self.viz_status)

        # Output file links grid
        self.viz_grid = QWidget()
        grid = QGridLayout(self.viz_grid)
        grid.setSpacing(12)
        self.viz_grid.setVisible(False)
        canvas_layout.addWidget(self.viz_grid)

        v.addWidget(canvas)
        return w

    # ── Tab 4 – Settings ────────────────────────────────────────────────────
    def _tab_settings(self):
        w = QWidget()
        scroll = QScrollArea()
        scroll.setWidget(w)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        v = QVBoxLayout(w)
        v.setContentsMargins(0, 0, 0, 32)
        v.setSpacing(28)

        # Data section
        v.addWidget(section_label("Data"))
        v.addWidget(self._setting_row(
            "Cache Folder",
            "FastF1 local data cache location",
            self._cache_input_widget()
        ))
        v.addWidget(self._setting_row(
            "Default Year",
            "Pre-selected year on launch",
            make_combo(self.YEARS, 200)
        ))
        v.addWidget(self._setting_row(
            "Default Track",
            "Pre-selected circuit on launch",
            make_combo(self.TRACKS, 200)
        ))

        v.addWidget(section_label("Appearance"))
        v.addWidget(self._setting_row(
            "Theme",
            "Interface colour scheme",
            QLabel("Light  (default)  ·  More themes coming soon")
        ))
        v.addStretch()

        wrapper = QWidget()
        wl = QVBoxLayout(wrapper)
        wl.addWidget(scroll)
        return wrapper

    def _cache_input_widget(self):
        box = QWidget()
        h = QHBoxLayout(box)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(8)
        self.cache_path = QLineEdit(os.path.expanduser("~/.fastf1"))
        self.cache_path.setReadOnly(True)
        self.cache_path.setStyleSheet(f"""
            QLineEdit {{
                background: {BG};
                border: 1.5px solid {BORDER};
                border-radius: 8px;
                padding: 8px 12px;
                color: {TEXT_DARK};
                font-size: 12px;
                font-family: monospace;
            }}
        """)
        browse = make_button("Browse", primary=False, small=True)
        browse.clicked.connect(self._browse_cache)
        h.addWidget(self.cache_path)
        h.addWidget(browse)
        return box

    def _setting_row(self, title, subtitle, widget):
        card = Card()
        h = QHBoxLayout(card)
        h.setContentsMargins(20, 14, 20, 14)

        meta = QVBoxLayout()
        meta.setSpacing(2)
        t = QLabel(title)
        t.setStyleSheet(f"color:{TEXT_DARK}; font-size:13px; font-weight:600;")
        s = QLabel(subtitle)
        s.setStyleSheet(f"color:{TEXT_LIGHT}; font-size:11px;")
        meta.addWidget(t)
        meta.addWidget(s)

        h.addLayout(meta)
        h.addStretch()
        h.addWidget(widget)
        return card

    # ── Status bar ───────────────────────────────────────────────────────────
    def _build_statusbar(self):
        bar = QFrame()
        bar.setFixedHeight(30)
        bar.setStyleSheet(f"background:{WARM}; border-top:1px solid {BORDER};")
        h = QHBoxLayout(bar)
        h.setContentsMargins(16, 0, 16, 0)

        self.status_msg = QLabel("Ready")
        self.status_msg.setStyleSheet(f"color:{TEXT_MID}; font-size:11px;")

        self.ts_label = QLabel()
        self.ts_label.setStyleSheet(f"color:{TEXT_LIGHT}; font-size:10px; font-family:monospace;")
        self._tick_ts()
        self._ts_timer = QTimer()
        self._ts_timer.timeout.connect(self._tick_ts)
        self._ts_timer.start(30000)

        h.addWidget(self.status_msg)
        h.addStretch()
        h.addWidget(self.ts_label)
        return bar

    def _tick_ts(self):
        self.ts_label.setText(datetime.now().strftime("%H:%M  ·  %d %b %Y"))

    # ── Actions ──────────────────────────────────────────────────────────────
    def _pill_mutex(self, checked):
        if not checked:
            return
        sender = self.sender()
        for p in self.viz_pills:
            if p is not sender:
                p.setChecked(False)

    def _browse_cache(self):
        d = QFileDialog.getExistingDirectory(self, "Select Cache Folder")
        if d:
            self.cache_path.setText(d)

    def _set_loading(self, loading, btn=None):
        if btn:
            btn.setEnabled(not loading)
            btn.setText("Loading…" if loading else btn._orig_text)
        self.progress.setVisible(loading)
        self._badge.set_state("loading" if loading else "idle")
        self._conn_label.setText("Loading data…" if loading else "Idle")

    def _do_load_race(self):
        year  = self.r_year.currentText()
        track = self.r_track.currentText()
        self.r_load._orig_text = "Load Race"
        self._set_loading(True, self.r_load)
        self.status_msg.setText(f"Loading {year} {track}…")
        self.progress.animate_to(10)

        self._worker = DataWorker(year, track, mode="race")
        self._worker.progress.connect(self._on_progress)
        self._worker.result.connect(self._on_race_loaded)
        self._worker.error.connect(self._on_error)
        self._worker.start()

    def _do_compare(self):
        d1    = self.c_d1.currentText()
        d2    = self.c_d2.currentText()
        year  = self.c_year.currentText()
        track = self.c_track.currentText()

        if d1 == d2:
            self.status_msg.setText("Choose two different drivers")
            return

        self.c_btn._orig_text = "Compare"
        self._set_loading(True, self.c_btn)
        self.status_msg.setText(f"Comparing {d1} vs {d2} – {year} {track}…")

        self._worker = DataWorker(year, track, mode="compare", driver1=d1, driver2=d2)
        self._worker.progress.connect(self._on_progress)
        self._worker.result.connect(lambda s: self._on_compare_loaded(s, d1, d2))
        self._worker.error.connect(self._on_error)
        self._worker.start()

    def _on_viz_error(self, msg):
        self.viz_status.setText(f"Error: {msg}")
        self.viz_status.setVisible(True)
        self.viz_grid.setVisible(False)
        self.v_gen.setEnabled(True)
        self.v_gen.setText("Generate All")
        self._badge.set_state("error")
        self.progress.setVisible(False)
        self.status_msg.setText(f"Error: {msg[:80]}")
    def _open_file(self, path):
        import subprocess, sys
        if sys.platform == "win32":
            os.startfile(path)
        elif sys.platform == "darwin":
            subprocess.run(["open", path])
        else:
            subprocess.run(["xdg-open", path])
    def _do_generate(self):
        year  = self.v_year.currentText()
        track = self.v_track.currentText()
        active = next((p.text() for p in self.viz_pills if p.isChecked()), "Lap Chart")

        self.viz_status.setText(f"Generating {active} for {year} {track}…")
        self.viz_status.setVisible(True)
        self.viz_grid.setVisible(False)
        self.v_gen.setEnabled(False)
        self.v_gen.setText("Generating…")
        self.progress.setVisible(True)
        self.progress.animate_to(20)
        self.status_msg.setText(f"Generating {active}…")
        self._badge.set_state("loading")

        self._viz_worker = VizWorker(int(year), track)
        self._viz_worker.progress.connect(self._on_progress)
        self._viz_worker.result.connect(
            lambda files: self._finish_generate(year, track, files))
        self._viz_worker.error.connect(self._on_viz_error)
        self._viz_worker.start()

    def _finish_generate(self, year, track, files):
        self.viz_status.setVisible(False)
        self.viz_grid.setVisible(True)
        self.v_gen.setEnabled(True)
        self.v_gen.setText("Generate All")
        self._badge.set_state("ok")
        self.progress.animate_to(100)
        QTimer.singleShot(1500, lambda: self.progress.setVisible(False))

        grid = self.viz_grid.layout()
        while grid.count():
            item = grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not files:
            self.viz_status.setText("No files generated. Check the track name.")
            self.viz_status.setVisible(True)
            self.status_msg.setText("Visualization failed")
            return

        labels = {
            "lap_comparison": "Lap Comparison",
            "interactive":    "Interactive Replay",
            "podium":         "Podium",
            "dashboard":      "Dashboard",
        }

        for i, path in enumerate(files):
            key = next((k for k in labels if k in path), "Output")
            label = labels.get(key, "Output")

            tile = Card()
            tl = QVBoxLayout(tile)
            tl.setContentsMargins(14, 12, 14, 12)
            tl.setSpacing(6)

            lbl = QLabel(label)
            lbl.setStyleSheet(
                f"color:{PRIMARY}; font-weight:600; font-size:12px;")

            p = QLabel(path)
            p.setStyleSheet(
                f"color:{TEXT_LIGHT}; font-size:10px; font-family:monospace;")
            p.setWordWrap(True)

            open_btn = make_button("Open", primary=False, small=True)
            open_btn.clicked.connect(lambda _, fp=path: self._open_file(fp))

            tl.addWidget(lbl)
            tl.addWidget(p)
            tl.addWidget(open_btn)
            grid.addWidget(tile, i // 2, i % 2)

        self.status_msg.setText(
            f"{len(files)} files generated — {year} {track}")


    # ── Slots ─────────────────────────────────────────────────────────────────
    def _on_progress(self, value, msg):
        self.progress.animate_to(value)
        self.status_msg.setText(msg)

    def _on_race_loaded(self, session):
        self._session = session
        self._set_loading(False, self.r_load)
        self.r_load.setText("Load Race")
        self._badge.set_state("ok")
        self._conn_label.setText("Connected")
        self._populate_results(session)
        self.status_msg.setText(
            f"Loaded: {session.event.get('EventName', 'Race')} {session.event['EventDate'].year}")
        QTimer.singleShot(2000, lambda: self.progress.setVisible(False))

    def _on_compare_loaded(self, session, d1, d2):
        self._set_loading(False, self.c_btn)
        self.c_btn.setText("Compare")
        self._badge.set_state("ok")
        self._conn_label.setText("Connected")
        self._populate_compare(session, d1, d2)
        QTimer.singleShot(2000, lambda: self.progress.setVisible(False))

    def _on_error(self, msg):
        self._set_loading(False)
        for btn in [self.r_load, self.c_btn]:
            btn.setEnabled(True)
        self.r_load.setText("Load Race")
        self.c_btn.setText("Compare")
        self._badge.set_state("error")
        self._conn_label.setText("Error")
        self.status_msg.setText(f"Error: {msg[:80]}")
        self.progress.setVisible(False)

    # ── Table population ─────────────────────────────────────────────────────
    def _populate_results(self, session):
        res = session.results
        self.results_table.setRowCount(len(res))

        # KPIs
        winner = res.iloc[0]
        self.kpi_winner._value_lbl.setText(str(winner.get("Abbreviation", "?")))
        self.kpi_laps._value_lbl.setText(
            str(session.total_laps) if hasattr(session, "total_laps") else "?")
        dnf_count = sum(1 for _, r in res.iterrows() if pd.isna(r.get("Time")))
        self.kpi_dnf._value_lbl.setText(str(dnf_count))

        try:
            fastest = session.laps.pick_fastest()
            ft = str(fastest["LapTime"])[:8]
            fd = fastest.get("Driver", "?")
            self.kpi_fast._value_lbl.setText(f"{fd}  {ft}")
        except Exception:
            pass

        # Colours for pos 1-3
        medal_bg = [QColor(GOLD + "40"), QColor(SILVER + "40"), QColor(BRONZE + "40")]
        medal_fg = [QColor(GOLD),        QColor(SILVER),        QColor(BRONZE)]

        for i, row in res.iterrows():
            pos = res.index.get_loc(i) + 1
            self.results_table.setRowHeight(res.index.get_loc(i), 46)

            pos_item = QTableWidgetItem(str(pos))
            pos_item.setTextAlignment(Qt.AlignCenter)
            pos_item.setFont(QFont("JetBrains Mono", 10, QFont.Bold))

            if pos <= 3:
                pos_item.setBackground(QBrush(medal_bg[pos-1]))
                pos_item.setForeground(QBrush(medal_fg[pos-1]))

            self.results_table.setItem(res.index.get_loc(i), 0, pos_item)
            self.results_table.setItem(res.index.get_loc(i), 1,
                QTableWidgetItem(str(row.get("Abbreviation", "?"))))
            self.results_table.setItem(res.index.get_loc(i), 2,
                QTableWidgetItem(str(row.get("TeamName", "?"))))

            time_val = row.get("Time")
            time_str = str(time_val)[:12] if pd.notna(time_val) else "DNF"
            t_item = QTableWidgetItem(time_str)
            t_item.setFont(QFont("JetBrains Mono", 10))
            self.results_table.setItem(res.index.get_loc(i), 3, t_item)
            self.results_table.setItem(res.index.get_loc(i), 4, QTableWidgetItem("—"))
            self.results_table.setItem(res.index.get_loc(i), 5, QTableWidgetItem("—"))

    def _populate_compare(self, session, d1, d2):
        def stats(code):
            laps = session.laps.pick_driver(code)
            if laps.empty:
                return None
            fastest  = laps.pick_fastest()
            avg_lap  = laps["LapTime"].mean()
            row      = session.results[session.results["Abbreviation"] == code]
            pos      = row.iloc[0].get("Position", "?") if not row.empty else "?"
            team     = row.iloc[0].get("TeamName",  "?") if not row.empty else "?"
            return dict(team=team, pos=pos,
                        fastest=fastest["LapTime"],
                        avg=avg_lap, laps=len(laps))

        s1, s2 = stats(d1), stats(d2)
        if not s1 or not s2:
            self.delta_text.setText("No data for one or both drivers.")
            return

        def fmt(td):
            if pd.isna(td):
                return "—"
            t = td.total_seconds()
            return f"{int(t//60)}:{t%60:06.3f}"

        for card, code, st in [(self.card_d1, d1, s1), (self.card_d2, d2, s2)]:
            card.code_lbl.setText(code)
            card.team_lbl.setText(str(st["team"]))
            card.stat_items["Fastest Lap"].set_value(fmt(st["fastest"]))
            card.stat_items["Average Lap"].set_value(fmt(st["avg"]))
            card.stat_items["Total Laps"].set_value(str(st["laps"]))
            card.stat_items["Finishing Position"].set_value(f"P{st['pos']}")

        delta = abs(s1["fastest"].total_seconds() - s2["fastest"].total_seconds())
        faster = d1 if s1["fastest"] < s2["fastest"] else d2
        self.delta_text.setText(f"⚡  {faster}  is faster by  {delta:.3f}s  on best lap")
        self.delta_text.setStyleSheet(f"""
            color:{PRIMARY}; font-size:14px; font-weight:700;
            font-family:'JetBrains Mono','Courier New',monospace;
        """)
        self.status_msg.setText(f"Comparison complete: {d1} vs {d2}")


# ─────────────────────────────────────────────────────────────────────────────
def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    pal = QPalette()
    pal.setColor(QPalette.Window,      QColor(BG))
    pal.setColor(QPalette.WindowText,  QColor(TEXT_DARK))
    pal.setColor(QPalette.Base,        QColor(WHITE))
    pal.setColor(QPalette.Text,        QColor(TEXT_DARK))
    pal.setColor(QPalette.Button,      QColor(WARM))
    pal.setColor(QPalette.ButtonText,  QColor(PRIMARY))
    app.setPalette(pal)

    font = QFont()
    font.setFamily("SF Pro Display, Segoe UI, Helvetica Neue, Arial")
    font.setPointSize(10)
    app.setFont(font)

    win = F1App()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
