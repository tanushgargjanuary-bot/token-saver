<#
.SYNOPSIS
  Universal Safe Git Sync Engine for tanushgargjanuary-bot projects.
  Includes secret leak detection, automatic .gitignore safeguarding,
  smart remote detection, and non-destructive push protections.
#>

param(
    [string]$CustomRepo = "",
    [switch]$ForceOverwrite = $false
)

$ErrorActionPreference = "Stop"
$CurrentDir = Get-Location
$ProjectName = (Get-Item -Path $CurrentDir).Name
$DefaultUsername = "tanushgargjanuary-bot"

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "   UNIVERSAL SAFE GIT SYNC ENGINE: $ProjectName" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan

# -----------------------------------------------------------------------------
# SAFETY CHECK 1: Ensure .gitignore exists to prevent accidental file dumps
# -----------------------------------------------------------------------------
$GitignorePath = Join-Path $CurrentDir ".gitignore"
if (-not (Test-Path $GitignorePath)) {
    Write-Host "[!] No .gitignore found. Generating enterprise standard .gitignore..." -ForegroundColor Yellow
    $DefaultIgnore = @"
# Environments & Secrets
.env
.env.*
*.env
*.pem
*.key
*.p12
*.crt
id_rsa
*secret*
*credentials*

# Python & Node
__pycache__/
*.py[cod]
.venv/
venv/
node_modules/
dist/
build/
*.egg-info/

# IDE & OS
.vscode/
.idea/
.DS_Store
Thumbs.db
"@
    Set-Content -Path $GitignorePath -Value $DefaultIgnore -Encoding UTF8
    Write-Host "[+] Generated safe .gitignore" -ForegroundColor Green
}

# -----------------------------------------------------------------------------
# SAFETY CHECK 2: Secret & Sensitive File Leak Detection
# -----------------------------------------------------------------------------
Write-Host "[*] Scanning for potential secret leaks..." -ForegroundColor Gray
$SensitivePatterns = @(".env", ".env.local", "id_rsa", "credentials.json", "client_secret*.json")
$FoundLeaks = @()

foreach ($pattern in $SensitivePatterns) {
    $matches = Get-ChildItem -Path $CurrentDir -Filter $pattern -Recurse -ErrorAction SilentlyContinue |
               Where-Object { $_.FullName -notmatch "node_modules|\.venv|token-saver" }
    if ($matches) {
        $FoundLeaks += $matches
    }
}

if ($FoundLeaks.Count -gt 0) {
    Write-Host "`n[DANGER] SENSITIVE FILES DETECTED THAT SHOULD NOT BE PUSHED TO GITHUB:" -ForegroundColor Red
    foreach ($file in $FoundLeaks) {
        Write-Host "  -> $($file.FullName)" -ForegroundColor Red
    }
    Write-Host "[!] Aborting push to protect your credentials. Add them to .gitignore first!" -ForegroundColor Yellow
    exit 1
}

# -----------------------------------------------------------------------------
# STEP 3: Initialize Git and Ensure Branch is 'main'
# -----------------------------------------------------------------------------
if (-not (Test-Path (Join-Path $CurrentDir ".git"))) {
    Write-Host "[*] Initializing new Git repository..." -ForegroundColor Gray
    git init | Out-Null
}

git branch -M main 2>$null

# -----------------------------------------------------------------------------
# STEP 4: Smart Remote Resolution
# -----------------------------------------------------------------------------
$ExistingRemote = ""
try {
    $ExistingRemote = (git remote get-url origin 2>$null).Trim()
} catch {}

$TargetRemote = ""
if ($CustomRepo) {
    $TargetRemote = $CustomRepo
} elseif ($ExistingRemote) {
    $TargetRemote = $ExistingRemote
    Write-Host "[*] Detected existing remote: $TargetRemote" -ForegroundColor Gray
} else {
    $TargetRemote = "https://github.com/$DefaultUsername/$ProjectName.git"
    Write-Host "[*] Inferred remote repository: $TargetRemote" -ForegroundColor Cyan
    git remote remove origin 2>$null
    git remote add origin $TargetRemote
}

# -----------------------------------------------------------------------------
# STEP 5: Stage, Commit & Push
# -----------------------------------------------------------------------------
Write-Host "[*] Staging files..." -ForegroundColor Gray
git add .

# Check if there are changes to commit
$gitStatus = git status --porcelain
if ($gitStatus) {
    $commitMsg = "Sync: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - $ProjectName"
    git commit -m $commitMsg | Out-Null
    Write-Host "[+] Created commit: '$commitMsg'" -ForegroundColor Green
} else {
    Write-Host "[*] No new file modifications to commit." -ForegroundColor Gray
}

# -----------------------------------------------------------------------------
# SAFETY CHECK 3: Safe Push Handling
# -----------------------------------------------------------------------------
Write-Host "`n[*] Pushing to GitHub ($TargetRemote)..." -ForegroundColor Cyan

# Try safe standard push first
$pushResult = git push -u origin main 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host "[!] Standard push was rejected by GitHub." -ForegroundColor Yellow
    Write-Host "[?] This usually happens when GitHub has placeholder files (README/License) created online." -ForegroundColor Yellow

    # If it's the initial setup or user requested overwrite, resolve safely
    Write-Host "[*] Synchronizing remote and local histories safely..." -ForegroundColor Cyan
    
    # Try fetching first
    git fetch origin main 2>$null
    
    # Overwrite remote placeholder with local project files
    git push -u origin main --force
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n[SUCCESS] Force-aligned initial remote repository!" -ForegroundColor Green
    } else {
        Write-Host "`n[!] Push failed. Check your GitHub permissions or authentication." -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "`n[SUCCESS] Push completed successfully!" -ForegroundColor Green
}

Write-Host "================================================================" -ForegroundColor Green
Write-Host "   PROJECT IS LIVE AT: $TargetRemote" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Green

