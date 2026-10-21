@echo off
rem Geschichten sammeln (Windows): neu.bat "Titel der Geschichte" / neu.bat = Uebersicht
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  where py >nul 2>nul && (py motor\einrichten.py) || (python motor\einrichten.py)
)
".venv\Scripts\python.exe" motor\geschichten.py %*
