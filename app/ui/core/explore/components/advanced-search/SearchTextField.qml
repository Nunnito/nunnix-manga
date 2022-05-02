import QtQuick 2.15
import QtQuick.Controls 2.15
import "../../../../components" as C

Column {
    property string parameter: modelData.parameter
    property var value: textField.text

    objectName: "textField"

    width: listView.width
    topPadding: modelData.topPadding ? modelData.topPadding : topPadding
    bottomPadding: modelData.bottomPadding ? modelData.bottomPadding : bottomPadding
    C.Label {
        width: parent.width
        text: modelData.name
        font.bold: true
        wrapMode: Text.WordWrap
    }
    C.TextField {
        id: textField

        outlined: true
        width: parent.width
        placeholderText: modelData.name
    }
}
