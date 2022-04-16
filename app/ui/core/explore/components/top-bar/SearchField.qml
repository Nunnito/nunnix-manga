import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../../../../components" as C


C.TextField {
    Layout.fillWidth: true
    Layout.leftMargin: 20
    Layout.rightMargin: 20

    placeholderText: qsTr("Search")
}
