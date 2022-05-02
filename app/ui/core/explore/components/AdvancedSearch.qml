import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import Qt.labs.qmlmodels 1.0
import "advanced-search"
import "../../../components" as C

import "../../../utils" as U

Pane {
    property int _width: 300
    property alias openAnim: openAnim
    property alias closeAnim: closeAnim
    property bool open: width > 0

    x: parent.width - width
    padding: 20

    Material.background: theme.advancedSearchBg
    SplitView.minimumWidth: item.width  // To animate the pane
    SplitView.preferredWidth: 0  // Initially hidden

    Column {
        width: _width - 40
        height: parent.height
        spacing: 55

        C.Label {
            width: contentWidth
            text: qsTr("Advanced search")
            color: theme.windowAccent
            font.bold: true
            font.pixelSize: 14
            anchors.horizontalCenter: parent.horizontalCenter
        }
        // Here will be the advanced search
        ListView {
            id: listView
            bottomMargin: parent.spacing + 20
            width: parent.width
            height: parent.height
            visible: width > 0
            spacing: 10
            model: Explorer.advanced_search
            delegate: chooser
            interactive: false
            boundsMovement: GridView.StopAtBounds
            U.WheelArea {}  // Custom scroll system
        }
    }

    DelegateChooser {
        id: chooser
        role: "type"
        DelegateChoice {roleValue: "textfield"; SearchTextField {}}
        DelegateChoice {roleValue: "combobox"; SearchComboBox {}}
        DelegateChoice {roleValue: "slider"; SearchSlider {}}
        DelegateChoice {roleValue: "checkbox"; SearchCheckBox {tristate: false}}
        DelegateChoice {roleValue: "tristate-checkbox"; SearchCheckBox {}}
        DelegateChoice {roleValue: "separator"; SearchSeparator {}}
        DelegateChoice {roleValue: "label"; SearchLabel {}}
    }

    Item {id: item; width: 0}  // To animate the pane

    // Open and close animations
    PropertyAnimation {
        id: openAnim
        target: item
        properties: "width"
        duration: 500
        to: _width
        easing.type: Easing.OutQuint
    }
    PropertyAnimation {
        id: closeAnim
        target: item
        properties: "width"
        duration: 500
        to: 0
        easing.type: Easing.OutQuint
    }
}
