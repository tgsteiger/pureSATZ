@echo off
rem Buchdaten mit GitHub abgleichen (Windows), am Anfang und am Ende der Arbeit
cd /d "%~dp0"
if exist ".venv\Scripts\python.exe" (".venv\Scripts\python.exe" motor\sync.py %*) else (where py >nul 2>nul && (py motor\sync.py %*) || (python motor\sync.py %*))
