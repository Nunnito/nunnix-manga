import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import "../../../../components" as C
import "../../../../utils" as U

Column {
    property var ascParameter: modelData.asc_parameter
    property var descParameter: modelData.desc_parameter
    property var defaultParam: modelData.default

    id: ascDesc
    objectName: "ascDescMap"

    topPadding: modelData.topPadding ? modelData.topPadding : topPadding
    bottomPadding: modelData.bottomPadding ? modelData.bottomPadding : bottomPadding
    width: listView.width
    spacing: 6

    Row {
        id: rowLayout
        width: parent.width
        C.Label {
            id: label
            width: parent.width - expandIcon.width - 7
            text: modelData.name
            font.bold: true
            wrapMode: Text.WordWrap
            MouseArea {
                width: rowLayout.width
                height: parent.height
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor
                onClicked: {
                    if (!collapsibleListView.height) {
                        openAnimation.start()
                        }
                    else {
                        closeAnimation.start()
                    }
                }
            }
        }
        Image {
            id: expandIcon
            source: Icon.get_icon("expand.svg")
            U.ChangeColor {color: theme.windowFg}
        }
    }

    ListView {
        id: collapsibleListView
        width: parent.width
        height: 0
        model: modelData.content
        delegate: itemDelegate
        visible: height > 0
        cacheBuffer: count > 0 ? contentHeight: 0
    }

    Component {
        id: itemDelegate
        C.CheckDelegate {
            property var value: modelData.parameter
            property string parameter

            ButtonGroup.group: buttonsGroup

            text: modelData.name
            width: listView.width
            tristate: true

            // Never set the value to Qt.Unchecked
            nextCheckState: function() {
                if (checkState === Qt.Checked && tristate) {
                    return Qt.PartiallyChecked
                }
                else if (checkState === Qt.Unchecked) {
                    return Qt.Checked
                }
                else {
                    return Qt.Checked
                }
            }

            Component.onCompleted: {
                if (value == ascDesc.defaultParam) {
                    checked = true
                }
            }

            // This connection is to just change value property when button is clicked
            Connections {
                target: advancedSearchButtons.searchButton
                function onClicked() {
                    if (checkState == Qt.Checked) {
                        parameter = ascDesc.ascParameter
                    }
                    else if (checkState == Qt.PartiallyChecked) {
                        parameter = ascDesc.descParameter
                    }
                    else {
                        parameter = null
                    }
                }
            }
        }
    }

    ButtonGroup {
        id: buttonsGroup

        // This unchecks all buttons but the one that was clicked
        onClicked: {
            for (let i in buttons) {
                if (button != buttons[i]) {
                    buttons[i].checkState = Qt.Unchecked
                }
            }
        }
    }

    ParallelAnimation {
        id: openAnimation
        PropertyAnimation {
            target: collapsibleListView
            property: "height"
            to: collapsibleListView.contentHeight
            easing.type: Easing.InQuart
            duration: 250
        }
        OpacityAnimator {
            target: collapsibleListView
            from: 0
            to: 1
            easing.type: Easing.InQuart
            duration: 250
        }
        RotationAnimator {
            target: expandIcon
            from: 0
            to: 180
            duration: 100
            easing.type: Easing.InQuart
        }
    }
    ParallelAnimation {
        id: closeAnimation
        PropertyAnimation {
            target: collapsibleListView
            property: "height"
            to: 0
            easing.type: Easing.OutQuart
            duration: 250
        }
        OpacityAnimator {
            target: collapsibleListView
            from: 1
            to: 0
            easing.type: Easing.OutQuart
            duration: 250
        }
        RotationAnimator {
            target: expandIcon
            from: 180
            to: 0
            duration: 100
            easing.type: Easing.InQuart
        }
    }
}
