"""Gate the buildable native CUDA/Vulkan QSGRenderNode surface."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
NATIVE = REPO / "apps/cella_graph_workbench/native"
PLUGIN = NATIVE / "build/qml/Cella/Graph/Native/libcella_graph_native.so"
FAILS = []


def check(name, condition):
    print(f"[{'PASS' if condition else 'FAIL'}] {name}")
    if not condition:
        FAILS.append(name)


build = subprocess.run(
    [sys.executable, str(NATIVE / "build_native.py")],
    cwd=REPO,
    text=True,
    capture_output=True,
)
check("native renderer builds incrementally", build.returncode == 0)
check("QML plugin artifact exists", PLUGIN.is_file())

if PLUGIN.is_file():
    symbols = subprocess.run(["nm", "-D", str(PLUGIN)], text=True, capture_output=True, check=True).stdout
    check("plugin does not bind newer CUDA runtime v2 aliases", " U cudaSignalExternalSemaphoresAsync_v2" not in symbols and " U cudaGetDeviceProperties_v2" not in symbols)
    check("plugin imports CUDA external-memory APIs", " U cudaImportExternalMemory" in symbols and " U cudaImportExternalSemaphore" in symbols)

source = (NATIVE / "src/cuda_vulkan_render_node.cpp").read_text()
check("renderer enforces Vulkan/CUDA UUID equality", "cuDeviceGetUuid_v2" in source and "deviceUUID" in source)
check("renderer exports opaque-FD memory and semaphores", "vkGetMemoryFdKHR" in source and "vkGetSemaphoreFdKHR" in source)
check("renderer records inline native draw commands", "vkCmdDraw" in source and "QSGRenderNode" in (NATIVE / "src/cuda_vulkan_render_node.h").read_text())

status = subprocess.run(
    [sys.executable, str(REPO / "apps/cella_graph_workbench/main.py"), "--check"],
    cwd=REPO,
    text=True,
    capture_output=True,
)
report = json.loads(status.stdout)
check("non-GUI workbench check sees the built plugin", status.returncode == 0 and report["graphics"]["native_renderer_built"])

if FAILS:
    print(f"NATIVE GRAPH WORKBENCH GATE: OPEN — {len(FAILS)} failure(s): {FAILS}")
    raise SystemExit(1)
print("NATIVE GRAPH WORKBENCH GATE: CLOSED")
