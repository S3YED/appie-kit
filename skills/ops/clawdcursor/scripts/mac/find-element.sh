#!/usr/bin/env bash
# find-element.sh — Find UI elements on macOS using JXA + System Events
#
# Wrapper around find-element.jxa for UIDriver cross-platform support.
# Outputs JSON matching the Windows find-element.ps1 format:
#   [{ name, automationId, controlType, className, processId, isEnabled, bounds }]
#
# Parameters:
#   -Name <string>           Match elements by name (contains, case-insensitive)
#   -AutomationId <string>   Match by description/identifier (mapped to name search)
#   -ControlType <string>    Match by role (e.g. Button, Edit, MenuItem)
#   -ProcessId <number>      Limit to a specific process
#   -MaxResults <number>     Max results (default 20)
#
# Usage:
#   chmod +x scripts/mac/find-element.sh
#   ./scripts/mac/find-element.sh -Name "OK" -ControlType "Button" -ProcessId 1234

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Parse arguments
NAME=""
AUTOMATION_ID=""
CONTROL_TYPE=""
PROCESS_ID=""
MAX_RESULTS="20"

while [[ $# -gt 0 ]]; do
  case "$1" in
    -Name)         NAME="$2"; shift 2 ;;
    -AutomationId) AUTOMATION_ID="$2"; shift 2 ;;
    -ControlType)  CONTROL_TYPE="$2"; shift 2 ;;
    -ProcessId)    PROCESS_ID="$2"; shift 2 ;;
    -MaxResults)   MAX_RESULTS="$2"; shift 2 ;;
    *)             shift ;;
  esac
done

# Map Windows ControlType names to macOS accessibility roles
map_control_type() {
  local ct="$1"
  case "$ct" in
    Button)       echo "button" ;;
    Edit)         echo "text field" ;;
    Text)         echo "static text" ;;
    CheckBox)     echo "checkbox" ;;
    RadioButton)  echo "radio button" ;;
    ComboBox)     echo "pop up button" ;;
    MenuItem)     echo "menu item" ;;
    Menu)         echo "menu" ;;
    MenuBar)      echo "menu bar" ;;
    List)         echo "list" ;;
    ListItem)     echo "row" ;;
    Tree)         echo "outline" ;;
    TreeItem)     echo "row" ;;
    Tab)          echo "tab group" ;;
    TabItem)      echo "radio button" ;;
    Slider)       echo "slider" ;;
    ProgressBar)  echo "progress indicator" ;;
    ToolBar)      echo "toolbar" ;;
    Window)       echo "window" ;;
    Group)        echo "group" ;;
    Image)        echo "image" ;;
    Hyperlink)    echo "link" ;;
    ScrollBar)    echo "scroll bar" ;;
    Table)        echo "table" ;;
    Document)     echo "text area" ;;
    *)            echo "$ct" ;;
  esac
}

# Build JXA arguments
JXA_ARGS=()

# Use Name or AutomationId as the search name
SEARCH_NAME="${NAME:-$AUTOMATION_ID}"
if [[ -n "$SEARCH_NAME" ]]; then
  JXA_ARGS+=("-name" "$SEARCH_NAME")
fi

# Map control type to macOS role
if [[ -n "$CONTROL_TYPE" ]]; then
  MAPPED_ROLE=$(map_control_type "$CONTROL_TYPE")
  JXA_ARGS+=("-role" "$MAPPED_ROLE")
fi

if [[ -n "$PROCESS_ID" && "$PROCESS_ID" != "0" ]]; then
  JXA_ARGS+=("-processId" "$PROCESS_ID")
fi

# Run the JXA script
RAW_OUTPUT=$(osascript -l JavaScript "$SCRIPT_DIR/find-element.jxa" "${JXA_ARGS[@]}" 2>/dev/null || echo "[]")

# Transform the JXA output to match Windows format:
# JXA returns: { name, role, value, bounds, processId }
# Windows expects: { name, automationId, controlType, className, processId, isEnabled, bounds }
echo "$RAW_OUTPUT" | /usr/bin/python3 -c "
import sys, json

try:
    data = json.load(sys.stdin)
except:
    print('[]')
    sys.exit(0)

if isinstance(data, dict) and 'error' in data:
    print(json.dumps(data))
    sys.exit(0)

if not isinstance(data, list):
    data = [data]

# Map macOS roles back to Windows ControlType names
ROLE_MAP = {
    'AXButton': 'Button', 'button': 'Button',
    'AXTextField': 'Edit', 'text field': 'Edit',
    'AXStaticText': 'Text', 'static text': 'Text',
    'AXCheckBox': 'CheckBox', 'checkbox': 'CheckBox',
    'AXRadioButton': 'RadioButton', 'radio button': 'RadioButton',
    'AXPopUpButton': 'ComboBox', 'pop up button': 'ComboBox',
    'AXMenuItem': 'MenuItem', 'menu item': 'MenuItem',
    'AXMenu': 'Menu', 'menu': 'Menu',
    'AXMenuBar': 'MenuBar', 'menu bar': 'MenuBar',
    'AXList': 'List', 'list': 'List',
    'AXRow': 'ListItem', 'row': 'ListItem',
    'AXOutline': 'Tree', 'outline': 'Tree',
    'AXTabGroup': 'Tab', 'tab group': 'Tab',
    'AXSlider': 'Slider', 'slider': 'Slider',
    'AXProgressIndicator': 'ProgressBar', 'progress indicator': 'ProgressBar',
    'AXToolbar': 'ToolBar', 'toolbar': 'ToolBar',
    'AXWindow': 'Window', 'window': 'Window',
    'AXGroup': 'Group', 'group': 'Group',
    'AXImage': 'Image', 'image': 'Image',
    'AXLink': 'Hyperlink', 'link': 'Hyperlink',
    'AXScrollBar': 'ScrollBar', 'scroll bar': 'ScrollBar',
    'AXTable': 'Table', 'table': 'Table',
    'AXTextArea': 'Document', 'text area': 'Document',
    'AXScrollArea': 'Pane', 'scroll area': 'Pane',
}

max_results = int('${MAX_RESULTS}')
results = []

for item in data[:max_results]:
    role = item.get('role', '')
    control_type = ROLE_MAP.get(role, role)
    
    results.append({
        'name': item.get('name', ''),
        'automationId': '',  # macOS doesn't have AutomationId; use identifier if available
        'controlType': control_type,
        'className': role,  # Store original macOS role as className
        'processId': item.get('processId', 0),
        'isEnabled': True,  # macOS doesn't easily expose enabled state in bulk
        'bounds': item.get('bounds', {'x': 0, 'y': 0, 'width': 0, 'height': 0})
    })

print(json.dumps(results, separators=(',', ':')))
"
