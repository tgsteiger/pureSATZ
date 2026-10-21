# pureSATZ – Installation für ein eigenes Buch

Diese Anleitung ist für alle, die mit dem «pureSATZ» ein **eigenes Buch** schreiben möchten –
auf Linux, Mac oder Windows. Das Buch bleibt privat: Es liegt auf deinem Computer und, wenn du willst,
in deinem eigenen privaten GitHub-Repository.

**Platzhalter** in den Befehlen – bitte ersetzen:

| Platzhalter | Bedeutung | Beispiel |
|---|---|---|
| `BENUTZER` | dein GitHub-Benutzername | `annamuster` |
| `NUMMER+BENUTZER@users.noreply.github.com` | deine geschützte GitHub-Mail (GitHub → Settings → Emails → «Keep my email addresses private») | `12345678+annamuster@users.noreply.github.com` |
| `MEIN-BUCH` | Name deines Buchs (Ordner und Repository, ohne Leerzeichen) | `Gartenjahr` |

## 0. pureSATZ bekommen

pureSATZ liegt öffentlich auf GitHub: **github.com/tgsteiger/pureSATZ**. Holen geht ohne Einladung
und ohne GitHub-Konto:

- **Mit git** (empfohlen): `git clone https://github.com/tgsteiger/pureSATZ.git pureSATZ` (Schritt 2).
  Später holt `git pull` im Ordner pureSATZ den neuesten Stand.
- **Als ZIP**: auf github.com/tgsteiger/pureSATZ → **Code → Download ZIP**, entpacken, den Ordner
  `pureSATZ` nennen und bei Schritt 3 weitermachen.

Neue Motor-Versionen holt jedes Buch selbst mit `sh update.sh` (Windows: `update.bat`) – ohne Anmeldung.
Ein **GitHub-Konto** brauchst du nur, wenn dein Buch privat auf GitHub liegen und zwischen Computern
wandern soll (Schritt 4). Ohne GitHub: Schritt 4 weglassen; gesichert wird mit `sh sicherung.sh` (ZIP).
Nutzungsbedingungen: `LIZENZ.md`.

**Am einfachsten:** Im Ordner pureSATZ das Einrichte-Skript starten. Es prüft Python, git und venv,
installiert, was fehlt, fragt, ob du mit GitHub arbeiten willst, holt auf Wunsch Bücher und legt ein neues an.
Es darf beliebig oft laufen.

| Linux | Mac | Windows |
|---|---|---|
| `bash pc-einrichten/linux-einrichten.sh` | `bash pc-einrichten/mac-einrichten.sh` | `pc-einrichten\win-einrichten.bat` (Doppelklick) |

Die Schritte unten sind dasselbe von Hand.

---

## Linux (Terminal)

```sh
## 1. Werkzeuge (einmalig)
sudo apt install git python3-venv

## 2. pureSATZ holen (öffentlich, ohne Anmeldung)
mkdir -p ~/Buecher && cd ~/Buecher
git clone https://github.com/tgsteiger/pureSATZ.git pureSATZ

## 3. Eigenes Buch anlegen – fragt Titel, Untertitel, Autor, Name, Format …
cd pureSATZ
sh setup/setup.sh                                     # legt daneben den Ordner ../MEIN-BUCH an

## 4. Optional: Buch privat mit deinem GitHub verbinden (einmalig, braucht ein GitHub-Konto)
sudo apt install gh
gh auth login                                   # GitHub.com → HTTPS → Yes → Login with a web browser
git config --global user.name "Vorname Nachname"
git config --global user.email "NUMMER+BENUTZER@users.noreply.github.com"
cd ../MEIN-BUCH
git init -b main
git add .
git commit -m "Erster Stand"
gh repo create MEIN-BUCH --private --source . --push

## 5. Alltag
sh sync.sh              # am Anfang und am Ende der Arbeit (nur mit Schritt 4)
sh build.sh schnell     # beim Schreiben: Lese-PDF in wenigen Sekunden
sh build.sh final       # Druckfassung
sh update.sh            # neue pureSATZ-Version ins Buch holen
```

## Mac (Terminal) – Intel und Apple-Chip, ohne Homebrew

Homebrew läuft auf Intel-Macs nicht mehr. Darum geht es auf dem Mac ohne Homebrew und ohne `gh`:
pureSATZ einmal als ZIP oder mit `git clone` holen, dann richtet `pc-einrichten/mac-einrichten.sh` den Rest ein.

```sh
## 1. Apple-Werkzeuge (bringen git mit) – Fenster «Installieren» klicken
xcode-select --install
#   Python 3.10+ von python.org: «macOS 64-bit universal2 installer» (Intel und Apple-Chip)

## 2. pureSATZ holen (öffentlich, ohne Anmeldung)
mkdir -p ~/Documents/Buecher && cd ~/Documents/Buecher
git clone https://github.com/tgsteiger/pureSATZ.git pureSATZ

## 3. Rest einrichten: prüft Werkzeuge, Python, git-Name/Mail, GitHub-Zugang; holt auf Wunsch Bücher
cd pureSATZ
bash pc-einrichten/mac-einrichten.sh            # hält es an: Anweisung befolgen, nochmals starten

## 4. Neues Buch anlegen (oder bestehendes mit pc-einrichten/mac-einrichten.sh holen)
sh setup/setup.sh

## 5. Optional: Buch privat mit GitHub verbinden (einmalig; braucht Konto und Token, siehe Kasten unten):
##    auf github.com/new ein leeres privates Repository MEIN-BUCH anlegen (ohne README), dann:
cd ../MEIN-BUCH
git init -b main
git add .
git commit -m "Erster Stand"
git remote add origin https://github.com/BENUTZER/MEIN-BUCH.git
git push -u origin main

## 6. Alltag
sh sync.sh              # nur mit Schritt 5
sh build.sh schnell
sh build.sh final
sh update.sh            # neue pureSATZ-Version ins Buch holen
```

**GitHub-Token (Mac, einmalig – nur für ein eigenes privates Buch-Repository)** – GitHub nimmt im Terminal kein Passwort an:

1. github.com/settings/tokens → **Generate new token** → **Generate new token (classic)**
2. Note: «Mac Buchmotor» · Expiration: **No expiration** (gelbe Warnung darf man ignorieren)
3. **Nur den obersten Haken `repo`** setzen – die Unterpunkte kommen automatisch mit. Sonst nichts.
4. **Generate token** → Token (`ghp_…`) kopieren, er wird nur einmal angezeigt.
5. Beim ersten `git push` oder `git clone` deines Buchs: Username = GitHub-Benutzer, Password = Token (**Cmd+V**; das Terminal zeigt
   absichtlich nichts an), Enter. Der Mac merkt ihn sich im Schlüsselbund.

Häufige Fehler:
- `Authentication failed` → kein oder falscher Token. Gespeicherten Versuch vergessen:
  `printf "protocol=https\nhost=github.com\n\n" | git credential reject`, dann nochmals.
- `403 Write access to repository not granted` → Haken `repo` fehlt: Token löschen, neuen machen.
- Einfügen geht nicht → anderes Terminal nehmen (Programme → Dienstprogramme → Terminal).
- Token nie in einen Chat oder eine Datei kopieren; ist das passiert: auf github.com/settings/tokens löschen, neu machen.

## Windows (PowerShell)

```powershell
## 1. Werkzeuge (einmalig) – danach PowerShell SCHLIESSEN und NEU ÖFFNEN
## («--source winget» umgeht den Store-Fehler «Serverzertifikat» auf älterem Windows 10)
winget install -e --source winget --id Python.Python.3.12
winget install -e --source winget --id Git.Git

## 2. pureSATZ holen (öffentlich, ohne Anmeldung)
mkdir $HOME\Documents\Buecher; cd $HOME\Documents\Buecher
git clone https://github.com/tgsteiger/pureSATZ.git pureSATZ

## 3. Eigenes Buch anlegen
cd pureSATZ
.\setup\setup.bat

## 4. Optional: Buch privat mit GitHub verbinden (einmalig, braucht ein GitHub-Konto)
winget install -e --source winget --id GitHub.cli     # danach PowerShell neu öffnen
gh auth login
git config --global user.name "Vorname Nachname"
git config --global user.email "NUMMER+BENUTZER@users.noreply.github.com"
cd ..\MEIN-BUCH
git init -b main
git add .
git commit -m "Erster Stand"
gh repo create MEIN-BUCH --private --source . --push

## 5. Alltag
.\sync.bat               # nur mit Schritt 4
.\build.bat schnell
.\build.bat final
.\update.bat             # neue pureSATZ-Version ins Buch holen
```

---

## Mit LibreOffice oder Word schreiben (Testphase)

Wer lieber in **LibreOffice Writer** oder **Word** schreibt, kann daraus ein Buch machen lassen.
*Diese Funktion ist noch in der Testphase und nicht voll ausgereift – das Ergebnis immer im PDF kontrollieren.*

**Regeln für das Dokument:**

- Formatvorlagen benutzen: **Titel**, **Untertitel**, **Überschrift 1 / 2 / 3**, **Standard** bzw. **Textkörper**, **Zitat**.
- Erlaubt: **fett**, Aufzählungen, Links, manueller Seitenumbruch.
- Bilder über **Einfügen → Bild** einfügen, **ohne «Verknüpfen»**. Bildunterschrift: Rechtsklick → **Beschriftung
  einfügen**. Beschreibung fürs E-Book: Rechtsklick → Eigenschaften → Optionen → **Alternativtext**.
- Speichern als **.odt** (LibreOffice) oder **.docx** (Word). Alte .doc-Dateien wandelt LibreOffice um, falls installiert.
- Zwei oder mehr «Überschrift 1» mit «Überschrift 2» darunter werden **Teile** (eigene Teil-Seite) mit Kapiteln,
  sonst wird «Überschrift 1» ein Kapitel.
- Nicht übernommen: Fussnoten, Kommentare, Kursivschrift; Tabellen nur als Text.

**Befehl** (im Ordner pureSATZ):

```sh
sh import/import-text.sh manuskript.odt --autor "Vorname Nachname"      # Windows: import\import-text.bat manuskript.odt …
cd ../Manuskript-Titel
sh build.sh schnell
```

Es entsteht ein Buchordner neben pureSATZ (Name aus dem Titel, sonst `--name Mein-Buch`) mit dem Text,
den Bildern in `fotos/` und **`IMPORT-BERICHT.txt`**: was übernommen wurde und was nicht. Danach geht es
weiter wie bei jedem Buch – ab hier wird in der MD-Datei weitergeschrieben.

## Dasselbe Buch auf einem zweiten Computer

Werkzeuge wie oben (Schritt 1), dann im Ordner neben pureSATZ
(Mac: einfacher mit `bash pc-einrichten/mac-einrichten.sh` in pureSATZ – fragt nach dem Repository-Namen;
oder `git clone https://github.com/BENUTZER/MEIN-BUCH.git MEIN-BUCH`):

```sh
gh repo clone BENUTZER/MEIN-BUCH MEIN-BUCH
cd MEIN-BUCH
sh build.sh schnell        # Windows: .\build.bat schnell – richtet beim ersten Mal Python ein
```

Ab dann auf beiden Computern: `sh sync.sh` am Anfang und am Ende (Windows: `.\sync.bat`).
Wurde auf beiden Computern dieselbe Stelle geändert, geht nichts verloren: Deine Version bleibt,
die andere liegt daneben als `…_KONFLIKT-anderer-Computer_….md` – vergleichen, übernehmen, löschen,
nochmals `sh sync.sh`.

## Verbesserungen am Motor übernehmen

```sh
cd pureSATZ
git pull                              # neueste Version holen
sh setup/setup.sh motor ../MEIN-BUCH        # Windows: .\setup\setup.bat motor ..\MEIN-BUCH
cd ../MEIN-BUCH
sh sync.sh                            # neuer Motor geht auch auf den zweiten Computer
```

Der alte Motor bleibt als `motor-alt-…` im Buch, bis du `sh cleanup.sh` laufen lässt.

## Wie weiter?

- **`ERSTES-BUCH.md`** im Ordner pureSATZ: fünf Schritte vom Anlegen bis zur Bestellung.
- **`README.md`** in deinem Buchordner: alle Befehle und Möglichkeiten.
- **`readme4ki.txt`** in deinem Buchordner: kurze Regeln für eine KI, die beim Schreiben hilft.
- Fragen und Fehler: Screenshot an die Person, die dir pureSATZ gegeben hat.
