[CmdletBinding()]
param(
    [string]$DataRoot = 'D:\rgbww-optimizer',
    [string]$ParentRunName = '20260829-19-node-probes-rerun7',
    [string]$SuffixRunName = '20260901-19-node-probes-rerun7-suffix',
    [ValidateSet('Inspect', 'RunSuffix', 'CombineAnalyze')]
    [string]$Action = 'Inspect'
)

$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent (Split-Path -Parent $PSCommandPath)
$python = Join-Path $DataRoot '.venv-windows\Scripts\python.exe'
$runParent = Join-Path $DataRoot 'guide9-white70-no-jac-probes-20260829'
$parentRoot = Join-Path $runParent $ParentRunName
$suffixRoot = Join-Path $runParent $SuffixRunName
$analysis = Join-Path $runParent 'guide9-white70-no-jac-probes-recovered-analysis.json'

if (-not (Test-Path -LiteralPath $python)) {
    throw "Windows experiment Python is missing: $python"
}

Set-Location $projectRoot
try {
    switch ($Action) {
        'Inspect' {
            & $python -m camera_based_rgbww_optimizer.optimization.guide9_white70_recovery `
                inspect --parent-root $parentRoot
        }
        'RunSuffix' {
            & $python -m camera_based_rgbww_optimizer.optimization.guide9_white70_recovery `
                run-suffix --parent-root $parentRoot --data-root $DataRoot `
                --output-dir $runParent --run-name $SuffixRunName
        }
        'CombineAnalyze' {
            & $python -m camera_based_rgbww_optimizer.optimization.guide9_white70_recovery `
                combine-analyze --parent-root $parentRoot --suffix-root $suffixRoot --output $analysis
        }
    }
    if ($LASTEXITCODE -ne 0) { throw "GUIDE9 recovery action failed with exit code $LASTEXITCODE" }
}
finally {
    & $python -m camera_based_rgbww_optimizer.control.all_off --ray-timeout 5
}
