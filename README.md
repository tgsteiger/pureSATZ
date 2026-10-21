# pureSATZ – Vorlage für neue Bücher (Motor 2.16)

Ein Satzsystem für Bücher aus Markdown: **alles steht in drei MD-Dateien**, der Motor macht das
Layout. Zwei Ausgaben (normal und z. B. Director's Cut / Unzensiert), daraus Bildschirm-PDF,
Druckdateien für epubli (Hardcover/Softcover), E-Book und Booklets. Entstanden aus «Leben 1.0, 2.0, 3.0».

**Webseite:** [tgsteiger.github.io/pureSATZ](https://tgsteiger.github.io/pureSATZ/) – Download, fünf Schritte, Hilfe online.

**Zum Starten:** `hilfe.html` doppelklicken und oben auf «Start» klicken – dort steht alles Schritt für Schritt.

**Nur schnell sehen, wie es aussieht?** Im Ordner pureSATZ `sh hallo.sh` (Windows: `hallo.bat` doppelklicken):
legt ein Beispielbuch an und öffnet das PDF. Checkliste dazu: **`START.md`** (auch in `hilfe.html`, Knopf «Start»).

Neu hier? Zuerst **`ERSTES-BUCH.md`** lesen – fünf Schritte vom Anlegen bis zur Bestellung.
Installation auf Linux, Mac oder Windows, auch für andere Personen mit eigenem Buch: **`INSTALLATION.md`**.

## Ein neues Buch beginnen

```sh
sh setup/setup.sh              # fragt alles ab
sh setup/setup.sh start.txt    # nimmt die Werte aus setup/start.txt, fragt nur, was fehlt
```

Gefragt wird: Titel, Untertitel, Autor, **technischer Buchname** (Ordner und Dateien),
**Format** (a5, taschenbuch, sachbuch, a4, quadrat), **Bindung** (hardcover, softcover),
zweite Ausgabe, Ort, Jahr, Website, Verlagsadresse.

Das legt **neben** `pureSATZ` einen Buchordner an (z. B. `../Mein-Buch/`):

| Datei | Inhalt |
|---|---|
| `Mein-Buch-variablen.md` | `# VARIABLEN`, `# TECHNIK`, `# LAYOUT` |
| `Mein-Buch-buch.md` | das Buch: Titelei und ein Demo-Kapitel mit allen Möglichkeiten |
| `Mein-Buch-umschlag.md` | Vorderseite, Buchrücken, Rückseite |
| `stichworte-Mein-Buch.txt` | Stichwortverzeichnis, eine Zeile pro Stichwort |
| `CHECKLISTE.md` | zum Abhaken vor der Bestellung |
| `readme4ki.txt` | kurze Anleitung für eine andere KI |
| `sync.sh`, `update.sh`, `.gitignore` | Buch zwischen Computern abgleichen, Motor-Update von GitHub (siehe `GITHUB.md`) |
| `fotos/`, `bilder/`, `build.sh`, `cleanup.sh`, `sicherung.sh`, `README.md`, `motor/` | Bilder, Bauen, Aufräumen, Sicherung, Hilfe, Satzsystem |

Alle drei MD-Dateien haben dieselben Regeln: Überschriften `#`, `##`, `###`, Werte als `- name: wert`,
erklärende Sätze sind erlaubt. Danach im Buchordner:

```sh
sh build.sh             # Entwurf
sh build.sh schnell     # nur Lese-PDFs, beim Schreiben
sh build.sh final       # Druckfassung
sh build.sh leseprobe   # Leseprobe       sh build.sh korrektur   # Korrekturfassung
sh sicherung.sh         # ZIP-Sicherung (lokal und/oder cloud)
```

Die Hilfe zum Buch steht im Buchordner in `README.md`.

## Geschichten sammeln (ab 2.11)

Wer lieber einzelne Geschichten schreibt: jede Geschichte eine eigene Datei in `geschichten/`, im Buch eingebunden
mit einer Zeile `@@name`. `sh neu.sh "Titel"` legt eine an (Windows `neu.bat`), `sh neu.sh` zeigt die Übersicht,
`sh build.sh geschichten` macht ein Sammel-PDF; `geschichten-uebersicht.html` zeigt Stand, Wörter und Kanban.
Freiwillig – ein Buch aus einer einzigen Buchdatei läuft wie bisher. Details: `hilfe.html`, Abschnitt «Geschichten sammeln».

## Tabellen und Leseprobe (ab 2.12)

Tabellen als CSV in `tabellen/`, im Buch mit einer Zeile `@#name`; zu breite Tabellen werden verkleinert oder quer
gestellt (`@#name quer` / `@#name hoch`). Neue Tabelle: `sh neu.sh tabelle "Titel"`. Leseprobe nach Seiten:
`leseprobe-seiten: 14,16,17-20,22` (auch `-uz`), ohne Angabe die 4 Seiten nach dem Inhaltsverzeichnis.
Details: `hilfe.html`, Abschnitte «Tabellen» und «Bauen».

## Hilfe mit Suche (ab 2.13)

Jedes Buch hat eine `hilfe.html` (Doppelklick): alle Anleitungen, Befehle, Blöcke und die Variablen des Buchs auf
einer Seite, mit Suche und Schalter Linux/Mac ↔ Windows. `sh build.sh hilfe` erzeugt und öffnet sie. Eigene
Notizen in `meine-hilfe.md` stehen ganz oben. Diese Hilfe für den Ordner pureSATZ: `python3 motor/hilfe.py`.

## Aus LibreOffice oder Word (Testphase)

```sh
sh import/import-text.sh manuskript.odt --autor "Vorname Nachname"    # auch .docx; Windows: import\import-text.bat
```

Legt wie `setup/setup.sh` ein Buch an, aber mit dem Text, den Bildern und einem `IMPORT-BERICHT.txt`. Noch nicht voll
ausgereift – Regeln für das Dokument und Einschränkungen in `INSTALLATION.md`.

## Weitere Aufrufe

```sh
sh setup/setup.sh motor ../Mein-Buch    # nur den neuesten Motor ins Buch (alter bleibt als motor-alt-…)
sh setup/setup.sh ../Mein-Buch          # bestehender Ordner: Fehlendes ergänzen
```

**Motor-Update im Buch selbst:** `sh update.sh` holt den neuesten Motor direkt von GitHub (`sh update.sh pruefen`
= nur nachsehen). Ein Ordner pureSATZ auf dem Computer ist dafür nicht nötig – praktisch für alle, die nur ihr Buch haben.

Bestehende Dateien werden **nie überschrieben**. Jedes Buch hat seinen eigenen Motor: So lässt sich
ein fertiges Buch auch in Jahren noch genau gleich erstellen.

## Formate (Masse laut epubli, Hardcover laut Coverrechner)

| Format | Seite | Hardcover-Deckel |
|---|---|---|
| `a5` (Standard) | 148 × 210 mm | 157 × 228 mm |
| `taschenbuch` | 125 × 190 mm | 134 × 208 mm |
| `sachbuch` | 135 × 205 mm | 144 × 223 mm |
| `a4` | 210 × 297 mm | 219 × 315 mm |
| `quadrat` | 205 × 205 mm | 214 × 223 mm |

Einschlag Hardcover 11 mm, Beschnitt Softcover und Innenseiten 3 mm – alles in der Variablen-Datei änderbar (`beschnitt-…`, `deckel-hardcover`). Weitere Formate: in `motor/build.py` bei `FORMATE`.

## setup/start.txt

```text
TITEL = Mein Buch
UNTERTITEL = Eine Geschichte in drei Teilen
AUTOR = Vorname Nachname
NAME = Mein-Buch                  # technischer Buchname
FORMAT = a5                       # a5, taschenbuch, sachbuch, a4, quadrat
BINDUNG = hardcover               # hardcover, softcover
ZWEITE_AUSGABE = nein             # ja = zweite Ausgabe (Director's Cut …)
ZWEITE_NAME = Director's Cut
ORT = Ort
JAHR = 2027
WEBSITE = www.beispiel.ch
ADRESSE = Strasse 1, 3000 Bern, mail@beispiel.ch
```

## Inhalt dieses Ordners

| Datei / Ordner | Inhalt |
|---|---|
| `pc-einrichten/` (`linux-einrichten.sh`, `mac-einrichten.sh`, `win-einrichten.bat`) | Computer einmalig einrichten (Python, git, GitHub freiwillig) |
| `setup/` (`setup.sh`, `setup.bat`, `setup.py`) | neues Buch anlegen, Motor aktualisieren |
| `import/` (`import-text.sh`, `.bat`, `.py`) | Buch aus LibreOffice/Word anlegen (Testphase) |
| `setup/start.txt` | Beispielwerte für `sh setup/setup.sh start.txt` |
| `motor/` | Satzsystem: `manuskript.py` (liest und prüft die MD), `build.py`, `build-broschuere.py`, `build-epub.py`, `bauen.py`, `fassungen.py` (Leseprobe, Korrektur), `sicherung.py`, `sync.py`, `update.py` (Motor-Update von GitHub), `aufraeumen.py`, `einrichten.py`, `booklet.py`, `stichworte-vorschlag.py`, `layout.py` (Vorgaben), Schriften, Verzierung |
| `vorlage/` | `variablen.md`, `buch.md`, `umschlag.md`, `stichworte-buch.txt`, `build.sh`, `cleanup.sh`, `sicherung.sh`, `readme4ki.txt`, `README.md`, `CHECKLISTE.md`, Beispielbilder, Beispiel-PDF |

## Mit einer anderen KI arbeiten

Gib der KI zuerst `readme4ki.txt` (kurze Regeln, passt auch in kostenlose KI-Chats), dann die MD-Datei,
an der sie arbeiten soll. Danach `sh build.sh pruefen` – der Motor meldet sofort, falls etwas nicht passt.

## Voraussetzungen

- Python 3.10 oder neuer mit venv (Linux: `sudo apt install python3-venv`; Mac/Windows: von python.org)
- Internet beim ersten Einrichten der Python-Umgebung (reportlab, Pillow, pypdf, pypdfium2)
- Sonst nichts: Cover-JPG und E-Book-Titelbild macht pypdfium2 – auf Linux, Mac und Windows gleich.

| | Linux / Mac | Windows |
|---|---|---|
| Neues Buch | `sh setup/setup.sh` | `setup\setup.bat` |
| Bauen | `sh build.sh final` | `build.bat final` |
| Sichern / Aufräumen | `sh sicherung.sh` · `sh cleanup.sh` | `sicherung.bat` · `cleanup.bat` |

## GitHub

Anleitung: **`GITHUB.md`** (einrichten, hochladen, Alltag, anderer Computer). Bei jedem `git push` baut GitHub
ein Testbuch auf Linux, Mac und Windows (`test/selbsttest.py`) und prüft das E-Book mit EPUBCheck.
`motor/VERSION` und `motor/CHANGELOG.md` führen die Versionen. Bücher gehören nicht ins Repository.

## Lizenz

pureSATZ ist öffentlich einsehbar und darf kostenlos genutzt werden, um eigene Bücher zu setzen – die Bücher
gehören ihren Autoren. Verändern und weitergeben nur mit Zustimmung; GPL-3.0 auf Anfrage.
Details: **`LIZENZ.md`**. Die Schriften Lora und Poppins stehen unter der SIL Open Font License
(`motor/fonts/SCHRIFTEN-LIZENZ.md`).

## Kontakt und Webseite

Fragen und Fehler: [Issues auf GitHub](https://github.com/tgsteiger/pureSATZ/issues) oder puresatz@gsteiger.ch.
Die Webseite liegt in `docs/` (GitHub Pages) und wird mit `python3 docs/landingpage.py` erneuert
(baut das Hallo-Buch, macht die Bilder, kopiert die Hilfe).
