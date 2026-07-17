#include "cuda_vulkan_graph_item.h"

#include <QQmlExtensionPlugin>
#include <qqml.h>

class CellaGraphNativePlugin final : public QQmlExtensionPlugin
{
    Q_OBJECT
    Q_PLUGIN_METADATA(IID QQmlExtensionInterface_iid)

public:
    void registerTypes(const char *uri) override
    {
        Q_ASSERT(QString::fromLatin1(uri) == QStringLiteral("Cella.Graph.Native"));
        qmlRegisterType<CudaVulkanGraphItem>(uri, 1, 0, "CudaVulkanGraph");
    }
};

#include "plugin.moc"
