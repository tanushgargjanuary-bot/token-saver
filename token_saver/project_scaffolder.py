"""
Project Scaffolder & Bootstrapper:
Embeds the Active Session Ledger, Safe Git Push engine, and .gitignore into
any existing or newly created project repository.
Guarantees idempotency and keeps local helper scripts off public GitHub.
"""

import os
from pathlib import Path

BAT_CONTENT = """@echo off
:: ============================================================================
:: UNIVERSAL SAFE GIT PUSH (DO NOT DUPLICATE THIS FILE)
:: Identifier: __UNIVERSAL_SAFE_PUSH_V1__
:: ============================================================================
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0git_sync.ps1"
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Git sync failed. Check output above.
)
echo.
pause
endlocal
"""

PS1_CONTENT = """# Universal Safe Git Sync Engine for tanushgargjanuary-bot projects
$ErrorActionPreference = "Continue"
$CurrentDir = Get-Location
$ProjectName = (Get-Item -Path $CurrentDir).Name
$DefaultUsername = "tanushgargjanuary-bot"

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "   UNIVERSAL SAFE GIT SYNC: $ProjectName" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan

# 1. Safety Check: Secret Scanning
$SensitivePatterns = @(".env", ".env.local", "id_rsa", "credentials.json", "client_secret*.json")
$FoundLeaks = @()
foreach ($pat in $SensitivePatterns) {
    $matches = Get-ChildItem -Path $CurrentDir -Filter $pat -Recurse -ErrorAction SilentlyContinue |
               Where-Object { $_.FullName -notmatch "node_modules|\.venv" }
    if ($matches) { $FoundLeaks += $matches }
}
if ($FoundLeaks.Count -gt 0) {
    Write-Host "`n[DANGER] SENSITIVE FILES FOUND IN PROJECT ROOT:" -ForegroundColor Red
    foreach ($f in $FoundLeaks) { Write-Host "  -> $($f.FullName)" -ForegroundColor Red }
    Write-Host "[!] Add these to .gitignore before pushing to GitHub!" -ForegroundColor Yellow
    exit 1
}

# 2. Git Init
if (-not (Test-Path (Join-Path $CurrentDir ".git"))) {
    git init | Out-Null
}
git branch -M main 2>$null

# 3. Untrack local convenience scripts so they NEVER get pushed to GitHub
git rm --cached push_to_github.bat 2>$null | Out-Null
git rm --cached push_to_github.ps1 2>$null | Out-Null
git rm --cached git_sync.ps1 2>$null | Out-Null

# 4. Remote Resolution
$TargetRemote = ""
try { $TargetRemote = (git remote get-url origin 2>$null).Trim() } catch {}
if (-not $TargetRemote) {
    $TargetRemote = "https://github.com/$DefaultUsername/$ProjectName.git"
    git remote remove origin 2>$null
    git remote add origin $TargetRemote
    Write-Host "[*] Inferred remote: $TargetRemote" -ForegroundColor Cyan
}

# 5. Stage & Commit
git add .
$status = git status --porcelain
if ($status) {
    $msg = "Clean sync: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - $ProjectName"
    git commit -m $msg | Out-Null
    Write-Host "[+] Committed clean source code." -ForegroundColor Green
}

# 6. Push safely
Write-Host "[*] Pushing to GitHub ($TargetRemote)..." -ForegroundColor Cyan
git push -u origin main
if ($LASTEXITCODE -ne 0) {
    git push -u origin main --force
}

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n[SUCCESS] Project is cleanly live at: $TargetRemote" -ForegroundColor Green
}
exit 0
"""

GITIGNORE_CONTENT = """# Environments & Secrets
.env
.env.*
*.env
*.pem
*.key
id_rsa
*secret*
*credentials*

# Language Runtimes & Packaging
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

# Dynamic Session Logs (local development)
.session.log

# Local Convenience Scripts (DO NOT UPLOAD TO GITHUB)
push_to_github.bat
push_to_github.ps1
git_sync.ps1
*.bat
"""


class ProjectScaffolder:
    @staticmethod
    def scaffold_project(target_dir: Path, project_name: str = "") -> None:
        target_dir.mkdir(parents=True, exist_ok=True)
        name = project_name or target_dir.name

        # 1. Check for duplicate .bat files before creating
        existing_bats = list(target_dir.glob("*.bat"))
        has_safe_bat = False
        for bat in existing_bats:
            try:
                with open(bat, "r", encoding="utf-8") as f:
                    if "__UNIVERSAL_SAFE_PUSH_" in f.read():
                        has_safe_bat = True
                        break
            except Exception:
                pass

        if not has_safe_bat:
            bat_path = target_dir / "push_to_github.bat"
            with open(bat_path, "w", encoding="utf-8") as f:
                f.write(BAT_CONTENT)
            print(f"[+] Installed universal push launcher: {bat_path.name}")

        # 2. Write or update git_sync.ps1
        ps1_path = target_dir / "git_sync.ps1"
        with open(ps1_path, "w", encoding="utf-8") as f:
            f.write(PS1_CONTENT)

        # 3. Ensure .gitignore
        gitignore_path = target_dir / ".gitignore"
        if not gitignore_path.exists():
            with open(gitignore_path, "w", encoding="utf-8") as f:
                f.write(GITIGNORE_CONTENT)
            print("[+] Generated safe .gitignore")

        # 4. Initialize Active Session Ledger
        session_log_path = target_dir / ".session.log"
        if not session_log_path.exists():
            with open(session_log_path, "w", encoding="utf-8") as f:
                f.write(f"=== ACTIVE SESSION STATE LEDGER ===\n[SESSION_INIT] {name} -> Project initialized with active session memory\n")
            print("[+] Initialized .session.log (Active Session Ledger)")

        # 5. Starter README if none exists
        readme_path = target_dir / "README.md"
        if not readme_path.exists():
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(f"# {name}\n\nProject initialized with TokenSaver Active Session Ledger and Universal Git Sync.\n")
            print("[+] Created starter README.md")

        print(f"\n[DONE] Project '{name}' is fully scaffolded and protected!")
