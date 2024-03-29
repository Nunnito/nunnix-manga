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

import QtQuick 2.12
import QtQuick.Controls.Material 2.12
import QtQuick.Controls.Material.impl 2.12
import "../utils" as U

Rectangle {
    id: indicatorItem
    implicitWidth: 18
    implicitHeight: 18
    color: "transparent"
    border.color: ascDescMode ? "transparent" 
        : !control.enabled ? control.Material.hintTextColor
        : checkState == Qt.PartiallyChecked && boolTristate ? checkBoxPartially
        : checkState !== Qt.Unchecked ? control.Material.accentColor
        : control.Material.secondaryTextColor
    border.width: checkState !== Qt.Unchecked ? width / 2 : 2
    radius: 2

    // Added properties
    property Item control
    property int checkState: control.checkState
    property bool boolTristate: false
    property string checkBoxPartially: theme.checkboxPartial
    property bool ascDescMode: false

    Behavior on border.width {
        NumberAnimation {
            duration: 100
            easing.type: Easing.OutCubic
        }
    }

    Behavior on border.color {
        ColorAnimation {
            duration: 100
            easing.type: Easing.OutCubic
        }
    }

    // TODO: This needs to be transparent
    Image {
        id: checkImage
        x: (parent.width - width) / 2
        y: (parent.height - height) / 2
        width: ascDescMode ? 18 : 14
        height: ascDescMode ? 18 : 14
        source: {
            if (ascDescMode) {
                return Icon.get_icon("arrow_upward.svg")
            }
            else {
                return "qrc:/qt-project.org/imports/QtQuick/Controls.2/Material/images/check.png"
            }
        }
        fillMode: Image.PreserveAspectFit

        scale: indicatorItem.checkState === Qt.Checked ||
               (ascDescMode && (indicatorItem.checkState === Qt.Checked ||
                indicatorItem.checkState === Qt.PartiallyChecked)) ? 1 : 0
        Behavior on scale { NumberAnimation { duration: 100 } }

        U.ChangeColor {color: ascDescMode ? theme.windowAccent : theme.windowFg}
    }

    Rectangle {
        x: (parent.width - width) / 2
        y: (parent.height - height) / 2
        width: 12
        height: 3

        scale: indicatorItem.checkState == Qt.PartiallyChecked &&
               !boolTristate && !ascDescMode ? 1 : 0
        Behavior on scale { NumberAnimation { duration: 100 } }
    }
    Image {
        id: partiallyCheckImage
        x: (parent.width - width) / 2
        y: (parent.height - height) / 2
        width: 24
        height: 24
        source: Icon.get_icon("close_sharp.svg")
        fillMode: Image.PreserveAspectFit

        scale: indicatorItem.checkState == Qt.PartiallyChecked && boolTristate ? 1 : 0
        Behavior on scale { NumberAnimation { duration: 100 } }
    }

    states: [
        State {
            name: "checked"
            when: indicatorItem.checkState === Qt.Checked
        },
        State {
            name: "partiallychecked"
            when: indicatorItem.checkState === Qt.PartiallyChecked
        }
    ]

    transitions: Transition {
        SequentialAnimation {
            NumberAnimation {
                target: indicatorItem
                property: "scale"
                // Go down 2 pixels in size.
                to: 1 - 2 / indicatorItem.width
                duration: 120
            }
            NumberAnimation {
                target: indicatorItem
                property: "scale"
                to: 1
                duration: 120
            }
        }
    }

    RotationAnimator {
        target: checkImage
        from: 0
        to: 180
        duration: 100
        easing.type: Easing.InQuart
        running: ascDescMode && indicatorItem.state == "partiallychecked"
    }
    RotationAnimator {
        target: checkImage
        from: 180
        to: 0
        duration: 100
        easing.type: Easing.InQuart
        running: ascDescMode && indicatorItem.state == "checked"
    }
}
