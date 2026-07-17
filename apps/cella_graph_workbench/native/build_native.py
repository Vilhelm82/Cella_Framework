#!/usr/bin/env python3
"""Configure and build the Cella native graph renderer plugin."""
from __future__ import annotations

import argparse
import importlib.util
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BUILD = ROOT / "build"


def _valid_cuda_root(candidate: Path) -> bool:
    return (
        (candidate / "include/cuda_runtime_api.h").is_file()
        and (candidate / "include/crt/host_defines.h").is_file()
        and (candidate / "lib/libcudart.so.13").is_file()
    )


def cuda_compat_root() -> Path:
    system_roots = []
    for variable in ("CUDA_HOME", "CUDA_PATH"):
        if os.environ.get(variable):
            system_roots.append(Path(os.environ[variable]))
    system_roots.extend((Path("/usr/local/cuda"), Path("/usr/local/cuda-13.1")))
    for root in system_roots:
        for candidate in (root / "targets/x86_64-linux", root):
            if _valid_cuda_root(candidate):
                return candidate.resolve()

    spec = importlib.util.find_spec("nvidia")
    if spec is None or not spec.submodule_search_locations:
        raise RuntimeError("no system CUDA 13 development prefix or PyTorch nvidia/cu13 package is available")
    for location in spec.submodule_search_locations:
        candidate = Path(location) / "cu13"
        if _valid_cuda_root(candidate):
            return candidate.resolve()
    raise RuntimeError("could not locate complete CUDA 13 headers and libcudart")


def cuda_include_root(cuda: Path) -> Path:
    if (cuda / "include/crt/host_defines.h").is_file():
        return (cuda / "include").resolve()
    spec = importlib.util.find_spec("triton")
    if spec is not None and spec.submodule_search_locations:
        for location in spec.submodule_search_locations:
            candidate = Path(location) / "backends/nvidia/include"
            if (candidate / "cuda_runtime_api.h").is_file() and (candidate / "crt/host_defines.h").is_file():
                return candidate.resolve()
    raise RuntimeError("could not locate complete CUDA runtime headers")


def run(command: list[str]):
    print("+", " ".join(command))
    subprocess.run(command, check=True, cwd=ROOT)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--clean", action="store_true")
    parser.add_argument("--jobs", type=int, default=4)
    args = parser.parse_args(argv)
    if args.clean and BUILD.exists():
        import shutil
        shutil.rmtree(BUILD)
    cuda = cuda_compat_root()
    cuda_include = cuda_include_root(cuda)
    run([
        "cmake", "-S", str(ROOT), "-B", str(BUILD), "-G", "Ninja",
        "-DCMAKE_BUILD_TYPE=RelWithDebInfo",
        f"-DCUDA_COMPAT_ROOT={cuda}",
        f"-DCUDA_RUNTIME_INCLUDE_ROOT={cuda_include}",
    ])
    run(["cmake", "--build", str(BUILD), "--parallel", str(max(1, args.jobs))])
    plugin = BUILD / "qml/Cella/Graph/Native/libcella_graph_native.so"
    if not plugin.is_file():
        raise RuntimeError(f"build completed without expected plugin: {plugin}")
    print(plugin)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
