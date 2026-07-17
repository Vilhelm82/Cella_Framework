import QtQuick
import QtQuick.Controls

Popup {
    id: root

    property Item anchorItem
    property bool alignRight: false
    property int edgeMargin: 10
    property int anchorGap: 5

    modal: false
    closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside

    function reposition() {
        if (!root.parent || !root.anchorItem)
            return

        const anchorPosition = root.anchorItem.mapToItem(root.parent, 0, 0)
        const maximumX = Math.max(root.edgeMargin,
                                  root.parent.width - root.width - root.edgeMargin)
        const preferredX = root.alignRight
                ? anchorPosition.x + root.anchorItem.width - root.width
                : anchorPosition.x
        root.x = Math.max(root.edgeMargin, Math.min(preferredX, maximumX))

        const below = anchorPosition.y + root.anchorItem.height + root.anchorGap
        const maximumY = Math.max(root.edgeMargin,
                                  root.parent.height - root.height - root.edgeMargin)
        const above = anchorPosition.y - root.height - root.anchorGap
        root.y = below + root.height <= root.parent.height - root.edgeMargin
                ? below
                : Math.max(root.edgeMargin, Math.min(above, maximumY))
    }

    onAboutToShow: Qt.callLater(reposition)
    onOpened: reposition()
    onWidthChanged: if (opened) Qt.callLater(reposition)
    onHeightChanged: if (opened) Qt.callLater(reposition)

    Connections {
        target: root.parent
        ignoreUnknownSignals: true
        function onWidthChanged() { if (root.opened) Qt.callLater(root.reposition) }
        function onHeightChanged() { if (root.opened) Qt.callLater(root.reposition) }
    }
}
