#include "cuda_vulkan_graph_item.h"
#include "cuda_vulkan_render_node.h"

#include <QHoverEvent>
#include <QMouseEvent>
#include <QQuickWindow>
#include <QtMath>

CudaVulkanGraphItem::CudaVulkanGraphItem(QQuickItem *parent)
    : QQuickItem(parent)
{
    setFlag(ItemHasContents, true);
    setAcceptedMouseButtons(Qt::LeftButton);
    setAcceptHoverEvents(true);
    m_animTimer = new QTimer(this);
    m_animTimer->setInterval(16);  // ~60 fps while flow animation is active
    connect(m_animTimer, &QTimer::timeout, this, [this]() { update(); });
}

void CudaVulkanGraphItem::setLineWidth(qreal value)
{
    m_lineWidth = static_cast<float>(value);
    emit effectsChanged();
    update();
}

void CudaVulkanGraphItem::setGlowIntensity(qreal value)
{
    m_glowIntensity = static_cast<float>(value);
    emit effectsChanged();
    update();
}

void CudaVulkanGraphItem::setFlowSpeed(qreal value)
{
    m_flowSpeed = static_cast<float>(value);
    emit effectsChanged();
    updateAnimation();
    update();
}

void CudaVulkanGraphItem::setFlowAmount(qreal value)
{
    m_flowAmount = static_cast<float>(value);
    emit effectsChanged();
    updateAnimation();
    update();
}

void CudaVulkanGraphItem::updateAnimation()
{
    const bool animate = m_flowAmount > 0.001F && m_flowSpeed > 0.001F;
    if (animate && !m_animTimer->isActive())
        m_animTimer->start();
    else if (!animate && m_animTimer->isActive())
        m_animTimer->stop();
}

void CudaVulkanGraphItem::setNodes(const QVariantList &nodes)
{
    if (m_nodes == nodes)
        return;
    m_nodes = nodes;
    emit nodesChanged();
    update();
}

void CudaVulkanGraphItem::setEdges(const QVariantList &edges)
{
    if (m_edges == edges)
        return;
    m_edges = edges;
    emit edgesChanged();
    update();
}

void CudaVulkanGraphItem::publishRendererStatus(const QString &mode,
                                                const QString &status,
                                                qulonglong bytes,
                                                qulonglong generation)
{
    if (m_renderMode == mode && m_interopStatus == status
        && m_sharedBytes == bytes && m_generation == generation) {
        return;
    }
    m_renderMode = mode;
    m_interopStatus = status;
    m_sharedBytes = bytes;
    m_generation = generation;
    emit rendererStatusChanged();
}

QSGNode *CudaVulkanGraphItem::updatePaintNode(QSGNode *oldNode,
                                               UpdatePaintNodeData *)
{
    auto *node = static_cast<CudaVulkanRenderNode *>(oldNode);
    if (!node)
        node = new CudaVulkanRenderNode(window(), this);
    node->sync(m_nodes, m_edges, QSizeF(width(), height()), opacity(),
               m_lineWidth, m_glowIntensity, m_flowSpeed, m_flowAmount);
    return node;
}

QVariantMap CudaVulkanGraphItem::nearestNode(const QPointF &position,
                                             qreal radius) const
{
    QVariantMap nearest;
    qreal bestDistance2 = radius * radius;
    for (const QVariant &value : m_nodes) {
        const QVariantMap node = value.toMap();
        const QPointF candidate(node.value(QStringLiteral("x")).toDouble() * width(),
                                node.value(QStringLiteral("y")).toDouble() * height());
        const qreal dx = candidate.x() - position.x();
        const qreal dy = candidate.y() - position.y();
        const qreal distance2 = dx * dx + dy * dy;
        if (distance2 <= bestDistance2) {
            bestDistance2 = distance2;
            nearest = node;
        }
    }
    return nearest;
}

void CudaVulkanGraphItem::updateHoveredNode(const QPointF &position)
{
    const QVariantMap node = nearestNode(position, 18.0);
    const QString id = node.value(QStringLiteral("id")).toString();
    const QString label = node.value(QStringLiteral("label")).toString();
    if (id == m_hoveredNodeId && label == m_hoveredLabel)
        return;
    m_hoveredNodeId = id;
    m_hoveredLabel = label;
    emit hoveredNodeChanged();
}

void CudaVulkanGraphItem::mousePressEvent(QMouseEvent *event)
{
    const QVariantMap node = nearestNode(event->position(), 20.0);
    const QString id = node.value(QStringLiteral("id")).toString();
    if (!id.isEmpty()) {
        emit nodeClicked(id);
        event->accept();
        return;
    }
    event->ignore();
}

void CudaVulkanGraphItem::hoverMoveEvent(QHoverEvent *event)
{
    updateHoveredNode(event->position());
}

void CudaVulkanGraphItem::hoverLeaveEvent(QHoverEvent *)
{
    if (m_hoveredNodeId.isEmpty() && m_hoveredLabel.isEmpty())
        return;
    m_hoveredNodeId.clear();
    m_hoveredLabel.clear();
    emit hoveredNodeChanged();
}
