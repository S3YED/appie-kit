#!/usr/bin/env bash
# interact-element.sh — Click, type, set value, focus elements on macOS
#
# Uses JXA (JavaScript for Automation) + System Events to interact with
# native macOS UI elements via the Accessibility API.
#
# Outputs JSON matching the Windows invoke-element.ps1 / interact-element.ps1 format.
#
# Parameters:
#   -Name <string>           Match elements by name (contains, case-insensitive)
#   -AutomationId <string>   Match by description/identifier
#   -ControlType <string>    Filter by control type (Button, Edit, etc.)
#   -ProcessId <number>      Required. Process ID of the target application
#   -Action <string>         Required. Action: click, set-value, get-value, focus,
#                            toggle, expand, collapse, select, sendkeys
#   -Value <string>          Value for set-value/sendkeys actions
#
# Usage:
#   chmod +x scripts/mac/interact-element.sh
#   ./scripts/mac/interact-element.sh -Name "Save" -Action click -ProcessId 1234
#   ./scripts/mac/interact-element.sh -Name "Search" -Action set-value -Value "hello" -ProcessId 1234

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Parse arguments
NAME=""
AUTOMATION_ID=""
CONTROL_TYPE=""
PROCESS_ID=""
ACTION=""
VALUE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    -Name)         NAME="$2"; shift 2 ;;
    -AutomationId) AUTOMATION_ID="$2"; shift 2 ;;
    -ControlType)  CONTROL_TYPE="$2"; shift 2 ;;
    -ProcessId)    PROCESS_ID="$2"; shift 2 ;;
    -Action)       ACTION="$2"; shift 2 ;;
    -Value)        VALUE="$2"; shift 2 ;;
    *)             shift ;;
  esac
done

# Validate required parameters
if [[ -z "$ACTION" ]]; then
  echo '{"success":false,"error":"Missing required parameter: -Action"}'
  exit 1
fi

if [[ -z "$PROCESS_ID" || "$PROCESS_ID" == "0" ]]; then
  echo '{"success":false,"error":"Missing required parameter: -ProcessId"}'
  exit 1
fi

# Map Windows ControlType to macOS role
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
    List)         echo "list" ;;
    ListItem)     echo "row" ;;
    Tree)         echo "outline" ;;
    TreeItem)     echo "row" ;;
    Tab)          echo "tab group" ;;
    TabItem)      echo "radio button" ;;
    Window)       echo "window" ;;
    *)            echo "" ;;
  esac
}

# Determine search name (use Name or AutomationId)
SEARCH_NAME="${NAME:-$AUTOMATION_ID}"

# For actions that can use the existing invoke-element.jxa
case "$ACTION" in
  click|set-value|get-value|focus)
    # Build JXA arguments
    JXA_ARGS=("-action" "$ACTION" "-processId" "$PROCESS_ID")
    
    if [[ -n "$SEARCH_NAME" ]]; then
      JXA_ARGS+=("-name" "$SEARCH_NAME")
    fi
    
    if [[ -n "$CONTROL_TYPE" ]]; then
      MAPPED_ROLE=$(map_control_type "$CONTROL_TYPE")
      if [[ -n "$MAPPED_ROLE" ]]; then
        JXA_ARGS+=("-role" "$MAPPED_ROLE")
      fi
    fi
    
    if [[ -n "$VALUE" ]]; then
      JXA_ARGS+=("-value" "$VALUE")
    fi
    
    # Run invoke-element.jxa
    osascript -l JavaScript "$SCRIPT_DIR/invoke-element.jxa" "${JXA_ARGS[@]}" 2>/dev/null || \
      echo '{"success":false,"error":"JXA script failed"}'
    ;;
    
  sendkeys)
    # Focus the element, then use System Events keystroke
    if [[ -z "$VALUE" ]]; then
      echo '{"success":false,"error":"Value parameter required for sendkeys action"}'
      exit 0
    fi
    
    # First focus the element
    JXA_ARGS=("-action" "focus" "-processId" "$PROCESS_ID")
    if [[ -n "$SEARCH_NAME" ]]; then
      JXA_ARGS+=("-name" "$SEARCH_NAME")
    fi
    
    FOCUS_RESULT=$(osascript -l JavaScript "$SCRIPT_DIR/invoke-element.jxa" "${JXA_ARGS[@]}" 2>/dev/null || echo '{"success":false}')
    
    # Check if focus succeeded
    FOCUS_OK=$(echo "$FOCUS_RESULT" | /usr/bin/python3 -c "import sys,json; d=json.load(sys.stdin); print('true' if d.get('success') else 'false')" 2>/dev/null || echo "false")
    
    if [[ "$FOCUS_OK" != "true" ]]; then
      echo '{"success":false,"error":"Failed to focus element for sendkeys"}'
      exit 0
    fi
    
    # Small delay for focus to take effect
    sleep 0.1
    
    # Send keystrokes via System Events (sanitize input via python3)
    SAFE_VALUE=$(/usr/bin/python3 -c "import sys,json; print(json.dumps(sys.argv[1]))" "$VALUE" 2>/dev/null)
    # SAFE_VALUE is now a JSON-quoted string like "hello \"world\""
    # Strip outer quotes for AppleScript
    SAFE_VALUE=${SAFE_VALUE:1:-1}
    osascript -e "
      tell application \"System Events\"
        keystroke \"${SAFE_VALUE}\"
      end tell
    " 2>/dev/null
    
    if [[ $? -eq 0 ]]; then
      echo "{\"success\":true,\"action\":\"sendkeys\",\"method\":\"keystroke\",\"value\":$(echo "$VALUE" | /usr/bin/python3 -c 'import sys,json; print(json.dumps(sys.stdin.read().strip()))')}"
    else
      echo '{"success":false,"error":"keystroke failed"}'
    fi
    ;;
    
  toggle)
    # Toggle a checkbox: click it to toggle state
    JXA_ARGS=("-action" "click" "-processId" "$PROCESS_ID")
    if [[ -n "$SEARCH_NAME" ]]; then
      JXA_ARGS+=("-name" "$SEARCH_NAME")
    fi
    if [[ -n "$CONTROL_TYPE" ]]; then
      MAPPED_ROLE=$(map_control_type "$CONTROL_TYPE")
      if [[ -n "$MAPPED_ROLE" ]]; then
        JXA_ARGS+=("-role" "$MAPPED_ROLE")
      fi
    fi
    
    RESULT=$(osascript -l JavaScript "$SCRIPT_DIR/invoke-element.jxa" "${JXA_ARGS[@]}" 2>/dev/null || echo '{"success":false}')
    
    # Rewrite the result to indicate toggle action
    echo "$RESULT" | /usr/bin/python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    d['action'] = 'toggle'
    if d.get('success'):
        d['method'] = 'click-toggle'
    print(json.dumps(d, separators=(',', ':')))
except:
    print('{\"success\":false,\"error\":\"toggle failed\"}')" 2>/dev/null || echo '{"success":false,"error":"toggle failed"}'
    ;;
    
  expand|collapse)
    # macOS doesn't have ExpandCollapsePattern directly.
    # Try AXPress action (works for disclosure triangles) or click
    JXA_ARGS=("-action" "click" "-processId" "$PROCESS_ID")
    if [[ -n "$SEARCH_NAME" ]]; then
      JXA_ARGS+=("-name" "$SEARCH_NAME")
    fi
    
    RESULT=$(osascript -l JavaScript "$SCRIPT_DIR/invoke-element.jxa" "${JXA_ARGS[@]}" 2>/dev/null || echo '{"success":false}')
    
    echo "$RESULT" | /usr/bin/python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    d['action'] = '${ACTION}'
    if d.get('success'):
        d['method'] = 'click-${ACTION}'
    print(json.dumps(d, separators=(',', ':')))
except:
    print('{\"success\":false,\"error\":\"${ACTION} failed\"}')" 2>/dev/null || echo "{\"success\":false,\"error\":\"${ACTION} failed\"}"
    ;;
    
  select)
    # Select: click the item (works for list items, tabs, radio buttons)
    JXA_ARGS=("-action" "click" "-processId" "$PROCESS_ID")
    if [[ -n "$SEARCH_NAME" ]]; then
      JXA_ARGS+=("-name" "$SEARCH_NAME")
    fi
    if [[ -n "$CONTROL_TYPE" ]]; then
      MAPPED_ROLE=$(map_control_type "$CONTROL_TYPE")
      if [[ -n "$MAPPED_ROLE" ]]; then
        JXA_ARGS+=("-role" "$MAPPED_ROLE")
      fi
    fi
    
    RESULT=$(osascript -l JavaScript "$SCRIPT_DIR/invoke-element.jxa" "${JXA_ARGS[@]}" 2>/dev/null || echo '{"success":false}')
    
    echo "$RESULT" | /usr/bin/python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    d['action'] = 'select'
    if d.get('success'):
        d['method'] = 'click-select'
    print(json.dumps(d, separators=(',', ':')))
except:
    print('{\"success\":false,\"error\":\"select failed\"}')" 2>/dev/null || echo '{"success":false,"error":"select failed"}'
    ;;
    
  *)
    echo "{\"success\":false,\"error\":\"Unknown action: $ACTION\"}"
    exit 0
    ;;
esac
