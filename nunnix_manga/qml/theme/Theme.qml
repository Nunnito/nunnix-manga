// If there is a custom theme, load it, else load the default theme
import QtQuick 2.15

QtObject {
    id: t
    property bool ct: Object.keys(thm).length != 0 // Is there a custom theme?


    // Custom window titlebar background
    property string titleBg: ct ? thm.titleBg : "#000000"

    // Custom window titlebar minimize/maximize/restore button background
    property string titleButtonBg: ct ? thm.titleButtonBg : "#000000"

    // Custom window titlebar minimize/maximize/restore button icon color
    property string titleButtonFg: ct ? thm.titleButtonFg : "#000000"

    // Custom window titlebar minimize/maximize/restore button background with mouse over
    property string titleButtonBgOver: ct ? thm.titleButtonBgOver : "#000000"

    // Custom window titlebar minimize/maximize/restore button icon color with mouse over
    property string titleButtonFgOver: ct ? thm.titleButtonFgOver : "#000000"

    // Custom window titlebar close button background
    property string titleButtonCloseBg: ct ? thm.titleButtonCloseBg : "#000000"

    // Custom window titlebar close button icon color
    property string titleButtonCloseFg: ct ? thm.titleButtonCloseFg : "#000000"

    // Custom window titlebar close button background with mouse over
    property string titleButtonCloseBgOver: ct ? thm.titleButtonCloseBgOver : "#000000"

    // Custom window titlebar close button icon color with mouse over
    property string titleButtonCloseFgOver: ct ? thm.titleButtonCloseFgOver : "#000000"
}
