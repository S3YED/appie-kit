<#
.SYNOPSIS
    Shim — returns window list. Use get-screen-context.ps1 for combined data.
#>
try {
    Add-Type -AssemblyName UIAutomationClient
    Add-Type -AssemblyName UIAutomationTypes
} catch {
    [Console]::Out.Write((@() | ConvertTo-Json -Compress))
    exit 0
}

$ErrorActionPreference = 'Stop'

try {
    $root = [System.Windows.Automation.AutomationElement]::RootElement
    $windowCondition = New-Object System.Windows.Automation.PropertyCondition(
        [System.Windows.Automation.AutomationElement]::ControlTypeProperty,
        [System.Windows.Automation.ControlType]::Window
    )
    $allWindows = $root.FindAll(
        [System.Windows.Automation.TreeScope]::Children,
        $windowCondition
    )

    $windowList = @()
    foreach ($win in $allWindows) {
        try {
            $c = $win.Current
            if (-not $c.Name -or $c.Name.Trim().Length -eq 0) { continue }
            $processName = ""
            try {
                $proc = [System.Diagnostics.Process]::GetProcessById($c.ProcessId)
                $processName = $proc.ProcessName
            } catch { $processName = "unknown" }

            $rect = $c.BoundingRectangle
            if ([double]::IsInfinity($rect.X)) {
                $bounds = @{ x = 0; y = 0; width = 0; height = 0 }
            } else {
                $bounds = @{ x = [int]$rect.X; y = [int]$rect.Y; width = [int]$rect.Width; height = [int]$rect.Height }
            }

            $isMinimized = $false
            try {
                $winPattern = $win.GetCurrentPattern([System.Windows.Automation.WindowPattern]::Pattern)
                if ($winPattern.Current.WindowVisualState -eq [System.Windows.Automation.WindowVisualState]::Minimized) {
                    $isMinimized = $true
                }
            } catch {}

            $windowList += [ordered]@{
                handle      = $c.NativeWindowHandle
                title       = $c.Name
                processName = $processName
                processId   = $c.ProcessId
                bounds      = $bounds
                isMinimized = $isMinimized
            }
        } catch {}
    }

    [Console]::Out.Write(($windowList | ConvertTo-Json -Depth 10 -Compress))
} catch {
    [Console]::Out.Write((@() | ConvertTo-Json -Compress))
}
