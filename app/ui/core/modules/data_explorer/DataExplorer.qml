import QtQuick 2.15
import QtQuick.Controls 2.15

Item {
    property string name: "data_explorer"
    property var _data

    id: dataExplorer

    Rectangle {color: "yellow"; anchors.fill: parent}

    Shortcut {
        sequence: StandardKey.Cancel
        onActivated: stackView.pop()
    }

    // Connections
    Connections {
        target: SignalHandler
        function onContentData(contentData) {
            _data = Cast.from_manga(contentData)
        }
    }
}
