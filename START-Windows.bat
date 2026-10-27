@echo off
rem =====================================================================
rem  pureSATZ starten (Windows) - Doppelklick genuegt.
rem  Fuehrt in fuenf Schritten durch: Technik, Ort fuer die Buecher,
rem  Hallo-Buch, dein eigenes Buch, Fertig und Extras.
rem  Die Arbeit macht pc-einrichten\win-einrichten.bat.
rem =====================================================================
cd /d "%~dp0"
if exist "%~dp0pc-einrichten\win-einrichten.bat" goto los
echo Das ZIP ist noch nicht ausgepackt.
echo Bitte: Rechtsklick auf die ZIP-Datei - "Alle extrahieren ..." -
echo dann im ausgepackten Ordner START-Windows.bat doppelklicken.
echo.
pause
exit /b 1
:los
call "%~dp0pc-einrichten\win-einrichten.bat" %*
