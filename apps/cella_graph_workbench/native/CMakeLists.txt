cmake_minimum_required(VERSION 3.24)
project(cella_graph_native VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

find_package(Qt6 6.6 REQUIRED COMPONENTS Core Gui Qml Quick)
find_package(Vulkan REQUIRED)
find_program(GLSLANG_VALIDATOR glslangValidator REQUIRED)

if(NOT CUDA_COMPAT_ROOT)
    message(FATAL_ERROR "CUDA_COMPAT_ROOT must name a CUDA runtime/header prefix")
endif()
find_path(CUDA_RUNTIME_INCLUDE cuda_runtime_api.h
    PATHS "${CUDA_RUNTIME_INCLUDE_ROOT}" "${CUDA_COMPAT_ROOT}/include"
    NO_DEFAULT_PATH REQUIRED)
find_library(CUDA_RUNTIME_LIBRARY NAMES cudart libcudart.so.13 PATHS "${CUDA_COMPAT_ROOT}/lib" NO_DEFAULT_PATH REQUIRED)
find_library(CUDA_DRIVER_LIBRARY NAMES cuda PATHS /lib64 /usr/lib64 REQUIRED)

set(SHADER_OUTPUT_DIR "${CMAKE_CURRENT_BINARY_DIR}/shaders")
file(MAKE_DIRECTORY "${SHADER_OUTPUT_DIR}")
set(SHADER_SPV "")
foreach(name graph tonemap)
    foreach(stage vert frag)
        add_custom_command(
            OUTPUT "${SHADER_OUTPUT_DIR}/${name}.${stage}.spv"
            COMMAND "${GLSLANG_VALIDATOR}" -V --target-env vulkan1.1
                    -o "${SHADER_OUTPUT_DIR}/${name}.${stage}.spv"
                    "${CMAKE_CURRENT_SOURCE_DIR}/shaders/${name}.${stage}"
            DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/shaders/${name}.${stage}"
            VERBATIM
        )
        list(APPEND SHADER_SPV "${SHADER_OUTPUT_DIR}/${name}.${stage}.spv")
        set_source_files_properties(
            "${SHADER_OUTPUT_DIR}/${name}.${stage}.spv"
            PROPERTIES GENERATED TRUE QT_RESOURCE_ALIAS "${name}.${stage}.spv"
        )
    endforeach()
endforeach()

add_library(cella_graph_native SHARED
    src/cuda_vulkan_graph_item.cpp
    src/cuda_vulkan_graph_item.h
    src/cuda_vulkan_render_node.cpp
    src/cuda_vulkan_render_node.h
    src/plugin.cpp
    ${SHADER_SPV}
)

qt_add_resources(cella_graph_native "cella_graph_native_shaders"
    PREFIX "/cella/graph/native"
    FILES ${SHADER_SPV}
)

# Keep the runtime-matched CUDA headers first. CUDA_RUNTIME_INCLUDE_ROOT may be
# the same system include directory or a compatibility supplement for a wheel
# whose CUDA runtime package omits the crt/ directory.
target_include_directories(cella_graph_native PRIVATE
    "${CUDA_COMPAT_ROOT}/include"
    "${CUDA_RUNTIME_INCLUDE_ROOT}"
)
target_link_libraries(cella_graph_native PRIVATE
    Qt6::Core Qt6::Gui Qt6::Qml Qt6::Quick
    Vulkan::Vulkan
    "${CUDA_RUNTIME_LIBRARY}"
    "${CUDA_DRIVER_LIBRARY}"
)

get_filename_component(CUDA_RUNTIME_DIR "${CUDA_RUNTIME_LIBRARY}" DIRECTORY)
set_target_properties(cella_graph_native PROPERTIES
    OUTPUT_NAME cella_graph_native
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/qml/Cella/Graph/Native"
    BUILD_RPATH "${CUDA_RUNTIME_DIR}"
    INSTALL_RPATH "${CUDA_RUNTIME_DIR}"
)

configure_file(qmldir.in "${CMAKE_CURRENT_BINARY_DIR}/qml/Cella/Graph/Native/qmldir" @ONLY)
