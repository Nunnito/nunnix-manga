// TODO: Return the ligth theme
// This will return, but then the theme system will have to be completely
// rewritten

pragma Singleton
import QtQuick 2.15

QtObject {
    // Window background
    property string windowBg: "#EDEDD0"
    // Text and icon color (control)
    property string windowFg: "#EDEDD0"
    // Accent color
    property string windowAccent: "#645474"


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
    // Default control background dialog color
    property string controlBgDialog: "#907FA4"


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

    // Scrollbar background
    property string scrollbarBg: "#88e0e0e0"
    // Scrollbar item background
    property string scrollbarItemBg: "#9f8db6"
    // Scrollbar item background with mouse over
    property string scrollbarItemBgOver: "#907FA4"
    // Scrollbar item background with mouse clicked
    property string scrollbarItemBgClick: "#645474"

    // Separator color
    property string separator: "#5a5a5a"

    // Advanced search background
    property string advancedSearchBg: "#907FA4"
    // Advanced search separator color
    property string advancedSearchSeparator: "#5a5a5a"
    // Advanced search scrollbar item background
    property string advancedSearchScrollbarItemBg: "#907FA4"
    // Advanced search search button background over (ripple color in #AARRGGBB)
    property string advancedSearchSearchButtonBgOver: "#22111111"
    // Advanced search search background 2
    property string advancedSearchSearchBg2: "#907FA4"

    // Checkbox partiallly checked color (red pastel)
    property string checkboxPartial: "#626262"

    // Combo box decoration inactive color
    property string comboBoxDecorationInactive: "#5a5a5a"
    // Combo box decoration active color
    property string comboBoxDecorationActive: "#645474"
    // Combo box decoration hover color
    property string comboBoxDecorationHover: "#EDEDD0"
    // Combobox item background with mouse over (ripple color in #AARRGGBB)
    property string comboBoxItemBgOver: "#aa3c3c3c"
}
