import QtQuick 2.15
import QtQuick.Controls 2.15

import "components"
import "../../../components" as C
import "../../../utils" as U


Item {
    property string name: "viewer"
    property var _data

    id: viewer

    Column {
        width: parent.width
        TopBar {id: topBar}

        ListView {
            id: listView

            width: parent.width
            height: parent.parent.height - topBar.height

            header: Header {}
            clip: true

            boundsMovement: Flickable.StopAtBounds
            interactive: false

            model: _data ? _data.chapters_data.chapters : []
            delegate: Chapters {}

            ScrollBar.vertical: C.ScrollBar {}
            U.WheelArea {}
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
            _data = Viewer.from_manga(contentData)
            _data.save_to_cache()  // Save to cache for later use
        }
    }

    Component.onCompleted: {sideBar.visible = false}
}
