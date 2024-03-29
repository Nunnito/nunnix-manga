import QtQuick 2.15
import QtQuick.Controls 2.15
import "../../../../components" as C
import "../../../../utils/utils.js" as Utils

Menu {
    // Bookmark/unbookmark chapter
    C.MenuItem {
        id: bookmark
        text: modelData.bookmarked ? qsTr("Unbookmark") : qsTr("Bookmark")
        onTriggered: {
            modelData.bookmarked = !modelData.bookmarked
             _data.is_saved ? _data.save(false) : _data.save(true)
        }
    }
    // Mark chapter as read/unread
    C.MenuItem {
        id: markAsRead
        text: modelData.read ? qsTr("Mark as unread") : qsTr("Mark as read")
        onTriggered: {
            modelData.read = !modelData.read
             _data.is_saved ? _data.save(false) : _data.save(true)
        }
    }

    C.MenuSeparator {}

    C.MenuItem {
        id: select
        text: modelData.selected ? qsTr("Deselect") : qsTr("Select")
        onTriggered: modelData.selected = !modelData.selected
            
    }
    // Copy chapter link
    C.MenuItem {
        id: copyLink
        text: qsTr("Copy chapter link")
        onTriggered: Utils.copy(modelData.link)
    }
    // Mark all previous chapters as read
    C.MenuItem {
        id: previousAsRead
        text: qsTr("Mark previous as read")
        onTriggered: {
            _data.chapters_data.mark_previous_as_read(index)
            _data.is_saved ? _data.save(false) : _data.save(true)
        }
    }


    onClosed: parent.active = false
    Component.onCompleted: popup()
}
