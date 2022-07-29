import QtQuick 2.15
import QtQuick.Controls 2.15

import "../../../../../../components" as C

BaseButton {
    highlighted: true
    text: {
        if (allSelectedAreBookmarked()) {
            return qsTr("Unbookmark")
        } else {
            return qsTr("Bookmark")
        }
    }

    C.CursorShape {cursorShape: Qt.PointingHandCursor}

    onClicked: {
        if (allSelectedAreBookmarked()) {
            _data.chapters_data.unmark_selected_as_bookmarked()
        } else {
            _data.chapters_data.mark_selected_as_bookmarked()
        }

        _data.is_saved ? _data.save(false) : _data.save(true)
    }


    function allSelectedAreBookmarked() {
        let chapters = _data.chapters_data.chapters
        for (let i = 0; i < chapters.length; i++) {
            if (!chapters[i].bookmarked && chapters[i].selected) {
                return false
            }
        }
        return true
    }
}
