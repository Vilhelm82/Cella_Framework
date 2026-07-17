pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs
import Cella.Graph.Native 1.0

ApplicationWindow {
    id: window
    width: 1500
    height: 920
    minimumWidth: 900
    minimumHeight: 620
    visible: false
    title: "Cella Graph Workbench"
    color: "#101419"

    palette.window: "#101419"
    palette.windowText: "#e5edf5"
    palette.base: "#161c23"
    palette.text: "#e5edf5"
    palette.button: "#26313d"
    palette.buttonText: "#e5edf5"
    palette.highlight: "#62d6a7"
    palette.highlightedText: "#0d1713"

    header: ToolBar {
        id: headerBar
        objectName: "headerBar"
        implicitHeight: headerGrid.implicitHeight + 16
        height: implicitHeight
        background: Rectangle { color: "#171d24"; border.color: "#2a3541" }

        contentItem: GridLayout {
            id: headerGrid
            objectName: "headerGrid"
            anchors.fill: parent
            anchors.margins: 8
            columns: window.width >= 1420 ? 2 : 1
            columnSpacing: 18
            rowSpacing: 7

            RowLayout {
                id: findControls
                Layout.fillWidth: true
                spacing: 8

                Label { text: "CELLA"; font.pixelSize: 19; font.bold: true; color: "#62d6a7" }
                Rectangle { Layout.preferredWidth: 1; Layout.preferredHeight: 34; color: "#34404c" }
                Label { text: "FIND"; color: "#7f91a3"; font.pixelSize: 10; font.bold: true }
                TextField {
                    id: searchField
                    Layout.fillWidth: true
                    Layout.minimumWidth: 190
                    Layout.preferredWidth: 270
                    placeholderText: "Search id, title, summary…"
                    onAccepted: workbench.applyFilters(text, typeBox.currentText, lifecycleBox.currentText)
                }
                ComboBox { id: typeBox; model: workbench.artifactTypes; Layout.preferredWidth: 150 }
                ComboBox { id: lifecycleBox; model: workbench.lifecycleStatuses; Layout.preferredWidth: 150 }
                Button {
                    text: "Filter"
                    onClicked: workbench.applyFilters(searchField.text, typeBox.currentText, lifecycleBox.currentText)
                }
            }

            RowLayout {
                id: layoutControls
                Layout.fillWidth: true
                spacing: 8

                Item { Layout.fillWidth: true }
                Label { text: "LAYOUT"; color: "#7f91a3"; font.pixelSize: 10; font.bold: true }
                Rectangle { Layout.preferredWidth: 1; Layout.preferredHeight: 34; color: "#34404c" }
                ComboBox { id: layoutBox; model: workbench.layoutNames; Layout.preferredWidth: 120 }
                ComboBox {
                    id: clusterKeyBox
                    visible: layoutBox.currentText === "clustered"
                    model: workbench.clusterKeys
                    textRole: "label"
                    valueRole: "key"
                    Layout.preferredWidth: 230
                    Component.onCompleted: { var i = indexOfValue("facets.subject"); if (i >= 0) currentIndex = i }
                }
                ComboBox {
                    id: backendBox
                    model: workbench.cudaAvailable ? ["auto", "cpu", "cuda"] : ["auto", "cpu"]
                    Layout.preferredWidth: 100
                }
                Button {
                    text: workbench.busy ? "Computing…" : "Compute"
                    enabled: !workbench.busy
                    onClicked: workbench.computeLayout(layoutBox.currentText, backendBox.currentText, false, clusterKeyBox.currentValue || "")
                }
                Button {
                    text: "Save view"
                    enabled: !workbench.busy
                    onClicked: workbench.computeLayout(layoutBox.currentText, backendBox.currentText, true, clusterKeyBox.currentValue || "")
                }
            }

            RowLayout {
                id: appearanceControls
                Layout.fillWidth: true
                Layout.columnSpan: headerGrid.columns
                spacing: 8

                Label { text: "APPEARANCE"; color: "#7f91a3"; font.pixelSize: 10; font.bold: true }
                Rectangle { Layout.preferredWidth: 1; Layout.preferredHeight: 28; color: "#34404c" }

                Button {
                    id: sourcesButton
                    text: "Sources ▾"
                    Layout.preferredWidth: 110
                    onClicked: sourcesPopup.opened ? sourcesPopup.close() : sourcesPopup.open()

                    EdgeSafePopup {
                        id: sourcesPopup
                        objectName: "sourcesPopup"
                        parent: Overlay.overlay
                        anchorItem: sourcesButton
                        width: Math.min(430, Math.max(280, parent ? parent.width - 20 : 430))
                        height: Math.min(
                                    Math.max(240, 100 + (workbench.sourceList ? workbench.sourceList.length : 0) * 30),
                                    parent ? parent.height - 20 : 560)
                        padding: 12
                        background: Rectangle { color: "#1b232c"; border.color: "#2a3541"; radius: 6 }

                        contentItem: ColumnLayout {
                            spacing: 8
                            Label { text: "SOURCES"; color: "#7f91a3"; font.bold: true }
                            ScrollView {
                                id: sourcesScroll
                                objectName: "sourcesScroll"
                                Layout.fillWidth: true
                                Layout.fillHeight: true
                                clip: true
                                ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
                                Column {
                                    id: sourceItems
                                    width: sourcesScroll.availableWidth
                                    spacing: 2
                                    Repeater {
                                        model: workbench.sourceList
                                        delegate: CheckBox {
                                            required property var modelData
                                            width: sourceItems.width
                                            text: modelData.label
                                            checked: modelData.enabled
                                            hoverEnabled: true
                                            font.pixelSize: 11
                                            onToggled: workbench.setSourceEnabled(modelData.id, checked)
                                            ToolTip.visible: hovered && implicitWidth > width
                                            ToolTip.text: modelData.label
                                        }
                                    }
                                }
                            }
                            Rectangle { Layout.fillWidth: true; Layout.preferredHeight: 1; color: "#2a3541" }
                            RowLayout {
                                Layout.fillWidth: true
                                spacing: 7
                                Button { text: "Show all"; onClicked: workbench.setAllSources(true) }
                                Button { text: "Hide all"; onClicked: workbench.setAllSources(false) }
                                Item { Layout.fillWidth: true }
                            }
                        }
                    }
                }

                Button {
                    id: colorsButton
                    text: "Colors ▾"
                    Layout.preferredWidth: 105
                    property string editingType: ""
                    onClicked: colorsPopup.opened ? colorsPopup.close() : colorsPopup.open()

                    EdgeSafePopup {
                        id: colorsPopup
                        objectName: "colorsPopup"
                        parent: Overlay.overlay
                        anchorItem: colorsButton
                        width: Math.min(340, Math.max(280, parent ? parent.width - 20 : 340))
                        height: Math.min(390, parent ? parent.height - 20 : 390)
                        padding: 12
                        background: Rectangle { color: "#1b232c"; border.color: "#2a3541"; radius: 6 }

                        contentItem: ScrollView {
                            clip: true
                            ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
                            ColumnLayout {
                                width: colorsPopup.availableWidth
                                spacing: 8
                                Label { text: "NODE COLOURS"; color: "#7f91a3"; font.bold: true }
                                Grid {
                                    columns: 2
                                    columnSpacing: 16
                                    rowSpacing: 7
                                    Repeater {
                                        model: workbench.typeColours
                                        delegate: Row {
                                            required property var modelData
                                            spacing: 7
                                            Rectangle {
                                                width: 18; height: 18; radius: 3
                                                color: modelData.colour
                                                border.color: "#e8f0f7"; border.width: 0.5
                                                MouseArea {
                                                    anchors.fill: parent
                                                    cursorShape: Qt.PointingHandCursor
                                                    onClicked: {
                                                        colorsButton.editingType = modelData.type
                                                        colourDialog.selectedColor = modelData.colour
                                                        colourDialog.open()
                                                    }
                                                }
                                            }
                                            Label { text: modelData.type; color: "#cdd8e2"; font.pixelSize: 11; anchors.verticalCenter: parent.verticalCenter }
                                        }
                                    }
                                }
                                Rectangle { Layout.fillWidth: true; Layout.preferredHeight: 1; color: "#2a3541" }
                                Button { text: "Reset defaults"; onClicked: workbench.resetColours() }
                            }
                        }
                    }
                }

                Button {
                    id: effectsButton
                    text: "Effects ▾"
                    Layout.preferredWidth: 100
                    onClicked: effectsPopup.opened ? effectsPopup.close() : effectsPopup.open()

                    EdgeSafePopup {
                        id: effectsPopup
                        objectName: "effectsPopup"
                        parent: Overlay.overlay
                        anchorItem: effectsButton
                        width: Math.min(290, Math.max(260, parent ? parent.width - 20 : 290))
                        height: Math.min(360, parent ? parent.height - 20 : 360)
                        padding: 12
                        background: Rectangle { color: "#1b232c"; border.color: "#2a3541"; radius: 6 }

                        contentItem: ScrollView {
                            clip: true
                            ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
                            ColumnLayout {
                                width: effectsPopup.availableWidth
                                spacing: 6
                                Label { text: "EFFECTS"; color: "#7f91a3"; font.bold: true }

                                Label { text: "Line width  " + nativeGraph.lineWidth.toFixed(1); color: "#cdd8e2"; font.pixelSize: 11 }
                                Slider { Layout.fillWidth: true; from: 0.5; to: 8.0; value: nativeGraph.lineWidth; onMoved: nativeGraph.lineWidth = value }

                                Label { text: "Glow  " + nativeGraph.glowIntensity.toFixed(2); color: "#cdd8e2"; font.pixelSize: 11 }
                                Slider { Layout.fillWidth: true; from: 0.0; to: 3.0; value: nativeGraph.glowIntensity; onMoved: nativeGraph.glowIntensity = value }

                                Label { text: "Flow amount  " + nativeGraph.flowAmount.toFixed(2); color: "#cdd8e2"; font.pixelSize: 11 }
                                Slider { Layout.fillWidth: true; from: 0.0; to: 1.0; value: nativeGraph.flowAmount; onMoved: nativeGraph.flowAmount = value }

                                Label { text: "Flow speed  " + nativeGraph.flowSpeed.toFixed(1); color: "#cdd8e2"; font.pixelSize: 11 }
                                Slider { Layout.fillWidth: true; from: 0.0; to: 6.0; value: nativeGraph.flowSpeed; onMoved: nativeGraph.flowSpeed = value }

                                Label { text: "Bundle  " + bundleSlider.value.toFixed(2); color: "#cdd8e2"; font.pixelSize: 11 }
                                Slider {
                                    id: bundleSlider
                                    Layout.fillWidth: true
                                    from: 0.0; to: 1.0
                                    value: workbench.bundleStrength
                                    onPressedChanged: if (!pressed) workbench.setBundleStrength(value)
                                }
                            }
                        }
                    }
                }
                Item { Layout.fillWidth: true }
            }
        }
    }

    footer: Rectangle {
        height: 34
        color: "#171d24"
        border.color: "#2a3541"
        RowLayout {
            anchors.fill: parent
            anchors.leftMargin: 12
            anchors.rightMargin: 12
            Label { text: workbench.statusText; Layout.fillWidth: true; elide: Text.ElideRight; color: "#b9c6d1" }
            Label { text: "CUDA: " + workbench.cudaLabel; color: workbench.cudaAvailable ? "#62d6a7" : "#ff9b75" }
            Label { text: "rev " + workbench.graphRevision.slice(7, 19); color: "#7f91a3" }
        }
    }

    SplitView {
        anchors.fill: parent
        orientation: Qt.Horizontal

        Rectangle {
            SplitView.preferredWidth: 270
            SplitView.minimumWidth: 210
            color: "#141a20"
            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 12
                Label { text: "VISIBLE ARTIFACTS"; color: "#7f91a3"; font.bold: true }
                ListView {
                    id: nodeList
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    clip: true
                    model: workbench.nodes
                    spacing: 4
                    delegate: Rectangle {
                        required property var modelData
                        width: nodeList.width
                        height: 56
                        radius: 5
                        color: modelData.affected ? "#3a2630" : "#1b232c"
                        border.color: modelData.colour
                        border.width: 1
                        Column {
                            anchors.fill: parent
                            anchors.margins: 7
                            spacing: 2
                            Text { width: parent.width; text: modelData.label; color: "#e4ebf1"; elide: Text.ElideRight; font.pixelSize: 12 }
                            Text { width: parent.width; text: modelData.type + " · " + modelData.lifecycle; color: modelData.colour; elide: Text.ElideRight; font.pixelSize: 10 }
                        }
                        MouseArea { anchors.fill: parent; onClicked: workbench.selectNode(modelData.id) }
                    }
                }
            }
        }

        Rectangle {
            id: viewport
            SplitView.fillWidth: true
            SplitView.fillHeight: true
            color: "#0d1217"
            clip: true

            Item {
                id: graphLayer
                x: 30
                y: 30
                width: viewport.width - 60
                height: viewport.height - 60
                transformOrigin: Item.Center
                property real zoom: 1.0
                property bool nativeActive: nativeGraph.renderMode !== "initializing" && nativeGraph.renderMode !== "unavailable"
                scale: zoom

                CudaVulkanGraph {
                    id: nativeGraph
                    objectName: "nativeGraph"
                    anchors.fill: parent
                    nodes: workbench.nodes
                    edges: workbench.edges
                    z: 2
                    onNodeClicked: function(nodeId) { workbench.selectNode(nodeId) }
                }

                Repeater {
                    model: graphLayer.nativeActive ? [] : workbench.edges
                    delegate: Rectangle {
                        required property var modelData
                        property real sx: 22 + modelData.x1 * Math.max(1, graphLayer.width - 44)
                        property real sy: 22 + modelData.y1 * Math.max(1, graphLayer.height - 44)
                        property real tx: 22 + modelData.x2 * Math.max(1, graphLayer.width - 44)
                        property real ty: 22 + modelData.y2 * Math.max(1, graphLayer.height - 44)
                        x: sx
                        y: sy
                        width: Math.sqrt(Math.pow(tx - sx, 2) + Math.pow(ty - sy, 2))
                        height: modelData.affected ? 2.5 : 1.2
                        color: modelData.affected ? "#ff657a" : "#40505f"
                        opacity: modelData.affected ? 0.95 : 0.62
                        transformOrigin: Item.Left
                        rotation: Math.atan2(ty - sy, tx - sx) * 180 / Math.PI
                    }
                }

                Repeater {
                    model: graphLayer.nativeActive ? [] : workbench.nodes
                    delegate: Item {
                        required property var modelData
                        x: 22 + modelData.x * Math.max(1, graphLayer.width - 44) - 8
                        y: 22 + modelData.y * Math.max(1, graphLayer.height - 44) - 8
                        width: 18
                        height: 18
                        z: 2
                        Rectangle {
                            anchors.centerIn: parent
                            width: modelData.affected ? 20 : 15
                            height: width
                            radius: width / 2
                            color: modelData.affected ? "#ff657a" : modelData.colour
                            border.color: "#e8f0f7"
                            border.width: modelData.tracked ? 2 : 0.7
                            scale: nodeMouse.containsMouse ? 1.35 : 1.0
                            Behavior on scale { NumberAnimation { duration: 90 } }
                        }
                        Rectangle {
                            visible: nodeMouse.containsMouse
                            x: 17; y: -12
                            width: Math.min(280, nodeLabel.implicitWidth + 14)
                            height: 28
                            radius: 4
                            color: "#202a34"
                            border.color: modelData.colour
                            z: 5
                            Text { id: nodeLabel; anchors.centerIn: parent; text: modelData.label; color: "#edf3f8"; font.pixelSize: 11 }
                        }
                        MouseArea {
                            id: nodeMouse
                            anchors.fill: parent
                            hoverEnabled: true
                            onClicked: workbench.selectNode(modelData.id)
                        }
                    }
                }

                DragHandler { target: graphLayer }
            }

            MouseArea {
                anchors.fill: parent
                acceptedButtons: Qt.NoButton
                onWheel: function(wheel) {
                    graphLayer.zoom = Math.max(0.35, Math.min(4.0, graphLayer.zoom * (wheel.angleDelta.y > 0 ? 1.12 : 0.89)))
                    wheel.accepted = true
                }
            }
            Row {
                anchors.left: parent.left
                anchors.bottom: parent.bottom
                anchors.margins: 12
                spacing: 7
                Button { text: "−"; onClicked: graphLayer.zoom = Math.max(0.35, graphLayer.zoom / 1.2) }
                Label { text: Math.round(graphLayer.zoom * 100) + "%"; anchors.verticalCenter: parent.verticalCenter; color: "#9bacbb" }
                Button { text: "+"; onClicked: graphLayer.zoom = Math.min(4.0, graphLayer.zoom * 1.2) }
                Button { text: "Fit"; onClicked: { graphLayer.zoom = 1.0; graphLayer.x = 30; graphLayer.y = 30 } }
            }
            Label {
                anchors.top: parent.top
                anchors.right: parent.right
                anchors.margins: 12
                text: nativeGraph.renderMode + " · " + Math.round(nativeGraph.sharedBytes / 1024) + " KiB · gen " + nativeGraph.generation
                color: nativeGraph.renderMode === "cuda-vulkan-zero-copy" ? "#62d6a7" : "#d7a65a"
                font.pixelSize: 10
            }
            ToolTip {
                visible: nativeGraph.hoveredLabel.length > 0
                text: nativeGraph.hoveredLabel
                delay: 250
            }
        }

        Rectangle {
            SplitView.preferredWidth: 355
            SplitView.minimumWidth: 290
            color: "#141a20"
            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 14
                spacing: 10
                Label { text: "ARTIFACT INSPECTOR"; color: "#7f91a3"; font.bold: true }
                Label {
                    Layout.fillWidth: true
                    text: workbench.selectedNode.label || "Select a graph node"
                    wrapMode: Text.WordWrap
                    font.pixelSize: 18
                    font.bold: true
                }
                Label { Layout.fillWidth: true; text: workbench.selectedNode.id || ""; color: "#62d6a7"; wrapMode: Text.WrapAnywhere; font.pixelSize: 11 }
                RowLayout {
                    visible: Boolean(workbench.selectedNode.id)
                    Label { text: (workbench.selectedNode.type || "") + " · " + (workbench.selectedNode.lifecycle_status || "") + " · claim " + (workbench.selectedNode.claim_status || "none"); Layout.fillWidth: true; wrapMode: Text.WordWrap; color: "#aebdca" }
                }
                RowLayout {
                    Button { text: "Impact closure"; enabled: Boolean(workbench.selectedNode.id); onClicked: workbench.impactSelected() }
                    Button { text: "Clear"; onClicked: workbench.clearImpact() }
                    Button { text: "Reveal"; enabled: Boolean(workbench.selectedNode.id); onClicked: workbench.revealSource() }
                    Button {
                        text: "Focus"
                        checkable: true
                        enabled: Boolean(workbench.selectedNode.id)
                        ToolTip.visible: hovered
                        ToolTip.text: "Isolate this node and its direct connections"
                        onToggled: workbench.setFocusEdges(checked)
                    }
                }
                ScrollView {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    clip: true
                    ColumnLayout {
                        width: 320
                        spacing: 11
                        Label { text: "SUMMARY"; visible: Boolean(workbench.selectedNode.id); color: "#7f91a3"; font.bold: true }
                        TextArea {
                            Layout.fillWidth: true
                            text: workbench.selectedNode.summary || ""
                            readOnly: true
                            wrapMode: TextEdit.WordWrap
                            background: Rectangle { color: "#1a222b"; radius: 5 }
                            visible: Boolean(workbench.selectedNode.id)
                        }
                        Label { text: "SOURCE BINDINGS"; visible: Boolean(workbench.selectedNode.id); color: "#7f91a3"; font.bold: true }
                        TextArea {
                            Layout.fillWidth: true
                            text: workbench.selectedNode.source_text || ""
                            readOnly: true
                            wrapMode: TextEdit.WrapAnywhere
                            background: Rectangle { color: "#1a222b"; radius: 5 }
                            visible: Boolean(workbench.selectedNode.id)
                        }
                        Label { text: "EXTERNAL IDS"; visible: Boolean(workbench.selectedNode.id); color: "#7f91a3"; font.bold: true }
                        TextArea {
                            Layout.fillWidth: true
                            text: workbench.selectedNode.external_text || ""
                            readOnly: true
                            wrapMode: TextEdit.WrapAnywhere
                            background: Rectangle { color: "#1a222b"; radius: 5 }
                            visible: Boolean(workbench.selectedNode.id)
                        }
                        Label { text: "LLM RETRIEVAL"; visible: Boolean(workbench.selectedNode.id); color: "#7f91a3"; font.bold: true }
                        TextArea {
                            Layout.fillWidth: true
                            text: workbench.selectedNode.retrieval_text || ""
                            readOnly: true
                            wrapMode: TextEdit.WrapAnywhere
                            background: Rectangle { color: "#1a222b"; radius: 5 }
                            visible: Boolean(workbench.selectedNode.id)
                        }
                    }
                }
            }
        }
    }

    ColorDialog {
        id: colourDialog
        title: "Colour for " + colorsButton.editingType
        onAccepted: workbench.setTypeColour(colorsButton.editingType, colourDialog.selectedColor)
    }
}
