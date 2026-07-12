$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectDir = Split-Path -Parent $ScriptDir
$LogDir = Join-Path $ProjectDir "logs"

New-Item -ItemType Directory -Force -Path $LogDir | Out-Null

# Load .env
$envFile = Join-Path $ProjectDir ".env"
if (Test-Path $envFile) {
    Get-Content $envFile | Where-Object { $_ -match '^[^#]' } | ForEach-Object {
        $name, $value = $_ -split '=', 2
        [Environment]::SetEnvironmentVariable($name.Trim(), $value.Trim(), "Process")
    }
}

$backendLog = Join-Path $LogDir "backend.log"
$frontendLog = Join-Path $LogDir "frontend.log"

Write-Host "Starting backend (FastAPI)..."
$backendJob = Start-Job -ScriptBlock {
    param($wd, $log)
    Set-Location $wd
    uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
} -ArgumentList (Join-Path $ProjectDir "backend"), $backendLog

$frontendJob = Start-Job -ScriptBlock {
    param($wd, $port, $log)
    Set-Location $wd
    npm run start -- --port $port *> $log
} -ArgumentList (Join-Path $ProjectDir "frontend"), 3000, $frontendLog

$backendJob | Out-Null
$frontendJob | Out-Null

Start-Sleep -Seconds 5

try {
    Invoke-RestMethod http://localhost:8000/health -ErrorAction Stop | Out-Null
    Write-Host "Backend OK at http://localhost:8000"
} catch {
    Write-Host "WARNING: Backend health check failed. See logs/backend.log"
}

Write-Host "Done. Backend: http://localhost:8000  Frontend: http://localhost:3000"
