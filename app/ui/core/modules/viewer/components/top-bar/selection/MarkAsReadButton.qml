import QtQuick 2.15
import QtQuick.Controls 2.15

import "../../../../../../components" as C

BaseButton {
    highlighted: true
    text: {
        if (allSelectedAreread()) {
            return qsTr("Mark as unread")
        } else {
            return qsTr("Mark as read")
        }
    }

    C.CursorShape {cursorShape: Qt.PointingHandCursor}

    onClicked: {
        if (allSelectedAreread()) {
            _data.chapters_data.unmark_selected_as_read()
        } else {
            _data.chapters_data.mark_selected_as_read()
        }

        _data.is_saved ? _data.save(false) : _data.save(true)
    }


    function allSelectedAreread() {
        let chapters = _data.chapters_data.chapters
        for (let i = 0; i < chapters.length; i++) {
            if (!chapters[i].read && chapters[i].selected) {
                return false
            }
        }
        return true
    }
}
