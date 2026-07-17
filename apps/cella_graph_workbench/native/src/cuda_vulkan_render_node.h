#pragma once

#include <QColor>
#include <QElapsedTimer>
#include <QMatrix4x4>
#include <QPointer>
#include <QRectF>
#include <QSGRenderNode>
#include <QSizeF>
#include <QVariantList>
#include <QVector>

#include <cuda_runtime_api.h>
#include <vulkan/vulkan.h>

class CudaVulkanGraphItem;
class QQuickWindow;

class CudaVulkanRenderNode final : public QSGRenderNode
{
public:
    CudaVulkanRenderNode(QQuickWindow *window, CudaVulkanGraphItem *item);
    ~CudaVulkanRenderNode() override;

    void sync(const QVariantList &nodes, const QVariantList &edges,
              const QSizeF &size, qreal opacity,
              float lineWidth, float glowIntensity, float flowSpeed, float flowAmount);

    void prepare() override;
    void render(const RenderState *state) override;
    void releaseResources() override;
    QRectF rect() const override { return QRectF(QPointF(0, 0), m_size); }
    RenderingFlags flags() const override { return BoundedRectRendering; }
    StateFlags changedStates() const override { return {}; }

private:
    struct Vertex {
        float x;
        float y;
        float dirX;
        float dirY;
        float side;
        float along;
        float r;
        float g;
        float b;
        float a;
    };

    struct PushConstants {
        float mvp[16];
        float itemWidth;
        float itemHeight;
        float opacity;
        float halfWidth;
        float time;
        float glowIntensity;
        float flowSpeed;
        float flowAmount;
    };

    struct TonemapPush {
        float mvp[16];
        float itemWidth;
        float itemHeight;
        float exposure;
        float pad;
    };

    enum class BufferMode { None, CudaVulkan, VulkanCpu, Software };

    void buildVertices(const QVariantList &nodes, const QVariantList &edges);
    void appendLine(float x1, float y1, float x2, float y2, const QColor &colour);
    void appendLine(float x1, float y1, float x2, float y2, const QColor &colourA, const QColor &colourB);
    void appendNode(float x, float y, float radiusX, float radiusY, const QColor &colour);
    bool acquireVulkanContext();
    bool ensurePipeline();
    bool ensureHdrTarget(uint32_t width, uint32_t height);
    bool ensureTonemapPipeline();
    void updateTonemapDescriptor();
    void recordOffscreen(const QMatrix4x4 &projection);
    void destroyHdrTarget();
    void destroyTonemap();
    bool ensureBuffer(VkDeviceSize requiredBytes);
    bool createCudaVulkanBuffer(VkDeviceSize capacity);
    bool createCpuVulkanBuffer(VkDeviceSize capacity);
    bool createInteropSemaphore();
    bool selectMatchingCudaDevice();
    QString cudaDeviceName() const;
    bool uploadPendingVertices();
    uint32_t findMemoryType(uint32_t typeBits, VkMemoryPropertyFlags required) const;
    void destroyBuffer();
    void destroyPipeline();
    void destroyAll();
    void publishStatus(const QString &mode, const QString &message);
    QString cudaErrorMessage(const char *operation, cudaError_t error) const;
    QByteArray loadShader(const QString &path) const;

    QQuickWindow *m_window = nullptr;
    QPointer<CudaVulkanGraphItem> m_item;
    QSizeF m_size;
    qreal m_opacity = 1.0;
    float m_lineWidth = 2.5F;
    float m_glowIntensity = 1.35F;
    float m_flowSpeed = 0.0F;
    float m_flowAmount = 0.0F;
    QElapsedTimer m_clock;
    QVector<Vertex> m_vertices;
    bool m_verticesDirty = true;
    qulonglong m_generation = 0;

    VkPhysicalDevice m_physicalDevice = VK_NULL_HANDLE;
    VkDevice m_device = VK_NULL_HANDLE;
    VkQueue m_queue = VK_NULL_HANDLE;
    VkRenderPass m_renderPass = VK_NULL_HANDLE;
    VkBuffer m_buffer = VK_NULL_HANDLE;
    VkDeviceMemory m_memory = VK_NULL_HANDLE;
    VkDeviceSize m_capacity = 0;
    void *m_cpuMapped = nullptr;
    VkSemaphore m_cudaReadySemaphore = VK_NULL_HANDLE;

    VkPipelineLayout m_pipelineLayout = VK_NULL_HANDLE;
    VkPipeline m_pipeline = VK_NULL_HANDLE;  // glow pipeline, renders into the HDR target
    VkShaderModule m_vertexShader = VK_NULL_HANDLE;
    VkShaderModule m_fragmentShader = VK_NULL_HANDLE;

    // HDR bloom: offscreen float target + tonemap resolve into Qt's pass
    VkRenderPass m_hdrRenderPass = VK_NULL_HANDLE;
    VkImage m_hdrImage = VK_NULL_HANDLE;
    VkDeviceMemory m_hdrMemory = VK_NULL_HANDLE;
    VkImageView m_hdrView = VK_NULL_HANDLE;
    VkFramebuffer m_hdrFramebuffer = VK_NULL_HANDLE;
    VkExtent2D m_hdrExtent{0, 0};
    VkPipeline m_tonemapPipeline = VK_NULL_HANDLE;
    VkPipelineLayout m_tonemapLayout = VK_NULL_HANDLE;
    VkShaderModule m_tonemapVert = VK_NULL_HANDLE;
    VkShaderModule m_tonemapFrag = VK_NULL_HANDLE;
    VkDescriptorSetLayout m_tonemapSetLayout = VK_NULL_HANDLE;
    VkDescriptorPool m_tonemapPool = VK_NULL_HANDLE;
    VkDescriptorSet m_tonemapSet = VK_NULL_HANDLE;
    VkSampler m_hdrSampler = VK_NULL_HANDLE;
    VkCommandPool m_offscreenPool = VK_NULL_HANDLE;
    VkCommandBuffer m_offscreenCmd = VK_NULL_HANDLE;
    VkFence m_offscreenFence = VK_NULL_HANDLE;

    cudaExternalMemory_t m_cudaExternalMemory = nullptr;
    cudaExternalSemaphore_t m_cudaExternalSemaphore = nullptr;
    void *m_cudaPointer = nullptr;
    cudaStream_t m_cudaStream = nullptr;
    int m_cudaDevice = -1;

    BufferMode m_mode = BufferMode::None;
    QString m_lastStatus;
};
