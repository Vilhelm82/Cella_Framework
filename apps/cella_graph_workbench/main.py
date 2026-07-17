#!/usr/bin/env python3
"""Launch the native Cella Graph Workbench."""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path


APP_ROOT = Path(__file__).resolve().parent
REPO_ROOT = APP_ROOT.parents[1]
ENGINE_SRC = REPO_ROOT / "engine" / "src"
NATIVE_ROOT = APP_ROOT / "native"
NATIVE_BUILD = NATIVE_ROOT / "build"
NATIVE_PLUGIN = NATIVE_BUILD / "qml/Cella/Graph/Native/libcella_graph_native.so"
sys.path.insert(0, str(ENGINE_SRC))


def _build_native_renderer(*, clean: bool = False) -> None:
    command = [sys.executable, str(NATIVE_ROOT / "build_native.py")]
    if clean:
        command.append("--clean")
    subprocess.run(command, check=True, cwd=REPO_ROOT)
    if not NATIVE_PLUGIN.is_file():
        raise RuntimeError(f"native build did not produce {NATIVE_PLUGIN}")


def _check() -> int:
    from cella.dag_service import dag_status
    from cella.dag_views import view_capabilities

    status = dag_status()
    report = {
        "ok": bool(status["ok"]),
        "application": "cella-graph-workbench-v1",
        "qt_binding": {
            "available": importlib.util.find_spec("PySide6") is not None,
            "required": "PySide6>=6.8",
        },
        "graph": status,
        "views": view_capabilities(),
        "graphics": {
            "requested_default": "vulkan",
            "environment_override": os.environ.get("QSG_RHI_BACKEND"),
            "native_renderer_source": (NATIVE_ROOT / "src/cuda_vulkan_render_node.cpp").is_file(),
            "native_renderer_built": NATIVE_PLUGIN.is_file(),
            "native_plugin": str(NATIVE_PLUGIN),
        },
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["ok"] else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Native Cella DAG navigator")
    parser.add_argument("--check", action="store_true", help="check graph, Qt and CUDA capabilities without opening a window")
    parser.add_argument("--graphics-api", choices=("vulkan", "auto"), default="vulkan")
    parser.add_argument("--smoke-ms", type=int, default=0, help="quit after this many milliseconds (automation)")
    parser.add_argument("--verify-native", action="store_true", help="report the live renderer mode and quit within five seconds")
    parser.add_argument("--rebuild-native", action="store_true", help="cleanly rebuild the CUDA/Vulkan QSGRenderNode plugin")
    args = parser.parse_args(argv)
    if args.check:
        return _check()
    if importlib.util.find_spec("PySide6") is None:
        print(
            "PySide6 is required for the native workbench. Install with:\n"
            "  python -m pip install --user 'PySide6>=6.8'",
            file=sys.stderr,
        )
        return 2
    try:
        if args.rebuild_native or not NATIVE_PLUGIN.is_file():
            _build_native_renderer(clean=args.rebuild_native)
    except (OSError, subprocess.CalledProcessError, RuntimeError) as exc:
        print(f"Native renderer build failed: {exc}", file=sys.stderr)
        return 5
    if args.graphics_api == "vulkan":
        os.environ.setdefault("QSG_RHI_BACKEND", "vulkan")

    from PySide6.QtCore import QTimer, QUrl
    from PySide6.QtGui import QGuiApplication
    from PySide6.QtQml import QQmlApplicationEngine
    from PySide6.QtQuick import QQuickGraphicsConfiguration, QQuickWindow
    import shiboken6

    from backend import WorkbenchBridge

    app = QGuiApplication(sys.argv[:1])
    app.setApplicationName("Cella Graph Workbench")
    app.setOrganizationName("Cella Framework")
    bridge = WorkbenchBridge()
    engine = QQmlApplicationEngine()
    engine.addImportPath(str(NATIVE_BUILD / "qml"))
    engine.rootContext().setContextProperty("workbench", bridge)
    engine.load(QUrl.fromLocalFile(str(APP_ROOT / "qml" / "Main.qml")))
    if not engine.rootObjects():
        return 3
    root = engine.rootObjects()[0]
    quick_window = shiboken6.wrapInstance(shiboken6.getCppPointer(root)[0], QQuickWindow)
    graphics = QQuickGraphicsConfiguration()
    graphics.setDeviceExtensions([
        b"VK_KHR_external_memory",
        b"VK_KHR_external_memory_fd",
        b"VK_KHR_external_semaphore",
        b"VK_KHR_external_semaphore_fd",
    ])
    quick_window.setGraphicsConfiguration(graphics)
    quick_window.show()
    if args.verify_native:
        from PySide6.QtCore import QObject

        deadline_ms = 5000

        def poll_renderer():
            graph_item = quick_window.findChild(QObject, "nativeGraph")
            mode = graph_item.property("renderMode") if graph_item else "initializing"
            if mode not in {None, "", "initializing"}:
                status = graph_item.property("interopStatus")
                payload = {
                    "ok": mode == "cuda-vulkan-zero-copy",
                    "render_mode": mode,
                    "interop_status": status,
                    "shared_bytes": graph_item.property("sharedBytes"),
                    "generation": graph_item.property("generation"),
                }
                print(json.dumps(payload, ensure_ascii=False))
                app.exit(0 if payload["ok"] else 6)
                return
            QTimer.singleShot(50, poll_renderer)

        def watchdog():
            print(json.dumps({"ok": False, "render_mode": "timeout", "deadline_ms": deadline_ms}))
            app.exit(7)

        QTimer.singleShot(0, poll_renderer)
        QTimer.singleShot(deadline_ms, watchdog)
    elif args.smoke_ms:
        QTimer.singleShot(max(100, args.smoke_ms), app.quit)
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
