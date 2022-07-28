import QtQuick 2.15
import QtQuick.Controls 2.15

import "../../../../../../components" as C

BaseButton {
    highlighted: true
    flat: true
    text: {
        // If selected chapters is equal to total chapters
        if (_data.chapters_data.selected_length == listView.count) {
            return qsTr("Unselect all")
        } else {
            return qsTr("Select all")
        }
    }

    C.CursorShape {cursorShape: Qt.PointingHandCursor}
    onClicked: {
        // If selected chapters is equal to total chapters
        if (_data.chapters_data.selected_length == listView.count) {
            _data.chapters_data.unselect_all()
        } else {
            _data.chapters_data.select_all()
        }
    }
}
