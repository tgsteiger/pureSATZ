# Schreiben

## Die Buchdateien

**Das Buch steht in drei MD-Dateien.** Alles andere macht der Motor.

| Datei | Inhalt |
|---|---|
| `<buch>-variablen.md` | `# VARIABLEN` (Buch, Impressum, Ausgaben mit ISBN und Preis, Shop), `# TECHNIK` (Dateien, Sicherung), `# LAYOUT` (Farben, Schriften) |
| `<buch>-buch.md` | das Buch: `## @TITEL`, `## @IMPRESSUM`, `## @HINWEIS`, `## @WIDMUNG`, `## @KERNSATZ`, `## @INHALTSVERZEICHNIS`, Kapitel und Teile |
| `<buch>-umschlag.md` | `## Vorderseite`, `## Buchrücken`, `## Rückseite`, darunter `feld: text` (`-druck`, `-bildschirm`, `-ebook`, `-uz` am Namen = nur dort), `> Erklärung` |
| `stichworte-<buch>.txt` | Stichwortverzeichnis: eine Zeile pro Stichwort, Varianten mit `\|`, `#` = Kommentar |
| `druck/<datei>.md` | Plattform-Datei: Technik einer Druckerei (Rücken, Beschnitt, Strichcode) |
| `fotos/`, `bilder/` | Fotos und Bilder (Porträt, eigene Verzierung) |
| `readme4ki.txt` | kurze Anleitung für eine andere KI (siehe unten) |

**Schreibweise der Einstellungs-Dateien** (Variablen, Plattform-Dateien, Umschlag, Kopf der Geschichten) – überall gleich:

| Zeile | Bedeutung |
|---|---|
| `# Titel`, `## Abschnitt` | Gliederung (Navigation im Editor) |
| `> Erklärung` | Kommentar, wird nie gedruckt und nie als Wert gelesen |
| `{name}: wert` | setzt eine Variable; im Buch erscheint sie als `{name}` |
| `feld: text` | Feld des Umschlags, eines Fotos oder einer Geschichte (keine Variable, darum ohne Klammern) |

**Das Zeichen `>` heisst je nach Datei etwas anderes:**

| Datei | `> …` heisst |
|---|---|
| Buchtext (`<buch>-buch.md`, Geschichten) | Zitat mit Verzierung – Markdown-Kurzform von `@ZITAT-ZIER` |
| Einstellungs-Dateien (Variablen, Umschlag, Plattform-Dateien) | Erklärung, wird nie gedruckt |

In jedem Abschnitt zuerst die Werte, darunter die Erklärungen: `> {name}: …`. Kein `- ` davor – das ist nur für
echte Listen (Aufzählung im Buch, Stichwort-Liste).

**Wo steht was?**

| Was | Wo | Im Buch / Umschlag |
|---|---|---|
| alles, was fürs ganze Buch gilt (Titel, Format, Shop, gemeinsames Impressum) | `<buch>-variablen.md`, z. B. `{impressum-rechte}: …` | `{impressum-rechte}` |
| alles, was nur für **eine Ausgabe** gilt: Plattform-Datei, ISBN, Preis, Herstellung, Logo | `<buch>-variablen.md` unter `## Ausgabe: Druck normal`, `Druck unzensiert`, `E-Book`, `E-Book unzensiert`, `PDF` | `{isbn}`, `{impressum-herstellung}` |
| die **Technik einer Druckerei** (Rücken, Beschnitt, Strichcode) | Plattform-Datei `druck/<datei>.md` | – |

Suchst du nach `{name}`, findest du beide Stellen: wo der Wert steht und wo er erscheint.
Unter `## Ausgabe: …` gilt ein Wert nur für diese Ausgabe und ersetzt dort den gleichnamigen von oben – so hat jede
Ausgabe ihr Impressum und ihre ISBN, mit kurzen Namen. Für einzelne Werte gibt es auch Endungen: `{name-uz}`,
`{name-druck}` … (der genauere Name gewinnt).

Das **Demo-Kapitel** in der Buch-Datei zeigt alle Möglichkeiten. Einmal `sh build.sh` laufen lassen,
das PDF ansehen und mit der MD vergleichen – danach das Demo löschen und schreiben.

## Schreiben

**Die Regel – vier Formen, je nach Aufgabe:**

| Form | Wofür | Beispiel |
|---|---|---|
| Markdown | alles, was Markdown kann: Absatz, Zeilenumbruch, neue Seite, fett, Liste | `\` am Zeilenende · `---` · `**fett**` · `- Punkt` |
| `@BEFEHL` | eine Zeile, eine Wirkung – nur für das, was Markdown nicht kann | `@PLATZ 40`, `@KOPF Ecuador`, `@ZITAT-ZIER …` |
| `## @…` / `#### @…` | Titelei-Seite (`##`) bzw. Element mit Angaben darunter (`####`, Ende = Leerzeile); steht in der Gliederung des Editors | `## @IMPRESSUM`, `#### @FOTO Sommer` |
| `::: art` … `:::` | Textbereich mit Anfang und Ende: nur in einer Fassung, umrahmt oder zusammenhaltend | `::: nur-uz`, `::: uz Titel`, `::: mitte` |

| Im Text | Wirkung |
|---|---|
| `# Teil 1\|Titel\|Untertitel` (`\|bild.jpg`) | neuer Teil mit Teil-Seite (optional eigenes Bild) |
| `# \|Anhang\|Untertitel` | Teil-Seite ohne Nummer, z. B. für den Anhang; darunter Kapitel mit `##` (Kopfzeile «Anhang · Kapitel») |
| `# Titel` | Kapitel oberster Ebene, neue Seite (Anhang, Zeitstrahl, Über den Autor) |
| `## Kapitel` / `### Zwischentitel` | Kapitel (im Inhalt) / kleiner Titel |
| `## @BEFEHL` | Befehl als Überschrift (sichtbar in der Navigation des Editors) |
| `@ZITAT Satz` · `@ZITAT-ZIER Satz` (kurz `> Satz`) · `~ Satz` | Zitat schlicht · Zitat mit Verzierung · Randbemerkung |
| `- Punkt` · `**fett**` · `[Text](https://…)` | Liste · fett · Link |
| `1. Punkt` `2. Punkt` | nummerierte Aufzählung (zählt selbst: die erste Zahl ist der Start) |
| `  - Unterpunkt` | Unterpunkt, 2–4 Leerzeichen eingerückt (unter `-` und unter `1.`) |
| `3\. Mai war …` | Zahl mit Punkt am Zeilenanfang, aber keine Aufzählung |
| Leerzeile | neuer Absatz |
| `\` am Zeilenende | Zeilenumbruch im Absatz: die nächste Zeile gehört zum selben Absatz (in Variablen: `<br/>`) |
| `---` (eigene Zeile, davor eine Leerzeile) | neue Seite, wie `@UMBRUCH` (im Editor eine waagrechte Linie) |

**Blöcke** `::: art-ausgabe Titel` … `:::` – Art: `nur`, `mitte`, `zusammen`, `offen`,
`offen-notiz`, `zeitstrahl`, `uz` (Kasten der zweiten Ausgabe). Endung: keine (überall),
`-normal`, `-uz` (`-dc`), `-bildschirm`, `-druck`, `-ebook`, `-buch`, `-privatdruck`.

**Foto:** beginnt mit `#### @FOTO Titel` (steht so in der Gliederung des Editors), darunter die Angaben,
eine pro Zeile. **Die erste Leerzeile beendet das Foto** – ein `:::` braucht es nicht. `#### @FOTO-UZ Titel` = nur in der
zweiten Ausgabe (auch `-NORMAL`, `-DRUCK`, `-EBOOK` …).
```text
#### @FOTO Sommer
datei: sommer-1980.jpg     Bild im Ordner fotos/ (Grösse: fotos/readme.txt)
text: Bildunterschrift     (optional)
breite: 60                 (optional) Breite in mm
fluss: rechts              (optional) Text umfliesst das Bild, rechts oder links
quelle: Foto: Max Muster   (optional) erscheint im Bildnachweis im Anhang
alt: Kind auf rotem Dreirad (optional) Beschreibung fürs E-Book (Vorlesefunktion); sonst gilt text:
ausschnitt: oben           (optional, nur mit foto-format) was beim Zuschneiden bleibt: oben, unten, links, rechts

Hier geht der Text weiter.
```
Eine Zeile ohne bekanntes Feld (z. B. `Vorschlag: …`) erscheint im Entwurf im Kasten, solange das Foto fehlt.

**Titelei:** Titelseite, Impressum, Hinweis und Widmung stehen ohne `:::` als eigene Abschnitte:
```text
## @TITEL
{titel}
{untertitel}
{titel-zusatz}               weitere Zeilen werden mit « · » an den Untertitel gehängt

## @IMPRESSUM
                             leer lassen: der Motor setzt die Zeilen je Ausgabe selbst ein (siehe unten)

## @HINWEIS
Unten im Impressum, mit Abstand (z. B. «ersetzt keine Beratung»).

## @WIDMUNG
Im Druck allein auf der rechten Seite gegenüber dem Impressum, im unteren Drittel; im Lese-PDF auf eigener Seite.
```
**Impressum:** Bleibt `## @IMPRESSUM` leer, setzt der Motor für jede Ausgabe ein:
`© {jahr} {autor}` · `{website}` · `{impressum-herstellung}` · `{impressum-satz1}` · `{impressum-satz2}` · `{impressum-rechte}` · `{impressum-hinweis}` · `{impressum-kontakt}` · `{auflage}` · `ISBN {isbn}`.
Leere Zeilen fallen weg (im Lese-PDF also Herstellung, Logo und ISBN). Die Werte stehen in der Variablen-Datei:
gemeinsame unter `## Impressum`, die einer Ausgabe unter `## Ausgabe: …`. Eigene Zeilen unter `## @IMPRESSUM`
gehen auch; dann gelten nur diese. Im Druck: Seite 2 links Impressum (oben das Logo aus `{impressum-logo}`),
Seite 3 rechts Widmung. Im Lese-PDF: Titel allein, danach Impressum auf eigener Seite unten.

**Auflage:** `{auflage}: 1. Auflage 2026` steht über der ISBN. Bei Print-on-Demand bleibt sie bei kleinen
Korrekturen gleich; erst bei spürbar geändertem Inhalt z. B. `2., überarbeitete Auflage 2028` (dann meist neue ISBN).
Nur in einer Fassung: `{auflage-uz}:` leer = dort keine Auflage-Zeile.

**Satz und Begleitung:** `{impressum-satz1}` und `{impressum-satz2}` sind zwei freie Zeilen direkt unter der
Herstellung, z. B. `{impressum-satz1}: Gesetzt mit pureSATZ · github.com/tgsteiger/pureSATZ` (Vorgabe in neuen
Büchern) und `{impressum-satz2}: LLM Begleitung: …`. Sie stehen in allen Ausgaben (Lese-PDF, Druck, E-Book,
Leseprobe …); leer = Zeile fällt weg.

**Seiten:** `---` oder `@UMBRUCH` neue Seite · `@UMBRUCH-RECHTS` im Druck rechts · `@PLATZ 60` neue Seite, wenn
weniger als 60 mm Platz · `@ABSTAND 8` Leerraum · `::: zusammen` nie trennen · `@SEITENMITTE`.

**Weiteres:** `@TITEL`, `@IMPRESSUM`, `@HINWEIS`, `@WIDMUNG`, `@KERNSATZ`, `@INHALTSVERZEICHNIS`, `@ZITAT`, `@ZITAT-ZIER`, `@MOTTO`, `@UNTEN`,
`@ZIER 12`, `@ZIER-UNTEN`, `@ZIER-TRENNER`, `@QR url | Text`, `@QR-PAAR … ;; …`, `@PORTRAIT bild | Text`,
`@KOPF`, `@STICHWORTE`, `@RUECKSEITE`. Vollständige Liste: `python3 motor/manuskript.py`.

## Variablen

- In der Variablen-Datei `{titel}: …`, im Buch und im Umschlag `{titel}` – derselbe Name an beiden Stellen.
- `name-normal` / `name-uz`: Wert je Ausgabe. `{name}` nimmt automatisch den richtigen.
- Eine Zeile, in der eine Variable leer ist, fällt weg.
- `format`: `a5` · `taschenbuch` · `sachbuch` · `a4` · `quadrat` (Masse laut epubli) oder eigenes Mass `150 x 215` (mm)
- `## Ausgabe: …`: Werte nur für diese Ausgabe (siehe «Ausgaben»)
- `zier`: eigenes Bild für die Verzierung (sonst die Standard-Verzierung)
- `# LAYOUT`: `farbschema`, `farbe-haupt`, `farbe-akzent` …, `schrift-text`, `schrift-titel`, `schriftgroesse`, `blocksatz`

**Alle Variablen der Vorlage auf einen Blick** (Erklärungen auch direkt in der Variablen-Datei):

| Bereich | Variablen |
|---|---|
| Buch | `titel`, `untertitel`, `autor`, `website`, `ort`, `jahr`, `auflage`, `stand`, `format` |
| Zwei Ausgaben | `zweite-ausgabe` (ja/nein), `ausgabe-name-normal` / `-uz`, `stempel-uz` (z. B. UNZENSIERT), `kasten-hinweis` |
| Impressum | `impressum-rechte`, `impressum-kontakt` |
| Ausgabe: … | `druck-datei`, `isbn`, `preis`, `impressum-herstellung`, `impressum-kontakt`, `impressum-logo`, `erstellen` (nur E-Book) |
| E-Book | `ebook-epub2` (ja = zusätzlich EPUB 2), `ebook-rueckseite` (bild / text / nein), `ebook-barrierefreiheit`, `farbe-akzent-ebook` |
| Shop | `shop-beschreibung`, `shop-schlagwoerter`, `shop-kategorie`, `shop-link` |
| Leseprobe | `leseprobe`, `leseprobe-seiten`, `leseprobe-seiten-uz`, `leseprobe-text` |
| Technik | `kurz-…`, `datei-…`, `ordner-…` |
| Weiteres | `stichworte`, `trennstellen` (Welt\|anschauung), `zier`, `zier-hell`, `kopfzeile` (ohne-autor · autor · wechselnd), `foto-format`, `md-history-behalten`, `bildschirm-dunkler`, `mockup-hintergrund` |
| Sicherung | `sicherung-lokal`, `sicherung-cloud`, `sicherung-behalten` |
| Layout | `farbschema`, `farbe-text`, `farbe-leise`, `farbe-haupt`, `farbe-akzent`, `farbe-papier`, `farbe-kasten`, `farbe-stempel`, `schrift-text`, `schrift-titel`, `schriftgroesse`, `zeilenabstand`, `inhalt-dichte`, `blocksatz` |

**Rückenbreite:** steht in der Plattform-Datei (siehe «Plattform-Dateien», Coverrechner).

## Farbschemas

Unter `## Farben` stehen mehrere Farbschemas; eine Zahl wählt, welches gilt – für alle Ausgaben:

```text
## Farben
{farbschema}: 2

### Farbschema 1: Standard
{farbe-text}: #2E2A26
{farbe-leise}: #6E655C
…                                alle Farben
### Farbschema 2: dunkler für den Druck
{farbe-text}: #1A1714
{farbe-leise}: #4E4741          nur was anders ist
```

Schema 1 ist immer die Grundlage; das gewählte Schema ersetzt nur die Werte, die darin stehen. Andere Schemas
werden übergangen. Ausprobieren: Zahl ändern, `sh build.sh nur-pdf`, PDF ansehen (vorher das alte PDF unter
anderem Namen sichern – jeder Bau überschreibt es). Zurück auf `1`: beim nächsten Bau ist alles wie vorher.
Der Bau zeigt am Anfang und am Ende, welches gilt (z. B. «Farben: Farbschema 2: dunkler für den Druck»). Fehlt das gewählte Schema, meldet der Bau «Farbschema … fehlt – nehme Schema 1». Ohne `{farbschema}` gelten
die `{farbe-…}`-Zeilen direkt unter `## Farben`.

## Bilder und Fotos

| Ordner | Was | Format | Pixel (300 dpi: Breite in mm × 12) |
|---|---|---|---|
| `fotos/` | Fotos im Text (`#### @FOTO`) | JPG, RGB (nicht CMYK) | ganze Breite A5: mind. 1400 · `breite: 60`: 700 · `fluss`: 500 |
| `bilder/` | Porträt, Verzierung, Teil-Bilder | PNG, gern transparent | Porträt 600 × 600 · Teil-Bild 1200 |

Dateinamen ohne Leerzeichen und Umlaute, z. B. `sommer-1980.jpg`. Handyfotos sind ideal.

**Das macht der Motor selbst:** grosse Fotos auf 1800 Pixel verkleinern (`_bildcache/`, kleine PDFs, schneller Bau) ·
im Druck Transparenz auf Papierfarbe setzen (epubli) · fehlendes Foto: im Entwurf ein Kasten, im Druck nichts ·
`quelle:` kommt in den Bildnachweis · `sh build.sh pruefen` meldet Fotos, die im Druck unscharf würden.

**Grösse:** Ohne Angaben ist ein Foto so breit wie der Text und höchstens 75 mm hoch – ein Querformat wird also
breit, ein Hochformat schmaler. Steht es am Seitenende, wird es etwas kleiner (bis 38 mm), damit keine Lücke bleibt.

**Alle Fotos gleich gross** (Variablen-Datei, Abschnitt «Fotos», alles freiwillig):

```text
{foto-format}: 3:2        alle auf dasselbe Seitenverhältnis zuschneiden (4:3, 16:9, quadrat …)
{foto-breite}: 100        einheitliche Breite in mm (ein «breite:» im Foto geht vor)
{foto-anpassen}: nein     am Seitenende nie verkleinern
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
`@@` ist das Buch eine einzige Buchdatei.

```sh
sh neu.sh "Schutzschild hoch!"     # legt geschichten/schutzschild-hoch.md an (Windows: neu.bat "…")
sh neu.sh                          # Übersicht: Stand, Wörter, im Buch ja/nein
sh build.sh geschichten            # Sammel-PDF aller Geschichten (normal) · «geschichten uz» auch unzensiert
```

**Eine Geschichte** (`geschichten/schutzschild-hoch.md`):

```
## Schutzschild hoch!
stand: entwurf
stichworte: Emotionscode, Schutz
quelle: Praxis 2018

Text, wie im Buch: Absätze, **fett**, @ZITAT-ZIER Zitat, ::: Blöcke, Fotos, {variablen}.
```

- Die drei Zeilen unter dem Titel sind freiwillig und werden nicht gedruckt.
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

## Menü

`sh menu.sh` (Windows: `menu.bat`) zeigt die häufigsten Befehle. Ein Buchstabe genügt:

```
  s  schnell       k  komplett      b  bauen …       m  MD öffnen …
  p  PDF …         o  Ordner …      g  gegenlesen …  a  änderungen
  sy sync          u  update        t  Ton ein/aus   h  hilfe
  q  beenden
```

- `b`, `m`, `p`, `o`, `g` haben ein Untermenü (Enter oder `z` = zurück). `o` Ordner: Buchordner, normal,
  unzensiert, druck. `g` gegenlesen (Personen prüfen ihre Stellen): `l` Liste neu (personen-seiten.txt),
  `c` check-PDF für eine Person (check_Name_Gegenlesen.pdf, öffnet sich danach), `t` Textdatei öffnen.
- ↑ ↓ = letzte Befehle, Enter führt sie aus. Ganze Befehle gehen auch: `final`, `leseprobe uz 18,20`, `personen Eltern`.
- MD, PDF und Ordner öffnen im eigenen Programm, das Menü bleibt bereit. Bauen läuft im Menüfenster;
  am Schluss «Fertig» mit Dauer und Ton (`t` = ein/aus). Eigener Klang: `klang.wav` in den Buchordner legen.
- `ul` (update lokal) erscheint nur, wenn neben dem Buch ein Ordner `pureSATZ` liegt.
- Ton und letzte Befehle stehen in `.menu` (kommt nicht zu GitHub).

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
sh build.sh leseprobe uz 18,20,23   # einmalig diese Seiten, nur diese Fassung (normal oder uz; ohne = beide)
sh build.sh korrektur       # Korrekturfassung: A4, Zeilennummern pro Seite, Rand für Notizen
sh build.sh geschichten     # Sammel-PDF aller Geschichten aus geschichten/ (mit «uz»: auch unzensiert)
sh build.sh stand "Probedruck 1"   # jetzigen Stand festhalten · sh build.sh stand = alle Stände
sh build.sh personen        # Personen im Buch mit Seiten und Zeilen → personen-seiten.txt
sh build.sh personen Thomas # check_Thomas_Gegenlesen.pdf: seine Seiten zum Gegenlesen
sh build.sh aenderungen     # letzte Änderungen als PDF · aenderungen 3 = seit Stand 3 · aenderungen 22.10. = seit Datum
sh neu.sh "Titel"           # neue Geschichte anlegen · sh neu.sh = Übersicht (Windows: neu.bat)
sh sicherung.sh             # ganzes Buch als ZIP sichern (lokal und/oder cloud)
sh cleanup.sh               # aufräumen: Altes löschen / entfernen (delete), fragt zuerst; md-history/ bleibt
sh cleanup.sh ausgaben      # dazu auch die Ausgabeordner löschen (macht sh build.sh final jederzeit neu)
python3 motor/manuskript.py # Liste aller @-Befehle
python3 motor/stichworte-vorschlag.py   # Vorschläge fürs Stichwortverzeichnis
```

**final oder komplett?**

| | `sh build.sh final` | `sh build.sh komplett` |
|---|---|---|
| Lese-PDF (normal, unzensiert) | ✔ | ✔ |
| Druckdateien: Buchblock, Umschlag | ✔ | ✔ |
| E-Book (EPUB) | ✔ | ✔ |
| Probedruck-Booklet, Mockup, Shop-Angaben, Seitenbilanz, Kontrast | ✔ | ✔ |
| Leseprobe (PDF und EPUB) | – | ✔ |
| Korrektur-PDF (A4, Zeilennummern) | – | ✔ |
| Dauer | normal | etwas länger |

**final** für jede Druckfassung und jedes Hochladen. **komplett** vor einer Bestellung, Veröffentlichung oder
Korrekturrunde. Leseprobe und Korrektur gehen auch einzeln: `sh build.sh leseprobe`, `sh build.sh korrektur`.

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
kommen aus Zeilen `feld-ebook:` (oder Blöcken `::: nur-ebook`); gibt es keine, gelten die des Drucks
(`fuss-druck: Erstausgabe {jahr}` statt `fuss-bildschirm: Stand {stand}`). Dasselbe gilt für das Titelbild im E-Book.
Das Vorne-Bild ist das **Titelbild für E-Book-Shops** (tolino media, neobooks, BoD, KDP verlangen ein JPG im
Hochformat, mindestens 1600 Pixel breit); beide eignen sich auch für Presse, Verlag und Webseite.
Unterschied zu `<KURZ>_Cover_Vorderseite.jpg` im Druckordner: Jenes ist für die Druckerei (400 dpi, mit 3 mm
Beschnitt rundum, der beim Schneiden wegfällt) – fürs E-Book also das `…_Cover-vorne.jpg` nehmen.

**Leseprobe** (`…_Leseprobe.pdf` und `…_Leseprobe.epub`, Schlussseite mit QR-Code zu `shop-link:`, sonst zur Website):
Umschlag und Titelei bis zum Inhaltsverzeichnis, dann die Seiten aus `leseprobe-seiten:` (gedruckte Seitenzahlen,
z. B. `14,16,17-20,22`; für die zweite Ausgabe eigene mit `leseprobe-seiten-uz:`). Seiten gehen auch direkt in `leseprobe:` (mit Komma oder Strich, z. B.
`leseprobe: 17,18-22, 74, 88-92`; eine Zahl allein = Anzahl Kapitel). Einmalig andere Seiten ohne die Variablen zu
ändern: `sh build.sh leseprobe 18,20,23` (mit `normal` oder `uz` nur diese Fassung). Ohne Seiten gilt `leseprobe:`
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
`stichworte-vorschlag.txt`. Mit `sh cleanup.sh ausgaben` auch die Ausgabeordner. **Nie gelöscht:** `md-history/`, `staende/`,
die MD-Dateien, Stichworte, `fotos/`, `bilder/`, `motor/`, `.venv/` und alles, was das Skript nicht kennt.
Alte ZIP-Sicherungen räumt `sicherung-behalten:` auf, alte Stände in md-history `md-history-behalten:`.

Vor jedem Bau werden die drei MD-Dateien nach `md-history/` gesichert und geprüft (unbekannte
`{Variablen}` oder `@Befehle`, fehlende Fotos – mit Zeilennummer). Gebaut wird parallel.

## Was im Ausgabeordner liegt (00-UEBERSICHT.txt)

Nach jedem Bau steht zuoberst im Ausgabeordner (`ausgabe-normal/`, `ausgabe-unzensiert/` …) die Datei
`00-UEBERSICHT.txt`. Sie zeigt, **welche Datei wofür** ist. Oben: der letzte Bau (Art, Datum, pureSATZ-Version,
Druckdatei) und eine eigene Zeile **Druckdateien: FINAL** bzw. **ENTWURF – nicht hochladen!** – sie bleibt auch nach
`schnell` oder `leseprobe` stehen. Bei jeder Datei stehen Datum und Uhrzeit: so sieht man, ob sie vom letzten Bau stammt.
Aufbau wie in `personen-seiten.txt` und den Meldungen im Terminal: `#` Titel · `>` Erklärung · `$` Befehl
(fehlt etwas, steht der Befehl dazu in einer eigenen Zeile – ab `sh` kopieren).

Am Ende jedes Baus listet das Terminal die **neuen PDFs und E-Books** auf, darunter den Befehl zum Öffnen mit dem
Standardprogramm: Linux `xdg-open <Datei>` · Mac `open <Datei>` · Windows `start "" <Datei>`. Welches Programm
E-Books öffnet, stellt man im System ein (Linux z. B. Calibre:
`xdg-mime default calibre-ebook-viewer.desktop application/epub+zip`).

| Gruppe | Dateien |
|---|---|
| Bei der Druckerei hochladen | `<kurz>_Buchblock.pdf`, `<kurz>_Umschlag_Hardcover` bzw. `_Softcover` (PDF und JPG) |
| E-Book | `<datei>.epub` (und `_EPUB2.epub`), `<datei>_Inhalt.pdf` (Inhaltsverzeichnis), `<datei>_Cover-vorne.jpg` (Titelbild, auch als `_2000px`, `_1600px`, `_900px`) |
| Zum Lesen und Verschicken | `<datei>.pdf`, `_Leseprobe.pdf`, `_Korrektur.pdf` (fürs Lektorat), `_Aenderungen.pdf` |
| Gegenlesen | `check_<Name>_Gegenlesen.pdf` (nur wenn vorhanden, `sh build.sh personen Name`) |
| Werbung | `<datei>_Mockup.jpg`, `<datei>_Vorderseite.jpg` |
| Selber drucken | `<kurz>_Probedruck_booklet.pdf` bzw. `<datei>_booklet.pdf` |
| Texte für den Shop | `shop-angaben.txt` |
| Weitere Dateien | z. B. Vorder- und Rückseite einzeln als PDF und JPG – zur Auswahl |

Fehlt etwas, nennt die Übersicht den Befehl dazu (z. B. `sh build.sh leseprobe`). Testläufe
(`druck=…`) haben in `ausgabe-test/<datei>/` ihre eigene Übersicht. Hat eine Ausgabe kein E-Book
(`{erstellen}: nein`), steht das in der Gruppe E-Book.

## Tipps aus der Praxis

**Arbeiten im Alltag**
- Beim Schreiben `sh build.sh schnell`, vor dem Hochladen oder Bestellen `sh build.sh final`. `nur-druck` braucht man kaum.
- Nach jeder Korrekturrunde `sh build.sh stand "Name"`. `sh build.sh aenderungen` zeigt dann, was du geändert hast.
- Am Anfang und am Ende der Arbeit `sh sync.sh` (mit GitHub).

**Editor (z. B. ghostwriter)**
- «Auto save» ausschalten, nur mit Ctrl+S speichern.
- Meldet der Editor «Datei wurde geändert – neu laden?»: mit Ja neu laden und erst danach weiterschreiben.
- Ändert jemand anders an der Datei (ein Skript, eine KI): sie vorher im Editor schliessen.
- Ging etwas verloren: Die letzten Fassungen liegen in `md-history/` (siehe «Sichern und zurückholen»).

**Gestalten**
- Mehrere Leerzeilen geben nicht mehr Abstand. Für Luft: `@ABSTAND 8` (nicht innerhalb eines `:::`-Blocks).
- `::: mitte` passt für kurze Abschlüsse am Ende eines Teils.
- Eine Dankesseite oder ein Nachwort wirkt als normales Kapitel ruhiger und steht im Inhaltsverzeichnis:
  `## Danke`, Text im Blocksatz, zum Schluss `@ZITAT Gruss<br/>Name` und `@ZIER 10`.
- Nur eine Verzierung pro Seite – sonst wird es unruhig.

**Probedruck und Farben**
- Farben am Bildschirm nur grob beurteilen. Was zählt, ist der Probedruck auf dem echten Papier (matt/glänzend, weiss/creme).
- Seitenzahl geändert: im Coverrechner der Druckerei prüfen, ob Rücken und Umschlag gleich bleiben. Dann
  `{berechnet-fuer-seiten}` anpassen und `{neu-berechnen}: nein` setzen.

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
bzw. `_Softcover.jpg` hochladen. Erst ein Testexemplar (`{projekt}: privatdruck` in der Plattform-Datei), dann
«Buch veröffentlichen»; die ISBN von epubli unter `## Ausgabe: Druck normal` bei `{isbn}:` eintragen und neu bauen.
E-Book (`.epub`): eigene ISBN unter `## Ausgabe: E-Book` bei `{isbn}:`, dann bei tolino media oder KDP hochladen.
Das E-Book enthält Angaben zur **Barrierefreiheit** (Gliederung, Inhaltsverzeichnis, Bildbeschreibungen);
`sh build.sh` warnt bei Fotos ohne `alt:` und ohne `text:`. Eigene Zusammenfassung: `ebook-barrierefreiheit:`. Die Akzentfarbe für Text wird im E-Book automatisch
lesbar dunkel gesetzt (Kontrast 4,5:1); eigene Farbe mit `farbe-akzent-ebook:`.

## Ausgaben

In der Variablen-Datei hat jede Ausgabe einen Abschnitt. Was dort steht, gilt nur für diese Ausgabe:

```text
## Ausgabe: PDF                  Lese-PDF, Leseprobe, Korrektur, Booklet – meist leer
## Ausgabe: Druck normal         {druck-datei}, {isbn}, {preis}, {impressum-herstellung}, {impressum-logo} …
## Ausgabe: Druck unzensiert     (zweite Ausgabe; auch «Druck zweite Ausgabe»)
## Ausgabe: E-Book               {isbn}, {preis}, {impressum-herstellung} …
## Ausgabe: E-Book unzensiert    {erstellen}: nein = kein E-Book dieser Ausgabe
```

Ein Wert hier ersetzt den gleichnamigen aus `## Impressum` (z. B. eine eigene `{impressum-kontakt}`-Zeile der
Druckerei). Fehlt er, gilt der gemeinsame. Leer (`{isbn}:`) = die Zeile fällt weg. `{druck-datei}` nennt die
Plattform-Datei in `druck/` (Name ohne `.md`; auch `reserve/bod-a5`). `shop-angaben.txt` zeigt ISBN und Preis.

Beispiel Leben123: Normal gedruckt bei tredition (mit Logo und ISBN), Unzensiert als Privatdruck bei epubli
(ohne ISBN, mit der Kontaktzeile von epubli), E-Book bei tredition, kein E-Book der unzensierten Fassung.
Wechselst du die Druckerei, änderst du `{druck-datei}` und die Impressum-Zeilen dieser Ausgabe.

## Plattform-Dateien (druck/)

Die Plattform-Datei enthält nur die **Technik** einer Druckerei. Ihre Werte gelten nur für Buchblock und Umschlag.
Lese-PDF, E-Book, Leseprobe, Korrektur und Mockup bleiben beim `{format}` der Variablen-Datei (Grundformat).

| In der Plattform-Datei | Bedeutung |
|---|---|
| `neu-berechnen` | `ja` = Seitenzahl hat sich geändert, im Coverrechner neu berechnen (der Bau erinnert daran) · `nein` = Werte passen |
| `berechnet-fuer-seiten` | Seiten des Buchblocks, für die Rücken und Umschlag berechnet sind; weicht der Buchblock ab, warnt `final` |
| `plattform` | `epubli`, `bod`, `tredition` oder `kdp` (bestimmt Strichcode-Platz und Füllseite; tredition und kdp wie bod) |
| `farbmodus` | `rgb` (Standard) oder `cmyk`: Buchblock und Umschlag werden bei `final` und `komplett` mit Ghostscript nach CMYK umgewandelt (z. B. für tredition); im Entwurf bleiben sie RGB (schneller). Jeder Bau rechnet neu aus den Originalbildern, es wird nie mehrfach umgewandelt. Braucht Ghostscript (Linux `sudo apt install ghostscript` · Mac `brew install ghostscript` · Windows `winget install ArtifexSoftware.GhostScript`). Lese-PDF, E-Book und Leseprobe bleiben RGB. |
| `format` | nur, wenn das Druckformat vom Grundformat abweicht; auch eigenes Mass `148 x 210` (Ränder und Schrift vom nächstliegenden Format) |
| `bindung`, `projekt`, `papier`, `extra-seiten` | `hardcover`/`softcover`/`beide` · `veroeffentlichen`/`privatdruck` · Papier zur Info · leere Notizseiten am Schluss |
| `ruecken-hardcover`, `ruecken-softcover` | Rücken in mm laut Coverrechner der Plattform |
| `beschnitt-buchblock`, `beschnitt-hardcover`, `beschnitt-softcover`, `deckel-hardcover` | Masse in mm (BoD: Buchblock 0, Deckel 153x216, Einschlag 17) |
| `barcode-position` | `links` · `mitte` · `rechts` (leer: epubli links frei, BoD rechts) |
| `barcode-groesse` | z. B. `40x20` (mm, 16 mm vom Rand seitlich, 8 mm von unten); leer = 60 × 35 mm ab der Ecke frei |
| `barcode-bild` | PNG aus `bilder/` auf weissem Feld; leer = nichts zeichnen (BoD: Strichcode aus der ISBN) |
| `versatz-vertikal`, `versatz-horizontal` | ganzen Seiteninhalt verschieben, in mm: vertikal + = nach oben, horizontal + = nach aussen (nach Messung am Probeexemplar) |

Zuunterst steht `## Coverrechner (Rohdaten)`: Dort fügst du ein, was der Coverrechner der Plattform ausgibt
(Text, wie er kommt). Der Motor liest diesen Abschnitt nicht. Mit Claude: «Coverwerte übernehmen» – dann stehen die
Werte oben, `{neu-berechnen}: nein` und `{berechnet-fuer-seiten}` passen.

**Rückenbreite:** `sh build.sh final` zeigt die Seitenzahl des Buchblocks. Diese im Coverrechner eingeben (mit dem
Papier, das du bestellst), Werte übernehmen, nochmals bauen. `final` zeigt die Masse des Umschlags (z. B. 344 × 250 mm)
– sie müssen mit Gesamtbreite und Gesamthöhe im Coverrechner übereinstimmen.

`name-normal` / `name-uz` gehen auch in der Plattform-Datei. Weicht das Druckformat vom Grundformat ab, meldet der
Bau «Seitenzahlen im Druck anders als im Lese-PDF». Beim Bau steht `Druckangaben: druck/…md`, und eine Kopie der
Datei liegt im Ausgabeordner. `sh build.sh pruefen` meldet fehlende Plattform-Dateien und unbekannte Namen.

**Versatz nach dem Probeexemplar:** Am gedruckten Buch messen: oben vom Papierrand bis zur Kopfzeile (Soll bei A5
8 mm) und unten bis zur Seitenzahl (Soll 10,5 mm). Misst du z. B. oben 6,5 und unten 12 mm, sitzt alles 1,5 mm zu hoch:
in der Plattform-Datei `{versatz-vertikal}: -1.5`. Seitlich genauso mit `versatz-horizontal` (+ = nach aussen). Text, Kopfzeile,
Seitenzahl und Bilder verschieben sich gemeinsam, das Layout bleibt gleich; nur der Buchblock dieser Druckerei ist
betroffen. Der Beschnitt reicht als Reserve (bei 5 mm bis etwa 3 mm Versatz); mehr meldet der Bau als Warnung.

**Ausgabeordner:** Ein normaler Bau legt die Druckdateien immer in `ausgabe-normal/` bzw. `ausgabe-unzensiert/` –
egal welche Plattform. **Testlauf:** `sh build.sh final druck=<datei>` baut nur Buchblock und Umschlag mit dieser
Datei nach `ausgabe-test/<datei>/` (mit `normal` oder `uz`: nur diese Fassung); ein neuer Test überschreibt den alten.
`ausgabe-test/` kommt nicht zu GitHub und nicht in die Sicherung, `sh cleanup.sh ausgaben` löscht ihn mit. Gefällt der
Test, `{druck-datei}` der Ausgabe umstellen. Nicht gebrauchte Plattform-Dateien liegen in `druck/reserve/`.
**Andere Plattform** (z. B. KDP): eine Musterdatei kopieren, z. B. als `druck/kdp-dein-format.md`, die Werte aus
dem Coverrechner der Plattform eintragen und mit `druck=kdp-dein-format` testen. Als `plattform` passt meist `bod`.
**Muster** (beim neuen Buch schon in `druck/`, sonst in `pureSATZ/vorlage/druck/`): `epubli-a5`,
`epubli-taschenbuch`, `epubli-sachbuch`, `epubli-a4`, `epubli-quadrat`, `bod-a5-hardcover`, `tredition-a5-hardcover`.
Unter `## Notizen` steht bei jedem Muster, welche Impressum-Zeilen diese Plattform verlangt.

# Andere Plattformen

## Druck bei KDP, Lulu und anderen

Für technisch Interessierte – der Motor kennt epubli und BoD, andere Druckereien gehen über eine eigene Druckdatei:

1. Eine Musterdatei kopieren, z. B. `druck/bod-a5-hardcover.md` als `druck/kdp-dein-format.md`.
2. Werte aus dem **Coverrechner** bzw. der Formatliste der Plattform eintragen: `{format}: 152,4 x 228,6`
   (eigenes Mass in mm), `ruecken-…`, `beschnitt-…`, `deckel-hardcover`, `papier`.
   Ohne Coverrechner: ein PDF hochladen – die Plattform nennt die Masse, die sie erwartet.
3. `plattform: bod` stehen lassen (Strichcode-Feld selbst bestimmen, keine epubli-Füllseite).
   Setzt die Plattform den Strichcode selbst (z. B. KDP), das Feld mit `barcode-position` / `barcode-groesse`
   frei lassen und `barcode-bild` leer.
4. Testen: `sh build.sh final druck=kdp-dein-format` → `ausgabe-test/kdp-dein-format/`, Masse in `00-UEBERSICHT.txt`
   mit dem Rechner der Plattform vergleichen. Passt alles: `{druck-datei}` unter `## Ausgabe: Druck …` umstellen.

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
- ISBN: eigene E-Book-ISBN unter `## Ausgabe: E-Book` bei `{isbn}:` eintragen und neu bauen (manche Shops vergeben selbst eine).
- Leseprobe als E-Book: `<datei>_Leseprobe.epub` (`sh build.sh leseprobe`).
- **EPUB 2:** pureSATZ baut EPUB 3, das tolino, KDP, Apple, BoD und XinXii annehmen. Verlangt ein Shop oder
  Prüfprogramm EPUB 2 (z. B. epubli: «EPUB-Version zu hoch»), in der Variablen-Datei `ebook-epub2: ja` setzen –
  dann entsteht zusätzlich `<datei>_EPUB2.epub` («epub2-light»: gleicher Inhalt, mit den Angaben zur Barrierefreiheit).
  Von Hand aus einem fertigen E-Book: `python3 motor/epub2.py ausgabe-normal/<datei>.epub`.
- **Vorder- und Rückseite im E-Book:** Erste Seite ist immer das Cover vorne. Als letzte Seite kommt die Rückseite
  (`ebook-rueckseite`, Standard `bild`): das Bild der Rückseite ohne Strichcode, Slogan, Klappentext und Zitate stehen
  als Beschreibung für Vorleseprogramme dabei. `text` = dieselben Texte als Seite «Über dieses Buch» (gut lesbar auf
  kleinen Geräten), `nein` = keine Rückseite. Gilt auch für EPUB 2 und die Leseprobe. Die Texte kommen aus `# Rückseite`
  der Umschlag-Datei. Das Bildschirm-PDF hat Vorder- und Rückseite schon immer.

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

## Was hat sich geändert? (Stände)

| Ich will … | Befehl |
|---|---|
| eine Runde abschliessen | `sh build.sh stand "Korrektur Eltern"` |
| die letzten Änderungen sehen | `sh build.sh aenderungen` |
| Änderungen seit Stand 3 | `sh build.sh aenderungen 3` |
| Änderungen seit einem Datum | `sh build.sh aenderungen 22.10.` |
| alle Stände (nummeriert, 1 = letzter) | `sh build.sh stand` |

Am Schluss steht der Befehl zum Öffnen: `PDF: xdg-open "…"`. Ist seit dem letzten Stand nichts geändert,
zeigt `aenderungen` die letzte Runde. Bei jeder Änderung steht das Datum: der erste Bau mit dieser Änderung
(aus md-history/), «heute» = seither noch nicht gebaut.

Mehr: `sh build.sh aenderungen "Probedruck 1" "Probedruck 2"` vergleicht zwei Stände;
`sh build.sh stand "Probedruck 1" 23.10.2026 15:00` hält einen Stand nachträglich fest (aus md-history/).

- **Ergebnis:** `…_Aenderungen.pdf` im Ausgabeordner der normalen Fassung (wird jedes Mal ersetzt). Oben eine
  Zusammenfassung («3 Absätze geändert · 1 neu · 1 gestrichen») und die betroffenen Kapitel, darunter nur die
  geänderten Absätze, nach Teil und Kapitel: neue Wörter **grün und unterstrichen**, gestrichene **rot und
  durchgestrichen**. Absätze in `::: nur-uz` / `nur-normal` sind markiert («nur Unzensiert»). Am Schluss
  geänderte Werte aus Variablen und Umschlag sowie neue oder entfernte Stichwörter.
- **Geschichten** aus `geschichten/` stehen an ihrer Stelle im Buch und werden mitverglichen.
- **Wo:** Jeder Stand ist eine Kopie der Texte in `staende/<datum>_<name>/` (Buch-, Variablen-, Umschlag-MD,
  Stichwörter, Geschichten). Der Ordner kommt mit `sh sync.sh` auf die anderen Computer und ins ZIP;
  `sh cleanup.sh` löscht ihn nie. Einen Stand nicht mehr gebraucht: seinen Ordner löschen.
- **Vergessen, den Stand festzuhalten?** Mit Datum und Uhrzeit dahinter holt der Motor die letzte Fassung vor
  diesem Zeitpunkt aus `md-history/` (der Bau für die Bestellung hat sie dort automatisch gesichert). Nur Datum =
  bis Ende Tag, nur Uhrzeit = heute. Der Stand bekommt das Datum dieser Fassung.
- Der Name muss nicht vollständig sein: `sh build.sh aenderungen probe` findet «Probedruck 1», wenn es eindeutig ist.
- **Tipp:** Stand festhalten, *bevor* du den Probedruck bestellst. Dann zeigt `aenderungen` nach den Korrekturen
  genau, was du seit dem gedruckten Exemplar verbessert hast – und Testleser lesen nur das Neue.

## Personen im Buch: Gegenlesen

Wer im Buch vorkommt, soll seine Stellen vorher lesen dürfen. pureSATZ findet die Personen, zeigt Seite und Zeile
(zum Anstreichen im Probedruck) und stellt pro Person ein PDF **zum Gegenlesen** zusammen. Neu gebaut wird dabei
nichts: gesucht wird in den fertigen Lese-PDFs, das dauert Sekunden.

```sh
sh build.sh personen          # 1. Personen finden → personen-seiten.txt
                              # 2. personen-seiten.txt korrigieren und speichern
sh build.sh personen Thomas   # 3. check_Thomas_Gegenlesen.pdf (und …_Gegenlesen-uz.pdf)
```

**personen-seiten.txt** (im Buchordner) ist Ergebnis und Eingabe zugleich:

```
# PERSONEN UND SEITEN – Mein Buch · 24.10.2026 22:40
> Begriffe derselben Person in eine Zeile, mit | getrennt. Der erste ist der Name (für die Datei).
> «--- Wort» = keine Person, nicht mehr vorschlagen (solange diese Datei besteht; ich sammle sie unten).
> Ganze Zeile gelöscht = wird beim nächsten Mal wieder vorgeschlagen. Datei löschen = alles neu.
$ sh build.sh personen   (Seiten neu, nach dem Korrigieren)
$ sh build.sh personen Thomas   (check_Thomas_Gegenlesen.pdf)

Thomas | Thom | Autor | Techniker               5 Stellen
  normal       S. 112 Z. 8 · S. 113 Z. 2, 17
               Kapitel: Schwitzhütte
  unzensiert   S. 118 Z. 4
  {leseprobe-seiten}: 112-113
  {leseprobe-seiten-uz}: 118

# KEINE PERSONEN
> nicht mehr vorschlagen – Zeile löschen = wieder vorschlagen
--- Ecuador
```

- `#` Titel · `>` Erklärung · `$` Befehl. Wichtig sind nur die Zeilen mit den Namen (ganz links): Begriffe
  **derselben Person** mit `|` in eine Zeile nehmen, der **erste** gibt den Dateinamen. `--- Wort` (irgendwo in
  der Datei) = keine Person: wird unten unter «KEINE PERSONEN» gesammelt und nicht mehr vorgeschlagen, solange die
  Datei besteht. Eine ganz gelöschte Zeile kommt beim nächsten Mal wieder als Vorschlag. Eine eigene Zeile mit
  einem Namen, den der Motor nicht kennt, geht auch. Datei löschen = alles beginnt neu.
- **Ganzes Kapitel:** Steht ein Begriff im **Kapiteltitel** (z. B. «Ecuador» in «Ecuador und das runde Rad»), kommen
  alle Seiten dieses Kapitels dazu – in `{leseprobe-seiten…}` und im Gegenlesen-PDF (Zeile «ganzes Kapitel: …»).
- **Seiten von Hand:** Eine Zeile `+ uz: 59-60, 63` oder `+ normal: 41` direkt unter einer Person (ganz links) nimmt
  diese Seiten dazu, z. B. die Folgeseite eines Kastens. Der Motor lässt sie stehen, passt sie aber nicht an:
  nach einem Umbau selbst prüfen.
- Die Kopfzeile jeder Seite («Teil · Kapitel») zählt nicht als Fundstelle.
- Die eingerückten Zeilen schreibt der Motor bei jedem `sh build.sh personen` neu. Deine Namenszeilen bleiben,
  neu Gefundenes kommt unten dazu. Vorgeschlagen werden Vornamen, Rollen (Vater, Tochter, Nachbarin …) und
  Stichwörter mit Vornamen – der eigene Vorname (`{autor}`) nicht. Das Stichwortverzeichnis zählt nicht mit.
- **S.** = gedruckte Seite – gleich im Lese-PDF, im Probedruck und in der Leseprobe. **Z.** = Zeile auf der Seite,
  gezählt wie im Korrektur-PDF (die Kopfzeile ist Zeile 1); bei Fotos und Titeln ±1.
- **Gegenlesen:** `sh build.sh personen Thomas` sucht alle Begriffe der Zeile «Thomas» frisch und macht wie die
  Leseprobe Umschlag, Titelei, die Seiten und eine Schlussseite «Danke fürs Gegenlesen» – alles im Format des
  Korrektur-PDFs: A4, Zeilennummern links, Notizlinien rechts. Die Stellen der Person sind links mit einem roten ▶
  und roter Zeilennummer markiert. So kommt die Rückmeldung als «S. 41, Z. 7: …».
  Massgebend ist die Seitenzahl **unten auf der Buchseite** (oben rechts zählt die Datei: «Seite 3 / 9»). Kommt die Person nur in
  einer Fassung vor, entsteht nur dieses PDF. Die Zeilen `{leseprobe-seiten…}` lassen sich auch in die
  Variablen kopieren (dann `sh build.sh leseprobe`).
- Sind die Texte neuer als das Lese-PDF, kommt ein Hinweis: zuerst `sh build.sh final`.

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

## Ein neues Buch anlegen

Im Ordner pureSATZ: zuerst den neuesten Stand holen, dann das Buch anlegen. Es entsteht neben pureSATZ;
ein leerer Ordner mit demselben Namen wird einfach gefüllt, bestehende Dateien bleiben unberührt.

```sh
cd ../pureSATZ
git pull                    # neuester Motor und neueste Vorlage von GitHub
sh setup/setup.sh           # fragt Titel, Autor, technischen Namen (= Ordnername), Format, Bindung
```

Danach im neuen Buchordner `sh build.sh`. Mit GitHub: dort `git init -b main` und
`gh repo create <buchname> --private --source . --push` (siehe «Auf mehreren Computern»).

## Windows

Statt `sh build.sh …` einfach `build.bat …` (gleiche Optionen), ebenso `cleanup.bat`, `sicherung.bat` und `sync.bat`.

## Mit einer anderen KI arbeiten

Gib der KI zuerst `readme4ki.txt` (kurze Regeln, passt auch in kostenlose KI-Chats), dann die MD-Datei,
an der sie arbeiten soll (auch eine Druckdatei aus `druck/`). Danach `sh build.sh pruefen` – der Motor meldet sofort, falls etwas nicht passt.
