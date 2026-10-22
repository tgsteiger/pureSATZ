# Schreiben

## Die Buchdateien

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

## Variablen

- Im Buch und im Umschlag: Name in geschweiften Klammern, z. B. `{titel}`, `{autor}`.
- `name-normal` / `name-uz`: Wert je Ausgabe. `{name}` nimmt automatisch den richtigen.
- Eine Zeile, in der eine Variable leer ist, fällt weg. `{isbn}`: Buch bzw. E-Book, leer = «folgt».
- `format`: `a5` · `taschenbuch` · `sachbuch` · `a4` · `quadrat` (Masse laut epubli)
- `bindung`: `hardcover` · `softcover` · `beide`; `ruecken`: Rückenbreite in mm **laut epubli-Coverrechner**
- `druck-normal` / `druck-uz`: Datei aus `druck/` mit allen Angaben für den Druck (siehe «Druckangaben»)
- `zier`: eigenes Bild für die Verzierung (sonst die Standard-Verzierung)
- `# LAYOUT`: `farbe-haupt`, `farbe-akzent` …, `schrift-text`, `schrift-titel`, `schriftgroesse`, `blocksatz`

**Alle Variablen der Vorlage auf einen Blick** (Erklärungen auch direkt in der Variablen-Datei):

| Bereich | Variablen |
|---|---|
| Buch | `titel`, `untertitel`, `autor`, `website`, `ort`, `jahr`, `auflage`, `stand`, `verlag` |
| Zwei Ausgaben | `zweite-ausgabe` (ja/nein), `ausgabe-name-normal` / `-uz`, `stempel-uz` (z. B. UNZENSIERT), `kasten-hinweis` |
| ISBN | `isbn-buch`, `isbn-ebook` |
| E-Book | `ebook-epub2` (ja = zusätzlich EPUB 2), `ebook-barrierefreiheit`, `farbe-akzent-ebook` |
| Shop | `shop-beschreibung`, `shop-schlagwoerter`, `shop-kategorie`, `preis-buch`, `preis-ebook`, `shop-link` |
| Leseprobe | `leseprobe`, `leseprobe-seiten`, `leseprobe-seiten-uz`, `leseprobe-text` |
| Technik | `format`, `bindung`, `projekt`, `ruecken-…`, `beschnitt-…`, `deckel-hardcover`, `papier`, `druck-normal` / `-uz`, `kurz-…`, `datei-…`, `ordner-…` |
| Weiteres | `stichworte`, `trennstellen` (Welt\|anschauung), `zier`, `zier-hell`, `kopfzeile` (ohne-autor · autor · wechselnd), `foto-format`, `md-history-behalten`, `bildschirm-dunkler`, `mockup-hintergrund` |
| Sicherung | `sicherung-lokal`, `sicherung-cloud`, `sicherung-behalten` |
| Layout | `farbe-text`, `farbe-leise`, `farbe-haupt`, `farbe-akzent`, `farbe-papier`, `farbe-kasten`, `farbe-stempel`, `schrift-text`, `schrift-titel`, `schriftgroesse`, `zeilenabstand`, `blocksatz` |

**Rückenbreite:** `sh build.sh final` zeigt die Seitenzahl des Buchblocks. Diese im epubli-Coverrechner
eingeben (mit dem Papier, das du bestellst), `ruecken:` anpassen, nochmals bauen. Danach zeigt `final` die
Masse des Hardcover-Umschlags (z. B. 344 × 250 mm) – sie müssen mit Gesamtbreite und Gesamthöhe im
Coverrechner übereinstimmen. Beschnitt und Deckel: `beschnitt-hardcover` (11 mm), `beschnitt-softcover`,
`beschnitt-buchblock` (je 3 mm), `deckel-hardcover` (leer = laut Format), `papier`.

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

# Bauen

## Bauen

```sh
sh build.sh                 # alles als Entwurf (offene Stellen und Notizen sichtbar)
sh build.sh final           # alles als Druckfassung für epubli
sh build.sh komplett        # final + Leseprobe + Korrektur in einem Durchgang (vor Bestellung/Veröffentlichung)
sh build.sh schnell         # nur die Lese-PDFs, so schnell wie möglich – beim Schreiben
sh build.sh nur-pdf         # nur die Bildschirm-PDFs (mit Booklet und Statistik)
sh build.sh nur-pdf final   # nur Bildschirm-PDFs als Druckfassung
sh build.sh nur-druck       # nur Buchblock und Umschlag
sh build.sh nur-ebook       # nur die E-Books (mit «final» ohne offene Stellen)
sh build.sh sicherung       # nur die MD-Dateien nach md-history/ sichern (ohne Bau)
sh build.sh final druck=bod-a5-normal       # Test: nur Druckdateien mit einer anderen Datei aus druck/ → ausgabe-test/
sh build.sh final druck=bod-a5-normal uz    # … nur für eine Fassung (normal oder uz)
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

**Werbebilder (Mockup)** entstehen bei `sh build.sh final` und `nur-pdf final` im Ausgabeordner, aus dem
Bildschirm-PDF: `…_Mockup.jpg` (Vorder- und Rückseite leicht gedreht, mit Schatten, 1600 × 1600 Pixel – für Webseite,
Newsletter, Shop, Social Media) und `…_Vorderseite.jpg` (nur die Vorderseite, gerade). Jederzeit neu aus dem
vorhandenen PDF: `sh build.sh mockup`. Hintergrund ändern: `mockup-hintergrund: #E9EEF4, #C9D3DF` (oben, unten).

**Cover-Bilder** entstehen mit dem E-Book (`sh build.sh`, `final`, `nur-ebook`) im Ausgabeordner:
`…_Cover-vorne.jpg` und `…_Cover-hinten.jpg` – Vorder- und Rückseite gerade, randlos, ohne Schatten,
hochaufgelöst (lange Seite 2560 Pixel, kurze mindestens 1600, bei A5 etwa 300 dpi). Die Texte des Umschlags
kommen aus Blöcken `::: nur-ebook`; gibt es keine, gelten die des Drucks (`::: nur-druck`, z. B. «Erstausgabe»
statt «Stand»). Dasselbe gilt für das Titelbild im E-Book.
Das Vorne-Bild ist das **Titelbild für E-Book-Shops** (tolino media, neobooks, BoD, KDP verlangen ein JPG im
Hochformat, mindestens 1600 Pixel breit); beide eignen sich auch für Presse, Verlag und Webseite.
Unterschied zu `<KURZ>_Cover_Vorderseite.jpg` im Druckordner: Jenes ist für die Druckerei (400 dpi, mit 3 mm
Beschnitt rundum, der beim Schneiden wegfällt) – fürs E-Book also das `…_Cover-vorne.jpg` nehmen.

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

## Was im Ausgabeordner liegt (00-UEBERSICHT.txt)

Nach jedem Bau steht zuoberst im Ausgabeordner (`ausgabe-normal/`, `ausgabe-unzensiert/` …) die Datei
`00-UEBERSICHT.txt`. Sie zeigt, **welche Datei wofür** ist. Oben: der letzte Bau (Art, Datum, pureSATZ-Version,
Druckdatei) und eine eigene Zeile **Druckdateien: FINAL** bzw. **ENTWURF – nicht hochladen!** – sie bleibt auch nach
`schnell` oder `leseprobe` stehen. Bei jeder Datei stehen Datum und Uhrzeit: so sieht man, ob sie vom letzten Bau stammt.

| Gruppe | Dateien |
|---|---|
| Bei der Druckerei hochladen | `<kurz>_Buchblock.pdf`, `<kurz>_Umschlag_Hardcover` bzw. `_Softcover` (PDF und JPG) |
| E-Book | `<datei>.epub` (und `_EPUB2.epub`), `<datei>_Inhalt.pdf` (Inhaltsverzeichnis), `<datei>_Cover-vorne.jpg` (Titelbild, auch als `_2000px`, `_1600px`, `_900px`) |
| Zum Lesen und Verschicken | `<datei>.pdf`, `_Leseprobe.pdf`, `_Korrektur.pdf` (fürs Lektorat) |
| Werbung | `<datei>_Mockup.jpg`, `<datei>_Vorderseite.jpg` |
| Selber drucken | `<kurz>_Probedruck_booklet.pdf` bzw. `<datei>_booklet.pdf` |
| Texte für den Shop | `shop-angaben.txt` |
| Weitere Dateien | z. B. Vorder- und Rückseite einzeln als PDF und JPG – zur Auswahl |

Fehlt etwas, nennt die Übersicht den Befehl dazu (z. B. `sh build.sh leseprobe`). Testläufe
(`druck=…`) haben in `ausgabe-test/<datei>/` ihre eigene Übersicht. Alle Dateien entstehen wie bisher.

## Schwarz-weiss drucken (freiwillig)

Die feinen Farben (Kopfzeile, Bildunterschriften, Gold) wirken im eigenen Schwarz-weiss-Ausdruck sehr hell.
Mit `bildschirm-dunkler: ja` in der Variablen-Datei (Abschnitt «Weiteres») werden sie **nur im Bildschirm-PDF**
(und in Leseprobe, Korrektur, Booklet zum Selberdrucken) etwas dunkler. Druckdateien für epubli und das E-Book
bleiben unverändert.

## Hilfe als Webseite

`sh build.sh hilfe` erzeugt `hilfe.html` im Buchordner und öffnet sie im Browser (Windows: `build.bat hilfe`).
Sie entsteht ausserdem bei jedem Bau neu. Oben ein **Suchfeld** (Taste `/`, `Esc` leert), ein Umschalter
**Linux/Mac · Windows** für alle Befehle und bei jedem Befehl ein Knopf **kopieren**.

Inhalt: Spickzettel, eigene Praxis-Notizen aus `meine-hilfe.md` (freiwillig, im Buchordner, selbst pflegen:
normales Markdown, jede `##`-Überschrift wird ein Abschnitt), diese Hilfe (`motor/HILFE.md`, kommt mit jedem
Motor-Update), alle Befehle und Blöcke direkt aus dem Motor und die Variablen dieses Buchs mit ihren Werten.

Der Knopf **Start** oben springt zur Checkliste für den Anfang (`START.md` im Ordner pureSATZ, mit Häkchen
zum Anklicken). Ein Beispielbuch zum Ausprobieren: im Ordner pureSATZ `sh hallo.sh` (Windows: `hallo.bat`).

# Drucken und veröffentlichen

## Bei epubli

Ausgabeordner (z. B. `ausgabe-normal/`): `<kurz>_Buchblock.pdf` und `<kurz>_Umschlag_Hardcover.jpg`
bzw. `_Softcover.jpg` hochladen. Erst ein Testexemplar (`projekt-normal: privatdruck`), dann
«Buch veröffentlichen»; die ISBN von epubli bei `isbn-buch:` eintragen und neu bauen.
E-Book (`.epub`): eigene ISBN bei `isbn-ebook:`, dann bei tolino media oder KDP hochladen.
Das E-Book enthält Angaben zur **Barrierefreiheit** (Gliederung, Inhaltsverzeichnis, Bildbeschreibungen);
`sh build.sh` warnt bei Fotos ohne `alt:` und ohne `text:`. Eigene Zusammenfassung: `ebook-barrierefreiheit:`. Die Akzentfarbe für Text wird im E-Book automatisch
lesbar dunkel gesetzt (Kontrast 4,5:1); eigene Farbe mit `farbe-akzent-ebook:`.

## Druckangaben (druck/)

Alles, was nur den **Druck** betrifft, kann pro Fassung in einer eigenen Datei im Ordner `druck/` stehen –
so lassen sich epubli, BoD (und später andere) nebeneinander vorbereiten, ohne die Variablen-Datei umzubauen.
In der Variablen-Datei: `- druck-normal: epubli-a5-normal` und `- druck-uz: epubli-a5-uz` (Name ohne `.md`).
Die Werte der Druckdatei gelten **nur für Buchblock und Umschlag** und haben Vorrang. Lese-PDF, E-Book,
Leseprobe, Korrektur und Mockup bleiben beim `format:` der Variablen-Datei (Grundformat).
Ohne `druck`-Zeile gilt alles wie bisher.

| In der Druckdatei | Bedeutung |
|---|---|
| `plattform` | `epubli` oder `bod` (bestimmt Strichcode-Platz und Füllseite) |
| `format` / `seite` | Format wie oben; `seite: 148 x 210` = eigenes Mass in mm (Ränder und Schrift vom nächstliegenden Format) |
| `bindung`, `projekt`, `papier`, `extra-seiten`, `isbn-buch` | wie in der Variablen-Datei |
| `ruecken-hardcover`, `ruecken-softcover` | Rücken in mm laut Coverrechner der Plattform |
| `beschnitt-buchblock`, `beschnitt-hardcover`, `beschnitt-softcover`, `deckel-hardcover` | Masse in mm (BoD: Buchblock 0, Deckel 153x216, Einschlag 17) |
| `barcode-position` | `links` · `mitte` · `rechts` (leer = wie bisher: epubli links frei, BoD rechts) |
| `barcode-groesse` | z. B. `40x20` (mm, 16 mm vom Rand seitlich, 8 mm von unten); leer = 60 × 35 mm ab der Ecke frei |
| `barcode-bild` | PNG aus `bilder/` auf weissem Feld; leer = nichts zeichnen (BoD: Strichcode aus der ISBN) |

`name-normal` / `name-uz` gehen auch in der Druckdatei. Weicht das Druckformat vom Grundformat ab, meldet der
Bau «Seitenzahlen im Druck anders als im Lese-PDF». Beim Bau steht `Druckangaben: druck/…md`, und eine Kopie der
Datei liegt im Ausgabeordner. `sh build.sh pruefen` meldet fehlende Druckdateien und unbekannte Namen.

**Ausgabeordner:** Ein normaler Bau legt die Druckdateien immer in `ausgabe-normal/` bzw. `ausgabe-unzensiert/` –
egal welche Plattform die aktive Druckdatei nennt. **Testlauf:** `sh build.sh final druck=<datei>` baut nur
Buchblock und Umschlag mit dieser Datei nach `ausgabe-test/<datei>/` (mit `normal` oder `uz`: nur diese Fassung);
ein neuer Test überschreibt den alten. `ausgabe-test/` kommt nicht zu GitHub und nicht in die Sicherung,
`sh cleanup.sh ausgaben` löscht ihn mit. Gefällt der Test, in der Variablen-Datei `druck-normal:` / `druck-uz:` umstellen.
**Andere Plattform** (z. B. KDP): eine Musterdatei kopieren, z. B. als `druck/kdp-dein-format.md`, die Werte aus
dem Coverrechner der Plattform eintragen (Seite, Rücken, Beschnitt, Deckel, Barcode) und mit `druck=kdp-dein-format`
testen. Als `plattform` passt meist `bod` (Strichcode-Feld selbst bestimmen, keine epubli-Füllseite).
**Muster** (beim neuen Buch schon in `druck/`, sonst in `pureSATZ/vorlage/druck/`): `epubli-a5`,
`epubli-taschenbuch`, `epubli-sachbuch`, `epubli-a4`, `epubli-quadrat`, `bod-a5-hardcover` (BoD noch ungetestet).
Ausprobieren ohne Umstellen: `sh build.sh final druck=bod-a5-hardcover` → `ausgabe-test/bod-a5-hardcover/`.

# Andere Plattformen

## Druck bei KDP, Lulu und anderen

Für technisch Interessierte – der Motor kennt epubli und BoD, andere Druckereien gehen über eine eigene Druckdatei:

1. Eine Musterdatei kopieren, z. B. `druck/bod-a5-hardcover.md` als `druck/kdp-dein-format.md`.
2. Werte aus dem **Coverrechner** bzw. der Formatliste der Plattform eintragen: `seite: 152,4 x 228,6`
   (eigenes Mass in mm) oder `format:`, `ruecken-…`, `beschnitt-…`, `deckel-hardcover`, `papier`.
   Ohne Coverrechner: ein PDF hochladen – die Plattform nennt die Masse, die sie erwartet.
3. `plattform: bod` stehen lassen (Strichcode-Feld selbst bestimmen, keine epubli-Füllseite).
   Setzt die Plattform den Strichcode selbst (z. B. KDP), das Feld mit `barcode-position` / `barcode-groesse`
   frei lassen und `barcode-bild` leer.
4. Testen: `sh build.sh final druck=kdp-dein-format` → `ausgabe-test/kdp-dein-format/`, Masse in `00-UEBERSICHT.txt`
   mit dem Rechner der Plattform vergleichen. Passt alles: `druck-normal:` bzw. `druck-uz:` umstellen.

**Grenzen:** Beschnitt gilt rundum. KDP will beim Buchblock keinen Beschnitt im Bund (nur oben, unten, aussen) –
das kann der Motor noch nicht. Masse nur in mm.

## E-Book bei XinXii, tolino, KDP und BoD

Das E-Book ist für alle Shops dasselbe – nur der Druck ist plattformabhängig:

- Datei: `<datei>.epub` (EPUB 3, mit Inhaltsverzeichnis und Angaben zur Barrierefreiheit).
- Titelbild: `<datei>_Cover-vorne.jpg` (Hochformat, lange Seite 2560 Pixel – passt für tolino media, KDP, BoD,
  neobooks). Für Shops mit Höchstgrösse zusätzlich `…_Cover-vorne_2000px.jpg`, `_1600px.jpg` und `_900px.jpg`
  (Zahl = lange Seite).
- Inhaltsverzeichnis als PDF: `<datei>_Inhalt.pdf` – die Inhaltsseiten aus dem Lese-PDF (verlangt z. B. XinXii).
- Texte: Beschreibung, Schlagwörter, Kategorie aus `shop-angaben.txt` kopieren.
- ISBN: eigene E-Book-ISBN bei `isbn-ebook:` eintragen und neu bauen (manche Shops vergeben selbst eine).
- Leseprobe als E-Book: `<datei>_Leseprobe.epub` (`sh build.sh leseprobe`).
- **EPUB 2:** pureSATZ baut EPUB 3, das tolino, KDP, Apple, BoD und XinXii annehmen. Verlangt ein Shop oder
  Prüfprogramm EPUB 2 (z. B. epubli: «EPUB-Version zu hoch»), in der Variablen-Datei `ebook-epub2: ja` setzen –
  dann entsteht zusätzlich `<datei>_EPUB2.epub` («epub2-light»: gleicher Inhalt, ohne Angaben zur Barrierefreiheit).
  Von Hand aus einem fertigen E-Book: `python3 motor/epub2.py ausgabe-normal/<datei>.epub`.

## Selber drucken oder im Copyshop

- **Booklet:** `<kurz>_Probedruck_booklet.pdf` (nach `final`) bzw. `<datei>_booklet.pdf` (Entwurf):
  A4 quer, doppelseitig, an der kurzen Kante wenden, falten, heften – ein Probeexemplar in Originalgrösse.
- **Bildschirm-PDF** `<datei>.pdf` für den Copyshop (Klebebindung, Spiralbindung) oder zum Verschicken.
- **Korrektur-PDF** `<datei>_Korrektur.pdf` (`sh build.sh korrektur`): A4 mit Zeilennummern und Rand fürs Lektorat.
- Feine Farben im Schwarz-weiss-Druck zu hell: `bildschirm-dunkler: ja` (siehe «Schwarz-weiss drucken»).

# Sichern und mehrere Computer

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

## Windows

Statt `sh build.sh …` einfach `build.bat …` (gleiche Optionen), ebenso `cleanup.bat`, `sicherung.bat` und `sync.bat`.

## Mit einer anderen KI arbeiten

Gib der KI zuerst `readme4ki.txt` (kurze Regeln, passt auch in kostenlose KI-Chats), dann die MD-Datei,
an der sie arbeiten soll (auch eine Druckdatei aus `druck/`). Danach `sh build.sh pruefen` – der Motor meldet sofort, falls etwas nicht passt.
