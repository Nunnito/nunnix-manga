pragma Singleton
import QtQuick 2.15

QtObject {
    // Window background
    property string windowBg: "#121212"
    // Text color
    property string windowFg: "#ededed"
    // Accent color
    property string windowAccent: "#B39DDB"


    // Sidebar background
    property string sideBarBg: "#181818"
    // Sidebar icon color
    property string sideBarFg
    // Sidebar background with mouse over
    property string sidebarBgOver
    // Sidebar icon color with mouse over
    property string sideBarFgOver
    // Sidebar background selected
    property string sidebarBgSelect
    // Sidebar icon color selected
    property string sideBarFgSelect


    // Titlebar background
    property string titleBg: "#0e0e0e"
    // Titlebar minimize/maximize/restore button background
    property string titleButtonBg: "#0e0e0e"
    // Titlebar minimize/maximize/restore button icon color
    property string titleButtonFg: "#ededed"
    // Titlebar minimize/maximize/restore button background with mouse over
    property string titleButtonBgOver: "#151515"
    // Titlebar minimize/maximize/restore button icon color with mouse over
    property string titleButtonFgOver: "#ededed"
    // Titlebar close button background
    property string titleButtonCloseBg: "#0e0e0e"
    // Titlebar close button icon color
    property string titleButtonCloseFg: "#ededed"
    // Titlebar close button background with mouse over
    property string titleButtonCloseBgOver: "#ee4444"
    // Titlebar close button icon color with mouse over
    property string titleButtonCloseFgOver: "#ededed"
}
