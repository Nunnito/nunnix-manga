import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../../../../components" as C
import "top-bar"

C.TopBar {
    RowLayout {
        anchors.verticalCenter: parent.verticalCenter
        width: parent.width
        spacing: 0

        RowLayout {
            Layout.leftMargin: parent.width / 2 - width / 2
            spacing: 8

            NextPageButton {}
            CurrentPageLabel {}
            PreviousPageButton {}
        }
        RowLayout {
            Layout.alignment: Qt.AlignRight
            Layout.rightMargin: 8
            spacing: 8

            ZoomOutButton {}
            SizeComboBox {}
            ZoomInButton {}
        }
    }
}
