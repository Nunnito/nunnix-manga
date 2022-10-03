import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import QtQuick.Layouts 1.15

import "../../../../../components" as C


Pane {
    property alias openAnimation: openAnimation
    property alias closeAnimation: closeAnimation

    id: filters

    width: parent.width
    height: 0

    leftPadding: 40
    opacity: 0
    clip: true

    Material.background: theme.sidebarBg


    Column {
        id: column

        topPadding: 5
        bottomPadding: 20

        // Search field
        C.Label {
            text: qsTr("Search")
            font.bold: true
            font.capitalization: Font.AllUppercase
        }
        C.TextField {
            placeholderText: qsTr("Search")
            outlined: true
            width: parent.parent.width / 2

            onTextEdited: viewer.filterSearch = text
        }

        // Filters
        C.Label {
            text: qsTr("View")
            font.bold: true
            font.capitalization: Font.AllUppercase
        }
        Row {
            C.CheckDelegate {
                text: qsTr("Downloaded")
                tristate: true
                boolTristate: true
                visible: false

                onCheckStateChanged: {
                    if (checkState == Qt.Checked) {
                        viewer.filterDownloaded = true
                    } else if (checkState == Qt.PartiallyChecked) {
                        viewer.filterDownloaded = false
                    } else {
                        viewer.filterDownloaded = null
                    }
                }
            }
            C.CheckDelegate {
                text: qsTr("Unread")
                tristate: true
                boolTristate: true

                onCheckStateChanged: {
                    if (checkState == Qt.Checked) {
                        viewer.filterUnread = true
                    } else if (checkState == Qt.PartiallyChecked) {
                        viewer.filterUnread = false
                    } else {
                        viewer.filterUnread = null
                    }
                }
            }
            C.CheckDelegate {
                text: qsTr("Bookmarked")
                tristate: true
                boolTristate: true

                onCheckStateChanged: {
                    if (checkState == Qt.Checked) {
                        viewer.filterBookmarked = true
                    } else if (checkState == Qt.PartiallyChecked) {
                        viewer.filterBookmarked = false
                    } else {
                        viewer.filterBookmarked = null
                    }
                }
            }
        }
    }


    // Open animation
    ParallelAnimation {
        id: openAnimation
        PropertyAnimation {
            target: filters
            property: "height"
            to: column.height
            easing.type: Easing.InQuart
            duration: 250
        }
        OpacityAnimator {
            target: filters
            from: 0
            to: 1
            easing.type: Easing.InQuart
            duration: 250
        }
    }
    
    // Close animation
    ParallelAnimation {
        id: closeAnimation
        PropertyAnimation {
            target: filters
            property: "height"
            to: 0
            easing.type: Easing.OutQuart
            duration: 250
        }
        OpacityAnimator {
            target: filters
            from: 1
            to: 0
            easing.type: Easing.OutQuart
            duration: 250
        }
    }
}
