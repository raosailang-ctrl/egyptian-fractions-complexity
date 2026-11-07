param(
    [string]$ConfigPath = (Join-Path $PSScriptRoot "config.toml"),
    [string]$ProfileDir = "C:\egypt fractions\chatgpt-automation-profile",
    [string]$DownloadDir = "C:\egypt fractions\chatgpt-automation-downloads",
    [int]$CdpPort = 9222,
    [switch]$Once,
    [int]$Rounds = 0,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
$pythonScript = Join-Path $PSScriptRoot "chatgpt_research_sync.py"
$exampleConfig = Join-Path $PSScriptRoot "config.example.toml"

if (-not (Test-Path -LiteralPath $ConfigPath)) {
    Copy-Item -LiteralPath $exampleConfig -Destination $ConfigPath
    throw "Created $ConfigPath from the example. Edit chat_url and paths, then run this script again."
}

New-Item -ItemType Directory -Force -Path $ProfileDir | Out-Null
New-Item -ItemType Directory -Force -Path $DownloadDir | Out-Null

$chromeCandidates = @(
    "C:\Program Files\Google\Chrome\Application\chrome.exe",
    "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
)
$chrome = $chromeCandidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if (-not $chrome) {
    throw "Google Chrome was not found in the standard installation directories."
}

$portInUse = Get-NetTCPConnection -LocalPort $CdpPort -State Listen -ErrorAction SilentlyContinue
if (-not $portInUse) {
    Start-Process -FilePath $chrome -ArgumentList @(
        "--user-data-dir=$ProfileDir",
        "--remote-debugging-port=$CdpPort",
        "--download-default-directory=$DownloadDir",
        "--no-first-run",
        "--no-default-browser-check",
        "https://chatgpt.com/"
    ) | Out-Null
    Start-Sleep -Seconds 2
}

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    throw "Python was not found on PATH. Install Python 3.10 or newer first."
}

$arguments = @($pythonScript, "--config", $ConfigPath)
if ($Once) { $arguments += "--once" }
if ($Rounds -gt 0) { $arguments += @("--rounds", [string]$Rounds) }
if ($DryRun) { $arguments += "--dry-run" }

& $python.Source @arguments
exit $LASTEXITCODE
