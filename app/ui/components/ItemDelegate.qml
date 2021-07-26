/****************************************************************************
**
** Copyright (C) 2017 The Qt Company Ltd.
** Contact: http://www.qt.io/licensing/
**
** This file is part of the Qt Quick Controls 2 module of the Qt Toolkit.
**
** $QT_BEGIN_LICENSE:LGPL3$
** Commercial License Usage
** Licensees holding valid commercial Qt licenses may use this file in
** accordance with the commercial license agreement provided with the
** Software or, alternatively, in accordance with the terms contained in
** a written agreement between you and The Qt Company. For licensing terms
** and conditions see http://www.qt.io/terms-conditions. For further
** information use the contact form at http://www.qt.io/contact-us.
**
** GNU Lesser General Public License Usage
** Alternatively, this file may be used under the terms of the GNU Lesser
** General Public License version 3 as published by the Free Software
** Foundation and appearing in the file LICENSE.LGPLv3 included in the
** packaging of this file. Please review the following information to
** ensure the GNU Lesser General Public License version 3 requirements
** will be met: https://www.gnu.org/licenses/lgpl.html.
**
** GNU General Public License Usage
** Alternatively, this file may be used under the terms of the GNU
** General Public License version 2.0 or later as published by the Free
** Software Foundation and appearing in the file LICENSE.GPL included in
** the packaging of this file. Please review the following information to
** ensure the GNU General Public License version 2.0 requirements will be
** met: http://www.gnu.org/licenses/gpl-2.0.html.
**
** $QT_END_LICENSE$
**
****************************************************************************/

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
        color: control.enabled ? (control.hovered ? colorFgOver : colorFg) : control.Material.hintTextColor
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
