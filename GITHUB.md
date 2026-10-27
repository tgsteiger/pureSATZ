# pureSATZ auf GitHub – für den Betreuer von pureSATZ

Diese Seite ist für die Pflege von pureSATZ selbst. Wer pureSATZ nur **nutzen** will, braucht sie nicht:
siehe `INSTALLATION.md` (Holen geht ohne Konto, das Repository ist öffentlich).

Das Repository enthält **nur diesen Ordner** (Motor, Vorlage, Demo). Bücher wie `MeinBuch` liegen daneben
und kommen nie hinein. `.gitignore` hält Ausgaben, `.venv`, `md-history` und Sicherungen fern.

## Einmalig einrichten (ca. 15 Minuten)

**1. Programme installieren** (Linux Mint / Ubuntu):

```sh
sudo apt install git gh
```

Mac: ohne Homebrew, siehe unten (`pc-einrichten/mac-einrichten.sh`) · Windows: «Git for Windows» und «GitHub CLI» von git-scm.com bzw. cli.github.com.

**2. Bei GitHub anmelden** (öffnet den Browser, Benutzer, z. B. `deinname`):

```sh
gh auth login
```

Antworten: `GitHub.com` → `HTTPS` → `Yes` → `Login with a web browser`.

**3. Name und Mail für Git** – die «noreply»-Adresse, damit deine Mail nicht sichtbar wird
(GitHub → Settings → Emails → «Keep my email addresses private», dort steht die Adresse):

```sh
git config --global user.name "Vorname Nachname"
git config --global user.email "NUMMER+deinname@users.noreply.github.com"
```

**4. Repository anlegen und hochladen** (im Ordner pureSATZ, nur beim allerersten Mal):

```sh
git init -b main
git add .
git commit -m "pureSATZ, Motor $(cat motor/VERSION)"
gh repo create pureSATZ --public --source . --push
```

Fertig. Unter github.com/tgsteiger/pureSATZ → **Actions** läuft jetzt der Selbsttest auf Linux, Mac und
Windows (ca. 5 Minuten). Grünes Häkchen = alles in Ordnung.

## Im Alltag

| Was | Befehl (im Ordner pureSATZ) |
|---|---|
| Neuesten Stand holen (anderer Computer) | `git pull` |
| Änderung am Motor hochladen | `git add .` → `git commit -m "was geändert"` → `git push` |
| Was ist geändert? | `git status` |
| Motor ins Buch bringen (im Buch) | `sh update.sh` (von GitHub) oder `sh update.sh lokal` (aus `../pureSATZ`) |

**Regel:** Den Motor nur in pureSATZ ändern, hochladen, dann in den Büchern `sh update.sh`.
Wurde er doch im Buch geändert: `rsync -av --exclude "__pycache__" MeinBuch/motor/ pureSATZ/motor/`,
dann in pureSATZ `git status` (nur `motor/…` geändert?), `git add motor`, `git commit`, `git push`.

## Auf einem anderen Computer (Mac, Windows)

Herunterladen geht ohne Anmeldung (öffentlich). Zum **Hochladen** von Motor-Änderungen braucht es die
Anmeldung: Linux/Windows `gh auth login`, Mac ein Token (siehe `INSTALLATION.md`, Abschnitt Mac).

**Mac** (Terminal; Intel und Apple-Chip, ohne Homebrew – Homebrew läuft auf Intel-Macs nicht mehr):

```sh
xcode-select --install                     # Apple-Werkzeuge mit git; Python 3.10+ von python.org (universal2)
mkdir -p ~/Documents/Buchprojekt-TGS && cd ~/Documents/Buchprojekt-TGS
git clone https://github.com/tgsteiger/pureSATZ.git pureSATZ
cd pureSATZ
bash pc-einrichten/mac-einrichten.sh       # prüft alles, holt auf Wunsch eigene private Bücher (dafür Token)
```

Token, Fehlermeldungen und Lösungen: `INSTALLATION.md`, Abschnitt Mac.

**Windows** (cmd: im Explorer in die Adresszeile `cmd` tippen, Enter; nach den drei `winget`-Zeilen das Fenster
schliessen und neu öffnen):

```bat
winget install -e --source winget --id Python.Python.3.12
winget install -e --source winget --id Git.Git
winget install -e --source winget --id GitHub.cli
gh auth login
git config --global user.name "Vorname Nachname"
git config --global user.email "NUMMER+deinname@users.noreply.github.com"
mkdir "%USERPROFILE%\Documents\Buchprojekt-TGS"
cd /d "%USERPROFILE%\Documents\Buchprojekt-TGS"
git clone https://github.com/tgsteiger/pureSATZ.git pureSATZ
cd pureSATZ
setup\setup.bat
```

Ein bestehendes Buch (z. B. MeinBuch) ist nicht auf GitHub: den Buchordner **neben** pureSATZ kopieren
(Nextcloud oder ZIP aus `sicherung.sh`), dann im Buch `sh build.sh` bzw. `build.bat` – die Python-Umgebung
richtet sich beim ersten Mal selbst ein (`.venv` vorher löschen, falls mitkopiert).

## Bücher zwischen Computern abgleichen

Jedes Buch kann ein eigenes privates Repository sein (z. B. `<benutzer>/<buchname>`). Einmalig im Buchordner:

```sh
cd ~/"Dokumente/02 Nebenerwerb/Buchprojekt-TGS/MeinBuch"
git init -b main
gh repo create meinbuch --private --source . --push
```

Danach auf jedem Computer nur noch `sh sync.sh` (Windows: `sync.bat`) – am Anfang und am Ende der Arbeit.
Auf einem neuen Computer neben pureSATZ: `gh repo clone <benutzer>/<buchname> MeinBuch`, dann `sh build.sh`.

## Selbsttest von Hand

```sh
python3 test/selbsttest.py      # legt ein Testbuch in einem Temp-Ordner an und baut alles
```
