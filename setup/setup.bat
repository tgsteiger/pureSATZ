@echo off
rem Neues Buch anlegen oder Motor aktualisieren (Windows, im Ordner pureSATZ): setup\setup.bat / setup\setup.bat motor ..\Buch
where py >nul 2>nul && (py "%~dp0setup.py" %*) || (python "%~dp0setup.py" %*)
