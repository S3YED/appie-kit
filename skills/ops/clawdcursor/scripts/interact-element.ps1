<#
.SYNOPSIS
    Enhanced UI element interaction script with additional patterns.
    Extends invoke-element.ps1 with SendKeys, ScrollPattern, and partial name matching.

.DESCRIPTION
    This script provides advanced UI Automation interactions that go beyond
    what invoke-element.ps1 handles:
    
    - sendkeys: Focus element and send keystrokes (for elements without ValuePattern)
    - scroll: Scroll an element using ScrollPattern
    - get-patterns: List all supported patterns on an element (for debugging)
    - click-at: Click at the element's center using Win32 mouse_event
    - wait-enabled: Poll until an element becomes enabled
    
    Uses .NET System.Windows.Automation namespace for reliable element interaction.

.PARAMETER Name
    Find element by Name (exact match).

.PARAMETER AutomationId
    Find element by AutomationId (exact match).

.PARAMETER ControlType
    Filter by ControlType (e.g. "Button", "Edit", "MenuItem").

.PARAMETER ProcessId
    Required. Process ID of the target window.

.PARAMETER Action
    Action to perform: sendkeys, scroll, get-patterns, click-at, wait-enabled

.PARAMETER Value
    The text/keys to send (for sendkeys), or scroll amount (for scroll).

.PARAMETER Direction
    Scroll direction: "up", "down", "left", "right" (for scroll action).

.PARAMETER PartialMatch
    If specified, match Name using substring/contains instead of exact match.

.EXAMPLE
    # Send keys to a text field that doesn't support ValuePattern
    .\interact-element.ps1 -Name "Search" -Action sendkeys -Value "hello" -ProcessId 1234

    # Scroll a list down
    .\interact-element.ps1 -Name "ListView" -Action scroll -Direction down -Value "3" -ProcessId 1234

    # Get all supported patterns for debugging
    .\interact-element.ps1 -Name "Submit" -Action get-patterns -ProcessId 1234

    # Find by partial name match
    .\interact-element.ps1 -Name "Save" -Action click-at -ProcessId 1234 -PartialMatch
#>
param(
    [string]$Name = "",
    [string]$AutomationId = "",
    [string]$ControlType = "",
    [Parameter(Mandatory=$true)]
    [int]$ProcessId,
    [Parameter(Mandatory=$true)]
    [ValidateSet("sendkeys", "scroll", "get-patterns", "click-at", "wait-enabled")]
    [string]$Action,
    [string]$Value = "",
    [string]$Direction = "down",
    [switch]$PartialMatch
)

# ── Load UI Automation assemblies ──
try {
    Add-Type -AssemblyName UIAutomationClient
    Add-Type -AssemblyName UIAutomationTypes
    Add-Type -AssemblyName System.Windows.Forms
} catch {
    [Console]::Out.Write((@{ success = $false; error = "Failed to load assemblies: $($_.Exception.Message)" } | ConvertTo-Json -Compress))
    exit 1
}

# ── Win32 mouse_event for coordinate clicking ──
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Win32Mouse {
    [DllImport("user32.dll")]
    public static extern bool SetCursorPos(int X, int Y);
    
    [DllImport("user32.dll")]
    public static extern void mouse_event(uint dwFlags, int dx, int dy, uint dwData, IntPtr dwExtraInfo);
    
    public const uint MOUSEEVENTF_LEFTDOWN = 0x0002;
    public const uint MOUSEEVENTF_LEFTUP = 0x0004;
    
    public static void ClickAt(int x, int y) {
        SetCursorPos(x, y);
        System.Threading.Thread.Sleep(50);
        mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, IntPtr.Zero);
        System.Threading.Thread.Sleep(30);
        mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, IntPtr.Zero);
    }
}
"@ -ErrorAction SilentlyContinue

$ErrorActionPreference = 'Stop'

# ── Control type mapping ──
$ctMap = @{
    "Button"      = [System.Windows.Automation.ControlType]::Button
    "CheckBox"    = [System.Windows.Automation.ControlType]::CheckBox
    "ComboBox"    = [System.Windows.Automation.ControlType]::ComboBox
    "Custom"      = [System.Windows.Automation.ControlType]::Custom
    "DataItem"    = [System.Windows.Automation.ControlType]::DataItem
    "Document"    = [System.Windows.Automation.ControlType]::Document
    "Edit"        = [System.Windows.Automation.ControlType]::Edit
    "Group"       = [System.Windows.Automation.ControlType]::Group
    "Hyperlink"   = [System.Windows.Automation.ControlType]::Hyperlink
    "List"        = [System.Windows.Automation.ControlType]::List
    "ListItem"    = [System.Windows.Automation.ControlType]::ListItem
    "Menu"        = [System.Windows.Automation.ControlType]::Menu
    "MenuBar"     = [System.Windows.Automation.ControlType]::MenuBar
    "MenuItem"    = [System.Windows.Automation.ControlType]::MenuItem
    "Pane"        = [System.Windows.Automation.ControlType]::Pane
    "RadioButton" = [System.Windows.Automation.ControlType]::RadioButton
    "ScrollBar"   = [System.Windows.Automation.ControlType]::ScrollBar
    "Slider"      = [System.Windows.Automation.ControlType]::Slider
    "Spinner"     = [System.Windows.Automation.ControlType]::Spinner
    "SplitButton" = [System.Windows.Automation.ControlType]::SplitButton
    "Tab"         = [System.Windows.Automation.ControlType]::Tab
    "TabItem"     = [System.Windows.Automation.ControlType]::TabItem
    "Text"        = [System.Windows.Automation.ControlType]::Text
    "ToolBar"     = [System.Windows.Automation.ControlType]::ToolBar
    "Tree"        = [System.Windows.Automation.ControlType]::Tree
    "TreeItem"    = [System.Windows.Automation.ControlType]::TreeItem
    "Window"      = [System.Windows.Automation.ControlType]::Window
}

# ── Helper: Find element with optional partial match ──
function Find-UIElement {
    param(
        [System.Windows.Automation.AutomationElement]$SearchRoot,
        [string]$Name,
        [string]$AutomationId,
        [string]$ControlType,
        [switch]$PartialMatch
    )

    if ($PartialMatch -and $Name -ne "") {
        # For partial match, we can't use PropertyCondition — walk the tree
        $conditions = @()

        if ($ControlType -ne "" -and $ctMap.ContainsKey($ControlType)) {
            $conditions += New-Object System.Windows.Automation.PropertyCondition(
                [System.Windows.Automation.AutomationElement]::ControlTypeProperty,
                $ctMap[$ControlType]
            )
        }

        if ($conditions.Count -eq 0) {
            $searchCondition = [System.Windows.Automation.Condition]::TrueCondition
        } elseif ($conditions.Count -eq 1) {
            $searchCondition = $conditions[0]
        } else {
            $searchCondition = New-Object System.Windows.Automation.AndCondition(
                [System.Windows.Automation.Condition[]]$conditions
            )
        }

        $elements = $SearchRoot.FindAll(
            [System.Windows.Automation.TreeScope]::Descendants,
            $searchCondition
        )

        $lowerName = $Name.ToLower()
        foreach ($el in $elements) {
            try {
                $elName = $el.Current.Name
                if ($elName -and $elName.ToLower().Contains($lowerName)) {
                    return $el
                }
            } catch {
                continue
            }
        }
        return $null
    }

    # Exact match (standard approach)
    $conditions = @()

    if ($AutomationId -ne "") {
        $conditions += New-Object System.Windows.Automation.PropertyCondition(
            [System.Windows.Automation.AutomationElement]::AutomationIdProperty,
            $AutomationId
        )
    }

    if ($Name -ne "") {
        $conditions += New-Object System.Windows.Automation.PropertyCondition(
            [System.Windows.Automation.AutomationElement]::NameProperty,
            $Name
        )
    }

    if ($ControlType -ne "" -and $ctMap.ContainsKey($ControlType)) {
        $conditions += New-Object System.Windows.Automation.PropertyCondition(
            [System.Windows.Automation.AutomationElement]::ControlTypeProperty,
            $ctMap[$ControlType]
        )
    }

    if ($conditions.Count -eq 0) {
        return $null
    }

    if ($conditions.Count -eq 1) {
        $searchCondition = $conditions[0]
    } else {
        $searchCondition = New-Object System.Windows.Automation.AndCondition(
            [System.Windows.Automation.Condition[]]$conditions
        )
    }

    return $SearchRoot.FindFirst(
        [System.Windows.Automation.TreeScope]::Descendants,
        $searchCondition
    )
}

# ══════════════════════════════════════════════════════════════
# MAIN LOGIC
# ══════════════════════════════════════════════════════════════

try {
    $root = [System.Windows.Automation.AutomationElement]::RootElement

    # Find the target window by ProcessId
    $procCondition = New-Object System.Windows.Automation.PropertyCondition(
        [System.Windows.Automation.AutomationElement]::ProcessIdProperty,
        $ProcessId
    )
    $window = $root.FindFirst(
        [System.Windows.Automation.TreeScope]::Children,
        $procCondition
    )

    if ($null -eq $window) {
        [Console]::Out.Write((@{ success = $false; error = "No window found for ProcessId $ProcessId" } | ConvertTo-Json -Compress))
        exit 0
    }

    # Find the target element
    $element = Find-UIElement -SearchRoot $window -Name $Name -AutomationId $AutomationId -ControlType $ControlType -PartialMatch:$PartialMatch

    if ($null -eq $element) {
        $searchDesc = ""
        if ($AutomationId -ne "") { $searchDesc += "AutomationId='$AutomationId' " }
        if ($Name -ne "") { $searchDesc += "Name='$Name' " }
        if ($ControlType -ne "") { $searchDesc += "ControlType='$ControlType' " }
        if ($PartialMatch) { $searchDesc += "(partial match) " }
        [Console]::Out.Write((@{ success = $false; error = "Element not found: $($searchDesc.Trim())" } | ConvertTo-Json -Compress))
        exit 0
    }

    # Execute the action
    switch ($Action) {
        "sendkeys" {
            # Focus the element, then send keystrokes via SendKeys
            # This works for elements that don't support ValuePattern (e.g., web content, rich text)
            if ($Value -eq "") {
                [Console]::Out.Write((@{ success = $false; error = "Value parameter required for sendkeys action" } | ConvertTo-Json -Compress))
                exit 0
            }

            try {
                $element.SetFocus()
                Start-Sleep -Milliseconds 100

                # Use System.Windows.Forms.SendKeys for reliable text input
                # Escape special SendKeys characters: +, ^, %, ~, {, }, (, )
                $escaped = $Value -replace '([+^%~{}()\[\]])', '{$1}'
                [System.Windows.Forms.SendKeys]::SendWait($escaped)

                [Console]::Out.Write((@{
                    success = $true
                    action  = "sendkeys"
                    method  = "SendKeys"
                    value   = $Value
                } | ConvertTo-Json -Compress))
            } catch {
                [Console]::Out.Write((@{
                    success = $false
                    error   = "SendKeys failed: $($_.Exception.Message)"
                } | ConvertTo-Json -Compress))
            }
        }

        "scroll" {
            # Scroll using ScrollPattern
            try {
                $scrollPattern = $element.GetCurrentPattern([System.Windows.Automation.ScrollPattern]::Pattern)

                $amount = 3  # Default scroll amount (lines)
                if ($Value -ne "") {
                    $amount = [int]$Value
                }

                # ScrollPattern.Scroll uses ScrollAmount enum
                $scrollAmount = switch ($amount) {
                    1 { [System.Windows.Automation.ScrollAmount]::SmallIncrement }
                    default { [System.Windows.Automation.ScrollAmount]::LargeIncrement }
                }
                $noScroll = [System.Windows.Automation.ScrollAmount]::NoAmount

                switch ($Direction) {
                    "down"  { $scrollPattern.Scroll($noScroll, $scrollAmount) }
                    "up"    { $scrollPattern.Scroll($noScroll, [System.Windows.Automation.ScrollAmount]::SmallDecrement) }
                    "right" { $scrollPattern.Scroll($scrollAmount, $noScroll) }
                    "left"  { $scrollPattern.Scroll([System.Windows.Automation.ScrollAmount]::SmallDecrement, $noScroll) }
                }

                [Console]::Out.Write((@{
                    success   = $true
                    action    = "scroll"
                    direction = $Direction
                    amount    = $amount
                } | ConvertTo-Json -Compress))
            } catch {
                [Console]::Out.Write((@{
                    success = $false
                    error   = "ScrollPattern not supported or scroll failed: $($_.Exception.Message)"
                } | ConvertTo-Json -Compress))
            }
        }

        "get-patterns" {
            # List all supported UIA patterns on the element — useful for debugging
            $supported = @()
            $patternIds = $element.GetSupportedPatterns()

            foreach ($pid in $patternIds) {
                $supported += $pid.ProgrammaticName
            }

            $rect = $element.Current.BoundingRectangle
            $bounds = @{
                x      = [int]$rect.X
                y      = [int]$rect.Y
                width  = [int]$rect.Width
                height = [int]$rect.Height
            }

            [Console]::Out.Write((@{
                success      = $true
                action       = "get-patterns"
                name         = $element.Current.Name
                automationId = $element.Current.AutomationId
                controlType  = $element.Current.ControlType.ProgrammaticName
                className    = $element.Current.ClassName
                isEnabled    = $element.Current.IsEnabled
                patterns     = $supported
                bounds       = $bounds
            } | ConvertTo-Json -Depth 5 -Compress))
        }

        "click-at" {
            # Click at the element's center using Win32 mouse_event
            # More reliable than InvokePattern for some elements (e.g., custom controls)
            $rect = $element.Current.BoundingRectangle
            if ([double]::IsInfinity($rect.X) -or [double]::IsInfinity($rect.Y) -or $rect.Width -le 0 -or $rect.Height -le 0) {
                [Console]::Out.Write((@{
                    success = $false
                    error   = "Element has no valid bounds for coordinate click"
                } | ConvertTo-Json -Compress))
                exit 0
            }

            $clickX = [int]($rect.X + $rect.Width / 2)
            $clickY = [int]($rect.Y + $rect.Height / 2)

            try {
                [Win32Mouse]::ClickAt($clickX, $clickY)
                [Console]::Out.Write((@{
                    success    = $true
                    action     = "click-at"
                    method     = "Win32Mouse"
                    clickPoint = @{ x = $clickX; y = $clickY }
                } | ConvertTo-Json -Depth 5 -Compress))
            } catch {
                [Console]::Out.Write((@{
                    success = $false
                    error   = "Win32 click failed: $($_.Exception.Message)"
                    clickPoint = @{ x = $clickX; y = $clickY }
                } | ConvertTo-Json -Depth 5 -Compress))
            }
        }

        "wait-enabled" {
            # Poll until the element is enabled (or timeout after Value seconds)
            $timeout = 10
            if ($Value -ne "") { $timeout = [int]$Value }

            $deadline = (Get-Date).AddSeconds($timeout)
            $found = $false

            while ((Get-Date) -lt $deadline) {
                if ($element.Current.IsEnabled) {
                    $found = $true
                    break
                }
                Start-Sleep -Milliseconds 500
            }

            if ($found) {
                [Console]::Out.Write((@{
                    success = $true
                    action  = "wait-enabled"
                    enabled = $true
                } | ConvertTo-Json -Compress))
            } else {
                [Console]::Out.Write((@{
                    success = $false
                    action  = "wait-enabled"
                    enabled = $false
                    error   = "Element still disabled after ${timeout}s"
                } | ConvertTo-Json -Compress))
            }
        }
    }
} catch {
    [Console]::Out.Write((@{ success = $false; error = $_.Exception.Message } | ConvertTo-Json -Compress))
    exit 1
}
