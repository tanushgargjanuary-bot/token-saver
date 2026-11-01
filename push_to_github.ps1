# PowerShell Helper to Push to tanushgargjanuary-bot/token-saver
$ErrorActionPreference = "Continue"

Set-Location -Path $PSScriptRoot
Write-Host ">>> Initializing Git and committing project files..." -ForegroundColor Cyan

git init
git add .
git commit -m "Initial commit: TokenSaver & Active Session Ledger"
git branch -M main

# Reset remote if it was already set
git remote remove origin 2>$null
git remote add origin https://github.com/tanushgargjanuary-bot/token-saver.git

Write-Host ">>> Pushing to https://github.com/tanushgargjanuary-bot/token-saver..." -ForegroundColor Cyan
git push -u origin main --force

Write-Host "`n>>> COMPLETE! Visit: https://github.com/tanushgargjanuary-bot/token-saver" -ForegroundColor Green

