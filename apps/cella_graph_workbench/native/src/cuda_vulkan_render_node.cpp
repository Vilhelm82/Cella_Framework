#include "cuda_vulkan_render_node.h"
#include "cuda_vulkan_graph_item.h"

#include <QFile>
#include <QDebug>
#include <QMatrix4x4>
#include <QMetaObject>
#include <QPainter>
#include <QQuickWindow>
#include <QSGRendererInterface>

#include <algorithm>
#include <cmath>
#include <cstring>
#include <limits>
#include <unistd.h>
#include <cuda.h>

namespace {

VkDeviceSize nextPowerOfTwo(VkDeviceSize value)
{
    VkDeviceSize result = 4096;
    while (result < value)
        result *= 2;
    return result;
}

QColor colourFrom(const QVariantMap &record, const char *key, const char *fallback)
{
    const QColor value(record.value(QString::fromLatin1(key), QString::fromLatin1(fallback)).toString());
    return value.isValid() ? value : QColor(QString::fromLatin1(fallback));
}

QColor lerpColour(const QColor &a, const QColor &b, float t)
{
    return QColor::fromRgbF(a.redF() + (b.redF() - a.redF()) * t,
                            a.greenF() + (b.greenF() - a.greenF()) * t,
                            a.blueF() + (b.blueF() - a.blueF()) * t,
                            a.alphaF() + (b.alphaF() - a.alphaF()) * t);
}

} // namespace

CudaVulkanRenderNode::CudaVulkanRenderNode(QQuickWindow *window,
                                           CudaVulkanGraphItem *item)
    : m_window(window), m_item(item)
{
    m_clock.start();
}

CudaVulkanRenderNode::~CudaVulkanRenderNode()
{
    destroyAll();
}

void CudaVulkanRenderNode::sync(const QVariantList &nodes,
                                const QVariantList &edges,
                                const QSizeF &size,
                                qreal opacity,
                                float lineWidth, float glowIntensity,
                                float flowSpeed, float flowAmount)
{
    m_size = size;
    m_opacity = opacity;
    m_lineWidth = lineWidth;
    m_glowIntensity = glowIntensity;
    m_flowSpeed = flowSpeed;
    m_flowAmount = flowAmount;
    buildVertices(nodes, edges);
    m_verticesDirty = true;
    markDirty(QSGNode::DirtyGeometry);
}

void CudaVulkanRenderNode::appendLine(float x1, float y1, float x2, float y2,
                                      const QColor &colour)
{
    appendLine(x1, y1, x2, y2, colour, colour);
}

void CudaVulkanRenderNode::appendLine(float x1, float y1, float x2, float y2,
                                      const QColor &colourA, const QColor &colourB)
{
    // Expand the segment into a quad; the vertex shader offsets each corner by
    // +/- side * halfWidth along the screen-space perpendicular, and the fragment
    // shader fades across |side| for a soft glow. Direction is normalised in-shader.
    const float dx = x2 - x1;
    const float dy = y2 - y1;
    const float ar = static_cast<float>(colourA.redF()), ag = static_cast<float>(colourA.greenF()),
                ab = static_cast<float>(colourA.blueF()), aa = static_cast<float>(colourA.alphaF());
    const float br = static_cast<float>(colourB.redF()), bg = static_cast<float>(colourB.greenF()),
                bb = static_cast<float>(colourB.blueF()), ba = static_cast<float>(colourB.alphaF());
    const Vertex a0{x1, y1, dx, dy, -1.0F, 0.0F, ar, ag, ab, aa};
    const Vertex a1{x1, y1, dx, dy, 1.0F, 0.0F, ar, ag, ab, aa};
    const Vertex b0{x2, y2, dx, dy, -1.0F, 1.0F, br, bg, bb, ba};
    const Vertex b1{x2, y2, dx, dy, 1.0F, 1.0F, br, bg, bb, ba};
    m_vertices.append(a0);
    m_vertices.append(a1);
    m_vertices.append(b0);
    m_vertices.append(b0);
    m_vertices.append(a1);
    m_vertices.append(b1);
}

void CudaVulkanRenderNode::appendNode(float x, float y, float radiusX,
                                      float radiusY, const QColor &colour)
{
    appendLine(x - radiusX, y, x, y - radiusY, colour);
    appendLine(x, y - radiusY, x + radiusX, y, colour);
    appendLine(x + radiusX, y, x, y + radiusY, colour);
    appendLine(x, y + radiusY, x - radiusX, y, colour);
    appendLine(x - radiusX * 0.72F, y - radiusY * 0.72F,
               x + radiusX * 0.72F, y + radiusY * 0.72F, colour);
    appendLine(x + radiusX * 0.72F, y - radiusY * 0.72F,
               x - radiusX * 0.72F, y + radiusY * 0.72F, colour);
}

void CudaVulkanRenderNode::buildVertices(const QVariantList &nodes,
                                         const QVariantList &edges)
{
    m_vertices.clear();
    m_vertices.reserve(edges.size() * 132 + nodes.size() * 36);
    for (const QVariant &value : edges) {
        const QVariantMap edge = value.toMap();
        const bool affected = edge.value(QStringLiteral("affected")).toBool();
        const QColor colourA = affected ? QColor(QStringLiteral("#ff657a"))
                                        : colourFrom(edge, "colour1", "#40505f");
        const QColor colourB = affected ? QColor(QStringLiteral("#ff657a"))
                                        : colourFrom(edge, "colour2", "#40505f");
        const QVariantList path = edge.value(QStringLiteral("path")).toList();
        if (path.size() >= 6) {
            // Bundled polyline: interpolate colour along the path, one glowing quad per segment.
            const int points = path.size() / 2;
            float px = path.at(0).toFloat();
            float py = path.at(1).toFloat();
            for (int i = 1; i < points; ++i) {
                const float qx = path.at(2 * i).toFloat();
                const float qy = path.at(2 * i + 1).toFloat();
                const float t0 = static_cast<float>(i - 1) / static_cast<float>(points - 1);
                const float t1 = static_cast<float>(i) / static_cast<float>(points - 1);
                appendLine(px, py, qx, qy, lerpColour(colourA, colourB, t0), lerpColour(colourA, colourB, t1));
                px = qx;
                py = qy;
            }
        } else {
            appendLine(edge.value(QStringLiteral("x1")).toFloat(),
                       edge.value(QStringLiteral("y1")).toFloat(),
                       edge.value(QStringLiteral("x2")).toFloat(),
                       edge.value(QStringLiteral("y2")).toFloat(), colourA, colourB);
        }
    }
    const float radiusX = 8.0F / std::max(1.0, m_size.width());
    const float radiusY = 8.0F / std::max(1.0, m_size.height());
    for (const QVariant &value : nodes) {
        const QVariantMap node = value.toMap();
        QColor colour = node.value(QStringLiteral("affected")).toBool()
            ? QColor(QStringLiteral("#ff657a"))
            : colourFrom(node, "colour", "#9ba7b4");
        appendNode(node.value(QStringLiteral("x")).toFloat(),
                   node.value(QStringLiteral("y")).toFloat(),
                   radiusX, radiusY, colour);
    }
}

void CudaVulkanRenderNode::publishStatus(const QString &mode,
                                         const QString &message)
{
    const QString diagnostic = mode + QStringLiteral(": ") + message;
    if (diagnostic != m_lastStatus) {
        qInfo().noquote() << "CELLA_NATIVE_RENDERER" << diagnostic;
        m_lastStatus = diagnostic;
    }
    if (!m_item)
        return;
    const qulonglong bytes = static_cast<qulonglong>(m_capacity);
    const qulonglong generation = m_generation;
    QPointer<CudaVulkanGraphItem> item = m_item;
    QMetaObject::invokeMethod(m_item, [item, mode, message, bytes, generation]() {
        if (item)
            item->publishRendererStatus(mode, message, bytes, generation);
    }, Qt::QueuedConnection);
}

QString CudaVulkanRenderNode::cudaErrorMessage(const char *operation,
                                               cudaError_t error) const
{
    return QStringLiteral("%1 failed: %2 (%3)")
        .arg(QString::fromLatin1(operation),
             QString::fromLatin1(cudaGetErrorName(error)),
             QString::fromLatin1(cudaGetErrorString(error)));
}

bool CudaVulkanRenderNode::acquireVulkanContext()
{
    if (!m_window)
        return false;
    QSGRendererInterface *renderer = m_window->rendererInterface();
    if (!renderer)
        return false;
    if (renderer->graphicsApi() == QSGRendererInterface::Software) {
        m_mode = BufferMode::Software;
        publishStatus(QStringLiteral("software"),
                      QStringLiteral("Qt software renderer; no GPU buffer allocated"));
        return true;
    }
    if (renderer->graphicsApi() != QSGRendererInterface::Vulkan) {
        publishStatus(QStringLiteral("unavailable"),
                      QStringLiteral("Native graph renderer requires Vulkan or the Qt software backend"));
        return false;
    }

    auto handle = [renderer, this](QSGRendererInterface::Resource resource) -> void * {
        return renderer->getResource(m_window, resource);
    };
    void *physical = handle(QSGRendererInterface::PhysicalDeviceResource);
    void *device = handle(QSGRendererInterface::DeviceResource);
    void *queue = handle(QSGRendererInterface::CommandQueueResource);
    void *renderPass = handle(QSGRendererInterface::RenderPassResource);
    if (!physical || !device || !queue || !renderPass) {
        publishStatus(QStringLiteral("unavailable"),
                      QStringLiteral("Qt did not expose the required Vulkan handles"));
        return false;
    }
    m_physicalDevice = *static_cast<VkPhysicalDevice *>(physical);
    m_device = *static_cast<VkDevice *>(device);
    m_queue = *static_cast<VkQueue *>(queue);
    const VkRenderPass activeRenderPass = *static_cast<VkRenderPass *>(renderPass);
    if (m_renderPass != activeRenderPass) {
        destroyTonemap();  // only the tonemap pipeline depends on Qt's pass; glow uses the HDR pass
        m_renderPass = activeRenderPass;
    }
    return m_physicalDevice && m_device && m_queue && m_renderPass;
}

QByteArray CudaVulkanRenderNode::loadShader(const QString &path) const
{
    QFile file(path);
    if (!file.open(QIODevice::ReadOnly))
        return {};
    return file.readAll();
}

bool CudaVulkanRenderNode::ensurePipeline()
{
    if (m_pipeline)
        return true;
    const QByteArray vertexBytes = loadShader(QStringLiteral(":/cella/graph/native/graph.vert.spv"));
    const QByteArray fragmentBytes = loadShader(QStringLiteral(":/cella/graph/native/graph.frag.spv"));
    if (vertexBytes.isEmpty() || fragmentBytes.isEmpty()
        || vertexBytes.size() % 4 || fragmentBytes.size() % 4) {
        m_lastStatus = QStringLiteral("Embedded SPIR-V shaders are unavailable or invalid");
        return false;
    }

    VkShaderModuleCreateInfo moduleInfo{VK_STRUCTURE_TYPE_SHADER_MODULE_CREATE_INFO};
    moduleInfo.codeSize = static_cast<size_t>(vertexBytes.size());
    moduleInfo.pCode = reinterpret_cast<const uint32_t *>(vertexBytes.constData());
    if (vkCreateShaderModule(m_device, &moduleInfo, nullptr, &m_vertexShader) != VK_SUCCESS) {
        m_lastStatus = QStringLiteral("vkCreateShaderModule(vertex) failed");
        return false;
    }
    moduleInfo.codeSize = static_cast<size_t>(fragmentBytes.size());
    moduleInfo.pCode = reinterpret_cast<const uint32_t *>(fragmentBytes.constData());
    if (vkCreateShaderModule(m_device, &moduleInfo, nullptr, &m_fragmentShader) != VK_SUCCESS) {
        m_lastStatus = QStringLiteral("vkCreateShaderModule(fragment) failed");
        return false;
    }

    VkPushConstantRange pushRange{};
    pushRange.stageFlags = VK_SHADER_STAGE_VERTEX_BIT | VK_SHADER_STAGE_FRAGMENT_BIT;
    pushRange.size = sizeof(PushConstants);
    VkPipelineLayoutCreateInfo layoutInfo{VK_STRUCTURE_TYPE_PIPELINE_LAYOUT_CREATE_INFO};
    layoutInfo.pushConstantRangeCount = 1;
    layoutInfo.pPushConstantRanges = &pushRange;
    if (vkCreatePipelineLayout(m_device, &layoutInfo, nullptr, &m_pipelineLayout) != VK_SUCCESS) {
        m_lastStatus = QStringLiteral("vkCreatePipelineLayout failed");
        return false;
    }

    VkPipelineShaderStageCreateInfo stages[2]{};
    stages[0].sType = VK_STRUCTURE_TYPE_PIPELINE_SHADER_STAGE_CREATE_INFO;
    stages[0].stage = VK_SHADER_STAGE_VERTEX_BIT;
    stages[0].module = m_vertexShader;
    stages[0].pName = "main";
    stages[1].sType = VK_STRUCTURE_TYPE_PIPELINE_SHADER_STAGE_CREATE_INFO;
    stages[1].stage = VK_SHADER_STAGE_FRAGMENT_BIT;
    stages[1].module = m_fragmentShader;
    stages[1].pName = "main";

    VkVertexInputBindingDescription binding{};
    binding.binding = 0;
    binding.stride = sizeof(Vertex);
    binding.inputRate = VK_VERTEX_INPUT_RATE_VERTEX;
    VkVertexInputAttributeDescription attributes[3]{};
    attributes[0] = {0, 0, VK_FORMAT_R32G32_SFLOAT, offsetof(Vertex, x)};
    attributes[1] = {1, 0, VK_FORMAT_R32G32B32A32_SFLOAT, offsetof(Vertex, dirX)};
    attributes[2] = {2, 0, VK_FORMAT_R32G32B32A32_SFLOAT, offsetof(Vertex, r)};
    VkPipelineVertexInputStateCreateInfo vertexInput{VK_STRUCTURE_TYPE_PIPELINE_VERTEX_INPUT_STATE_CREATE_INFO};
    vertexInput.vertexBindingDescriptionCount = 1;
    vertexInput.pVertexBindingDescriptions = &binding;
    vertexInput.vertexAttributeDescriptionCount = 3;
    vertexInput.pVertexAttributeDescriptions = attributes;

    VkPipelineInputAssemblyStateCreateInfo assembly{VK_STRUCTURE_TYPE_PIPELINE_INPUT_ASSEMBLY_STATE_CREATE_INFO};
    assembly.topology = VK_PRIMITIVE_TOPOLOGY_TRIANGLE_LIST;
    VkPipelineViewportStateCreateInfo viewport{VK_STRUCTURE_TYPE_PIPELINE_VIEWPORT_STATE_CREATE_INFO};
    viewport.viewportCount = 1;
    viewport.scissorCount = 1;
    VkPipelineRasterizationStateCreateInfo raster{VK_STRUCTURE_TYPE_PIPELINE_RASTERIZATION_STATE_CREATE_INFO};
    raster.polygonMode = VK_POLYGON_MODE_FILL;
    raster.cullMode = VK_CULL_MODE_NONE;
    raster.frontFace = VK_FRONT_FACE_COUNTER_CLOCKWISE;
    raster.lineWidth = 1.0F;
    VkPipelineMultisampleStateCreateInfo multisample{VK_STRUCTURE_TYPE_PIPELINE_MULTISAMPLE_STATE_CREATE_INFO};
    multisample.rasterizationSamples = VK_SAMPLE_COUNT_1_BIT;
    VkPipelineColorBlendAttachmentState attachment{};
    attachment.blendEnable = VK_TRUE;
    attachment.srcColorBlendFactor = VK_BLEND_FACTOR_SRC_ALPHA;
    attachment.dstColorBlendFactor = VK_BLEND_FACTOR_ONE;  // additive glow: overlaps accumulate light
    attachment.colorBlendOp = VK_BLEND_OP_ADD;
    attachment.srcAlphaBlendFactor = VK_BLEND_FACTOR_ONE;
    attachment.dstAlphaBlendFactor = VK_BLEND_FACTOR_ONE_MINUS_SRC_ALPHA;
    attachment.alphaBlendOp = VK_BLEND_OP_ADD;
    attachment.colorWriteMask = VK_COLOR_COMPONENT_R_BIT | VK_COLOR_COMPONENT_G_BIT
        | VK_COLOR_COMPONENT_B_BIT | VK_COLOR_COMPONENT_A_BIT;
    VkPipelineColorBlendStateCreateInfo blend{VK_STRUCTURE_TYPE_PIPELINE_COLOR_BLEND_STATE_CREATE_INFO};
    blend.attachmentCount = 1;
    blend.pAttachments = &attachment;
    const VkDynamicState dynamicStates[] = {VK_DYNAMIC_STATE_VIEWPORT, VK_DYNAMIC_STATE_SCISSOR};
    VkPipelineDynamicStateCreateInfo dynamic{VK_STRUCTURE_TYPE_PIPELINE_DYNAMIC_STATE_CREATE_INFO};
    dynamic.dynamicStateCount = 2;
    dynamic.pDynamicStates = dynamicStates;

    VkGraphicsPipelineCreateInfo pipelineInfo{VK_STRUCTURE_TYPE_GRAPHICS_PIPELINE_CREATE_INFO};
    pipelineInfo.stageCount = 2;
    pipelineInfo.pStages = stages;
    pipelineInfo.pVertexInputState = &vertexInput;
    pipelineInfo.pInputAssemblyState = &assembly;
    pipelineInfo.pViewportState = &viewport;
    pipelineInfo.pRasterizationState = &raster;
    pipelineInfo.pMultisampleState = &multisample;
    pipelineInfo.pColorBlendState = &blend;
    pipelineInfo.pDynamicState = &dynamic;
    pipelineInfo.layout = m_pipelineLayout;
    pipelineInfo.renderPass = m_hdrRenderPass;  // glow renders into the offscreen HDR target
    pipelineInfo.subpass = 0;
    if (vkCreateGraphicsPipelines(m_device, VK_NULL_HANDLE, 1, &pipelineInfo,
                                  nullptr, &m_pipeline) != VK_SUCCESS) {
        m_lastStatus = QStringLiteral("vkCreateGraphicsPipelines failed");
        return false;
    }
    return true;
}

bool CudaVulkanRenderNode::ensureHdrTarget(uint32_t width, uint32_t height)
{
    width = std::max(1u, width);
    height = std::max(1u, height);
    if (m_hdrRenderPass == VK_NULL_HANDLE) {
        VkAttachmentDescription colour{};
        colour.format = VK_FORMAT_R16G16B16A16_SFLOAT;
        colour.samples = VK_SAMPLE_COUNT_1_BIT;
        colour.loadOp = VK_ATTACHMENT_LOAD_OP_CLEAR;
        colour.storeOp = VK_ATTACHMENT_STORE_OP_STORE;
        colour.stencilLoadOp = VK_ATTACHMENT_LOAD_OP_DONT_CARE;
        colour.stencilStoreOp = VK_ATTACHMENT_STORE_OP_DONT_CARE;
        colour.initialLayout = VK_IMAGE_LAYOUT_UNDEFINED;
        colour.finalLayout = VK_IMAGE_LAYOUT_SHADER_READ_ONLY_OPTIMAL;
        VkAttachmentReference ref{0, VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL};
        VkSubpassDescription subpass{};
        subpass.pipelineBindPoint = VK_PIPELINE_BIND_POINT_GRAPHICS;
        subpass.colorAttachmentCount = 1;
        subpass.pColorAttachments = &ref;
        VkSubpassDependency deps[2]{};
        deps[0].srcSubpass = VK_SUBPASS_EXTERNAL;
        deps[0].dstSubpass = 0;
        deps[0].srcStageMask = VK_PIPELINE_STAGE_FRAGMENT_SHADER_BIT;
        deps[0].dstStageMask = VK_PIPELINE_STAGE_COLOR_ATTACHMENT_OUTPUT_BIT;
        deps[0].srcAccessMask = VK_ACCESS_SHADER_READ_BIT;
        deps[0].dstAccessMask = VK_ACCESS_COLOR_ATTACHMENT_WRITE_BIT;
        deps[1].srcSubpass = 0;
        deps[1].dstSubpass = VK_SUBPASS_EXTERNAL;
        deps[1].srcStageMask = VK_PIPELINE_STAGE_COLOR_ATTACHMENT_OUTPUT_BIT;
        deps[1].dstStageMask = VK_PIPELINE_STAGE_FRAGMENT_SHADER_BIT;
        deps[1].srcAccessMask = VK_ACCESS_COLOR_ATTACHMENT_WRITE_BIT;
        deps[1].dstAccessMask = VK_ACCESS_SHADER_READ_BIT;
        VkRenderPassCreateInfo rp{VK_STRUCTURE_TYPE_RENDER_PASS_CREATE_INFO};
        rp.attachmentCount = 1;
        rp.pAttachments = &colour;
        rp.subpassCount = 1;
        rp.pSubpasses = &subpass;
        rp.dependencyCount = 2;
        rp.pDependencies = deps;
        if (vkCreateRenderPass(m_device, &rp, nullptr, &m_hdrRenderPass) != VK_SUCCESS) {
            m_lastStatus = QStringLiteral("vkCreateRenderPass(hdr) failed");
            return false;
        }
    }
    if (m_hdrImage != VK_NULL_HANDLE && m_hdrExtent.width == width && m_hdrExtent.height == height)
        return true;
    destroyHdrTarget();

    VkImageCreateInfo img{VK_STRUCTURE_TYPE_IMAGE_CREATE_INFO};
    img.imageType = VK_IMAGE_TYPE_2D;
    img.format = VK_FORMAT_R16G16B16A16_SFLOAT;
    img.extent = {width, height, 1};
    img.mipLevels = 1;
    img.arrayLayers = 1;
    img.samples = VK_SAMPLE_COUNT_1_BIT;
    img.tiling = VK_IMAGE_TILING_OPTIMAL;
    img.usage = VK_IMAGE_USAGE_COLOR_ATTACHMENT_BIT | VK_IMAGE_USAGE_SAMPLED_BIT;
    img.initialLayout = VK_IMAGE_LAYOUT_UNDEFINED;
    if (vkCreateImage(m_device, &img, nullptr, &m_hdrImage) != VK_SUCCESS) {
        m_lastStatus = QStringLiteral("vkCreateImage(hdr) failed");
        return false;
    }
    VkMemoryRequirements req{};
    vkGetImageMemoryRequirements(m_device, m_hdrImage, &req);
    VkMemoryAllocateInfo alloc{VK_STRUCTURE_TYPE_MEMORY_ALLOCATE_INFO};
    alloc.allocationSize = req.size;
    alloc.memoryTypeIndex = findMemoryType(req.memoryTypeBits, VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT);
    if (vkAllocateMemory(m_device, &alloc, nullptr, &m_hdrMemory) != VK_SUCCESS) {
        m_lastStatus = QStringLiteral("vkAllocateMemory(hdr) failed");
        return false;
    }
    vkBindImageMemory(m_device, m_hdrImage, m_hdrMemory, 0);

    VkImageViewCreateInfo view{VK_STRUCTURE_TYPE_IMAGE_VIEW_CREATE_INFO};
    view.image = m_hdrImage;
    view.viewType = VK_IMAGE_VIEW_TYPE_2D;
    view.format = VK_FORMAT_R16G16B16A16_SFLOAT;
    view.subresourceRange = {VK_IMAGE_ASPECT_COLOR_BIT, 0, 1, 0, 1};
    if (vkCreateImageView(m_device, &view, nullptr, &m_hdrView) != VK_SUCCESS) {
        m_lastStatus = QStringLiteral("vkCreateImageView(hdr) failed");
        return false;
    }
    VkFramebufferCreateInfo fb{VK_STRUCTURE_TYPE_FRAMEBUFFER_CREATE_INFO};
    fb.renderPass = m_hdrRenderPass;
    fb.attachmentCount = 1;
    fb.pAttachments = &m_hdrView;
    fb.width = width;
    fb.height = height;
    fb.layers = 1;
    if (vkCreateFramebuffer(m_device, &fb, nullptr, &m_hdrFramebuffer) != VK_SUCCESS) {
        m_lastStatus = QStringLiteral("vkCreateFramebuffer(hdr) failed");
        return false;
    }
    m_hdrExtent = {width, height};
    return true;
}

bool CudaVulkanRenderNode::ensureTonemapPipeline()
{
    if (m_tonemapPipeline)
        return true;
    const QByteArray vertexBytes = loadShader(QStringLiteral(":/cella/graph/native/tonemap.vert.spv"));
    const QByteArray fragmentBytes = loadShader(QStringLiteral(":/cella/graph/native/tonemap.frag.spv"));
    if (vertexBytes.isEmpty() || fragmentBytes.isEmpty()) {
        m_lastStatus = QStringLiteral("tonemap SPIR-V unavailable");
        return false;
    }
    VkShaderModuleCreateInfo moduleInfo{VK_STRUCTURE_TYPE_SHADER_MODULE_CREATE_INFO};
    moduleInfo.codeSize = static_cast<size_t>(vertexBytes.size());
    moduleInfo.pCode = reinterpret_cast<const uint32_t *>(vertexBytes.constData());
    if (vkCreateShaderModule(m_device, &moduleInfo, nullptr, &m_tonemapVert) != VK_SUCCESS)
        return false;
    moduleInfo.codeSize = static_cast<size_t>(fragmentBytes.size());
    moduleInfo.pCode = reinterpret_cast<const uint32_t *>(fragmentBytes.constData());
    if (vkCreateShaderModule(m_device, &moduleInfo, nullptr, &m_tonemapFrag) != VK_SUCCESS)
        return false;

    VkDescriptorSetLayoutBinding binding{};
    binding.binding = 0;
    binding.descriptorType = VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER;
    binding.descriptorCount = 1;
    binding.stageFlags = VK_SHADER_STAGE_FRAGMENT_BIT;
    VkDescriptorSetLayoutCreateInfo setLayoutInfo{VK_STRUCTURE_TYPE_DESCRIPTOR_SET_LAYOUT_CREATE_INFO};
    setLayoutInfo.bindingCount = 1;
    setLayoutInfo.pBindings = &binding;
    if (vkCreateDescriptorSetLayout(m_device, &setLayoutInfo, nullptr, &m_tonemapSetLayout) != VK_SUCCESS)
        return false;

    VkDescriptorPoolSize poolSize{VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER, 1};
    VkDescriptorPoolCreateInfo poolInfo{VK_STRUCTURE_TYPE_DESCRIPTOR_POOL_CREATE_INFO};
    poolInfo.maxSets = 1;
    poolInfo.poolSizeCount = 1;
    poolInfo.pPoolSizes = &poolSize;
    if (vkCreateDescriptorPool(m_device, &poolInfo, nullptr, &m_tonemapPool) != VK_SUCCESS)
        return false;
    VkDescriptorSetAllocateInfo setAlloc{VK_STRUCTURE_TYPE_DESCRIPTOR_SET_ALLOCATE_INFO};
    setAlloc.descriptorPool = m_tonemapPool;
    setAlloc.descriptorSetCount = 1;
    setAlloc.pSetLayouts = &m_tonemapSetLayout;
    if (vkAllocateDescriptorSets(m_device, &setAlloc, &m_tonemapSet) != VK_SUCCESS)
        return false;

    VkSamplerCreateInfo samplerInfo{VK_STRUCTURE_TYPE_SAMPLER_CREATE_INFO};
    samplerInfo.magFilter = VK_FILTER_LINEAR;
    samplerInfo.minFilter = VK_FILTER_LINEAR;
    samplerInfo.addressModeU = VK_SAMPLER_ADDRESS_MODE_CLAMP_TO_EDGE;
    samplerInfo.addressModeV = VK_SAMPLER_ADDRESS_MODE_CLAMP_TO_EDGE;
    samplerInfo.addressModeW = VK_SAMPLER_ADDRESS_MODE_CLAMP_TO_EDGE;
    if (vkCreateSampler(m_device, &samplerInfo, nullptr, &m_hdrSampler) != VK_SUCCESS)
        return false;

    VkPushConstantRange pushRange{};
    pushRange.stageFlags = VK_SHADER_STAGE_VERTEX_BIT | VK_SHADER_STAGE_FRAGMENT_BIT;
    pushRange.size = sizeof(TonemapPush);
    VkPipelineLayoutCreateInfo layoutInfo{VK_STRUCTURE_TYPE_PIPELINE_LAYOUT_CREATE_INFO};
    layoutInfo.setLayoutCount = 1;
    layoutInfo.pSetLayouts = &m_tonemapSetLayout;
    layoutInfo.pushConstantRangeCount = 1;
    layoutInfo.pPushConstantRanges = &pushRange;
    if (vkCreatePipelineLayout(m_device, &layoutInfo, nullptr, &m_tonemapLayout) != VK_SUCCESS)
        return false;

    VkPipelineShaderStageCreateInfo stages[2]{};
    stages[0].sType = VK_STRUCTURE_TYPE_PIPELINE_SHADER_STAGE_CREATE_INFO;
    stages[0].stage = VK_SHADER_STAGE_VERTEX_BIT;
    stages[0].module = m_tonemapVert;
    stages[0].pName = "main";
    stages[1].sType = VK_STRUCTURE_TYPE_PIPELINE_SHADER_STAGE_CREATE_INFO;
    stages[1].stage = VK_SHADER_STAGE_FRAGMENT_BIT;
    stages[1].module = m_tonemapFrag;
    stages[1].pName = "main";

    VkPipelineVertexInputStateCreateInfo vertexInput{VK_STRUCTURE_TYPE_PIPELINE_VERTEX_INPUT_STATE_CREATE_INFO};
    VkPipelineInputAssemblyStateCreateInfo assembly{VK_STRUCTURE_TYPE_PIPELINE_INPUT_ASSEMBLY_STATE_CREATE_INFO};
    assembly.topology = VK_PRIMITIVE_TOPOLOGY_TRIANGLE_LIST;
    VkPipelineViewportStateCreateInfo viewport{VK_STRUCTURE_TYPE_PIPELINE_VIEWPORT_STATE_CREATE_INFO};
    viewport.viewportCount = 1;
    viewport.scissorCount = 1;
    VkPipelineRasterizationStateCreateInfo raster{VK_STRUCTURE_TYPE_PIPELINE_RASTERIZATION_STATE_CREATE_INFO};
    raster.polygonMode = VK_POLYGON_MODE_FILL;
    raster.cullMode = VK_CULL_MODE_NONE;
    raster.frontFace = VK_FRONT_FACE_COUNTER_CLOCKWISE;
    raster.lineWidth = 1.0F;
    VkPipelineMultisampleStateCreateInfo multisample{VK_STRUCTURE_TYPE_PIPELINE_MULTISAMPLE_STATE_CREATE_INFO};
    multisample.rasterizationSamples = VK_SAMPLE_COUNT_1_BIT;
    VkPipelineColorBlendAttachmentState attachment{};
    attachment.blendEnable = VK_TRUE;
    attachment.srcColorBlendFactor = VK_BLEND_FACTOR_SRC_ALPHA;
    attachment.dstColorBlendFactor = VK_BLEND_FACTOR_ONE_MINUS_SRC_ALPHA;
    attachment.colorBlendOp = VK_BLEND_OP_ADD;
    attachment.srcAlphaBlendFactor = VK_BLEND_FACTOR_ONE;
    attachment.dstAlphaBlendFactor = VK_BLEND_FACTOR_ONE_MINUS_SRC_ALPHA;
    attachment.alphaBlendOp = VK_BLEND_OP_ADD;
    attachment.colorWriteMask = VK_COLOR_COMPONENT_R_BIT | VK_COLOR_COMPONENT_G_BIT
        | VK_COLOR_COMPONENT_B_BIT | VK_COLOR_COMPONENT_A_BIT;
    VkPipelineColorBlendStateCreateInfo blend{VK_STRUCTURE_TYPE_PIPELINE_COLOR_BLEND_STATE_CREATE_INFO};
    blend.attachmentCount = 1;
    blend.pAttachments = &attachment;
    const VkDynamicState dynamicStates[] = {VK_DYNAMIC_STATE_VIEWPORT, VK_DYNAMIC_STATE_SCISSOR};
    VkPipelineDynamicStateCreateInfo dynamic{VK_STRUCTURE_TYPE_PIPELINE_DYNAMIC_STATE_CREATE_INFO};
    dynamic.dynamicStateCount = 2;
    dynamic.pDynamicStates = dynamicStates;

    VkGraphicsPipelineCreateInfo pipelineInfo{VK_STRUCTURE_TYPE_GRAPHICS_PIPELINE_CREATE_INFO};
    pipelineInfo.stageCount = 2;
    pipelineInfo.pStages = stages;
    pipelineInfo.pVertexInputState = &vertexInput;
    pipelineInfo.pInputAssemblyState = &assembly;
    pipelineInfo.pViewportState = &viewport;
    pipelineInfo.pRasterizationState = &raster;
    pipelineInfo.pMultisampleState = &multisample;
    pipelineInfo.pColorBlendState = &blend;
    pipelineInfo.pDynamicState = &dynamic;
    pipelineInfo.layout = m_tonemapLayout;
    pipelineInfo.renderPass = m_renderPass;  // tonemap resolves into Qt's swapchain pass
    pipelineInfo.subpass = 0;
    if (vkCreateGraphicsPipelines(m_device, VK_NULL_HANDLE, 1, &pipelineInfo, nullptr, &m_tonemapPipeline) != VK_SUCCESS) {
        m_lastStatus = QStringLiteral("vkCreateGraphicsPipelines(tonemap) failed");
        return false;
    }

    if (m_offscreenPool == VK_NULL_HANDLE) {
        uint32_t familyCount = 0;
        vkGetPhysicalDeviceQueueFamilyProperties(m_physicalDevice, &familyCount, nullptr);
        QVector<VkQueueFamilyProperties> families(static_cast<int>(familyCount));
        vkGetPhysicalDeviceQueueFamilyProperties(m_physicalDevice, &familyCount, families.data());
        uint32_t graphicsFamily = 0;
        for (uint32_t i = 0; i < familyCount; ++i) {
            if (families[static_cast<int>(i)].queueFlags & VK_QUEUE_GRAPHICS_BIT) {
                graphicsFamily = i;
                break;
            }
        }
        VkCommandPoolCreateInfo poolCreate{VK_STRUCTURE_TYPE_COMMAND_POOL_CREATE_INFO};
        poolCreate.flags = VK_COMMAND_POOL_CREATE_RESET_COMMAND_BUFFER_BIT;
        poolCreate.queueFamilyIndex = graphicsFamily;
        if (vkCreateCommandPool(m_device, &poolCreate, nullptr, &m_offscreenPool) != VK_SUCCESS)
            return false;
        VkCommandBufferAllocateInfo cmdAlloc{VK_STRUCTURE_TYPE_COMMAND_BUFFER_ALLOCATE_INFO};
        cmdAlloc.commandPool = m_offscreenPool;
        cmdAlloc.level = VK_COMMAND_BUFFER_LEVEL_PRIMARY;
        cmdAlloc.commandBufferCount = 1;
        if (vkAllocateCommandBuffers(m_device, &cmdAlloc, &m_offscreenCmd) != VK_SUCCESS)
            return false;
        VkFenceCreateInfo fenceInfo{VK_STRUCTURE_TYPE_FENCE_CREATE_INFO};
        if (vkCreateFence(m_device, &fenceInfo, nullptr, &m_offscreenFence) != VK_SUCCESS)
            return false;
    }
    return true;
}

void CudaVulkanRenderNode::updateTonemapDescriptor()
{
    if (!m_tonemapSet || !m_hdrView || !m_hdrSampler)
        return;
    VkDescriptorImageInfo info{};
    info.sampler = m_hdrSampler;
    info.imageView = m_hdrView;
    info.imageLayout = VK_IMAGE_LAYOUT_SHADER_READ_ONLY_OPTIMAL;
    VkWriteDescriptorSet write{VK_STRUCTURE_TYPE_WRITE_DESCRIPTOR_SET};
    write.dstSet = m_tonemapSet;
    write.dstBinding = 0;
    write.descriptorCount = 1;
    write.descriptorType = VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER;
    write.pImageInfo = &info;
    vkUpdateDescriptorSets(m_device, 1, &write, 0, nullptr);
}

void CudaVulkanRenderNode::recordOffscreen(const QMatrix4x4 &projection)
{
    if (!m_offscreenCmd || !m_hdrFramebuffer || !m_pipeline)
        return;
    vkResetCommandBuffer(m_offscreenCmd, 0);
    VkCommandBufferBeginInfo begin{VK_STRUCTURE_TYPE_COMMAND_BUFFER_BEGIN_INFO};
    begin.flags = VK_COMMAND_BUFFER_USAGE_ONE_TIME_SUBMIT_BIT;
    vkBeginCommandBuffer(m_offscreenCmd, &begin);
    VkClearValue clear{};
    clear.color = {{0.0F, 0.0F, 0.0F, 0.0F}};
    VkRenderPassBeginInfo rpb{VK_STRUCTURE_TYPE_RENDER_PASS_BEGIN_INFO};
    rpb.renderPass = m_hdrRenderPass;
    rpb.framebuffer = m_hdrFramebuffer;
    rpb.renderArea.extent = m_hdrExtent;
    rpb.clearValueCount = 1;
    rpb.pClearValues = &clear;
    vkCmdBeginRenderPass(m_offscreenCmd, &rpb, VK_SUBPASS_CONTENTS_INLINE);
    VkViewport vp{0.0F, 0.0F, static_cast<float>(m_hdrExtent.width), static_cast<float>(m_hdrExtent.height), 0.0F, 1.0F};
    VkRect2D scissor{{0, 0}, m_hdrExtent};
    vkCmdSetViewport(m_offscreenCmd, 0, 1, &vp);
    vkCmdSetScissor(m_offscreenCmd, 0, 1, &scissor);
    if (!m_vertices.isEmpty() && m_buffer) {
        vkCmdBindPipeline(m_offscreenCmd, VK_PIPELINE_BIND_POINT_GRAPHICS, m_pipeline);
        const VkDeviceSize offset = 0;
        vkCmdBindVertexBuffers(m_offscreenCmd, 0, 1, &m_buffer, &offset);
        PushConstants push{};
        std::memcpy(push.mvp, projection.constData(), sizeof(push.mvp));
        push.itemWidth = static_cast<float>(m_hdrExtent.width);
        push.itemHeight = static_cast<float>(m_hdrExtent.height);
        push.opacity = 1.0F;
        push.halfWidth = m_lineWidth;
        push.time = static_cast<float>(m_clock.elapsed() / 1000.0);
        push.glowIntensity = 1.0F;  // raw accumulation into HDR; exposure applied at tonemap
        push.flowSpeed = m_flowSpeed;
        push.flowAmount = m_flowAmount;
        vkCmdPushConstants(m_offscreenCmd, m_pipelineLayout,
                           VK_SHADER_STAGE_VERTEX_BIT | VK_SHADER_STAGE_FRAGMENT_BIT,
                           0, sizeof(push), &push);
        vkCmdDraw(m_offscreenCmd, static_cast<uint32_t>(m_vertices.size()), 1, 0, 0);
    }
    vkCmdEndRenderPass(m_offscreenCmd);
    vkEndCommandBuffer(m_offscreenCmd);

    VkSubmitInfo submit{VK_STRUCTURE_TYPE_SUBMIT_INFO};
    submit.commandBufferCount = 1;
    submit.pCommandBuffers = &m_offscreenCmd;
    vkResetFences(m_device, 1, &m_offscreenFence);
    vkQueueSubmit(m_queue, 1, &submit, m_offscreenFence);
    vkWaitForFences(m_device, 1, &m_offscreenFence, VK_TRUE, UINT64_MAX);
}

void CudaVulkanRenderNode::destroyHdrTarget()
{
    if (m_hdrFramebuffer) { vkDestroyFramebuffer(m_device, m_hdrFramebuffer, nullptr); m_hdrFramebuffer = VK_NULL_HANDLE; }
    if (m_hdrView) { vkDestroyImageView(m_device, m_hdrView, nullptr); m_hdrView = VK_NULL_HANDLE; }
    if (m_hdrImage) { vkDestroyImage(m_device, m_hdrImage, nullptr); m_hdrImage = VK_NULL_HANDLE; }
    if (m_hdrMemory) { vkFreeMemory(m_device, m_hdrMemory, nullptr); m_hdrMemory = VK_NULL_HANDLE; }
    m_hdrExtent = {0, 0};
}

void CudaVulkanRenderNode::destroyTonemap()
{
    if (m_tonemapPipeline) { vkDestroyPipeline(m_device, m_tonemapPipeline, nullptr); m_tonemapPipeline = VK_NULL_HANDLE; }
    if (m_tonemapLayout) { vkDestroyPipelineLayout(m_device, m_tonemapLayout, nullptr); m_tonemapLayout = VK_NULL_HANDLE; }
    if (m_tonemapVert) { vkDestroyShaderModule(m_device, m_tonemapVert, nullptr); m_tonemapVert = VK_NULL_HANDLE; }
    if (m_tonemapFrag) { vkDestroyShaderModule(m_device, m_tonemapFrag, nullptr); m_tonemapFrag = VK_NULL_HANDLE; }
    if (m_hdrSampler) { vkDestroySampler(m_device, m_hdrSampler, nullptr); m_hdrSampler = VK_NULL_HANDLE; }
    if (m_tonemapPool) { vkDestroyDescriptorPool(m_device, m_tonemapPool, nullptr); m_tonemapPool = VK_NULL_HANDLE; m_tonemapSet = VK_NULL_HANDLE; }
    if (m_tonemapSetLayout) { vkDestroyDescriptorSetLayout(m_device, m_tonemapSetLayout, nullptr); m_tonemapSetLayout = VK_NULL_HANDLE; }
}

uint32_t CudaVulkanRenderNode::findMemoryType(uint32_t typeBits,
                                             VkMemoryPropertyFlags required) const
{
    VkPhysicalDeviceMemoryProperties properties{};
    vkGetPhysicalDeviceMemoryProperties(m_physicalDevice, &properties);
    for (uint32_t index = 0; index < properties.memoryTypeCount; ++index) {
        if ((typeBits & (1U << index))
            && (properties.memoryTypes[index].propertyFlags & required) == required) {
            return index;
        }
    }
    return std::numeric_limits<uint32_t>::max();
}

bool CudaVulkanRenderNode::selectMatchingCudaDevice()
{
    VkPhysicalDeviceIDProperties idProperties{VK_STRUCTURE_TYPE_PHYSICAL_DEVICE_ID_PROPERTIES};
    VkPhysicalDeviceProperties2 properties{VK_STRUCTURE_TYPE_PHYSICAL_DEVICE_PROPERTIES_2};
    properties.pNext = &idProperties;
    vkGetPhysicalDeviceProperties2(m_physicalDevice, &properties);
    if (cuInit(0) != CUDA_SUCCESS) {
        m_lastStatus = QStringLiteral("cuInit failed");
        return false;
    }
    int count = 0;
    if (cuDeviceGetCount(&count) != CUDA_SUCCESS) {
        m_lastStatus = QStringLiteral("cuDeviceGetCount failed");
        return false;
    }
    for (int device = 0; device < count; ++device) {
        CUdevice cudaDevice = 0;
        CUuuid uuid{};
        if (cuDeviceGet(&cudaDevice, device) != CUDA_SUCCESS
            || cuDeviceGetUuid_v2(&uuid, cudaDevice) != CUDA_SUCCESS) {
            continue;
        }
        if (std::memcmp(uuid.bytes, idProperties.deviceUUID, VK_UUID_SIZE) == 0) {
            const cudaError_t error = cudaSetDevice(device);
            if (error != cudaSuccess) {
                m_lastStatus = cudaErrorMessage("cudaSetDevice", error);
                return false;
            }
            m_cudaDevice = device;
            return true;
        }
    }
    m_lastStatus = QStringLiteral("No CUDA device UUID matches Qt's Vulkan physical device");
    return false;
}

QString CudaVulkanRenderNode::cudaDeviceName() const
{
    if (m_cudaDevice < 0)
        return QStringLiteral("unknown CUDA device");
    CUdevice device = 0;
    char name[256]{};
    if (cuDeviceGet(&device, m_cudaDevice) == CUDA_SUCCESS
        && cuDeviceGetName(name, sizeof(name), device) == CUDA_SUCCESS) {
        return QString::fromLatin1(name);
    }
    return QStringLiteral("CUDA device %1").arg(m_cudaDevice);
}

bool CudaVulkanRenderNode::createInteropSemaphore()
{
    VkExportSemaphoreCreateInfo exportInfo{VK_STRUCTURE_TYPE_EXPORT_SEMAPHORE_CREATE_INFO};
    exportInfo.handleTypes = VK_EXTERNAL_SEMAPHORE_HANDLE_TYPE_OPAQUE_FD_BIT;
    VkSemaphoreCreateInfo createInfo{VK_STRUCTURE_TYPE_SEMAPHORE_CREATE_INFO};
    createInfo.pNext = &exportInfo;
    if (vkCreateSemaphore(m_device, &createInfo, nullptr, &m_cudaReadySemaphore) != VK_SUCCESS) {
        m_lastStatus = QStringLiteral("vkCreateSemaphore(external) failed");
        return false;
    }
    auto getFd = reinterpret_cast<PFN_vkGetSemaphoreFdKHR>(
        vkGetDeviceProcAddr(m_device, "vkGetSemaphoreFdKHR"));
    if (!getFd) {
        m_lastStatus = QStringLiteral("vkGetSemaphoreFdKHR is unavailable");
        return false;
    }
    VkSemaphoreGetFdInfoKHR fdInfo{VK_STRUCTURE_TYPE_SEMAPHORE_GET_FD_INFO_KHR};
    fdInfo.semaphore = m_cudaReadySemaphore;
    fdInfo.handleType = VK_EXTERNAL_SEMAPHORE_HANDLE_TYPE_OPAQUE_FD_BIT;
    int fd = -1;
    if (getFd(m_device, &fdInfo, &fd) != VK_SUCCESS || fd < 0) {
        m_lastStatus = QStringLiteral("vkGetSemaphoreFdKHR failed");
        return false;
    }
    cudaExternalSemaphoreHandleDesc descriptor{};
    descriptor.type = cudaExternalSemaphoreHandleTypeOpaqueFd;
    descriptor.handle.fd = fd;
    const cudaError_t error = cudaImportExternalSemaphore(&m_cudaExternalSemaphore,
                                                          &descriptor);
    if (error != cudaSuccess) {
        ::close(fd);
        m_lastStatus = cudaErrorMessage("cudaImportExternalSemaphore", error);
        return false;
    }
    return true;
}

bool CudaVulkanRenderNode::createCudaVulkanBuffer(VkDeviceSize capacity)
{
    if (!selectMatchingCudaDevice())
        return false;

    VkPhysicalDeviceExternalBufferInfo externalInfo{VK_STRUCTURE_TYPE_PHYSICAL_DEVICE_EXTERNAL_BUFFER_INFO};
    externalInfo.usage = VK_BUFFER_USAGE_VERTEX_BUFFER_BIT;
    externalInfo.handleType = VK_EXTERNAL_MEMORY_HANDLE_TYPE_OPAQUE_FD_BIT;
    VkExternalBufferProperties externalProperties{VK_STRUCTURE_TYPE_EXTERNAL_BUFFER_PROPERTIES};
    vkGetPhysicalDeviceExternalBufferProperties(m_physicalDevice, &externalInfo,
                                                &externalProperties);
    const VkExternalMemoryFeatureFlags requiredFeatures =
        VK_EXTERNAL_MEMORY_FEATURE_EXPORTABLE_BIT | VK_EXTERNAL_MEMORY_FEATURE_IMPORTABLE_BIT;
    if ((externalProperties.externalMemoryProperties.externalMemoryFeatures & requiredFeatures)
        != requiredFeatures) {
        m_lastStatus = QStringLiteral("Vulkan vertex buffers do not support importable/exportable OPAQUE_FD memory");
        return false;
    }

    VkExternalMemoryBufferCreateInfo externalBuffer{VK_STRUCTURE_TYPE_EXTERNAL_MEMORY_BUFFER_CREATE_INFO};
    externalBuffer.handleTypes = VK_EXTERNAL_MEMORY_HANDLE_TYPE_OPAQUE_FD_BIT;
    VkBufferCreateInfo bufferInfo{VK_STRUCTURE_TYPE_BUFFER_CREATE_INFO};
    bufferInfo.pNext = &externalBuffer;
    bufferInfo.size = capacity;
    bufferInfo.usage = VK_BUFFER_USAGE_VERTEX_BUFFER_BIT;
    bufferInfo.sharingMode = VK_SHARING_MODE_EXCLUSIVE;
    if (vkCreateBuffer(m_device, &bufferInfo, nullptr, &m_buffer) != VK_SUCCESS) {
        m_lastStatus = QStringLiteral("vkCreateBuffer(external) failed");
        return false;
    }
    VkMemoryRequirements requirements{};
    vkGetBufferMemoryRequirements(m_device, m_buffer, &requirements);
    const uint32_t memoryType = findMemoryType(requirements.memoryTypeBits,
                                               VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT);
    if (memoryType == std::numeric_limits<uint32_t>::max()) {
        m_lastStatus = QStringLiteral("No device-local Vulkan memory type is compatible with the external buffer");
        return false;
    }
    VkExportMemoryAllocateInfo exportMemory{VK_STRUCTURE_TYPE_EXPORT_MEMORY_ALLOCATE_INFO};
    exportMemory.handleTypes = VK_EXTERNAL_MEMORY_HANDLE_TYPE_OPAQUE_FD_BIT;
    VkMemoryAllocateInfo allocateInfo{VK_STRUCTURE_TYPE_MEMORY_ALLOCATE_INFO};
    allocateInfo.pNext = &exportMemory;
    allocateInfo.allocationSize = requirements.size;
    allocateInfo.memoryTypeIndex = memoryType;
    if (vkAllocateMemory(m_device, &allocateInfo, nullptr, &m_memory) != VK_SUCCESS
        || vkBindBufferMemory(m_device, m_buffer, m_memory, 0) != VK_SUCCESS) {
        m_lastStatus = QStringLiteral("Vulkan external buffer allocation/bind failed");
        return false;
    }
    auto getFd = reinterpret_cast<PFN_vkGetMemoryFdKHR>(
        vkGetDeviceProcAddr(m_device, "vkGetMemoryFdKHR"));
    if (!getFd) {
        m_lastStatus = QStringLiteral("vkGetMemoryFdKHR is unavailable");
        return false;
    }
    VkMemoryGetFdInfoKHR fdInfo{VK_STRUCTURE_TYPE_MEMORY_GET_FD_INFO_KHR};
    fdInfo.memory = m_memory;
    fdInfo.handleType = VK_EXTERNAL_MEMORY_HANDLE_TYPE_OPAQUE_FD_BIT;
    int fd = -1;
    if (getFd(m_device, &fdInfo, &fd) != VK_SUCCESS || fd < 0) {
        m_lastStatus = QStringLiteral("vkGetMemoryFdKHR failed");
        return false;
    }

    cudaExternalMemoryHandleDesc memoryDescriptor{};
    memoryDescriptor.type = cudaExternalMemoryHandleTypeOpaqueFd;
    memoryDescriptor.handle.fd = fd;
    memoryDescriptor.size = requirements.size;
    cudaError_t error = cudaImportExternalMemory(&m_cudaExternalMemory,
                                                 &memoryDescriptor);
    if (error != cudaSuccess) {
        ::close(fd);
        m_lastStatus = cudaErrorMessage("cudaImportExternalMemory", error);
        return false;
    }
    cudaExternalMemoryBufferDesc mapDescriptor{};
    mapDescriptor.offset = 0;
    mapDescriptor.size = capacity;
    error = cudaExternalMemoryGetMappedBuffer(&m_cudaPointer,
                                              m_cudaExternalMemory,
                                              &mapDescriptor);
    if (error != cudaSuccess) {
        m_lastStatus = cudaErrorMessage("cudaExternalMemoryGetMappedBuffer", error);
        return false;
    }
    error = cudaStreamCreateWithFlags(&m_cudaStream, cudaStreamNonBlocking);
    if (error != cudaSuccess) {
        m_lastStatus = cudaErrorMessage("cudaStreamCreateWithFlags", error);
        return false;
    }
    if (!createInteropSemaphore())
        return false;
    m_capacity = capacity;
    m_mode = BufferMode::CudaVulkan;
    return true;
}

bool CudaVulkanRenderNode::createCpuVulkanBuffer(VkDeviceSize capacity)
{
    VkBufferCreateInfo bufferInfo{VK_STRUCTURE_TYPE_BUFFER_CREATE_INFO};
    bufferInfo.size = capacity;
    bufferInfo.usage = VK_BUFFER_USAGE_VERTEX_BUFFER_BIT;
    bufferInfo.sharingMode = VK_SHARING_MODE_EXCLUSIVE;
    if (vkCreateBuffer(m_device, &bufferInfo, nullptr, &m_buffer) != VK_SUCCESS) {
        m_lastStatus = QStringLiteral("vkCreateBuffer(CPU fallback) failed");
        return false;
    }
    VkMemoryRequirements requirements{};
    vkGetBufferMemoryRequirements(m_device, m_buffer, &requirements);
    const uint32_t memoryType = findMemoryType(
        requirements.memoryTypeBits,
        VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT | VK_MEMORY_PROPERTY_HOST_COHERENT_BIT);
    if (memoryType == std::numeric_limits<uint32_t>::max()) {
        m_lastStatus = QStringLiteral("No coherent host-visible Vulkan memory type is available");
        return false;
    }
    VkMemoryAllocateInfo allocateInfo{VK_STRUCTURE_TYPE_MEMORY_ALLOCATE_INFO};
    allocateInfo.allocationSize = requirements.size;
    allocateInfo.memoryTypeIndex = memoryType;
    if (vkAllocateMemory(m_device, &allocateInfo, nullptr, &m_memory) != VK_SUCCESS
        || vkBindBufferMemory(m_device, m_buffer, m_memory, 0) != VK_SUCCESS
        || vkMapMemory(m_device, m_memory, 0, capacity, 0, &m_cpuMapped) != VK_SUCCESS) {
        m_lastStatus = QStringLiteral("CPU fallback allocation/map failed");
        return false;
    }
    m_capacity = capacity;
    m_mode = BufferMode::VulkanCpu;
    return true;
}

bool CudaVulkanRenderNode::ensureBuffer(VkDeviceSize requiredBytes)
{
    if (m_buffer && m_capacity >= requiredBytes)
        return true;
    destroyBuffer();
    const VkDeviceSize capacity = nextPowerOfTwo(std::max<VkDeviceSize>(requiredBytes, 1));
    if (createCudaVulkanBuffer(capacity)) {
        publishStatus(QStringLiteral("cuda-vulkan-zero-copy"),
                      QStringLiteral("CUDA/Vulkan shared external memory on %1; explicit semaphore handoff")
                          .arg(cudaDeviceName()));
        return true;
    }
    const QString cudaFailure = m_lastStatus;
    destroyBuffer();
    if (createCpuVulkanBuffer(capacity)) {
        publishStatus(QStringLiteral("vulkan-cpu-fallback"),
                      QStringLiteral("CUDA interop unavailable (%1); using coherent Vulkan upload buffer")
                          .arg(cudaFailure));
        return true;
    }
    publishStatus(QStringLiteral("unavailable"), m_lastStatus);
    return false;
}

bool CudaVulkanRenderNode::uploadPendingVertices()
{
    if (!m_verticesDirty)
        return true;
    const size_t bytes = static_cast<size_t>(m_vertices.size()) * sizeof(Vertex);
    if (!ensureBuffer(static_cast<VkDeviceSize>(std::max<size_t>(bytes, 1))))
        return false;
    if (m_queue)
        vkQueueWaitIdle(m_queue);
    if (bytes) {
        if (m_mode == BufferMode::CudaVulkan) {
            cudaError_t error = cudaMemcpyAsync(m_cudaPointer, m_vertices.constData(),
                                                bytes, cudaMemcpyHostToDevice,
                                                m_cudaStream);
            if (error != cudaSuccess) {
                m_lastStatus = cudaErrorMessage("cudaMemcpyAsync(shared vertex buffer)", error);
                publishStatus(QStringLiteral("unavailable"), m_lastStatus);
                return false;
            }
            cudaExternalSemaphoreSignalParams signalParameters{};
            error = cudaSignalExternalSemaphoresAsync(&m_cudaExternalSemaphore,
                                                      &signalParameters, 1,
                                                      m_cudaStream);
            if (error != cudaSuccess) {
                m_lastStatus = cudaErrorMessage("cudaSignalExternalSemaphoresAsync", error);
                publishStatus(QStringLiteral("unavailable"), m_lastStatus);
                return false;
            }
            const VkPipelineStageFlags waitStage = VK_PIPELINE_STAGE_VERTEX_INPUT_BIT;
            VkSubmitInfo waitSubmit{VK_STRUCTURE_TYPE_SUBMIT_INFO};
            waitSubmit.waitSemaphoreCount = 1;
            waitSubmit.pWaitSemaphores = &m_cudaReadySemaphore;
            waitSubmit.pWaitDstStageMask = &waitStage;
            if (vkQueueSubmit(m_queue, 1, &waitSubmit, VK_NULL_HANDLE) != VK_SUCCESS) {
                m_lastStatus = QStringLiteral("vkQueueSubmit(CUDA semaphore wait) failed");
                publishStatus(QStringLiteral("unavailable"), m_lastStatus);
                return false;
            }
        } else if (m_mode == BufferMode::VulkanCpu && m_cpuMapped) {
            std::memcpy(m_cpuMapped, m_vertices.constData(), bytes);
        }
    }
    m_verticesDirty = false;
    ++m_generation;
    if (m_mode == BufferMode::CudaVulkan) {
        publishStatus(QStringLiteral("cuda-vulkan-zero-copy"),
                      QStringLiteral("CUDA/Vulkan shared external memory on %1; generation %2")
                          .arg(cudaDeviceName())
                          .arg(m_generation));
    } else if (m_mode == BufferMode::VulkanCpu) {
        publishStatus(QStringLiteral("vulkan-cpu-fallback"),
                      QStringLiteral("Coherent Vulkan CPU upload buffer; generation %1")
                          .arg(m_generation));
    }
    return true;
}

void CudaVulkanRenderNode::prepare()
{
    if (!acquireVulkanContext())
        return;
    if (m_mode == BufferMode::Software)
        return;
    const qreal dpr = m_window ? m_window->effectiveDevicePixelRatio() : 1.0;
    const uint32_t width = static_cast<uint32_t>(std::max(1.0, m_size.width() * dpr));
    const uint32_t height = static_cast<uint32_t>(std::max(1.0, m_size.height() * dpr));
    if (!ensureHdrTarget(width, height) || !ensurePipeline() || !ensureTonemapPipeline()) {
        publishStatus(QStringLiteral("unavailable"), m_lastStatus);
        return;
    }
    uploadPendingVertices();
    updateTonemapDescriptor();
    // Render the glow flat into the HDR target (item resolution, no zoom/pan);
    // the tonemap pass then places it through Qt's scene matrix.
    QMatrix4x4 projection;
    projection.ortho(0.0F, static_cast<float>(width), 0.0F, static_cast<float>(height), -1.0F, 1.0F);
    recordOffscreen(projection);
}

void CudaVulkanRenderNode::render(const RenderState *state)
{
    if (m_mode == BufferMode::None)
        acquireVulkanContext();
    if (m_mode == BufferMode::Software) {
        if (!m_window)
            return;
        auto *renderer = m_window->rendererInterface();
        auto *painter = static_cast<QPainter *>(
            renderer->getResource(m_window, QSGRendererInterface::PainterResource));
        if (!painter)
            return;
        painter->save();
        painter->setOpacity(m_opacity);
        for (qsizetype index = 0; index + 1 < m_vertices.size(); index += 2) {
            const Vertex &a = m_vertices[index];
            const Vertex &b = m_vertices[index + 1];
            painter->setPen(QColor::fromRgbF(a.r, a.g, a.b, a.a));
            painter->drawLine(QPointF(a.x * m_size.width(), a.y * m_size.height()),
                              QPointF(b.x * m_size.width(), b.y * m_size.height()));
        }
        painter->restore();
        return;
    }
    if (!m_tonemapPipeline || !m_hdrImage || !m_window)
        return;
    auto *renderer = m_window->rendererInterface();
    void *command = renderer->getResource(m_window,
                                          QSGRendererInterface::CommandListResource);
    if (!command)
        return;
    const VkCommandBuffer commandBuffer = *static_cast<VkCommandBuffer *>(command);
    QMatrix4x4 transform;
    if (state && state->projectionMatrix())
        transform = *state->projectionMatrix();
    else if (projectionMatrix())
        transform = *projectionMatrix();
    if (matrix())
        transform *= *matrix();
    // Resolve the HDR glow: a tonemapped quad in item-local space, placed by the scene matrix.
    TonemapPush tp{};
    std::memcpy(tp.mvp, transform.constData(), sizeof(tp.mvp));
    tp.itemWidth = static_cast<float>(m_size.width());
    tp.itemHeight = static_cast<float>(m_size.height());
    tp.exposure = m_glowIntensity;  // the Glow slider now drives HDR exposure
    tp.pad = 0.0F;
    vkCmdBindPipeline(commandBuffer, VK_PIPELINE_BIND_POINT_GRAPHICS, m_tonemapPipeline);
    vkCmdBindDescriptorSets(commandBuffer, VK_PIPELINE_BIND_POINT_GRAPHICS,
                            m_tonemapLayout, 0, 1, &m_tonemapSet, 0, nullptr);
    vkCmdPushConstants(commandBuffer, m_tonemapLayout,
                       VK_SHADER_STAGE_VERTEX_BIT | VK_SHADER_STAGE_FRAGMENT_BIT,
                       0, sizeof(tp), &tp);
    vkCmdDraw(commandBuffer, 6, 1, 0, 0);
}

void CudaVulkanRenderNode::destroyPipeline()
{
    if (!m_device)
        return;
    if (m_pipeline)
        vkDestroyPipeline(m_device, m_pipeline, nullptr);
    if (m_pipelineLayout)
        vkDestroyPipelineLayout(m_device, m_pipelineLayout, nullptr);
    if (m_vertexShader)
        vkDestroyShaderModule(m_device, m_vertexShader, nullptr);
    if (m_fragmentShader)
        vkDestroyShaderModule(m_device, m_fragmentShader, nullptr);
    m_pipeline = VK_NULL_HANDLE;
    m_pipelineLayout = VK_NULL_HANDLE;
    m_vertexShader = VK_NULL_HANDLE;
    m_fragmentShader = VK_NULL_HANDLE;
}

void CudaVulkanRenderNode::destroyBuffer()
{
    if (m_queue)
        vkQueueWaitIdle(m_queue);
    if (m_cudaStream)
        cudaStreamSynchronize(m_cudaStream);
    if (m_cudaPointer)
        cudaFree(m_cudaPointer);
    if (m_cudaExternalMemory)
        cudaDestroyExternalMemory(m_cudaExternalMemory);
    if (m_cudaExternalSemaphore)
        cudaDestroyExternalSemaphore(m_cudaExternalSemaphore);
    if (m_cudaStream)
        cudaStreamDestroy(m_cudaStream);
    m_cudaPointer = nullptr;
    m_cudaExternalMemory = nullptr;
    m_cudaExternalSemaphore = nullptr;
    m_cudaStream = nullptr;
    m_cudaDevice = -1;
    if (m_cpuMapped && m_device && m_memory)
        vkUnmapMemory(m_device, m_memory);
    m_cpuMapped = nullptr;
    if (m_cudaReadySemaphore && m_device)
        vkDestroySemaphore(m_device, m_cudaReadySemaphore, nullptr);
    if (m_buffer && m_device)
        vkDestroyBuffer(m_device, m_buffer, nullptr);
    if (m_memory && m_device)
        vkFreeMemory(m_device, m_memory, nullptr);
    m_cudaReadySemaphore = VK_NULL_HANDLE;
    m_buffer = VK_NULL_HANDLE;
    m_memory = VK_NULL_HANDLE;
    m_capacity = 0;
    m_mode = BufferMode::None;
}

void CudaVulkanRenderNode::destroyAll()
{
    destroyBuffer();
    destroyPipeline();
    destroyTonemap();
    destroyHdrTarget();
    if (m_hdrRenderPass) { vkDestroyRenderPass(m_device, m_hdrRenderPass, nullptr); m_hdrRenderPass = VK_NULL_HANDLE; }
    if (m_offscreenFence) { vkDestroyFence(m_device, m_offscreenFence, nullptr); m_offscreenFence = VK_NULL_HANDLE; }
    if (m_offscreenPool) { vkDestroyCommandPool(m_device, m_offscreenPool, nullptr); m_offscreenPool = VK_NULL_HANDLE; m_offscreenCmd = VK_NULL_HANDLE; }
}

void CudaVulkanRenderNode::releaseResources()
{
    destroyAll();
    m_physicalDevice = VK_NULL_HANDLE;
    m_device = VK_NULL_HANDLE;
    m_queue = VK_NULL_HANDLE;
    m_renderPass = VK_NULL_HANDLE;
    m_verticesDirty = true;
}
