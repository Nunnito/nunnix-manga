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

T.RoundButton {
    id: control

    // Added properties
    property string colorBg: theme.controlBg
    property string colorFg: Material.foreground
    property string colorBgOver: theme.controlBgOver
    property string colorFgOver: theme.controlFgOver
    property string colorBgClick: theme.controlBgClick
    property string colorFgClick: theme.controlFgClick

    implicitWidth: Math.max(implicitBackgroundWidth + leftInset + rightInset,
                            implicitContentWidth + leftPadding + rightPadding)
    implicitHeight: Math.max(implicitBackgroundHeight + topInset + bottomInset,
                             implicitContentHeight + topPadding + bottomPadding)

    topInset: 6
    leftInset: 6
    rightInset: 6
    bottomInset: 6
    padding: 12
    spacing: 6

    icon.width: 24
    icon.height: 24
    icon.color: !enabled ? Material.hintTextColor :
        flat && highlighted ? Material.accentColor :
        highlighted ? Material.primaryHighlightedTextColor :
        (control.down ? colorFgClick : control.hovered ? colorFgOver : colorFg)

    Material.elevation: flat ? control.down || control.hovered ? 0 : 0
                             : control.down ? 0 : 0
    Material.background: flat ? "transparent" : undefined

    contentItem: IconLabel {
        spacing: control.spacing
        mirrored: control.mirrored
        display: control.display

        icon: control.icon
        text: control.text
        font: control.font
        color: !control.enabled ? control.Material.hintTextColor :
            control.flat && control.highlighted ? control.Material.accentColor :
            control.highlighted ? control.Material.primaryHighlightedTextColor :
            (control.down ? colorFgClick : control.hovered ? colorFgOver : colorFg)
    }

    background: Rectangle {
        implicitWidth: control.Material.buttonHeight
        implicitHeight: control.Material.buttonHeight

        radius: control.radius
        color: !control.enabled ? control.Material.buttonDisabledColor
            : control.checked || control.highlighted ? control.Material.highlightedButtonColor : colorBg

        Rectangle {
            id: rectHover

            width: parent.width
            height: parent.height
            radius: control.radius
            color: colorBgOver
            opacity: 0

            OpacityAnimator {
                running: control.hovered || control.visualFocus;
                target: rectHover; from: 0; to: 1; duration: 300
            }
            OpacityAnimator {
                running: !control.hovered && !control.visualFocus;
                target: rectHover; from: 1; to: 0; duration: 300
            }
        }

        Rectangle {
            id: rectClicked

            width: parent.width
            height: parent.height
            radius: control.radius
            color: colorBgClick
            opacity: 0

            OpacityAnimator {
                running: control.down;
                target: rectClicked; from: opacity; to: 1; duration: 200
            }
            OpacityAnimator {
                running: !control.down;
                target: rectClicked; from: opacity; to: 0; duration: 200
            }
        }

        // The layer is disabled when the button color is transparent so that you can do
        // Material.background: "transparent" and get a proper flat button without needing
        // to set Material.elevation as well
        layer.enabled: control.enabled && control.Material.buttonColor.a > 0
        layer.effect: ElevationEffect {
            elevation: control.Material.elevation
        }
    }
}
