import QtQuick 2.15
import QtQuick.Controls 2.15

import "components"
import "components/exceptions"
import "../../../components" as C
import "../../../utils" as U


Item {
    property string name: "viewer"
    property var getData

    property bool completedAnims: false
    property var _data
    property var _chapters
    property var chapters: _chapters

    property bool connectionError: false
    property bool timeoutError: false
    property bool unknownError: false
    property string exceptionMessage: ""

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

            model: chapters ? chapters : []
            delegate: Chapters {}

            ScrollBar.vertical: C.ScrollBar {}
            U.WheelArea {}
        }
    }

    // Exceptions
    ConnectionError {}
    TimeOutError {}
    UnknownError {}

    Shortcut {
        sequence: "Escape"
        onActivated: {
            if (topBar.tbStackView.currentItem.name != "selection") {
                stackView.pop()
                sideBar.visible = true
            } else {
                topBar.tbStackView.pop()
                _data.chapters_data.unselect_all()
            }
        }
    }

    // Connections
    Connections {
        target: SignalHandler
        function onContentData(contentData) {
            if (contentData.is_exception) {
                let exceptionType = contentData.exception.type
                listView.visible = false

                connectionError = exceptionType == "connection_error"
                timeoutError = exceptionType == "timeout_error"
                unknownError = exceptionType == "unknown_error"
                exceptionMessage = contentData.exception.message
            }
            else {
                listView.visible = true
                completedAnims = false
                _data = Viewer.from_manga(contentData)
                _chapters = _data.chapters_data.chapters
                _data.save(true)  // Save to cache for later use
                if (_data.is_saved) {  // Save to manga folder if already exists
                    _data.save(false)
                }

                // Set exceptions to false
                connectionError = false
                timeoutError = false
                unknownError = false
            }
        }
    }

    Component.onCompleted: {sideBar.visible = false}
}
