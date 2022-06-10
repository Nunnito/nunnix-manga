import QtQuick 2.15
import QtQuick.Controls 2.15

import "../../../../../../components" as C

C.RoundButton {
    flat: true
    icon.source: {
        if (_data && _data.is_saved) {
            Icon.get_icon("bookmark_filled.svg")
        } else {
            Icon.get_icon("bookmark_outlined.svg")
        }
    }

    C.CursorShape {cursorShape: Qt.PointingHandCursor}
    C.ToolTip {label: qsTr("Save to library"); visible: hovered}

    onClicked: _data.is_saved ? _data.remove() : _data.save(false)
}
