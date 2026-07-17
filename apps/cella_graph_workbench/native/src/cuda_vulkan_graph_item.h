#pragma once

#include <QQuickItem>
#include <QTimer>
#include <QVariantList>

class CudaVulkanGraphItem : public QQuickItem
{
    Q_OBJECT
    Q_PROPERTY(QVariantList nodes READ nodes WRITE setNodes NOTIFY nodesChanged)
    Q_PROPERTY(QVariantList edges READ edges WRITE setEdges NOTIFY edgesChanged)
    Q_PROPERTY(QString renderMode READ renderMode NOTIFY rendererStatusChanged)
    Q_PROPERTY(QString interopStatus READ interopStatus NOTIFY rendererStatusChanged)
    Q_PROPERTY(qulonglong sharedBytes READ sharedBytes NOTIFY rendererStatusChanged)
    Q_PROPERTY(qulonglong generation READ generation NOTIFY rendererStatusChanged)
    Q_PROPERTY(QString hoveredNodeId READ hoveredNodeId NOTIFY hoveredNodeChanged)
    Q_PROPERTY(QString hoveredLabel READ hoveredLabel NOTIFY hoveredNodeChanged)
    Q_PROPERTY(qreal lineWidth READ lineWidth WRITE setLineWidth NOTIFY effectsChanged)
    Q_PROPERTY(qreal glowIntensity READ glowIntensity WRITE setGlowIntensity NOTIFY effectsChanged)
    Q_PROPERTY(qreal flowSpeed READ flowSpeed WRITE setFlowSpeed NOTIFY effectsChanged)
    Q_PROPERTY(qreal flowAmount READ flowAmount WRITE setFlowAmount NOTIFY effectsChanged)

public:
    explicit CudaVulkanGraphItem(QQuickItem *parent = nullptr);

    QVariantList nodes() const { return m_nodes; }
    QVariantList edges() const { return m_edges; }
    void setNodes(const QVariantList &nodes);
    void setEdges(const QVariantList &edges);

    QString renderMode() const { return m_renderMode; }
    QString interopStatus() const { return m_interopStatus; }
    qulonglong sharedBytes() const { return m_sharedBytes; }
    qulonglong generation() const { return m_generation; }
    QString hoveredNodeId() const { return m_hoveredNodeId; }
    QString hoveredLabel() const { return m_hoveredLabel; }

    qreal lineWidth() const { return m_lineWidth; }
    qreal glowIntensity() const { return m_glowIntensity; }
    qreal flowSpeed() const { return m_flowSpeed; }
    qreal flowAmount() const { return m_flowAmount; }
    void setLineWidth(qreal value);
    void setGlowIntensity(qreal value);
    void setFlowSpeed(qreal value);
    void setFlowAmount(qreal value);

    void publishRendererStatus(const QString &mode, const QString &status,
                               qulonglong bytes, qulonglong generation);

signals:
    void nodesChanged();
    void edgesChanged();
    void rendererStatusChanged();
    void hoveredNodeChanged();
    void effectsChanged();
    void nodeClicked(const QString &nodeId);

protected:
    QSGNode *updatePaintNode(QSGNode *oldNode, UpdatePaintNodeData *) override;
    void mousePressEvent(QMouseEvent *event) override;
    void hoverMoveEvent(QHoverEvent *event) override;
    void hoverLeaveEvent(QHoverEvent *event) override;

private:
    void updateHoveredNode(const QPointF &position);
    QVariantMap nearestNode(const QPointF &position, qreal radius) const;
    void updateAnimation();

    QVariantList m_nodes;
    QVariantList m_edges;
    float m_lineWidth = 2.5F;
    float m_glowIntensity = 1.35F;
    float m_flowSpeed = 0.0F;
    float m_flowAmount = 0.0F;
    QTimer *m_animTimer = nullptr;
    QString m_renderMode = QStringLiteral("initializing");
    QString m_interopStatus = QStringLiteral("Waiting for the Qt scene graph");
    qulonglong m_sharedBytes = 0;
    qulonglong m_generation = 0;
    QString m_hoveredNodeId;
    QString m_hoveredLabel;
};
