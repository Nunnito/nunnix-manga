import QtQuick 2.15
import QtQuick.Controls 2.15

import "../../../../../../components" as C
import "../../../../../../utils/utils.js" as Utils

C.RoundButton {
    flat: true
    icon.source: Icon.get_icon("menu.svg")

    C.CursorShape {cursorShape: Qt.PointingHandCursor}
    onClicked: menu.open()

    Menu {
        id: menu

        C.MenuItem {
            id: menuCopyLink
            action: Action {
                id: reloadAction
                text: qsTr("Reload")
                shortcut: "F5"
                onTriggered: {
                    _data.reload(), _data = null, _chapters = null
                    listView.headerItem.filterChapters.height = 0
                    listView.headerItem.filterChapters.opacity = 0
                }
            }
        }

        C.MenuItem {
            id: reloadMenu
            action: Action {
                id: copyAction
                text: qsTr("Copy link")
                shortcut: "Ctrl+Shift+C"
                onTriggered: Utils.copy(_data.web_link)
            }
        }
    }
}
