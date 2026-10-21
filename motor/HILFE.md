# Hilfe zu diesem Buch (pureSATZ)

**Das Buch steht in drei MD-Dateien.** Alles andere macht der Motor.

| Datei | Inhalt |
|---|---|
| `<buch>-variablen.md` | `# VARIABLEN` (Titel, Autor, ISBN …), `# TECHNIK` (Format, Bindung, Rücken, Dateien), `# LAYOUT` (Farben, Schriften) |
| `<buch>-buch.md` | das Buch: `## @TITEL`, `## @IMPRESSUM`, `### @WIDMUNG`, `## @KERNSATZ`, `## @INHALTSVERZEICHNIS`, Kapitel und Teile |
| `<buch>-umschlag.md` | `# Vorderseite`, `# Buchrücken`, `# Rückseite` |
| `stichworte-<buch>.txt` | Stichwortverzeichnis: eine Zeile pro Stichwort, Varianten mit `\|`, `#` = Kommentar |
| `fotos/`, `bilder/` | Fotos und Bilder (Porträt, eigene Verzierung) |
| `readme4ki.txt` | kurze Anleitung für eine andere KI (siehe unten) |

Alle drei Dateien haben dieselben Regeln: Überschriften `#`, `##`, `###` gliedern, Werte stehen als
`- name: wert`, erklärende Sätze sind erlaubt.

Das **Demo-Kapitel** in der Buch-Datei zeigt alle Möglichkeiten. Einmal `sh build.sh` laufen lassen,
das PDF ansehen und mit der MD vergleichen – danach das Demo löschen und schreiben.

## Bauen

```sh
sh build.sh                 # alles als Entwurf (offene Stellen und Notizen sichtbar)
sh build.sh final           # alles als Druckfassung für epubli
sh build.sh schnell         # nur die Lese-PDFs, so schnell wie möglich – beim Schreiben
sh build.sh nur-pdf         # nur die Bildschirm-PDFs (mit Booklet und Statistik)
sh build.sh nur-pdf final   # nur Bildschirm-PDFs als Druckfassung
sh build.sh nur-druck       # nur Buchblock und Umschlag    (auch: nur-ebook)
sh build.sh pruefen         # nur die MD prüfen
sh build.sh leseprobe       # Leseprobe: Umschlag, Titelei, gewählte Seiten, Schlussseite, Rückseite
sh build.sh korrektur       # Korrekturfassung: A4, Zeilennummern pro Seite, Rand für Notizen
sh build.sh geschichten     # Sammel-PDF aller Geschichten aus geschichten/ (mit «uz»: auch unzensiert)
sh neu.sh "Titel"           # neue Geschichte anlegen · sh neu.sh = Übersicht (Windows: neu.bat)
sh sicherung.sh             # ganzes Buch als ZIP sichern (lokal und/oder cloud)
sh cleanup.sh               # aufräumen: Altes löschen / entfernen (delete), fragt zuerst; md-history/ bleibt
sh cleanup.sh ausgaben      # dazu auch die Ausgabeordner löschen (macht sh build.sh final jederzeit neu)
python3 motor/manuskript.py # Liste aller @-Befehle
python3 motor/stichworte-vorschlag.py   # Vorschläge fürs Stichwortverzeichnis
```

**Booklets zum Selberdrucken** (A4 quer, doppelseitig, an der kurzen Kante wenden, falten) entstehen
automatisch im Ausgabeordner: im Entwurf und bei `nur-pdf` aus dem Bildschirm-PDF (`…_booklet.pdf`),
bei `sh build.sh final` als **Probedruck** genau wie das bestellte Buch: Vorderseite, Buchblock mit
ISBN-Impressum und Rückseite (`<kurz>_Probedruck_booklet.pdf`). Ausserdem nach `final`: `shop-angaben.txt`
(zum Kopieren für epubli, tolino, KDP) und nach jedem Bau eine kurze **Statistik** (Wörter, Lesezeit, Seiten pro Teil).
Vor der Bestellung: `CHECKLISTE.md` abhaken. Dazu zeigt `final` die **Seitenbilanz**:
Seiten mit Inhalt, Füllseiten und leere Seiten – so siehst du, ob sich Kürzen lohnt. Zudem prüft `final` den
**Kontrast** der Textfarben aus `# LAYOUT` (mind. 4,5:1) und schlägt bei Bedarf eine dunklere Farbe vor.

**Leseprobe** (`…_Leseprobe.pdf` und `…_Leseprobe.epub`, Schlussseite mit QR-Code zu `shop-link:`, sonst zur Website):
Umschlag und Titelei bis zum Inhaltsverzeichnis, dann die Seiten aus `leseprobe-seiten:` (gedruckte Seitenzahlen,
z. B. `14,16,17-20,22`; für die zweite Ausgabe eigene mit `leseprobe-seiten-uz:`). Ohne Seiten gilt `leseprobe:`
(Anzahl Kapitel oder Titel des letzten Kapitels), ist auch das leer: **die 4 Seiten nach dem Inhaltsverzeichnis**.
Die E-Book-Leseprobe nimmt die Kapitel, in denen die gewählten Seiten liegen. Text der Schlussseite: `leseprobe-text:`. **Korrekturfassung** (`…_Korrektur.pdf`): jede
Seite in Originalgrösse auf A4, links Zeilennummern, rechts Linien für Notizen – zum Ausdrucken und
Korrigieren («S. 12, Z. 5»). Im Entwurf mit offenen Stellen, mit `korrektur final` ohne.

**Sicherung:** `sh sicherung.sh` legt `<name>_JJJJMMTTHHMMSS.zip` an den Orten ab, die unter `# TECHNIK`
bei `sicherung-lokal:` und `sicherung-cloud:` stehen (Leerschläge im Pfad sind kein Problem); `sh sicherung.sh lokal` oder `cloud` nur dorthin. `sicherung-behalten: 10` = nur die 10 neuesten ZIPs bleiben.
Im ZIP: alle MD/TXT, Fotos, Bilder, md-history, Motor und je Ausgabe das Bildschirm-PDF – keine
Zwischenspeicher und keine anderen Ausgaben (die macht `sh build.sh final` jederzeit neu).

**Aufräumen, alte Dateien löschen, entfernen, delete:** `sh cleanup.sh` (Windows: `cleanup.bat`) zeigt zuerst
eine Liste und fragt, bevor etwas gelöscht wird. Weg kommen nur entbehrliche Dinge: Zwischenspeicher (`_bildcache`,
`_druckbilder`, `__pycache__`, `_epub_tmp`), alte Motoren (`motor-alt-…`), Sicherungen in `_backup/` und
`stichworte-vorschlag.txt`. Mit `sh cleanup.sh ausgaben` auch die Ausgabeordner. **Nie gelöscht:** `md-history/`,
die MD-Dateien, Stichworte, `fotos/`, `bilder/`, `motor/`, `.venv/` und alles, was das Skript nicht kennt.
Alte ZIP-Sicherungen räumt `sicherung-behalten:` auf, alte Stände in md-history `md-history-behalten:`.

Vor jedem Bau werden die drei MD-Dateien nach `md-history/` gesichert und geprüft (unbekannte
`{Variablen}` oder `@Befehle`, fehlende Fotos – mit Zeilennummer). Gebaut wird parallel.

## Geschichten sammeln (freiwillig)

Statt alles in die eine Buchdatei zu schreiben, kann jede Geschichte eine **eigene Datei** im Ordner
`geschichten/` sein. Das Buch bindet sie mit einer Zeile `@@name` ein. Ohne `geschichten/` und ohne
`@@` läuft alles wie bisher – ein Buch aus einer einzigen Buchdatei bleibt genau gleich.

```sh
sh neu.sh "Schutzschild hoch!"     # legt geschichten/schutzschild-hoch.md an (Windows: neu.bat "…")
sh neu.sh                          # Übersicht: Stand, Wörter, im Buch ja/nein
sh build.sh geschichten            # Sammel-PDF aller Geschichten (normal) · «geschichten uz» auch unzensiert
```

**Eine Geschichte** (`geschichten/schutzschild-hoch.md`):

```
## Schutzschild hoch!
- stand: entwurf
- stichworte: Emotionscode, Schutz
- quelle: Praxis 2018

Text, wie im Buch: Absätze, **fett**, > Zitat, ::: Blöcke, Fotos, {variablen}.
```

- Die drei Zeilen mit «-» sind freiwillig und werden nicht gedruckt.
  `stand`: **idee · entwurf · ueberarbeiten · fertig** – nur für die Übersicht, wirkt nicht auf den Druck.
  `stichworte` kommen automatisch ins Stichwortverzeichnis. `quelle` ist eine Notiz für dich.
- **Einbinden:** in der Buchdatei eine eigene Zeile `@@schutzschild-hoch` (Name = Dateiname ohne .md).
  Die Reihenfolge der `@@`-Zeilen ist die Reihenfolge im Buch. In `::: nur-uz` … `:::` gesetzt erscheint
  die Geschichte nur in der zweiten Ausgabe (die Geschichte selbst darf dann keine eigenen `:::`-Blöcke haben).
- **Übersicht:** Bei jedem Bau und bei `sh neu.sh` entsteht `geschichten-uebersicht.html` (im Browser öffnen:
  Fortschrittsbalken, Tabelle zum Sortieren und Filtern, Kanban-Ansicht) und `geschichten/UEBERSICHT.md`.
  Beide werden immer neu erzeugt und kommen nicht zu GitHub.
- **Prüfung:** `sh build.sh pruefen` meldet `@@`-Verweise ohne Datei (mit Vorschlag bei Tippfehlern),
  Geschichten, die noch nicht im Buch sind, und doppelt eingebundene. Fehler zeigen die richtige Datei
  («geschichten/schutzschild-hoch.md, Zeile 7: …»). md-history/ und Sicherung nehmen die Geschichten mit.

## Bilder und Fotos

| Ordner | Was | Format | Pixel (300 dpi: Breite in mm × 12) |
|---|---|---|---|
| `fotos/` | Fotos im Text (`::: foto`) | JPG, RGB (nicht CMYK) | ganze Breite A5: mind. 1400 · `breite: 60`: 700 · `fluss`: 500 |
| `bilder/` | Porträt, Verzierung, Teil-Bilder | PNG, gern transparent | Porträt 600 × 600 · Teil-Bild 1200 |

Dateinamen ohne Leerzeichen und Umlaute, z. B. `sommer-1980.jpg`. Handyfotos sind ideal.

**Das macht der Motor selbst:** grosse Fotos auf 1800 Pixel verkleinern (`_bildcache/`, kleine PDFs, schneller Bau) ·
im Druck Transparenz auf Papierfarbe setzen (epubli) · fehlendes Foto: im Entwurf ein Kasten, im Druck nichts ·
`quelle:` kommt in den Bildnachweis · `sh build.sh pruefen` meldet Fotos, die im Druck unscharf würden.

**Grösse:** Ohne Angaben ist ein Foto so breit wie der Text und höchstens 75 mm hoch – ein Querformat wird also
breit, ein Hochformat schmaler. Steht es am Seitenende, wird es etwas kleiner (bis 38 mm), damit keine Lücke bleibt.

**Alle Fotos gleich gross** (Variablen-Datei, Abschnitt «Fotos», alles freiwillig):

```text
- foto-format: 3:2        alle auf dasselbe Seitenverhältnis zuschneiden (4:3, 16:9, quadrat …)
- foto-breite: 100        einheitliche Breite in mm (ein «breite:» im Foto geht vor)
- foto-anpassen: nein     am Seitenende nie verkleinern
```

Beim Zuschneiden bleibt die Mitte; pro Foto `ausschnitt: oben` (Köpfe!), `unten`, `links` oder `rechts`.
Fotos mit `fluss:` werden nicht zugeschnitten. Das Original in `fotos/` bleibt immer unverändert.

## Sichern und zurückholen

| Was | Wann | Wohin |
|---|---|---|
| **md-history** | automatisch bei jedem Bau | `md-history/`: jede MD-Datei mit Datum und Uhrzeit |
| **sicherung.sh** | von Hand, z. B. am Abend | ZIP des ganzen Buchs nach `../Sicherungen` (und Cloud) |
| **sync.sh** (GitHub) | am Anfang und am Ende | alle Änderungen, auch auf dem anderen Computer |

**Alte Fassung zurückholen:** In `md-history/` die Datei mit passender Zeit öffnen (z. B.
`Mein-Buch-buch_20261021-15-08-32.md`), den Absatz kopieren und ins Buch einsetzen. Nie die ganze Datei
zurückkopieren, ohne zu vergleichen. Ganzes Buch: ZIP aus `../Sicherungen` auspacken.

`md-history-behalten: 200` = pro Datei nur die 200 neuesten Stände (leer = alle). `sicherung-behalten: 10` = nur
die 10 neuesten ZIPs. `sh cleanup.sh` löscht md-history nie.

## Tabellen

Tabellen liegen als **CSV** im Ordner `tabellen/` und werden mit einer eigenen Zeile `@#name` eingebunden.
Beispiel: `tabellen/muster.csv`, im Demo-Kapitel mit `@#muster` («Eine Tabelle»).

```sh
sh neu.sh tabelle "Behandlungen pro Jahr"   # legt tabellen/behandlungen-pro-jahr.csv an (Windows: neu.bat tabelle "…")
```

```
Behandlungen pro Jahr                  ← Zeile 1: Bezeichnung (steht über der Tabelle)
Jahr;Emotionscode;Body Code;Total      ← Zeile 2: Spaltenüberschriften
2018;40;12;52                          ← ab Zeile 3: Werte
Quelle: eigene Praxisstatistik         ← optional: letzte Zeile, klein darunter
```

- Bearbeiten mit LibreOffice: öffnen, ändern, **Speichern unter → Text CSV**, Feldtrenner `;`, Zeichensatz UTF-8.
  Trenner `;` oder `,` erkennt pureSATZ selbst. Gedruckt werden nur die Werte.
- Im Buch: `@#behandlungen-pro-jahr` (auch `@# name`). In Zellen gehen `**fett**` und `{variablen}`.
  Zahlen stehen rechtsbündig, lange Tabellen gehen über mehrere Seiten (Kopfzeile wiederholt sich).
- **Zu breit?** pureSATZ bricht zuerst Text in den Zellen um, verkleinert dann die Schrift (bis 7.5 pt) und
  stellt die Tabelle notfalls **quer** auf eine eigene Seite (um 90° gedreht, das Buch zum Lesen drehen).
  Selbst bestimmen: `@#name quer` (immer quer) oder `@#name hoch` (nie quer). Im E-Book wird nie gedreht –
  breite Tabellen lassen sich dort seitlich verschieben.
- Nur in einer Ausgabe: `::: nur-uz` / `@#name` / `:::`.
- `sh build.sh pruefen` meldet fehlende Tabellen (mit Vorschlag bei Tippfehlern) und Zeilen mit zu vielen Werten.

## Variablen

- Im Buch und im Umschlag: Name in geschweiften Klammern, z. B. `{titel}`, `{autor}`.
- `name-normal` / `name-uz`: Wert je Ausgabe. `{name}` nimmt automatisch den richtigen.
- Eine Zeile, in der eine Variable leer ist, fällt weg. `{isbn}`: Buch bzw. E-Book, leer = «folgt».
- `format`: `a5` · `taschenbuch` · `sachbuch` · `a4` · `quadrat` (Masse laut epubli)
- `bindung`: `hardcover` · `softcover` · `beide`; `ruecken`: Rückenbreite in mm **laut epubli-Coverrechner**
- `zier`: eigenes Bild für die Verzierung (sonst die Standard-Verzierung)
- `# LAYOUT`: `farbe-haupt`, `farbe-akzent` …, `schrift-text`, `schrift-titel`, `schriftgroesse`, `blocksatz`

**Rückenbreite:** `sh build.sh final` zeigt die Seitenzahl des Buchblocks. Diese im epubli-Coverrechner
eingeben (mit dem Papier, das du bestellst), `ruecken:` anpassen, nochmals bauen. Danach zeigt `final` die
Masse des Hardcover-Umschlags (z. B. 344 × 250 mm) – sie müssen mit Gesamtbreite und Gesamthöhe im
Coverrechner übereinstimmen. Beschnitt und Deckel: `beschnitt-hardcover` (11 mm), `beschnitt-softcover`,
`beschnitt-buchblock` (je 3 mm), `deckel-hardcover` (leer = laut Format), `papier`.

## Schreiben

| Im Text | Wirkung |
|---|---|
| `# Teil 1\|Titel\|Untertitel` (`\|bild.jpg`) | neuer Teil mit Teil-Seite (optional eigenes Bild) |
| `# Titel` | Kapitel oberster Ebene, neue Seite (Anhang, Zeitstrahl, Über den Autor) |
| `## Kapitel` / `### Zwischentitel` | Kapitel (im Inhalt) / kleiner Titel |
| `## @BEFEHL` | Befehl als Überschrift (sichtbar in der Navigation des Editors) |
| `> Zitat` · `~ Notiz` · `- Punkt` · `**fett**` · `[Text](https://…)` | Zitat · Randbemerkung · Liste · fett · Link |
| `1. Punkt` `2. Punkt` | nummerierte Aufzählung (zählt selbst: die erste Zahl ist der Start) |
| `  - Unterpunkt` | Unterpunkt, 2–4 Leerzeichen eingerückt (unter `-` und unter `1.`) |
| `3\. Mai war …` | Zahl mit Punkt am Zeilenanfang, aber keine Aufzählung |
| Leerzeile / `<br/>` | neuer Absatz / Zeilenumbruch im Absatz |

**Blöcke** `::: art-ausgabe Titel` … `:::` – Art: `nur`, `mitte`, `foto`, `zusammen`, `offen`,
`offen-notiz`, `zeitstrahl`, `uz` (Kasten der zweiten Ausgabe). Endung: keine (überall),
`-normal`, `-uz` (`-dc`), `-bildschirm`, `-druck`, `-ebook`, `-buch`, `-privatdruck`.

**Foto-Block:**
```text
::: foto Sommer
datei: sommer-1980.jpg     Bild im Ordner fotos/ (Grösse: fotos/readme.txt)
text: Bildunterschrift     (optional)
breite: 60                 (optional) Breite in mm
fluss: rechts              (optional) Text umfliesst das Bild, rechts oder links
quelle: Foto: Max Muster   (optional) erscheint im Bildnachweis im Anhang
alt: Kind auf rotem Dreirad (optional) Beschreibung fürs E-Book (Vorlesefunktion); sonst gilt text:
ausschnitt: oben           (optional, nur mit foto-format) was beim Zuschneiden bleibt: oben, unten, links, rechts
:::
```

**Seiten:** `@UMBRUCH` neue Seite · `@UMBRUCH-RECHTS` im Druck rechts · `@PLATZ 60` neue Seite, wenn
weniger als 60 mm Platz · `@ABSTAND 8` Leerraum · `::: zusammen` nie trennen · `@SEITENMITTE`.

**Weiteres:** `@TITEL`, `@IMPRESSUM`, `@WIDMUNG`, `@KERNSATZ`, `@INHALTSVERZEICHNIS`, `@ZITAT`, `@MOTTO`, `@UNTEN`,
`@ZIER 12`, `@ZIER-UNTEN`, `@ZIER-TRENNER`, `@QR url | Text`, `@QR-PAAR … ;; …`, `@PORTRAIT bild | Text`,
`@KOPF`, `@STICHWORTE`, `@RUECKSEITE`. Vollständige Liste: `python3 motor/manuskript.py`.

## Bei epubli

Ausgabeordner (z. B. `ausgabe-normal/`): `<kurz>_Buchblock.pdf` und `<kurz>_Umschlag_Hardcover.jpg`
bzw. `_Softcover.jpg` hochladen. Erst ein Testexemplar (`projekt-normal: privatdruck`), dann
«Buch veröffentlichen»; die ISBN von epubli bei `isbn-buch:` eintragen und neu bauen.
E-Book (`.epub`): eigene ISBN bei `isbn-ebook:`, dann bei tolino media oder KDP hochladen.
Das E-Book enthält Angaben zur **Barrierefreiheit** (Gliederung, Inhaltsverzeichnis, Bildbeschreibungen);
`sh build.sh` warnt bei Fotos ohne `alt:` und ohne `text:`. Eigene Zusammenfassung: `ebook-barrierefreiheit:`. Die Akzentfarbe für Text wird im E-Book automatisch
lesbar dunkel gesetzt (Kontrast 4,5:1); eigene Farbe mit `farbe-akzent-ebook:`.

## Mit einer anderen KI arbeiten

Gib der KI zuerst `readme4ki.txt` (kurze Regeln, passt auch in kostenlose KI-Chats), dann die MD-Datei,
an der sie arbeiten soll. Danach `sh build.sh pruefen` – der Motor meldet sofort, falls etwas nicht passt.

## Motor aktualisieren

```sh
sh update.sh            # auf GitHub nachsehen, Neuerungen zeigen, fragen, aktualisieren (Windows: update.bat)
sh update.sh pruefen    # nur nachsehen, nichts ändern
sh update.sh lokal      # aus dem Ordner ../pureSATZ statt von GitHub
```

Ersetzt wird nur der Ordner `motor/` – deine MD-Dateien, Stichworte, Fotos und Bilder bleiben unberührt.
Der alte Motor bleibt als `motor-alt-…` liegen. Braucht git und Internet, aber keine Anmeldung –
pureSATZ ist öffentlich. Danach `sh build.sh schnell` und, wenn das Buch auf mehreren Computern liegt, `sh sync.sh`.
Ohne Internet, aus dem Ordner `pureSATZ` neben dem Buch: `sh update.sh lokal`
(oder im Ordner pureSATZ: `sh setup/setup.sh motor ../<buch>`).

## Auf mehreren Computern (Linux, Mac, Windows)

Das Buch als eigenes **privates** GitHub-Repository – dann wandern MD-Dateien, Stichworte, Fotos und Bilder mit.
`.venv`, Ausgaben, Zwischenspeicher und `md-history` bleiben auf jedem Computer für sich (`.gitignore`).

```sh
sh sync.sh          # am Anfang und am Ende der Arbeit (Windows: sync.bat)
```

Einmalig im Buchordner: `git init -b main`, dann `gh repo create <buchname> --private --source . --push`.
Auf dem anderen Computer neben pureSATZ: `gh repo clone <benutzer>/<buchname> <Buchordner>`, dann `sh build.sh`.
Wurde dieselbe Stelle auf zwei Computern geändert, geht nichts verloren: deine Version bleibt, die andere liegt
daneben als `…_KONFLIKT-anderer-Computer_….md` – vergleichen, übernehmen, löschen, nochmals `sh sync.sh`.

## Windows

Statt `sh build.sh …` einfach `build.bat …` (gleiche Optionen), ebenso `cleanup.bat`, `sicherung.bat` und `sync.bat`.

## Hilfe als Webseite

`sh build.sh hilfe` erzeugt `hilfe.html` im Buchordner und öffnet sie im Browser (Windows: `build.bat hilfe`).
Sie entsteht ausserdem bei jedem Bau neu. Oben ein **Suchfeld** (Taste `/`, `Esc` leert), ein Umschalter
**Linux/Mac · Windows** für alle Befehle und bei jedem Befehl ein Knopf **kopieren**.

Inhalt: Spickzettel, eigene Praxis-Notizen aus `meine-hilfe.md` (freiwillig, im Buchordner, selbst pflegen:
normales Markdown, jede `##`-Überschrift wird ein Abschnitt), diese Hilfe (`motor/HILFE.md`, kommt mit jedem
Motor-Update), alle Befehle und Blöcke direkt aus dem Motor und die Variablen dieses Buchs mit ihren Werten.

Der Knopf **Start** oben springt zur Checkliste für den Anfang (`START.md` im Ordner pureSATZ, mit Häkchen
zum Anklicken). Ein Beispielbuch zum Ausprobieren: im Ordner pureSATZ `sh hallo.sh` (Windows: `hallo.bat`).

## Schwarz-weiss drucken (freiwillig)

Die feinen Farben (Kopfzeile, Bildunterschriften, Gold) wirken im eigenen Schwarz-weiss-Ausdruck sehr hell.
Mit `bildschirm-dunkler: ja` in der Variablen-Datei (Abschnitt «Weiteres») werden sie **nur im Bildschirm-PDF**
(und in Leseprobe, Korrektur, Booklet zum Selberdrucken) etwas dunkler. Druckdateien für epubli und das E-Book
bleiben unverändert.
