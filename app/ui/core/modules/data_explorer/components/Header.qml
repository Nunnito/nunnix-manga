import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../../../../components" as C
import "header" as H

Item {
    id: _header

    width: parent.width

    H.Background {id: background}
    Row {
        id: row

        padding: 40
        spacing: 20

        H.Image {id: image}
        Column {
            spacing: row.spacing

            H.Title {}
            Column {
                H.Author {}
                H.Status {}
            }
            H.Genres {}
            H.Description {}
        }
    }
}
