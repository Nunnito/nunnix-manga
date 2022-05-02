import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import "../../../../components" as C
import "../../../../utils" as U

Column {
    property bool tristate: modelData.type == "tristate-checkbox"
    property var parameter: modelData.parameter
    property var checkedParameter: modelData.checked_parameter
    property var uncheckedParameter: modelData.unchecked_parameter

    id: searchCheckBox
    objectName: tristate ? "tristate-checkBox" : "checkBox"

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
            property string parameter: {
                if (tristate) {
                    if (checkState == Qt.Checked) {
                        return searchCheckBox.checkedParameter
                    }
                    else if (checkState == Qt.PartiallyChecked) {
                        return searchCheckBox.uncheckedParameter
                    }
                    else {
                        return null
                    }
                }
                else {
                    if (checkState == Qt.Checked) {
                        return searchCheckBox.parameter
                    }
                    else {
                        return null
                    }   
                }
            }

            text: modelData.name
            width: listView.width
            tristate: searchCheckBox.tristate
            boolTristate: searchCheckBox.tristate
            nextCheckState: function() {
                if (checkState === Qt.Checked && tristate) {
                    return Qt.PartiallyChecked
                }
                else if (checkState === Qt.Unchecked) {
                    return Qt.Checked
                }
                else {
                    return Qt.Unchecked
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
