import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import Qt.labs.qmlmodels 1.0
import "advanced-search"
import "../../../../components" as C

import "../../../../utils" as U

Pane {
    property int _width: 300
    property alias openAnim: openAnim
    property alias closeAnim: closeAnim
    property alias controls: listView
    property bool open: width > 0

    id: advancedSearch

    x: parent.width - width

    leftPadding: 20
    rightPadding: 20
    topPadding: 15  // To center search label
    bottomPadding: 20

    Material.background: theme.advancedSearchBg
    SplitView.minimumWidth: item.width  // To animate the pane
    SplitView.preferredWidth: 0  // Initially hidden

    Column {
        width: _width - advancedSearch.leftPadding * 2
        height: parent.height
        spacing: 59

        C.Label {
            width: contentWidth
            text: qsTr("Advanced search")
            color: theme.windowAccent
            font.bold: true
            font.pixelSize: 14
            anchors.horizontalCenter: parent.horizontalCenter
            z: 1

            // Background to cover their siblings
            background: Pane {
                width: parent.parent.width + advancedSearch.leftPadding * 2
                height: 48  // Topbar height
                x: -(width - parent.width) / 2
                y: -advancedSearch.topPadding
                Material.elevation: 1
                Material.background: theme.advancedSearchSearchBg2
            }
        }
        // Here will be the advanced search
        ListView {
            id: listView
            bottomMargin: parent.spacing + advancedSearch.leftPadding
            width: parent.width
            height: parent.height - advancedSearchButtons.height - advancedSearch.leftPadding
            visible: width > 0
            spacing: 5
            model: Explorer.advanced_search
            delegate: chooser
            interactive: false
            boundsMovement: GridView.StopAtBounds
            U.WheelArea {}  // Custom scroll system
            cacheBuffer: count > 0 ? contentHeight: 0
            displayMarginBeginning: bottomMargin

            contentY: vsbar.position * contentHeight
        }
    }

    SearchButtons {id: advancedSearchButtons}

    C.ScrollBar {
        id: vsbar
        scrollBarItemBg: theme.advancedSearchScrollbarItemBg
        visible: advancedSearch.width == 300

        hoverEnabled: true
        active: hovered || pressed
        orientation: Qt.Vertical

        height: listView.height + 5
        x: parent.width + 4
        y: advancedSearch.leftPadding + advancedSearch.topPadding -1

        size: ((listView.height - (listView.bottomMargin)) / (listView.contentHeight))
        position: listView.count > 0 ? (listView.contentY) / (listView.contentHeight) : 0
    }

    DelegateChooser {
        id: chooser
        role: "type"
        DelegateChoice {roleValue: "textfield"; SearchTextField {}}
        DelegateChoice {roleValue: "combobox"; SearchComboBox {}}
        DelegateChoice {roleValue: "slider"; SearchSlider {}}
        DelegateChoice {roleValue: "checkbox"; SearchCheckBox {tristate: false}}
        DelegateChoice {roleValue: "tristate-checkbox"; SearchCheckBox {}}
        DelegateChoice {roleValue: "ascDescMap"; SearchAscDescMap {}}
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
