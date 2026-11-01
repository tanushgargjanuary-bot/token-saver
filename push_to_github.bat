@echo off
cd /d "%~dp0"
echo ========================================================
echo   PUSHING TO GITHUB: tanushgargjanuary-bot/token-saver
echo ========================================================
echo.

git init
git add .
git commit -m "Initial commit: TokenSaver & Active Session Ledger"
git branch -M main
git remote remove origin 2>nul
git remote add origin https://github.com/tanushgargjanuary-bot/token-saver.git

echo.
echo Pushing files to main branch...
git push -u origin main --force

echo.
echo ========================================================
echo   DONE! Check your repo at:
echo   https://github.com/tanushgargjanuary-bot/token-saver
echo ========================================================
pause

