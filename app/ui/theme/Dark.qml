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
    property string controlBg: "#282828"
    // Default control background with mouse over (ripple color in #AARRGGBB)
    property string controlBgOver: "#aa2c2c2c"
    // Default control icon color with mouse over
    property string controlFgOver: "#ededed"
    // Default control background with mouse clicked
    property string controlBgClick: "#212121"
    // Default control icon color with mouse clicked
    property string controlFgClick: "#ededed"
    // Default control background dialog color
    property string controlBgDialog: "#282828"


    // Sidebar background
    property string sidebarBg: "#1F1F1F"
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
    property string topBarBg: "#1D1D1D"
    // Topbar button background
    property string topBarButtonBg: "#1D1D1D"
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

    // Busy indicator color
    property string busyIndicator: "#B39DDB"

    // Scrollbar background
    property string scrollbarBg: "#881F1F1F"
    // Scrollbar item background
    property string scrollbarItemBg: "#222222"
    // Scrollbar item background with mouse over
    property string scrollbarItemBgOver: "#2f2f2f"
    // Scrollbar item background with mouse clicked
    property string scrollbarItemBgClick: "#3a3a3a"

    // Separator color
    property string separator: "#626262"

    // Advanced search background
    property string advancedSearchBg: "#1F1F1F"
    // Advanced search separator color
    property string advancedSearchSeparator: "#626262"
    // Advanced search scrollbar item background
    property string advancedSearchScrollbarItemBg: "#2a2a2a"

    // Checkbox partiallly checked color (red pastel)
    property string checkboxPartial: "#626262"

    // Combo box decoration inactive color
    property string comboBoxDecorationInactive: "#626262"
    // Combo box decoration active color
    property string comboBoxDecorationActive: "#B39DDB"
    // Combo box decoration hover color
    property string comboBoxDecorationHover: "#ededed"
    // Combobox item background with mouse over (ripple color in #AARRGGBB)
    property string comboBoxItemBgOver: "#aa3c3c3c"
}
