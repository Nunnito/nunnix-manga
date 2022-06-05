import QtQuick 2.15
import QtQuick.Controls 2.15

import "components"


Item {
    property string name: "viewer"
    property var _data

    id: viewer

    Column {
        width: parent.width
        TopBar {id: topBar}

        ListView {
            width: parent.width
            height: parent.parent.height - topBar.height

            header: Header {}
        }
    }

    Shortcut {
        sequence: StandardKey.Cancel
        onActivated: {
            stackView.pop()
            sideBar.visible = true
        }
    }

    // Connections
    Connections {
        target: SignalHandler
        function onContentData(contentData) {
            _data = Cast.from_manga(contentData)
        }
    }

    Component.onCompleted: {sideBar.visible = false}
}
