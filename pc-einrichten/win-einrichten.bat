@echo off
rem =====================================================================
rem  pureSATZ - Windows einrichten, in fuenf Schritten
rem  Am einfachsten: START-Windows.bat im Ordner pureSATZ doppelklicken (ruft dieses Skript auf).
rem    1. Technik (Python)   2. Ort fuer die Buecher   3. Hallo-Buch
rem    4. Dein eigenes Buch  5. Fertig und Extras (Ghostscript, GitHub - freiwillig)
rem  Darf beliebig oft laufen - Erledigtes wird uebersprungen.
rem  --weiter = nach dem Kopieren an den festen Ort (ohne Willkommen und Ort)
rem =====================================================================
setlocal
set "SELBST=%~f0"
cd /d "%~dp0.."
set "HIER=%CD%"
for %%I in ("%HIER%") do set "HIERNAME=%%~nxI"
for %%I in ("%HIER%\..") do set "OBEN=%%~fI"
for %%I in ("%OBEN%") do set "OBENNAME=%%~nxI"
set "WEITER="
if /i "%~1"=="--weiter" set "WEITER=1"
if exist "%TEMP%\puresatz-neustart-python.txt" set "WEITER=2"

rem --- Willkommen --------------------------------------------------------
if defined WEITER goto schritt1
call :titel "pureSATZ - Willkommen"
echo Das passiert jetzt, in fuenf Schritten:
echo.
echo   1. Technik einrichten       Python, einmalig
echo   2. Ort fuer deine Buecher   ein fester Ordner - nicht Downloads
echo   3. Hallo-Buch               ein Beispielbuch zum Anschauen
echo   4. Dein eigenes Buch        leer, mit deinem Titel und Namen
echo   5. Fertig                   Extras wie GitHub sind freiwillig
echo.
echo Bei jeder Frage nimmt Enter den Vorschlag.
call :weiter

rem --- Schritt 1: Technik -----------------------------------------------
:schritt1
call :titel "Schritt 1 von 5 - Technik einrichten"
echo pureSATZ braucht Python (3.10 oder neuer). Fehlt es, wird es jetzt installiert.
echo.
call :python_suchen
if defined PY goto python_ok
echo Python fehlt.
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
echo Danach dieses Fenster schliessen und START-Windows.bat nochmals doppelklicken.
start "" "https://www.python.org/downloads/windows/"
goto ende
:python_ok
del "%TEMP%\puresatz-neustart-python.txt" >nul 2>nul
for /f "delims=" %%v in ('%PY% --version') do echo OK  %%v
timeout /t 2 >nul

rem --- Schritt 2: Ort -----------------------------------------------------
if "%WEITER%"=="1" goto schritt3
call :titel "Schritt 2 von 5 - Ort fuer deine Buecher"
if exist "%HIER%\.git" goto ort_git
if /i "%OBENNAME%"=="Buchprojekte" goto ort_fest

set "ZIEL=%USERPROFILE%\Buchprojekte"
echo pureSATZ liegt jetzt in:  %HIER%
echo Deine Buecher entstehen neben pureSATZ. Besser ist ein fester Ort -
echo nicht Downloads, nicht Desktop, nicht OneDrive.
echo.
echo Vorschlag:  %ZIEL%
echo.
echo   Enter oder j  = Vorschlag uebernehmen
echo   anderer Pfad  = eintippen (oder Ordner ins Fenster ziehen)
echo   n             = hier lassen
echo.
set "ORT="
set /p "ORT=Deine Wahl: "
if defined ORT set "ORT=%ORT:"=%"
if /i "%ORT%"=="n" goto ort_hier
if /i "%ORT%"=="nein" goto ort_hier
if /i "%ORT%"=="j" set "ORT="
if /i "%ORT%"=="ja" set "ORT="
if defined ORT set "ZIEL=%ORT%"
if /i "%HIER%"=="%ZIEL%\pureSATZ" goto ort_fest

for /f "usebackq delims=" %%v in ("%HIER%\motor\VERSION") do set "VNEU=%%v"
if not exist "%ZIEL%\pureSATZ\motor\VERSION" goto kopieren
for /f "usebackq delims=" %%v in ("%ZIEL%\pureSATZ\motor\VERSION") do set "VALT=%%v"
echo.
echo pureSATZ %VALT% ist dort schon vorhanden (diese Version: %VNEU%).
set "ERS=j"
set /p "ERS=Ersetzen? Die alte bleibt als pureSATZ-alt-%VALT%. [Enter = ja, n = die vorhandene nehmen]: "
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
set /p "VK=Verknuepfung Buchprojekte auf dem Desktop anlegen? [Enter = ja, n = nein]: "
if /i "%VK%"=="ja" set "VK=j"
if /i not "%VK%"=="j" goto explorer
powershell -NoProfile -ExecutionPolicy Bypass -Command "$s=(New-Object -ComObject WScript.Shell).CreateShortcut([Environment]::GetFolderPath('Desktop')+'\Buchprojekte.lnk'); $s.TargetPath='%ZIEL%'; $s.Save()" >nul 2>nul
if errorlevel 1 (echo Verknuepfung ging nicht - nicht schlimm.) else (echo OK  Verknuepfung Buchprojekte auf dem Desktop)
:explorer
start "" explorer "%ZIEL%"
echo.
echo Ab jetzt geht es in %ZIEL%\pureSATZ weiter.
echo Den Ordner %HIER% darfst du am Schluss loeschen.
call :weiter
:dort_weiter
"%ZIEL%\pureSATZ\pc-einrichten\win-einrichten.bat" --weiter

:ort_git
echo pureSATZ wurde mit git geholt und bleibt, wo es ist:
echo   %HIER%
goto ort_ende
:ort_fest
echo pureSATZ liegt schon am festen Ort:
echo   %HIER%
goto ort_ende
:ort_hier
echo pureSATZ bleibt hier:
echo   %HIER%
:ort_ende
echo Deine Buecher entstehen daneben, in %OBEN%
call :weiter

rem --- Schritt 3: Hallo-Buch ------------------------------------------------
:schritt3
call :titel "Schritt 3 von 5 - Hallo-Buch"
rem hallo.py erklaert, fragt, baut und oeffnet Ordner und PDF
%PY% setup\hallo.py --kette
call :weiter

rem --- Schritt 4: Dein eigenes Buch ------------------------------------------
call :titel "Schritt 4 von 5 - Dein eigenes Buch"
rem setup.py erklaert, fragt Titel, Untertitel, Autor, Format und oeffnet den Buchordner
%PY% setup\setup.py --kette
call :weiter

rem --- Schritt 5: Fertig und Extras -------------------------------------------
call :titel "Schritt 5 von 5 - Fertig und Extras"
echo Zwei Extras - beide freiwillig, beide gehen auch spaeter (START-Windows.bat nochmals starten).
echo.
echo Ghostscript braucht es nur, wenn eine Druckerei CMYK verlangt (z. B. tredition).
set "GSDA="
where gswin64c >nul 2>nul && set "GSDA=1"
if exist "%ProgramFiles%\gs\" set "GSDA=1"
if defined GSDA (echo OK  Ghostscript vorhanden & goto gs_ok)
where winget >nul 2>nul || (echo Ghostscript fehlt - bei Bedarf: ghostscript.com & goto gs_ok)
set "GS=n"
set /p "GS=Ghostscript installieren? [j = ja, Enter = nein]: "
if /i "%GS%"=="ja" set "GS=j"
if /i "%GS%"=="j" winget install -e --source winget --id ArtifexSoftware.GhostScript --accept-package-agreements --accept-source-agreements
:gs_ok

echo.
echo GitHub: private Sicherung und dasselbe Buch auf mehreren Computern (sync.bat).
set "GH=n"
set /p "GH=Mit GitHub arbeiten? [j = ja, Enter = nein]: "
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
set /p "R=Eigenes Buch von GitHub holen? Repository-Name (z. B. mein-buch), Enter = weiter: "
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
echo ==============================================================
echo   Fertig - so sieht es jetzt aus:
echo ==============================================================
echo.
echo   %OBEN%\
for /d %%d in ("%OBEN%\*") do call :ordner_zeile "%%~nxd"
echo.
echo Geschrieben und gebaut wird im Ordner deines Buchs - nie in pureSATZ.
echo Im Buchordner "Terminal hier" doppelklicken, dann:
echo   build.bat schnell     Lese-PDF ansehen, in Sekunden
echo   build.bat final       Druckfassung
echo   sicherung.bat         ZIP-Sicherung
if /i "%GH%"=="j" echo   sync.bat              mit GitHub abgleichen (am Anfang und am Ende)
echo Hilfe: hilfe.html im Ordner pureSATZ doppelklicken, oben "Start".

:ende
echo.
pause
endlocal
goto :eof


rem ===================================================================== Hilfsteile
:titel
cls
echo ==============================================================
echo   %~1
echo ==============================================================
echo.
goto :eof

:weiter
echo.
set "X="
set /p "X=Weiter mit Enter ... "
goto :eof

:ordner_zeile
set "NM=%~1"
set "TXT="
if /i "%NM%"=="%HIERNAME%" set "TXT=die Werkstatt - hier nichts schreiben"
if /i "%NM:~0,13%"=="pureSATZ-alt-" set "TXT=alte Version - darf weg"
if /i "%NM%"=="Hallo-Buch" set "TXT=zum Ausprobieren - darf weg"
if not defined TXT if exist "%OBEN%\%NM%\build.bat" set "TXT=dein Buch - hier schreibst und baust du"
if defined TXT echo     %NM%\    %TXT%
goto :eof

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
echo Dieses Fenster schliesst sich jetzt. Danach START-Windows.bat
echo nochmals doppelklicken. Klappt es dann noch nicht: Computer neu starten.
pause
exit

:ren_fehler
echo Umbenennen ging nicht. Ist ein Fenster oder Programm in %ZIEL%\pureSATZ offen?
echo Schliessen und START-Windows.bat nochmals doppelklicken.
pause
exit /b 1
:kopier_fehler
echo Kopieren nach %ZIEL% ging nicht. START-Windows.bat nochmals starten und einen
echo anderen Ort waehlen oder "n" fuer hier lassen.
pause
exit /b 1
