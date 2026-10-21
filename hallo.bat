@echo off
rem Hallo-Buch: Beispielbuch anlegen, bauen und das PDF oeffnen (siehe START.md). Doppelklick genuegt.
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
  py setup\hallo.py %*
) else (
  where python >nul 2>nul && (python setup\hallo.py %*) || echo Python fehlt. Zuerst pc-einrichten\win-einrichten.bat doppelklicken - siehe START.md
)
pause
