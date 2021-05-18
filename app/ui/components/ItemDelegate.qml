import QtQuick 2.15
import QtQuick.Templates 2.15 as T
import QtQuick.Controls 2.15
import QtQuick.Controls.impl 2.15
import QtQuick.Controls.Material 2.15
import QtQuick.Controls.Material.impl 2.15

T.ItemDelegate {
    id: control

    // Added properties
    property string colorBg: theme.controlBg
    property string colorFg: Material.foreground
    property string colorBgOver: theme.controlBgOver
    property string colorFgOver: theme.controlFgOver

    property alias firstIcon: firstIcon
    property alias secondIcon: secondIcon

    implicitWidth: Math.max(implicitBackgroundWidth + leftInset + rightInset,
                            implicitContentWidth + leftPadding + rightPadding)
    implicitHeight: Math.max(implicitBackgroundHeight + topInset + bottomInset,
                             implicitContentHeight + topPadding + bottomPadding,
                             implicitIndicatorHeight + topPadding + bottomPadding)

    padding: 16
    verticalPadding: 8
    spacing: 16

    icon.width: 24
    icon.height: 24
    icon.color: enabled ? (control.hovered ? colorFgOver : colorFg) : Material.hintTextColor

    contentItem: IconLabel {
        id: firstIcon
        spacing: control.spacing
        mirrored: control.mirrored
        display: control.display
        alignment: control.display === IconLabel.IconOnly || control.display === IconLabel.TextUnderIcon ? Qt.AlignCenter : Qt.AlignLeft

        icon.width: control.icon.width
        icon.height: control.icon.height
        icon.color: control.icon.color
        text: control.text
        font: control.font
        color: control.enabled ? colorFgOver : control.Material.hintTextColor
    }

    background: Rectangle {
        implicitHeight: control.Material.delegateHeight

        color: control.highlighted ? colorBg : "transparent"

        Ripple {
            width: parent.width
            height: parent.height

            clip: visible
            pressed: control.pressed
            anchor: control
            active: control.down || control.visualFocus || control.hovered
            color: colorBgOver
        }
    }


    // Fade-in transition animation
    IconLabel {
        id: secondIcon
        spacing: control.spacing
        mirrored: control.mirrored
        display: control.display

        icon.width: control.icon.width
        icon.height: control.icon.height
        icon.color: control.icon.color
        text: control.text
        font: control.font
        color: control.enabled ? (control.hovered ? colorFgOver : colorFg) : control.Material.hintTextColor

        anchors.centerIn: parent
        opacity: 0
    }

    ParallelAnimation {
        running: highlighted
        OpacityAnimator {target: secondIcon; from: 0; to: 1; duration: 200}
        OpacityAnimator {target: firstIcon; from: 1; to: 0; duration: 200}
    }

    ParallelAnimation {
        running: !highlighted
        OpacityAnimator {target: secondIcon; from: 1; to: 0; duration: 200}
        OpacityAnimator {target: firstIcon; from: 0; to: 1; duration: 200}
    }
}
