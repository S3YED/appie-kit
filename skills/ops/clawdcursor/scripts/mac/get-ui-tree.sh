#!/usr/bin/env bash
# get-ui-tree.sh — Get the accessibility tree of the frontmost app on macOS
#
# Uses JXA (JavaScript for Automation) + System Events to walk the UI element
# hierarchy of the frontmost application.
#
# Returns JSON with name, role, subrole, description, position, size for each element.
#
# Parameters:
#   -ProcessId <number>  Optional. If specified, get tree for this process.
#                        Otherwise uses the frontmost app.
#   -MaxDepth <number>   Optional. Maximum traversal depth (default 6).
#
# Usage:
#   chmod +x scripts/mac/get-ui-tree.sh
#   ./scripts/mac/get-ui-tree.sh
#   ./scripts/mac/get-ui-tree.sh -ProcessId 1234

set -euo pipefail

# Parse arguments
PROCESS_ID=""
MAX_DEPTH="6"

while [[ $# -gt 0 ]]; do
  case "$1" in
    -ProcessId) PROCESS_ID="$2"; shift 2 ;;
    -MaxDepth)  MAX_DEPTH="$2"; shift 2 ;;
    *)          shift ;;
  esac
done

# Run JXA inline to walk the accessibility tree
osascript -l JavaScript - "$PROCESS_ID" "$MAX_DEPTH" <<'ENDSCRIPT'
ObjC.import('stdlib');

var args = ObjC.unwrap($.NSProcessInfo.processInfo.arguments);
// Arguments: [osascript, -, processId, maxDepth]
var targetPid = args.length > 2 ? parseInt(ObjC.unwrap(args[2]), 10) : 0;
var maxDepth = args.length > 3 ? parseInt(ObjC.unwrap(args[3]), 10) : 6;

function safeGet(obj, property, defaultValue) {
    try {
        var val = obj[property]();
        return val !== undefined && val !== null ? val : defaultValue;
    } catch (e) {
        return defaultValue;
    }
}

function walkTree(element, depth) {
    if (depth > maxDepth) return null;

    var node = {};

    try { node.name = element.name() || ''; } catch (e) { node.name = ''; }
    try { node.role = element.role() || ''; } catch (e) { node.role = ''; }
    try { node.subrole = element.subrole() || ''; } catch (e) { node.subrole = ''; }
    try { node.description = element.description() || ''; } catch (e) { node.description = ''; }
    try { node.value = String(element.value() || ''); } catch (e) { node.value = ''; }
    try { node.enabled = element.enabled(); } catch (e) { node.enabled = true; }

    // Position and size
    try {
        var pos = element.position();
        var sz = element.size();
        node.position = { x: pos[0] || 0, y: pos[1] || 0 };
        node.size = { width: sz[0] || 0, height: sz[1] || 0 };
    } catch (e) {
        node.position = { x: 0, y: 0 };
        node.size = { width: 0, height: 0 };
    }

    // Recurse into children
    var children = [];
    try {
        var uiElements = element.uiElements();
        for (var i = 0; i < uiElements.length && i < 50; i++) {
            var child = walkTree(uiElements[i], depth + 1);
            if (child) children.push(child);
        }
    } catch (e) {
        // No children accessible
    }

    if (children.length > 0) {
        node.children = children;
    }

    return node;
}

try {
    var SystemEvents = Application('System Events');
    SystemEvents.includeStandardAdditions = true;

    var targetProcess;
    if (targetPid && targetPid > 0) {
        var procs = SystemEvents.processes.where({ unixId: targetPid });
        if (procs.length === 0) {
            console.log(JSON.stringify({ error: 'No process found with ID ' + targetPid }));
            $.exit(1);
        }
        targetProcess = procs[0];
    } else {
        // Use frontmost process
        var frontProcs = SystemEvents.processes.where({ frontmost: true });
        if (frontProcs.length === 0) {
            console.log(JSON.stringify({ error: 'No frontmost process found' }));
            $.exit(1);
        }
        targetProcess = frontProcs[0];
    }

    var processName = safeGet(targetProcess, 'name', 'unknown');
    var processId = safeGet(targetProcess, 'unixId', 0);

    var tree = {
        processName: processName,
        processId: processId,
        windows: []
    };

    var windows = targetProcess.windows;
    for (var w = 0; w < windows.length && w < 5; w++) {
        try {
            var winNode = walkTree(windows[w], 0);
            if (winNode) {
                tree.windows.push(winNode);
            }
        } catch (e) {
            // Window not accessible
        }
    }

    console.log(JSON.stringify(tree, null, 0));
} catch (error) {
    console.log(JSON.stringify({ error: error.toString() }));
    $.exit(1);
}
ENDSCRIPT
