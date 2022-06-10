import QtQuick 2.15
import QtQuick.Controls 2.15

import "../../../../../../components" as C

C.Button {
    contentItem: C.Label {
        text: parent.text  
        color: parent.highlighted && !parent.flat ? theme.controlBg : theme.windowAccent 
        font.bold: true
        font.capitalization: Font.AllUppercase
    }
}
