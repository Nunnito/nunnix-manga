import QtQuick 2.15
import QtQuick.Controls 2.15

import "../../../components" as C
import "../../../utils" as U

import "components"


Item {
    property string name: "reader"
    id: reader


    Column {
        width: parent.width
        TopBar {id: topBar}
    }

    Shortcut {
        sequence: "Escape"
        enabled: stackView.currentItem.name == "reader"
        onActivated: {
            stackView.pop()
        }
    }
}
