@echo off
rem =====================================================================
rem  pureSATZ starten (Windows) - Doppelklick genuegt.
rem  1. Ort: schlaegt C:\Users\<Name>\Buchprojekte vor und kopiert pureSATZ dorthin
rem  2. Computer einrichten (pc-einrichten\win-einrichten.bat)
rem  3. Hallo-Buch ansehen, eigenes Buch anlegen, GitHub (freiwillig)
rem  Darf beliebig oft laufen. Mit git geholt oder schon in Buchprojekte: kein Kopieren.
rem =====================================================================
setlocal
cd /d "%~dp0"
set "HIER=%CD%"
for %%I in ("%HIER%\..") do set "OBENNAME=%%~nxI"
echo === pureSATZ ===
echo.

rem --- ZIP ausgepackt? (aus dem ZIP heraus fehlt der Rest) ---------------
if exist "%HIER%\motor\bauen.py" goto ausgepackt
echo Das ZIP ist noch nicht ausgepackt.
echo Bitte: Rechtsklick auf die ZIP-Datei - "Alle extrahieren ..." -
echo dann im ausgepackten Ordner start.bat doppelklicken.
echo.
pause
exit /b 1
:ausgepackt

rem --- 1. Ort fuer die Buchprojekte ---------------------------------------
if /i "%~1"=="--hier" goto einrichten
if exist "%HIER%\.git" goto einrichten
if /i "%OBENNAME%"=="Buchprojekte" goto einrichten

set "ZIEL=%USERPROFILE%\Buchprojekte"
echo pureSATZ liegt in:  %HIER%
echo Deine Buecher entstehen neben pureSATZ. Empfohlen ist ein fester Ort -
echo nicht Downloads oder Desktop und nicht OneDrive.
echo.
set "ORT="
set /p "ORT=Ort fuer Buchprojekte [%ZIEL%], n = hier bleiben: "
if defined ORT set "ORT=%ORT:"=%"
if /i "%ORT%"=="n" goto einrichten
if /i "%ORT%"=="nein" goto einrichten
if defined ORT set "ZIEL=%ORT%"
if /i "%HIER%"=="%ZIEL%\pureSATZ" goto einrichten

for /f "usebackq delims=" %%v in ("%HIER%\motor\VERSION") do set "VNEU=%%v"
if not exist "%ZIEL%\pureSATZ\motor\VERSION" goto kopieren
for /f "usebackq delims=" %%v in ("%ZIEL%\pureSATZ\motor\VERSION") do set "VALT=%%v"
echo.
echo pureSATZ %VALT% ist dort schon vorhanden (diese Version: %VNEU%).
set "ERS=j"
set /p "ERS=Ersetzen? Die alte bleibt als pureSATZ-alt-%VALT%. [j/n] (j): "
if /i "%ERS%"=="ja" set "ERS=j"
if /i not "%ERS%"=="j" goto dort_weiter
set "ALTNAME=pureSATZ-alt-%VALT%"
if exist "%ZIEL%\%ALTNAME%" set "ALTNAME=%ALTNAME%-%RANDOM%"
ren "%ZIEL%\pureSATZ" "%ALTNAME%"
if errorlevel 1 goto ren_fehler
echo OK  alte Version: %ZIEL%\%ALTNAME%

:kopieren
if not exist "%ZIEL%" mkdir "%ZIEL%"
if not exist "%ZIEL%" goto kopier_fehler
echo pureSATZ wird nach %ZIEL%\pureSATZ kopiert ...
robocopy "%HIER%" "%ZIEL%\pureSATZ" /E /XD .venv __pycache__ /NFL /NDL /NJH /NJS /NP >nul
if errorlevel 8 goto kopier_fehler
echo OK  kopiert.

rem Terminal hier: Doppelklick oeffnet das Befehlsfenster (cmd) in diesem Ordner
if exist "%ZIEL%\Terminal hier.bat" goto terminal_da
>"%ZIEL%\Terminal hier.bat" echo @cd /d "%%~dp0" ^& cmd /k
:terminal_da

echo.
set "VK=j"
set /p "VK=Verknuepfung Buchprojekte auf dem Desktop anlegen? [j/n] (j): "
if /i "%VK%"=="ja" set "VK=j"
if /i not "%VK%"=="j" goto explorer
powershell -NoProfile -ExecutionPolicy Bypass -Command "$s=(New-Object -ComObject WScript.Shell).CreateShortcut([Environment]::GetFolderPath('Desktop')+'\Buchprojekte.lnk'); $s.TargetPath='%ZIEL%'; $s.Save()" >nul 2>nul
if errorlevel 1 (echo Verknuepfung ging nicht - nicht schlimm.) else (echo OK  Verknuepfung Buchprojekte auf dem Desktop)

:explorer
start "" explorer "%ZIEL%"
echo.
echo Ab jetzt geht es in %ZIEL%\pureSATZ weiter.
echo Den Ordner %HIER% darfst du nach dem Einrichten loeschen.
echo.
:dort_weiter
"%ZIEL%\pureSATZ\start.bat" --hier

rem --- 2. Computer einrichten, Hallo-Buch, eigenes Buch ---------------------
:einrichten
call "%HIER%\pc-einrichten\win-einrichten.bat"
exit /b

:ren_fehler
echo Umbenennen ging nicht. Ist ein Fenster oder Programm in %ZIEL%\pureSATZ offen?
echo Schliessen und start.bat nochmals doppelklicken.
pause
exit /b 1
:kopier_fehler
echo Kopieren nach %ZIEL% ging nicht. Anderen Ort waehlen oder "n" fuer hier bleiben.
pause
exit /b 1
