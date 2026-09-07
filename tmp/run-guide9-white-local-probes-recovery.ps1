[CmdletBinding()]
param(
    [string]$DataRoot = 'D:\rgbww-optimizer',
    [string]$PrefixRoot = 'D:\rgbww-optimizer\guide9-white-local-probes-20260824\20260824-092424-no-model6',
    [string]$RecoveryRoot = 'D:\rgbww-optimizer\guide9-white-local-probes-recovery-20260824\20260905-remaining-two-node-probes-r1',
    [string]$ResumeRoot = 'D:\rgbww-optimizer\guide9-white-local-probes-recovery-20260824\20260906-remaining-two-node-probes-r1-suffix',
    [string]$OutputDir = 'D:\rgbww-optimizer\guide9-white-local-probes-recovery-20260824',
    [string]$RunName = '20260905-remaining-two-node-probes-r1',
    [string]$AnalysisPath = 'D:\rgbww-optimizer\guide9-white-local-probes-recovery-20260824\guide9-white-local-probes-recovered-analysis.json',
    [ValidateSet('RunRemaining', 'CombineAnalyze', 'InspectCandidates', 'RunCandidates', 'AnalyzeCandidates')]
    [string]$Action = 'RunRemaining'
)

$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent (Split-Path -Parent $PSCommandPath)
$python = Join-Path $DataRoot '.venv-windows\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $python)) { throw "Windows experiment Python is missing: $python" }
Set-Location $projectRoot
try {
    switch ($Action) {
        'RunRemaining' {
            & $python -m camera_based_rgbww_optimizer.optimization.guide9_white70_recovery `
                run-remaining-probes --prefix-root $PrefixRoot --data-root $DataRoot `
                --output-dir $OutputDir --run-name $RunName
        }
        'CombineAnalyze' {
            & $python -m camera_based_rgbww_optimizer.optimization.guide9_white70_recovery `
                combine-recovered-probes --prefix-root $PrefixRoot --recovery-root $RecoveryRoot `
                --resume-root $ResumeRoot --output $AnalysisPath
        }
        'InspectCandidates' {
            & $python -m camera_based_rgbww_optimizer.optimization.guide9_white70_recovery `
                inspect-candidates --parent-root $PrefixRoot --analysis $AnalysisPath `
                --data-root $DataRoot
        }
        'RunCandidates' {
            & $python -m camera_based_rgbww_optimizer.optimization.guide9_white70_recovery `
                run-candidates --parent-root $PrefixRoot --analysis $AnalysisPath `
                --data-root $DataRoot --output-dir $OutputDir --run-name $RunName
        }
        'AnalyzeCandidates' {
            & $python -m camera_based_rgbww_optimizer.optimization.guide9_white70_recovery `
                analyze-candidates --run-root (Join-Path $OutputDir $RunName) `
                --output (Join-Path $OutputDir "$RunName-analysis.json")
        }
    }
    if ($LASTEXITCODE -ne 0) { throw "GUIDE9 remaining probe recovery failed with exit code $LASTEXITCODE" }
}
finally {
    & $python -m camera_based_rgbww_optimizer.control.all_off --ray-timeout 5
}
