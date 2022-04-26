pragma Singleton
import QtQuick 2.15

QtObject {
    // Window background
    property string windowBg: "#EDEDD0"
    // Text and icon color (control)
    property string windowFg: "#EDEDD0"
    // Accent color
    property string accent: "#645474"


    // Default control background
    property string controlBg: "#907FA4"
    // Default control background with mouse over (ripple color in #AARRGGBB)
    property string controlBgOver: "#aaa995c1"
    // Default control icon color with mouse over
    property string controlFgOver: "#EDEDD0"
    // Default control background with mouse clicked
    property string controlBgClick: "#907FA4"
    // Default control icon color with mouse clicked
    property string controlFgClick: "#EDEDD0"


    // Sidebar background
    property string sidebarBg: "#907FA4"
    // Sidebar button background (when is selected)
    property string sidebarButtonBg: "#A58FAA"
    // Sidebar button icon color
    property string sidebarButtonFg: "#EDEDD0"
    // Sidebar button background with mouse over (ripple color in #AARRGGBB)
    property string sidebarButtonBgOver: "#aaa995c1"
    // Sidebar button icon color with mouse over
    property string sidebarButtonFgOver: "#EDEDD0"


    // Titlebar background
    property string titleBg: "#EDEDD0"
    // Titlebar minimize/maximize/restore button background
    property string titleButtonBg: "#EDEDD0"
    // Titlebar minimize/maximize/restore button icon color
    property string titleButtonFg: "#907FA4"
    // Titlebar minimize/maximize/restore button background with mouse over
    property string titleButtonBgOver: "#b6b6a0"
    // Titlebar minimize/maximize/restore button icon color with mouse over
    property string titleButtonFgOver: "#907FA4"
    // Titlebar close button background
    property string titleButtonCloseBg: "#EDEDD0"
    // Titlebar close button icon color
    property string titleButtonCloseFg: "#907FA4"
    // Titlebar close button background with mouse over
    property string titleButtonCloseBgOver: "#ee4444"
    // Titlebar close button icon color with mouse over
    property string titleButtonCloseFgOver: "#EDEDD0"


    // Topbar background
    property string topBarBg: "#9f8db6"
    // Topbar button background
    property string topBarButtonBg: "#9f8db6"
    // Topbar button icon color
    property string topBarButtonFg: "#EDEDD0"
    // Topbar button background with mouse over (ripple color in #AARRGGBB)
    property string topBarButtonBgOver: "#aab49fce"
    // Topbar button icon color with mouse over
    property string topBarButtonFgOver: "#EDEDD0"
    // Topbar button background with mouse clicked
    property string topBarButtonBgClick: "#bea8d9"
    // Topbar button icon color with mouse clicked
    property string topBarButtonFgClick: "#EDEDD0"


    // Textfield text color
    property string textfieldFg: "#EDEDD0"
    // Textfield selection background
    property string textfieldSelectionBg: "#645474"
    // Textfield selection text color
    property string textfieldSelectionFg: "#9f8db6"
    // Textfield placeholder text color
    property string textfieldPlaceholderFg: "#5a5a5a"
    // Textfield cursor color
    property string textfieldCursor: "#645474"
    // Textfield decoration inactive color
    property string textfieldDecorationInactive: "#5a5a5a"
    // Textfield decoration active color
    property string textfieldDecorationActive: "#645474"
    // Textfield decoration hover color
    property string textfieldDecorationHover: "#EDEDD0"

    // Busy indicator color
    property string busyIndicator: "#907FA4"
}
