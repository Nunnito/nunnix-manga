import QtQuick 2.15
import "../../../../components" as C

Column {
    property string parameter: modelData.parameter
    property int value: slider.value

    objectName: "slider"

    width: listView.width
    topPadding: modelData.topPadding ? modelData.topPadding : topPadding
    bottomPadding: modelData.bottomPadding ? modelData.bottomPadding : bottomPadding
    C.Label {
        width: parent.width
        text: modelData.name
        font.bold: true
        wrapMode: Text.WordWrap
    }
    Row {
        width: parent.width
        C.Slider {
            id: slider
            width: parent.width - 25
            stepSize: modelData.stepSize
            from: modelData.from
            to: modelData.to
        }
        C.Label {
            id: sliderLabel
            text: slider.value
            font.bold: true
            anchors.verticalCenter: slider.verticalCenter
        }
    }
}
