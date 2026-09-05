[CmdletBinding()]
param(
    [string]$DataRoot = 'D:\rgbww-optimizer',
    [string]$ParentRunName = '20260829-19-node-probes-rerun7',
    [string]$SuffixRunName = '20260901-19-node-probes-rerun7-suffix',
    [string]$CandidateRunName = '20260903-19-node-local-probe-candidates-r1',
    [string]$CandidateAnalysisPath = 'D:\rgbww-optimizer\guide9-white70-no-jac-probes-20260829\20260903-19-node-local-probe-candidates-analysis.json',
    [string]$ReassessmentRunName = '20260904-3-node-local-probe-reassessment-r1',
    [string]$ResumeRunRoot,
    [string]$ResumeRunName = 'resume-r1',
    [ValidateSet('Inspect', 'RunSuffix', 'CombineAnalyze', 'InspectCandidates', 'RunCandidates', 'AnalyzeCandidates', 'RunReassessment', 'Resume')]
    [string]$Action = 'Inspect'
)

$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent (Split-Path -Parent $PSCommandPath)
$python = Join-Path $DataRoot '.venv-windows\Scripts\python.exe'
$runParent = Join-Path $DataRoot 'guide9-white70-no-jac-probes-20260829'
$parentRoot = Join-Path $runParent $ParentRunName
$suffixRoot = Join-Path $runParent $SuffixRunName
$analysis = Join-Path $runParent 'guide9-white70-no-jac-probes-recovered-analysis.json'
$resumeRoot = if ($ResumeRunRoot) { $ResumeRunRoot } else { $parentRoot }

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
        'Resume' {
            & $python -m camera_based_rgbww_optimizer.optimization.guide9_white70_recovery `
                resume --run-root $resumeRoot --data-root $DataRoot `
                --output-dir $runParent --run-name $ResumeRunName
        }
        'CombineAnalyze' {
            & $python -m camera_based_rgbww_optimizer.optimization.guide9_white70_recovery `
                combine-analyze --parent-root $parentRoot --suffix-root $suffixRoot --output $analysis
        }
        'InspectCandidates' {
            & $python -m camera_based_rgbww_optimizer.optimization.guide9_white70_recovery `
                inspect-candidates --parent-root $parentRoot --analysis $analysis --data-root $DataRoot
        }
        'RunCandidates' {
            & $python -m camera_based_rgbww_optimizer.optimization.guide9_white70_recovery `
                run-candidates --parent-root $parentRoot --analysis $analysis --data-root $DataRoot `
                --output-dir $runParent --run-name $CandidateRunName
        }
        'AnalyzeCandidates' {
            & $python -m camera_based_rgbww_optimizer.optimization.guide9_white70_recovery `
                analyze-candidates --run-root (Join-Path $runParent $CandidateRunName) `
                --output $CandidateAnalysisPath
        }
        'RunReassessment' {
            & $python -m camera_based_rgbww_optimizer.optimization.guide9_white70_recovery `
                run-reassessment --candidate-root (Join-Path $runParent $CandidateRunName) `
                --candidate-analysis $CandidateAnalysisPath `
                --probe-analysis $analysis --data-root $DataRoot --output-dir $runParent `
                --run-name $ReassessmentRunName
        }
    }
    if ($LASTEXITCODE -ne 0) { throw "GUIDE9 recovery action failed with exit code $LASTEXITCODE" }
}
finally {
    & $python -m camera_based_rgbww_optimizer.control.all_off --ray-timeout 5
}
