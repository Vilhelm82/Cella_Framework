"""Runtime gate for responsive workbench controls and edge-safe popups."""
from __future__ import annotations

import os
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
APP = REPO / "apps/cella_graph_workbench"
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("QSG_RHI_BACKEND", "software")
sys.path.insert(0, str(APP))
sys.path.insert(0, str(REPO / "engine/src"))

from PySide6.QtCore import QMetaObject, QObject, QUrl  # noqa: E402
from PySide6.QtGui import QGuiApplication  # noqa: E402
from PySide6.QtQml import QQmlApplicationEngine  # noqa: E402

from backend import WorkbenchBridge  # noqa: E402


FAILS: list[str] = []


def check(name: str, condition: bool) -> None:
    print(f"[{'PASS' if condition else 'FAIL'}] {name}")
    if not condition:
        FAILS.append(name)


app = QGuiApplication(sys.argv[:1])
bridge = WorkbenchBridge()
engine = QQmlApplicationEngine()
engine.addImportPath(str(APP / "native/build/qml"))
engine.rootContext().setContextProperty("workbench", bridge)
engine.load(QUrl.fromLocalFile(str(APP / "qml/Main.qml")))
check("responsive workbench QML loads", bool(engine.rootObjects()))

if engine.rootObjects():
    window = engine.rootObjects()[0]
    window.setProperty("visible", True)
    window.setProperty("width", 1500)
    window.setProperty("height", 920)
    app.processEvents()

    header_grid = window.findChild(QObject, "headerGrid")
    source_scroll = window.findChild(QObject, "sourcesScroll")
    popups = [
        window.findChild(QObject, "sourcesPopup"),
        window.findChild(QObject, "colorsPopup"),
        window.findChild(QObject, "effectsPopup"),
    ]
    check("wide header keeps Find and Layout side by side", header_grid is not None and header_grid.property("columns") == 2)

    window.setProperty("width", 1000)
    app.processEvents()
    check("narrow header stacks control groups", header_grid is not None and header_grid.property("columns") == 1)
    check("source menu is vertically scrollable", source_scroll is not None and bool(source_scroll.property("clip")))

    bounded = True
    for popup in popups:
        if popup is None:
            bounded = False
            continue
        QMetaObject.invokeMethod(popup, "open")
        app.processEvents()
        x = float(popup.property("x"))
        y = float(popup.property("y"))
        width = float(popup.property("width"))
        height = float(popup.property("height"))
        bounded = bounded and x >= 9 and y >= 9
        bounded = bounded and x + width <= float(window.property("width")) - 9
        bounded = bounded and y + height <= float(window.property("height")) - 9
        QMetaObject.invokeMethod(popup, "close")
        app.processEvents()
    check("all appearance popups remain inside the narrow window", bounded)

if FAILS:
    print(f"GRAPH WORKBENCH UI GATE: OPEN — {len(FAILS)} failure(s): {FAILS}")
    raise SystemExit(1)
print("GRAPH WORKBENCH UI GATE: CLOSED")
