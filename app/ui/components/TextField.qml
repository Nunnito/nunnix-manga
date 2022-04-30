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

T.TextField {
    id: control
    property bool outlined: false
    property var currentRectColor: control.activeFocus ? decorationActiveColor
                        : (control.hovered ? decorationHoverColor : decorationInactiveColor)

    implicitWidth: implicitBackgroundWidth + leftInset + rightInset
                   || Math.max(contentWidth, placeholder.implicitWidth) + leftPadding + rightPadding
    implicitHeight: Math.max(implicitBackgroundHeight + topInset + bottomInset,
                             contentHeight + topPadding + bottomPadding,
                             placeholder.implicitHeight + topPadding + bottomPadding)

    topPadding: outlined ? 20 : 8
    bottomPadding: outlined ? 20 : 16
    leftPadding: outlined ? 8 : 0

    property string cursorColor: theme.textfieldCursor
    property string decorationActiveColor: theme.textfieldDecorationActive
    property string decorationInactiveColor: theme.textfieldDecorationInactive
    property string decorationHoverColor: theme.textfieldDecorationHover
    color: enabled ? theme.textfieldFg : Material.hintTextColor
    selectionColor: theme.textfieldSelectionBg
    selectedTextColor: theme.textfieldSelectionFg
    placeholderTextColor: theme.textfieldPlaceholderFg

    verticalAlignment: TextInput.AlignVCenter

    cursorDelegate: CursorDelegate {color: cursorColor}

    PlaceholderText {
        id: placeholder
        x: control.leftPadding
        y: control.topPadding
        width: control.width - (control.leftPadding + control.rightPadding)
        height: control.height - (control.topPadding + control.bottomPadding)
        text: control.placeholderText
        font: control.font
        color: control.placeholderTextColor
        verticalAlignment: control.verticalAlignment
        elide: Text.ElideRight
        renderType: control.renderType
        visible: !control.length && !control.preeditText && (!control.activeFocus || control.horizontalAlignment !== Qt.AlignHCenter)
    }

    background: Control {
        y: control.height - height - control.bottomPadding + (outlined ? control.topPadding / 2 : 8)
        implicitWidth: 120
        height: outlined ? control.height - (control.bottomPadding) :
                           control.activeFocus || control.hovered ? 2 : 1
        background: Rectangle {
            border.width: outlined ? control.activeFocus ? 2 : 1 : 0
            radius: outlined ? 3 : 0
            color: outlined ? "transparent" : currentRectColor
            border.color: outlined ? currentRectColor : "transparent"

            Behavior on color {
                ColorAnimation {duration: 250; easing.type: Easing.OutQuad}
            }
            Behavior on border.color {
                ColorAnimation {duration: 250; easing.type: Easing.OutQuad}
            }
        }
    }
}
