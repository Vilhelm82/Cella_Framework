# Native CUDA/Vulkan renderer

`cella_graph_native` is a Qt Quick extension implementing
`CudaVulkanGraph`, a `QQuickItem` backed by a native `QSGRenderNode`.

## Memory path

1. Qt creates the Vulkan device with Linux external-memory and
   external-semaphore FD extensions enabled.
2. The render node compares the Vulkan physical-device UUID with every CUDA
   device and refuses cross-device sharing.
3. Vulkan allocates a device-local, exportable vertex buffer.
4. Its `OPAQUE_FD` memory handle is imported with
   `cudaImportExternalMemory`; CUDA maps the same allocation.
5. Its exportable semaphore is imported with
   `cudaImportExternalSemaphore`.
6. Graph updates are copied into the CUDA mapping, CUDA signals the imported
   semaphore, and an ordered Vulkan queue wait makes the vertices available to
   the following Qt render submission.
7. `QSGRenderNode` records `vkCmdDraw` inline in Qt Quick's active render pass.

There is no CUDA-to-Vulkan buffer copy. Current layout adapters still
materialize their final positions on the host before updating the shared render
allocation. A future compute adapter can write the exported CUDA pointer
directly; that is a separate end-to-end layout optimization.

Previous Vulkan reads are drained only when vertex content or capacity changes.
Static navigation and redraw remain entirely GPU resident.

## Fallbacks

- If Vulkan works but CUDA import does not, a coherent host-visible Vulkan
  buffer is used (`vulkan-cpu-fallback`).
- With Qt's software scene graph, the same vertex pairs render through
  `QPainter` (`software`).
- Device mismatch, missing shaders, or an unsupported graphics API is surfaced
  as `unavailable`; it is never mislabeled zero-copy.

## Build

The normal launcher builds the plugin automatically when absent. A clean manual
build is available for diagnostics:

```bash
python apps/cella_graph_workbench/native/build_native.py --clean
```

Build output is ignored under `native/build/`. The source build requires CMake,
Ninja, Qt 6 Quick development headers, Vulkan headers/loader development files,
`glslangValidator`, and CUDA 13 runtime/header packages. The build helper uses
a complete system CUDA development prefix first and falls back to a local
PyTorch `nvidia/cu13` compatibility package.

## Bounded live verification

```bash
QSG_RHI_BACKEND=vulkan timeout 6s \
  python apps/cella_graph_workbench/main.py --verify-native
```

The application polls the QML item directly and exits within five seconds. A
successful result reports `render_mode: cuda-vulkan-zero-copy`, shared capacity,
and upload generation. Screen-capture automation is deliberately not part of
this gate because a failed capture callback can strand the GUI event loop.
