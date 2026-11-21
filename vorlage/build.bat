@echo off
rem Buch bauen (Windows): build.bat final, build.bat schnell ... Alle Befehle: build.bat befehle
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  where py >nul 2>nul && (py motor\einrichten.py) || (python motor\einrichten.py)
)
".venv\Scripts\python.exe" motor\bauen.py %*
