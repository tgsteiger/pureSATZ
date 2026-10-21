@echo off
rem Motor-Update (Windows): update.bat / update.bat pruefen / update.bat ja
cd /d "%~dp0"
where py >nul 2>nul && (py motor\update.py %*) || (python motor\update.py %*)
