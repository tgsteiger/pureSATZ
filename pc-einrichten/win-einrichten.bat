@echo off
rem =====================================================================
rem  pureSATZ - Windows einrichten (einmalig)
rem  Doppelklicken oder im Ordner pureSATZ:  .\pc-einrichten\win-einrichten.bat
rem  Darf beliebig oft laufen - Erledigtes wird uebersprungen.
rem  GitHub ist freiwillig: Ohne GitHub geht Schreiben und Bauen genauso.
rem =====================================================================
setlocal
cd /d "%~dp0.."
set "HIER=%CD%"
for %%I in ("%HIER%\..") do set "OBEN=%%~fI"
echo === pureSATZ: Windows einrichten ===
echo.

rem --- 1. Python 3.10+ ---------------------------------------------------
set "PY="
py -3 -c "import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)" >nul 2>nul && set "PY=py -3"
if not defined PY python -c "import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)" >nul 2>nul && set "PY=python"
if defined PY goto python_ok
echo Schritt 1: Es fehlt ein aktuelles Python (3.10 oder neuer).
where winget >nul 2>nul || goto python_web
echo Es wird jetzt installiert (winget). Bitte allfaellige Fenster bestaetigen.
winget install -e --source winget --id Python.Python.3.12 --accept-package-agreements --accept-source-agreements
if errorlevel 1 (echo. & echo winget ging nicht - Python bitte von Hand installieren: & goto python_web)
echo.
echo Danach dieses Fenster SCHLIESSEN und win-einrichten.bat NOCHMALS starten.
goto ende
:python_web
echo Variante 1 - in PowerShell eingeben:
echo    winget install -e --source winget --id Python.Python.3.12
echo Variante 2 - Gleich oeffnet sich python.org: den neusten "Windows installer (64-bit)" laden.
echo WICHTIG: beim Installieren unten den Haken "Add python.exe to PATH" setzen.
echo Danach dieses Fenster schliessen und win-einrichten.bat nochmals starten.
start "" "https://www.python.org/downloads/windows/"
goto ende
:python_ok
for /f "delims=" %%v in ('%PY% --version') do echo OK  %%v

rem --- 2. GitHub (freiwillig) -------------------------------------------
echo.
echo GitHub brauchst du nur fuer: Buch auf mehreren Computern (sync.bat)
echo und Motor-Updates direkt aus dem Buch (update.bat).
set "GH=n"
set /p "GH=Mit GitHub arbeiten? [j/n] (n): "
if /i "%GH%"=="ja" set "GH=j"
if /i not "%GH%"=="j" goto ohne_github

set "NEU="
where git >nul 2>nul || (echo git wird installiert ... & winget install -e --source winget --id Git.Git --accept-package-agreements --accept-source-agreements & set "NEU=1")
where gh >nul 2>nul || (echo GitHub-Programm gh wird installiert ... & winget install -e --source winget --id GitHub.cli --accept-package-agreements --accept-source-agreements & set "NEU=1")
if not defined NEU goto werkzeuge_ok
echo.
echo Programme installiert. Dieses Fenster SCHLIESSEN und win-einrichten.bat NOCHMALS starten.
goto ende
:werkzeuge_ok
for /f "delims=" %%v in ('git --version') do echo OK  %%v

set "N="
for /f "delims=" %%n in ('git config --global user.name') do set "N=%%n"
if defined N goto name_ok
set /p "N=Dein Name fuer git (z. B. Anna Muster): "
if defined N git config --global user.name "%N%"
:name_ok
set "M="
for /f "delims=" %%m in ('git config --global user.email') do set "M=%%m"
if defined M goto mail_ok
echo Mail fuer git: am besten die geschuetzte GitHub-Adresse
echo (GitHub - Settings - Emails - "Keep my email addresses private").
set /p "M=Mail: "
if defined M git config --global user.email "%M%"
:mail_ok
echo OK  git: %N% ^<%M%^>

gh auth status >nul 2>nul && goto angemeldet
echo.
echo Jetzt bei GitHub anmelden. Antworten: GitHub.com - HTTPS - Yes - Login with a web browser
gh auth login
gh auth status >nul 2>nul || (echo Anmeldung abgebrochen - spaeter nochmals starten. & goto ende)
:angemeldet
gh auth setup-git >nul 2>nul
set "BESITZER="
for /f "delims=" %%u in ('gh api user --jq .login') do set "BESITZER=%%u"
echo OK  bei GitHub angemeldet als %BESITZER%

:buch_holen
echo.
set "R="
set /p "R=Eigenes Buch von GitHub holen? Repository-Name (z. B. mein-buch), leer = weiter: "
if not defined R goto neues_buch
set "QUELLE=%BESITZER%/%R%"
echo %R% | find "/" >nul && set "QUELLE=%R%"
for %%a in ("%R:/=\%") do set "O=%%~nxa"
set /p "O=Ordnername [%O%]: "
if exist "%OBEN%\%O%\.git" (
    echo Schon da: %OBEN%\%O% - hole neusten Stand
    pushd "%OBEN%\%O%" & call sync.bat & popd
) else (
    gh repo clone "%QUELLE%" "%OBEN%\%O%" || goto buch_holen
)
set "B=n"
set /p "B=Jetzt einmal bauen (richtet beim ersten Mal Python ein, ca. 1-2 Min)? [j/n] "
if /i "%B%"=="j" (pushd "%OBEN%\%O%" & call build.bat schnell & popd)
goto buch_holen

:ohne_github
echo OK  ohne GitHub. Gesichert wird mit  sicherung.bat  (ZIP).

rem --- 3. Neues Buch? ----------------------------------------------------
:neues_buch
echo.
set "NB=n"
set /p "NB=Jetzt ein neues Buch anlegen (setup\setup.bat)? [j/n] (n): "
if /i "%NB%"=="ja" set "NB=j"
if /i "%NB%"=="j" call setup\setup.bat

echo.
echo === Fertig ===
echo Neues Buch:      setup\setup.bat        (im Ordner pureSATZ)
echo Im Buchordner:   build.bat schnell  -  build.bat final  -  sicherung.bat
if /i "%GH%"=="j" echo Mit GitHub:      sync.bat  -  update.bat
echo Erste Schritte:  ERSTES-BUCH.md

:ende
echo.
pause
endlocal
