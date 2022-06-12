import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../../../../components" as C
import "top-bar"


C.TopBar {
    property alias tbStackView: tbStackView

    id: topBar

    StackView {
        id: tbStackView

        width: parent.width
        height: parent.height

        initialItem: Menu {}
    }

    Connections{
        target: _data ? _data.chapters_data : null

        function onSelectedLength(length) {
            if (tbStackView.currentItem.name == "selection" && length == 0) {
                topBar.tbStackView.pop()
            } else if (tbStackView.currentItem.name == "menu" && length > 0) {
                topBar.tbStackView.push("top-bar/Selection.qml")
            }
        }
    }
}
