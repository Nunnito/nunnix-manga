import QtQuick 2.15
import QtQuick.Controls 2.15

import "../../../../../../components" as C

BaseButton {
    highlighted: true
    text: {
        if (allSelectedAreReaded()) {
            return qsTr("Mark as unread")
        } else {
            return qsTr("Mark as read")
        }
    }

    C.CursorShape {cursorShape: Qt.PointingHandCursor}

    onClicked: {
        if (allSelectedAreReaded()) {
            _data.chapters_data.unmark_selected_as_readed()
        } else {
            _data.chapters_data.mark_selected_as_readed()
        }

        _data.is_saved ? _data.save(false) : _data.save(true)
    }


    function allSelectedAreReaded() {
        let chapters = _data.chapters_data.chapters
        for (let i = 0; i < chapters.length; i++) {
            if (!chapters[i].readed && chapters[i].selected) {
                return false
            }
        }
        return true
    }
}
