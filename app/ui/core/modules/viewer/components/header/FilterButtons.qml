import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../../../../../components" as C
import "../../../../../utils" as U


RowLayout {
    spacing: 0

    C.RoundButton {
        flat: true
        icon.source: Icon.get_icon("swap-vert.svg")

        C.CursorShape {cursorShape: Qt.PointingHandCursor}

        onClicked: {
            // Reverse the chapters order
            _data.chapters_data.reversed = !_data.chapters_data.reversed
            _chapters = _data.chapters_data.chapters  // Force the chapters to be reloaded
            _data.save(!_data.is_saved)
        }
    }
    C.RoundButton {
        flat: true
        icon.source: Icon.get_icon("filter-list.svg")

        Layout.rightMargin: 20
        C.CursorShape {cursorShape: Qt.PointingHandCursor}

        onClicked: {
            if (filterChapters.height == 0) {
                filterChapters.openAnimation.start()
            } else {
                filterChapters.closeAnimation.start()
            }
        }
    }
}
