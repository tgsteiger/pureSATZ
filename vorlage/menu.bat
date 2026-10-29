@echo off
rem Menue mit den haeufigsten Befehlen (Windows): s schnell, k komplett, m MD oeffnen, o PDF oeffnen ...
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  where py >nul 2>nul && (py motor\einrichten.py) || (python motor\einrichten.py)
)
".venv\Scripts\python.exe" motor\menu.py %*
