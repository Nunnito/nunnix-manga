pragma Singleton
import QtQuick 2.15

QtObject {
    // Window background
    property string windowBg: "#121212"
    // Text and icon color (control)
    property string windowFg: "#ededed"
    // Accent color
    property string windowAccent: "#B39DDB"


    // Default control background
    property string controlBg: "#1d1d1d"
    // Default control background with mouse over (ripple color in #AARRGGBB)
    property string controlBgOver: "#aa282828"
    // Default control icon color with mouse over
    property string controlFgOver: "#ededed"
    // Default control background with mouse clicked
    property string controlBgClick: "#212121"
    // Default control icon color with mouse clicked
    property string controlFgClick: "#ededed"


    // Sidebar background
    property string sidebarBg: "#1D1D1D"
    // Sidebar button background (when is selected)
    property string sidebarButtonBg: "#2C2C2C"
    // Sidebar button icon color
    property string sidebarButtonFg: "#ededed"
    // Sidebar button background with mouse over (ripple color in #AARRGGBB)
    property string sidebarButtonBgOver: "#aa282828"
    // Sidebar button icon color with mouse over
    property string sidebarButtonFgOver: "#ededed"


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


    // Topbar background
    property string topBarBg: "#1F1F1F"
    // Topbar button background
    property string topBarButtonBg: "#1F1F1F"
    // Topbar button icon color
    property string topBarButtonFg: "#ededed"
    // Topbar button background with mouse over (ripple color in #AARRGGBB)
    property string topBarButtonBgOver: "#aa303030"
    // Topbar button icon color with mouse over
    property string topBarButtonFgOver: "#ededed"
    // Topbar button background with mouse clicked
    property string topBarButtonBgClick: "#3A3A3A"
    // Topbar button icon color with mouse clicked
    property string topBarButtonFgClick: "#ededed"


    // Textfield text color
    property string textfieldFg: "#ededed"
    // Textfield selection background
    property string textfieldSelectionBg: "#B39DDB"
    // Textfield selection text color
    property string textfieldSelectionFg: "#1F1F1F"
    // Textfield placeholder text color
    property string textfieldPlaceholderFg: "#626262"
    // Textfield cursor color
    property string textfieldCursor: "#B39DDB"
    // Textfield decoration inactive color
    property string textfieldDecorationInactive: "#626262"
    // Textfield decoration active color
    property string textfieldDecorationActive: "#B39DDB"
    // Textfield decoration hover color
    property string textfieldDecorationHover: "#ededed"
}
