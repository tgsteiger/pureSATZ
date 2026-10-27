@echo off
rem =====================================================================
rem  pureSATZ - Windows einrichten (einmalig)
rem  Am einfachsten: start.bat im Ordner pureSATZ doppelklicken (ruft dieses Skript auf).
rem  Auch direkt: doppelklicken oder in cmd im Ordner pureSATZ:  pc-einrichten\win-einrichten.bat
rem  Darf beliebig oft laufen - Erledigtes wird uebersprungen.
rem  GitHub ist freiwillig und kommt am Schluss: Ohne GitHub geht Schreiben und Bauen genauso.
rem =====================================================================
setlocal
set "SELBST=%~f0"
cd /d "%~dp0.."
set "HIER=%CD%"
for %%I in ("%HIER%\..") do set "OBEN=%%~fI"
echo === pureSATZ: Windows einrichten ===
echo.

rem --- 1. Python 3.10+ ---------------------------------------------------
call :python_suchen
if defined PY goto python_ok
echo Schritt 1: Es fehlt ein aktuelles Python (3.10 oder neuer).
where winget >nul 2>nul || goto python_web
echo Es wird jetzt installiert (winget). Bitte allfaellige Fenster bestaetigen.
winget install -e --source winget --id Python.Python.3.12 --accept-package-agreements --accept-source-agreements
if errorlevel 1 (echo. & echo winget ging nicht - Python bitte von Hand installieren: & goto python_web)
rem Neues PATH aus Windows lesen und gleich weitermachen; sonst neues Fenster
call :pfad_neu
call :python_suchen
if defined PY goto python_ok
call :neustart python
goto ende
:python_web
echo Variante 1 - in cmd eingeben:
echo    winget install -e --source winget --id Python.Python.3.12
echo Variante 2 - Gleich oeffnet sich python.org: den neusten "Windows installer (64-bit)" laden.
echo WICHTIG: beim Installieren unten den Haken "Add python.exe to PATH" setzen.
echo Danach dieses Fenster schliessen und start.bat (oder win-einrichten.bat) nochmals starten.
start "" "https://www.python.org/downloads/windows/"
goto ende
:python_ok
for /f "delims=" %%v in ('%PY% --version') do echo OK  %%v

rem --- 2. Ghostscript (freiwillig, fuer CMYK-Druckdateien) ---------------
rem Braucht es nur mit {farbmodus}: cmyk in einer Druckdatei (z. B. tredition), umgewandelt wird bei final.
set "GSDA="
where gswin64c >nul 2>nul && set "GSDA=1"
if exist "%ProgramFiles%\gs\" set "GSDA=1"
if defined GSDA (echo OK  Ghostscript vorhanden ^(fuer {farbmodus}: cmyk^) & goto gs_ok)
where winget >nul 2>nul || (echo Hinweis: Ghostscript fehlt - nur noetig fuer {farbmodus}: cmyk. Download: ghostscript.com & goto gs_ok)
echo.
set "GS=j"
set /p "GS=Ghostscript fuer CMYK-Druckdateien (z. B. tredition) installieren? [j/n] (j): "
if /i "%GS%"=="ja" set "GS=j"
if /i "%GS%"=="j" winget install -e --source winget --id ArtifexSoftware.GhostScript --accept-package-agreements --accept-source-agreements
:gs_ok

rem --- 3. Hallo-Buch und eigenes Buch -----------------------------------
echo.
set "HB=j"
set /p "HB=Hallo-Buch jetzt ansehen (Beispielbuch, das PDF oeffnet sich)? [j/n] (j): "
if /i "%HB%"=="ja" set "HB=j"
if /i not "%HB%"=="j" goto frage_buch
rem hallo.py fragt am Schluss selbst nach dem eigenen Buch
%PY% setup\hallo.py
goto github_frage
:frage_buch
set "NB=j"
set /p "NB=Jetzt dein eigenes Buch anlegen? [j/n] (j): "
if /i "%NB%"=="ja" set "NB=j"
if /i "%NB%"=="j" %PY% setup\setup.py

rem --- 4. GitHub (freiwillig, geht auch jederzeit spaeter) ----------------
:github_frage
echo.
echo GitHub ist freiwillig und geht auch spaeter (dieses Skript nochmals starten, siehe GITHUB.md):
echo private Sicherung und dasselbe Buch auf mehreren Computern (sync.bat).
set "GH=n"
set /p "GH=Mit GitHub arbeiten? [j/n] (n): "
if /i "%GH%"=="ja" set "GH=j"
if /i not "%GH%"=="j" goto ohne_github

set "NEU="
where git >nul 2>nul || (echo git wird installiert ... & winget install -e --source winget --id Git.Git --accept-package-agreements --accept-source-agreements & set "NEU=1")
where gh >nul 2>nul || (echo GitHub-Programm gh wird installiert ... & winget install -e --source winget --id GitHub.cli --accept-package-agreements --accept-source-agreements & set "NEU=1")
if not defined NEU goto werkzeuge_ok
call :pfad_neu
set "FEHLT="
where git >nul 2>nul || set "FEHLT=1"
where gh >nul 2>nul || set "FEHLT=1"
if not defined FEHLT goto werkzeuge_ok
call :neustart github
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
if not defined R goto fertig
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

:fertig
del "%TEMP%\puresatz-neustart-*.txt" >nul 2>nul
echo.
echo === Fertig ===
echo Deine Buecher liegen neben pureSATZ in %OBEN%
echo pureSATZ ist die Werkstatt - dort nichts schreiben.
echo Im Buchordner:   "Terminal hier" doppelklicken, dann  build.bat schnell  -  build.bat final  -  sicherung.bat
echo Neues Buch:      setup\setup.bat   (im Ordner pureSATZ)
if /i "%GH%"=="j" echo Mit GitHub:      sync.bat  -  update.bat
echo Hilfe:           hilfe.html doppelklicken, oben "Start"

:ende
echo.
pause
endlocal
goto :eof


rem ===================================================================== Hilfsteile
:python_suchen
set "PY="
py -3 -c "import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)" >nul 2>nul && set "PY=py -3"
if not defined PY python -c "import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)" >nul 2>nul && set "PY=python"
goto :eof

:pfad_neu
rem PATH neu aus Windows lesen (System + Benutzer), damit frisch installierte Programme gefunden werden
set "PM="
set "PU="
for /f "skip=2 tokens=2,*" %%a in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path 2^>nul') do set "PM=%%b"
for /f "skip=2 tokens=2,*" %%a in ('reg query "HKCU\Environment" /v Path 2^>nul') do set "PU=%%b"
if defined PM call set "PATH=%PM%;%PU%"
goto :eof

:neustart
rem Einmal ueber den Explorer neu starten (der kennt das neue PATH), sonst von Hand
if exist "%TEMP%\puresatz-neustart-%~1.txt" goto neustart_hand
echo neu>"%TEMP%\puresatz-neustart-%~1.txt"
echo.
echo Installiert. Es geht gleich in einem neuen Fenster weiter ...
timeout /t 3 >nul
start "" explorer.exe "%SELBST%"
exit
:neustart_hand
del "%TEMP%\puresatz-neustart-%~1.txt" >nul 2>nul
echo.
echo Das neue Programm ist in diesem Fenster noch nicht sichtbar.
echo Dieses Fenster schliesst sich jetzt. Danach start.bat (oder win-einrichten.bat)
echo nochmals doppelklicken. Klappt es dann noch nicht: Computer neu starten.
pause
exit
