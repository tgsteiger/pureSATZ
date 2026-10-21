@echo off
rem Ganzes Buch als ZIP sichern (Windows): sicherung.bat [lokal] [cloud]
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  where py >nul 2>nul && (py motor\einrichten.py) || (python motor\einrichten.py)
)
".venv\Scripts\python.exe" motor\sicherung.py %*
