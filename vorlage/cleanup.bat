@echo off
rem Aufraeumen (Windows), fragt zuerst. cleanup.bat ausgaben = auch Ausgabeordner
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  where py >nul 2>nul && (py motor\einrichten.py) || (python motor\einrichten.py)
)
".venv\Scripts\python.exe" motor\aufraeumen.py %*
