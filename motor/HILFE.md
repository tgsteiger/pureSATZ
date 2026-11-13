# Erste Schritte

## Hilfe verwenden, Lösungen finden

**Hilfe öffnen:** im Menü `h` (oder `?`) · ohne Menü `sh build.sh hilfe`.
**Suchen:** im Menü `hf wort` (hilfe finden) · in der Hilfe Taste `/`.

**Eine Lösung finden – in dieser Reihenfolge:**

1. In der Hilfe suchen: ein Wort aus der Meldung oder das, was du willst (z. B. `rücken`, `foto`).
2. [Wenn etwas klemmt](#Wenn-etwas-klemmt): häufige Meldungen und was hilft.
3. `sh build.sh pruefen`: nennt Datei und Zeile, wenn etwas nicht stimmt.
4. Eine KI fragen: [Mit einer KI arbeiten](#Mit-einer-KI-arbeiten).

**Die Hilfe als Webseite:** `sh build.sh hilfe` erzeugt `hilfe.html` im Buchordner und öffnet sie im Browser (Windows: `build.bat hilfe`).
Sie entsteht ausserdem bei jedem Bau neu. Oben ein **Suchfeld** (Taste `/`, `Esc` leert), ein Umschalter
**Linux/Mac · Windows** für alle Befehle und bei jedem Befehl ein Knopf **kopieren**.

**Suchen:** Die Hilfe schrumpft auf die Abschnitte mit dem Wort, es ist gelb markiert; grosse Tabellen zeigen nur
die passenden Zeilen («alle zeigen» holt den Rest). Verwandte Wörter finden sich gegenseitig: `isbn` findet auch
Strichcode, Barcode und EAN-13 · `löschen` auch aufräumen · `farbe` auch Farbschema · `hörbuch` auch vertonen.
Im Menü: `hf isbn` (hilfe finden) zeigt die Abschnitte als Liste, eine Nummer öffnet die Hilfe genau dort (schon gefiltert).
Ohne Menü: `sh build.sh hilfe isbn`.

Inhalt: Spickzettel, eigene Praxis-Notizen aus `meine-hilfe.md` (freiwillig, im Buchordner, selbst pflegen:
normales Markdown, jede `##`-Überschrift wird ein Abschnitt), diese Hilfe (`motor/HILFE.md`, kommt mit jedem
Motor-Update), alle Befehle und Blöcke direkt aus dem Motor und die Variablen dieses Buchs mit ihren Werten.

::: nur-webhilfe
Der Knopf **Start** oben springt zur Checkliste für den Anfang (`START.md` im Ordner pureSATZ, mit Häkchen
zum Anklicken).
:::

Ein Beispielbuch zum Ausprobieren: im Ordner pureSATZ `sh hallo.sh` (Windows: `hallo.bat`).

## Menü

`sh menu.sh` (Windows: `menu.bat`) zeigt die häufigsten Befehle, nach Arbeitsschritten geordnet. Ein Buchstabe genügt:

```
 ── Schreiben ─────────────────────   ── Bauen ─────────────────────────
  m  MD öffnen …                      s  schnell  (Lese-PDF)
  g  Geschichten …                    k  komplett (vor dem Druck)
  t  Tabellen …                       w  weitere …
  c  check / gegenlesen …             hb Hörbuch …   (nur Linux)
 ── Ansehen ───────────────────────   ── Abgleichen ────────────────────
  p  PDF öffnen …                     sy sync   (GitHub)
  o  Ordner öffnen …                  u  update (ul lokal)
  a  änderungen
 ── Weiteres:  n neu · $ Terminal · : Befehle · h hilfe · hf finden · ! Klang · ↵ beenden
```

**Coverrechner** (ab 2.78): Steht oben «⚠ Coverrechner …», passt der Umschlag nicht mehr zur Seitenzahl oder
`{neu-berechnen}: ja` steht noch in der Druckdatei. `cv` öffnet sie (siehe «Umschlag: Rücken und Seitenzahl»).

Ja/Nein-Fragen: `[J/n]` = Enter heisst ja, `[j/N]` = Enter heisst nein (der Grossbuchstabe gilt bei Enter).

Enter (oder `z`) = eine Stufe zurück; im Hauptmenü fragt Enter «Menü beenden? [j/N]» – nur `j` schliesst ·
Strg+C bei einer Frage = beenden (mit Rückfrage), während eines Laufs = nur den Lauf abbrechen.

Untermenüs («…» = nur was es gibt):

| | |
|---|---|
| `m` MD öffnen | `b` Buch · `v` Variablen · `u` Umschlag · `s` Stichworte · `h` meine Hilfe · `g` Geschichten … · `t` Tabellen … |
| `g` Geschichten | `e` schreiben … (Liste mit Kürzel) · `n` neue Geschichte (fragt nach dem Titel, öffnet sie) · `b` fehlende ins Buch · `a` alle in 1 Datei · `ü` Übersicht (auch `u`) · `s` Sammel-PDF |
| `t` Tabellen | `e` bearbeiten … (Liste mit Kürzel) · `n` neue Tabelle (öffnet die CSV, `@#name` kommt in den Block «## Noch einordnen» im Buch) · `o` Ordner |
| `c` check / gegenlesen | `n` Liste neu (personen-seiten.txt) · `c` check-PDF für eine Person (öffnet sich danach) · `t` Textdatei |
| `hb` Hörbuch (Linux) | `p` Probe hören · `w` Wörter hören · `t` Texte aus dem Buch · `v` vertonen · `k` Kapitel vertonen … · `e` Wörter/Probe/Einstellungen öffnen · `s` Azure-Schlüssel · `$` Terminal in audio/ · `o` Ordner · `h` Hilfe · `c` prüfen – siehe [Hörbuch: Das Menü](#Hörbuch-Das-Menü-hb) |
| `w` weitere | `l` Leseprobe · `k` Korrektur · `p` nur-pdf · `e` nur E-Book · `c` prüfen · `s` Stand merken · `i` Stichworte … (`v` Vorschläge · `u` übernehmen · `o` Stichwortdatei öffnen) · `a` aufräumen (wie `sh cleanup.sh`, fragt `[j/N]`) |
| `p` PDF öffnen | `n` normal · `u` unzensiert · `l` Leseprobe · `k` Korrektur … |
| `o` Ordner öffnen | `b` Buchordner · `n` normal · `u` unzensiert · `d` druck · `g` geschichten · `t` tabellen · `a` audio … · `p` Pfad Buchordner kopieren · dazu Taste + `t` = Terminal dort (`bt`, `at` …), + `p` = Pfad kopieren (`ap` …) |
| `n` neu | `b` neues Buch · `h` Hallo-Buch · `e` einrichten · `m` Motor-Selbsttest · `v` Verknüpfung |

- Geschichten (`g` → `e` oder `m` → `g`): jede hat ein festes Kürzel aus 1–3 Buchstaben, z. B. `h` herz-im-glueck,
  `he` heimweh. Neue bekommen das kürzeste freie (h · he · Anfänge der Wörter · hei), bestehende bleiben.
  Gespeichert in `geschichten/kuerzel.txt` (kommt mit sync zu GitHub, von Hand änderbar); gelöschte geben ihr Kürzel frei.
- ↑ ↓ = letzte Befehle, Enter führt sie aus. Ganze Befehle gehen auch: `final`, `leseprobe uz 18,20`, `personen Eltern`.
  `:` Befehle zeigt diese Befehle zum Tippen (aus dem Spickzettel der Hilfe), danach gleich eingeben. `?` = hilfe.
  Datei öffnen wie im Terminal: `xdg-open ausgabe-normal/….pdf` (Mac `open`, Windows `start`) – Pfad ab dem
  Buchordner, das Menü wartet nicht. Die Zeilen am Schluss eines Baus lassen sich so direkt einfügen.
- Nach einem Bau bleiben die Meldungen stehen: statt des Menüs nur «Eingabe (Enter = Menü)». Neu gebaute
  Lese-PDFs öffnen sich gleich (bei komplett nur normal und unzensiert).
- MD, PDF und Ordner öffnen im eigenen Programm, das Menü bleibt bereit. Bauen läuft im Menüfenster;
  am Schluss «Fertig» mit Dauer und Klang. Oben links der Buchname als goldenes Schild (auch im Fenster-/Tab-Titel),
  damit man bei mehreren Büchern sofort sieht, wo man ist. Oben rechts «Klang (!) ein/aus», Taste `!` (beim Einschalten klingt er einmal zur Probe).
  `$` öffnet ein Terminal im Buchordner, das Menü bleibt offen (praktisch, wenn das Menü per Lotus-Starter läuft).
  Klang: `motor/klang.wav`, eigener Klang: `klang.wav` in den Buchordner legen; sonst Piepton.
- `ul` (update lokal) erscheint nur, wenn neben dem Buch ein Ordner `pureSATZ` liegt; ebenso in `n` neu …:
  `b` neues Buch (setup), `h` Hallo-Buch, `e` einrichten (START-Linux.sh / START-Mac-imTerminal.sh / START-Windows.bat),
  `m` Motor-Selbsttest (test/selbsttest.py, einige Minuten, Ende «SELBSTTEST IN ORDNUNG»).
- `n` → `v` Verknüpfung (auch `sh menu.sh verknuepfung`): Starter mit Lotus, Doppelklick öffnet das Menü.
  Linux: Startmenü und Schreibtisch (beim ersten Mal Rechtsklick → «Start erlauben»), Windows: Buchordner und
  Schreibtisch, Mac: «Buch Menü.command» im Buchordner und auf dem Schreibtisch. Neue Bücher bekommen ihn mit `setup`.
  Buchordner verschoben? `v` nochmals – überschreibt den alten Starter.
- Klang und letzte Befehle stehen in `.menu` (kommt nicht zu GitHub).

## Die Buchdateien und Ordner

**Das Buch steht in drei MD-Dateien.** Alles andere macht der Motor.

| Datei | Inhalt |
|---|---|
| `<buch>-variablen.md` | `# VARIABLEN` (Buch, Impressum, Ausgaben mit ISBN und Preis, Shop), `# TECHNIK` (Dateien, Sicherung), `# LAYOUT` (Farben, Schriften) |
| `<buch>-buch.md` | das Buch: `## @TITEL`, `## @IMPRESSUM`, `## @HINWEIS`, `## @WIDMUNG`, `## @KERNSATZ`, `## @INHALTSVERZEICHNIS`, Kapitel und Teile |
| `<buch>-umschlag.md` | `## Vorderseite`, `## Buchrücken`, `## Rückseite`, darunter `feld: text` (`-druck`, `-bildschirm`, `-ebook`, `-uz` am Namen = nur dort), `> Erklärung` |
| `stichworte-<buch>.txt` | Stichwortverzeichnis: eine Zeile pro Stichwort, Varianten mit `\|`, `#` = Kommentar – siehe [Stichwortverzeichnis](#Stichwortverzeichnis) |
| `readme4ki.txt` | kurze Anleitung für eine andere KI (siehe unten) |

**Die Ordner im Buchordner:**

| Ordner | Inhalt |
|---|---|
| `druck/` | Plattform-Dateien: die Technik einer Druckerei (Rücken, Beschnitt, Strichcode), eine Datei pro Druckerei und Format. Welche gilt, steht in der Variablen-Datei bei `{druck-datei}` unter `## Ausgabe: Druck …`; nicht gebrauchte liegen in `druck/reserve/`. [→ Plattform-Dateien](#Plattform-Dateien) |
| `ausgabe-normal/` | was der Bau erzeugt: Lese-PDF, Druckdateien, E-Book, Booklet, Werbebilder. Zuoberst `00-UEBERSICHT.txt`: welche Datei wofür |
| `ausgabe-unzensiert/` | dasselbe für die zweite Fassung («uz»), falls dein Buch zwei hat. Text in `::: nur-uz` … `:::` steht nur dort, `::: nur-normal` … `:::` nur in der normalen |
| `ausgabe-test/` | Testläufe mit `druck=<datei>` – kommt nicht zu GitHub |
| `fotos/`, `bilder/` | Fotos und Bilder (Porträt, eigene Verzierung, Strichcode) |
| `geschichten/`, `tabellen/` | Geschichten und Tabellen (CSV), falls du sie brauchst |
| `md-history/` | ältere Fassungen deiner MD-Dateien, entstehen bei jedem Bau ([Sichern und zurückholen](#Sichern-und-zurueckholen)) |
| `motor/` | pureSATZ selbst – nie von Hand ändern, kommt mit `sh update.sh` |

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

# Schreiben

## Zum Kopieren

Die häufigsten Bausteine – mit «kopieren» übernehmen und in die Buch-MD oder in eine Geschichte einfügen.

**Teil und Kapitel**
```
# Teil 1|Titel des Teils|Untertitel

## Kapitel

### Zwischentitel

#### Kleiner Titel
```

**Geschichte einbinden** (eigene Zeile; mit `#####` erscheint sie in der Gliederung des Editors)
```
##### @@name-der-geschichte
```

**Kopf einer Geschichte** (wird nicht gedruckt)
```
## Titel der Geschichte
stand: idee
stichworte:
quelle:
notiz: stand = idee · entwurf · ueberarbeiten · fertig
```

**Foto, kurz** (eigenes Bild in `fotos/`; `beispiel-foto.jpg` hat jedes Buch (im Motor) – zum Ausprobieren)
```
#### @FOTO Titel
datei: beispiel-foto.jpg
text: Bildunterschrift
```

**Fotos – alle Möglichkeiten** (einfügen, `sh build.sh schnell`, ansehen; danach `beispiel-foto.jpg` durch dein Foto ersetzen)
```
#### @FOTO Bild 1 – volle Breite
datei: beispiel-foto.jpg
text: Bildunterschrift unter dem Foto
quelle: Foto: Vorname Nachname
alt: Was auf dem Bild zu sehen ist (für die Vorlesefunktion im E-Book)

Text nach Bild 1. Die erste Leerzeile oben beendet den Foto-Block.

#### @FOTO Bild 2 – klein, Text fliesst links daneben
datei: beispiel-foto.jpg
text: Bild rechts, 45 mm breit
breite: 45
fluss: rechts

Dieser Absatz fliesst links neben Bild 2. Auch die nächsten Absätze fliessen daneben, bis das Bild zu Ende ist.

Noch ein Absatz neben dem Bild.

#### @FOTO Bild 3 – klein, Text fliesst rechts daneben
datei: beispiel-foto.jpg
text: Bild links, 45 mm breit
breite: 45
fluss: links

Dieser Absatz fliesst rechts neben Bild 3.

#### @FOTO-UZ Bild 4 – nur in der unzensierten Fassung
datei: beispiel-foto.jpg
text: Erscheint nur in der zweiten Ausgabe
breite: 80
```

**Tabelle** (CSV in `tabellen/`) · **Zitat** · **neue Seite**
```
@#name-der-tabelle

> Ein Satz als Zitat mit Verzierung.

---
```

**Text hervorheben** – fett mitten im Satz, kursiv als eigene Zeile ([→ fett und kursiv](#Text-hervorheben))
```
Ein Satz mit **fettem Wort** mitten im Text.

~ Eine Randbemerkung: klein und kursiv.

@ZITAT Ein Zitat: kursiv, zentriert, schlicht.

> Ein Zitat: kursiv, zentriert, mit Verzierung.
```

**Nur in der unzensierten Fassung**
```
::: nur-uz
Dieser Text steht nur in der zweiten Ausgabe.
:::
```

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
| `## Kapitel` / `### Zwischentitel` / `#### Titel` | Kapitel (im Inhalt) / Zwischentitel / kleiner Titel. Wie tief ins Inhaltsverzeichnis: `{inhalt-tiefe}: 1–4` (Standard 2 = bis `##`) |
| `## @BEFEHL` | Befehl als Überschrift (sichtbar in der Navigation des Editors) |
| `@ZITAT Satz` · `@ZITAT-ZIER Satz` (kurz `> Satz`) · `~ Satz` | Zitat schlicht · Zitat mit Verzierung · Randbemerkung |
| `- Punkt` · `**fett**` · `[Text](https://…)` | Liste · fett · Link |
| `1. Punkt` `2. Punkt` | nummerierte Aufzählung (zählt selbst: die erste Zahl ist der Start) |
| `  - Unterpunkt` | Unterpunkt, 2–4 Leerzeichen eingerückt (unter `-` und unter `1.`) |
| `3\. Mai war …` | Zahl mit Punkt am Zeilenanfang, aber keine Aufzählung |
| Leerzeile | neuer Absatz |
| `\` am Zeilenende | Zeilenumbruch im Absatz: die nächste Zeile gehört zum selben Absatz (in Variablen: `<br/>`) |
| `---` (eigene Zeile, davor eine Leerzeile) | neue Seite, wie `@UMBRUCH` (im Editor eine waagrechte Linie) |

**Code** (ab 2.76): Ein Wort zwischen zwei Backticks (Taste neben dem Fragezeichen) steht in Code-Schrift und bleibt
wörtlich – keine Variablen, kein fett; gut für Befehle und Dateinamen. Mehrere Zeilen: eine Zeile mit drei Backticks
davor und eine danach – heller Kasten, jede Zeile genau wie getippt, in gleich breiter Schrift (DejaVu Sans Mono,
ab 2.77), damit Spalten untereinander stehen.

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

## Text hervorheben: fett und kursiv

Suchwörter: fett, kursiv, hervorheben, betonen. Bausteine: [Zum Kopieren](#Zum-Kopieren) · [← Ich will …](#Gestalten)

| Steuerzeichen | Wirkung |
|---|---|
| `**Wort**` | **fett**, mitten im Text (PDF und E-Book) |
| `~ Satz` | Randbemerkung: klein, kursiv, leicht eingerückt |
| `@ZITAT Satz` | Zitat: kursiv, zentriert, schlicht |
| `> Satz` oder `@ZITAT-ZIER Satz` | Zitat: kursiv, zentriert, mit Verzierung oben und unten |
| `text:` beim Foto | Bildunterschrift, automatisch kursiv |

Kursiv mitten im Satz (`*Wort*`) gibt es noch nicht – ein einzelner Stern bleibt als Stern stehen.
Tipp: Fett sparsam einsetzen. Eine Leerzeile vor einem kurzen Satz betont oft schon genug.

## Bilder und Fotos

[← Gestalten: Ich will …](#Gestalten) · [Zum Kopieren](#Zum-Kopieren)

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


**Bilderverzeichnis / Tabellenverzeichnis:** in der Variablen-Datei `{bilderverzeichnis}: ja` bzw.
`{tabellenverzeichnis}: ja` – eine eigene Seite listet alle Fotos (Bildtext, sonst Titel) bzw. Tabellen (Titel = erste
Zeile der CSV) mit Seitenzahl, vor dem Stichwortverzeichnis. An anderer Stelle: eigene Zeile `@BILDERVERZEICHNIS` bzw.
`@TABELLENVERZEICHNIS`. Im E-Book ohne Seitenzahlen.

## Tabellen

[← Gestalten: Ich will …](#Gestalten) · [Zum Kopieren](#Zum-Kopieren)

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
- Im Buch: `@#behandlungen-pro-jahr` (auch `@# name`), auch in einer Geschichte. In Zellen gehen `**fett**` und `{variablen}`.
  Zahlen stehen rechtsbündig, lange Tabellen gehen über mehrere Seiten (Kopfzeile wiederholt sich).
- **Zu breit?** pureSATZ bricht zuerst Text in den Zellen um, verkleinert dann die Schrift (bis 7.5 pt) und
  stellt die Tabelle notfalls **quer** auf eine eigene Seite (um 90° gedreht, das Buch zum Lesen drehen).
  Selbst bestimmen: `@#name quer` (immer quer) oder `@#name hoch` (nie quer). Im E-Book wird nie gedreht –
  breite Tabellen lassen sich dort seitlich verschieben.
- Nur in einer Ausgabe: `::: nur-uz` / `@#name` / `:::`.
- `sh build.sh pruefen` meldet fehlende Tabellen (mit Vorschlag bei Tippfehlern) und Zeilen mit zu vielen Werten.

## Geschichten sammeln (freiwillig)

[← Gestalten: Ich will …](#Gestalten) · [Zum Kopieren](#Zum-Kopieren)

Statt alles in die eine Buchdatei zu schreiben, kann jede Geschichte eine **eigene Datei** im Ordner
`geschichten/` sein. Das Buch bindet sie mit einer Zeile `@@name` ein (gleich: `##### @@name` – dann zeigt der
Editor sie in der Gliederung). Ohne `geschichten/` und ohne
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

- Die Zeilen unter dem Titel sind freiwillig und werden nicht gedruckt; `notiz:` (beliebig oft) für eigene Bemerkungen.
  `stand`: **idee · entwurf · ueberarbeiten · fertig** – nur für die Übersicht, wirkt nicht auf den Druck.
  `stichworte` kommen automatisch ins Stichwortverzeichnis. `quelle` ist eine Notiz für dich.
- **Einbinden:** in der Buchdatei eine eigene Zeile `@@schutzschild-hoch` (Name = Dateiname ohne .md).
  Die Reihenfolge der `@@`-Zeilen ist die Reihenfolge im Buch. In `::: nur-uz` … `:::` gesetzt erscheint
  die Geschichte nur in der zweiten Ausgabe (die Geschichte selbst darf dann keine eigenen `:::`-Blöcke haben).
- **Mit dem Menü ins Buch:** `g` → `b` setzt fehlende Geschichten (`@@`) und Tabellen (`@#`) in einen Block `## Noch einordnen`
  (nach der letzten `@@`-Zeile). Zeilen an ihren Platz schieben, Block löschen. Deine Reihenfolge im Buch bleibt immer.
  Neues Buch mit Demo-Inhalt: `b` fragt, ob Vorwort und Teil 1 der Demo durch deine Geschichten ersetzt werden
  (Titelei, Anhang, Über den Autor, Danke bleiben). Danach `s` schnell und `p` = deine Geschichten als Buch.
- **Reihenfolge** überall (Liste, Block, Sammel-PDF): zuerst wie im Buch, dann wie angelegt.
- **Alle in einer Datei** (z. B. für eine KI): `g` → `a` schreibt `geschichten-alle.md`, ändern, speichern,
  nochmals `g` → `a` holt alles zurück in die Einzeldateien (vorher Sicherung). Die Zeilen `@@@ name` nicht ändern.
  Solange die Datei existiert, sind die Einzeldateien im Menü gesperrt.
- **Übersicht:** Bei jedem Bau und bei `sh neu.sh` entsteht `geschichten-uebersicht.html` (im Browser öffnen:
  Fortschrittsbalken, Tabelle zum Sortieren und Filtern, Kanban-Ansicht) und `geschichten/UEBERSICHT.md`.
  Beide werden immer neu erzeugt und kommen nicht zu GitHub.
- **Prüfung:** `sh build.sh pruefen` meldet `@@`-Verweise ohne Datei (mit Vorschlag bei Tippfehlern),
  Geschichten, die noch nicht im Buch sind, und doppelt eingebundene. Fehler zeigen die richtige Datei
  («geschichten/schutzschild-hoch.md, Zeile 7: …»). md-history/ und Sicherung nehmen die Geschichten mit.

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
> normal: / uz: = Seiten fürs Check-PDF – eigene Seiten einfach dazuschreiben, z. B. normal: 44-45,47,55
> Zeilen mit > schreibt pureSATZ jedes Mal neu: S. = gedruckte Seite, Z. = Zeile (wie im Korrektur-PDF).
> Dir fehlt ein Name oder Begriff? Als eigene Zeile hinzufügen und sh build.sh personen nochmals aufrufen.
$ sh build.sh personen   (Seiten neu, nach dem Korrigieren)
$ sh build.sh personen Thomas   (check_Thomas_Gegenlesen.pdf)

# GEFUNDENE PERSONEN UND BEGRIFFE

Thomas | Thom | Autor | Techniker
normal: 112-113,115
uz: 118
> 4 Stellen gefunden
> normal: S. 112 Z. 8 · S. 113 Z. 2, 17
> uz: S. 118 Z. 4

# KEINE PERSONEN
> nicht mehr vorschlagen – Zeile löschen = wieder vorschlagen
--- Ecuador
```

- Wichtig sind nur die Zeilen **ganz links**: Begriffe **derselben Person** mit `|` in eine Zeile nehmen, der
  **erste** gibt den Dateinamen. `--- Wort` (unter «KEINE PERSONEN») = keine Person, nicht mehr vorschlagen
  (`--- MusterName` ist nur ein Beispiel). Eine ganz gelöschte Zeile kommt beim nächsten Mal wieder als Vorschlag.
  Eine eigene Zeile mit einem Namen, den der Motor nicht kennt, geht auch. Datei löschen = alles beginnt neu.
- **`normal:` / `uz:`** = die Seiten fürs Check-PDF. **Eigene Seiten einfach dazuschreiben**, mit Komma und
  Bereichen: `normal: 44-45,47,49-52`. Sie bleiben beim nächsten Lauf stehen (der Motor vergleicht mit den
  gefundenen Seiten in der `>`-Zeile); gefundene Seiten berechnet er jedes Mal neu. Nach einem Umbau eigene
  Seiten selbst prüfen. Ohne unzensierte Fassung gibt es nur `normal:`. (Alte Zeilen `+ normal: 45` gehen weiter.)
- **`>`-Zeilen** schreibt der Motor: zuerst die Anzahl («4 Stellen gefunden» bzw. «kommt nicht vor»), dann Seite
  und Zeile jeder Fundstelle. **Ganzes Kapitel:** Steht ein Begriff im
  **Kapiteltitel** (z. B. «Ecuador» in «Ecuador und das runde Rad»), kommen alle Seiten dieses Kapitels dazu.
- Die Kopfzeile jeder Seite («Teil · Kapitel») zählt nicht als Fundstelle.
- Die `>`-Zeilen und Seiten schreibt der Motor bei jedem `sh build.sh personen` neu. Deine Namenszeilen bleiben,
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

## Korrekturlesen mit KI

Eine KI findet Tippfehler, doppelte Wörter und holprige Sätze. Ein Lektorat durch einen Menschen ersetzt sie nicht.

1. **Ein Kapitel nach dem anderen** geben, nicht das ganze Buch – sonst übersieht die KI vieles.
2. **Klar sagen, was du willst**, z. B.: «Prüfe nur Rechtschreibung und Zeichensetzung (Schweizer Schreibweise:
   ss statt ß). Ändere keinen Stil. Liste jede Stelle als: alt → neu.»
3. **Vorschläge selber übernehmen**, nicht den ganzen Text zurückkopieren. So bleibt deine Sprache, und die Befehle
   (`@…`, `:::`, `{…}`) bleiben heil.
4. **Mehrere Durchgänge**, jeder mit einem Ziel, am besten jeweils in einem neuen Chat:
   1. Rechtschreibung und Zeichensetzung
   2. Wiederholungen und Füllwörter
   3. Logik und roter Faden
   4. nochmals Rechtschreibung, nach allen Änderungen
5. **Nach jedem Durchgang** `sh build.sh stand "KI-Durchgang 1"` – `sh build.sh aenderungen` zeigt danach, was sich
   geändert hat.

Für ein Lektorat auf Papier: `sh build.sh korrektur` (A4 mit Zeilennummern).

# Gestalten

## Aufbau eines Buchs: Seite für Seite

Ein Buch beginnt mit einer **rechten** Seite (ungerade Seitenzahl). Den Anfang – die Titelei – setzt pureSATZ aus
diesen Zeilen der Buch-MD:

| Seite | Inhalt | In der Buch-MD |
|---|---|---|
| 1 (rechts) | Titel, Untertitel, Autor | `## @TITEL` |
| 2 (links) | Impressum: ©, Druckerei, Kontakt, ISBN | `## @IMPRESSUM` – setzt sich selbst zusammen |
| 3 (rechts) | Widmung im unteren Drittel (freiwillig) | `## @WIDMUNG` |
| danach | ein Satz allein auf einer Seite (freiwillig) | `## @KERNSATZ Satz` |
| danach | Inhaltsverzeichnis | `## @INHALTSVERZEICHNIS` |
| danach | Vorwort, dann Teil 1 | `## Vorwort` · `# Teil 1\|Titel\|Untertitel` |

**Gut zu wissen:**

- Ein Kapitel soll auf einer rechten Seite beginnen: `@UMBRUCH-RECHTS` davor.
- Die Druckerei will eine gerade Seitenzahl (epubli: dazu die letzte Seite frei für den Strichcode). pureSATZ füllt
  am Schluss selbst mit leeren Seiten auf; `sh build.sh final` zeigt die **Seitenbilanz**.
- In den Word-Vorlagen der Druckereien macht man das von Hand – Leerseiten, weisse Kästen über Seitenzahlen,
  Abschnittswechsel. In pureSATZ ist das nicht nötig.
- Schöner Kapitelanfang: `{initial}: ja` (grosser Anfangsbuchstabe), siehe «Seitengestaltung».

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
| Zwei Ausgaben | `zweite-ausgabe` (ja/nein), `ausgabe-name-normal` / `-uz`, `titel-zusatz-normal` / `-uz` (Zeile unter dem Untertitel, je Ausgabe), `stempel-uz` (z. B. UNZENSIERT), `kasten-hinweis`, `kasten-kopf` (Wort oben im Kasten der zweiten Ausgabe, Standard: wie der Stempel) |
| Impressum | `impressum-rechte`, `impressum-kontakt` |
| Ausgabe: … | `druck-datei`, `isbn`, `preis`, `impressum-herstellung`, `impressum-kontakt`, `impressum-logo`, `erstellen` (nur E-Book) |
| E-Book | `ebook-epub2` (ja = zusätzlich EPUB 2), `ebook-rueckseite` (bild / text / nein), `ebook-barrierefreiheit`, `farbe-akzent-ebook`, `ebook-id` bzw. `buch-id` (feste Kennung des E-Books; leer = Website/Titel) |
| Shop | `shop-beschreibung`, `shop-schlagwoerter`, `shop-kategorie`, `shop-link`, `sprache` (Standard `de`, steht in den Shop-Angaben) |
| Leseprobe | `leseprobe`, `leseprobe-seiten`, `leseprobe-seiten-uz`, `leseprobe-text` |
| Technik | `kurz-normal` / `-uz` (Kürzel vorne an den Druckdateien, z. B. L123), `datei-normal` / `-uz` (Name der Lese-PDFs und E-Books), `ordner-normal` / `-uz` (Ausgabeordner) |
| Weiteres | `stichworte`, `stichworte-gruppen` (zusammen · fortlaufend), `bilderverzeichnis`, `tabellenverzeichnis` (ja · nein), `trennstellen` (Welt\|anschauung), `zier`, `zier-hell`, `initial` (ja · nein), `initial-farbe` (akzent · haupt), `initial-stil` (normal · rand · feld), `initial-zeilen` (3 · 4), `initial-schrift` (fett · datei.ttf), `kapitaelchen` (ja · nein), `absatz-einzug` (ja · nein), `kopfzeile` (ohne-autor · autor · wechselnd), `foto-format`, `md-history-behalten`, `bildschirm-dunkler`, `mockup-hintergrund` |
| Sicherung | `sicherung-lokal`, `sicherung-cloud`, `sicherung-behalten` |
| Layout | `farbschema`, `farbe-text`, `farbe-leise`, `farbe-haupt`, `farbe-akzent`, `farbe-papier`, `farbe-kasten`, `farbe-stempel`, `schrift-text`, `schrift-titel`, `schriftgroesse`, `zeilenabstand`, `blocksatz` · Inhaltsverzeichnis: `inhalt-tiefe`, `inhalt-dichte`, `inhalt-teile`, `inhalt-punkte`, `inhalt-schrift` |

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

## Seitengestaltung: neue Seite, Umbruch, Zierde

Nach einer Änderung `sh build.sh schnell` und ansehen.

| Ich will … | So |
|---|---|
| eine neue Seite | `---` auf eigener Zeile (davor eine Leerzeile) oder `@UMBRUCH` |
| eine neue Seite, im Druck immer rechts (z. B. vor einem Kapitel) | `@UMBRUCH-RECHTS` |
| eine neue Seite nur, wenn unten zu wenig Platz bleibt | `@PLATZ 60` (mm) – gut vor einem Foto oder Zwischentitel |
| einen Abschnitt nie trennen | `::: zusammen` … `:::` |
| Leerraum | `@ABSTAND 8` (mm) – mehrere Leerzeilen geben keinen Abstand |
| den Inhalt einer Seite senkrecht in die Mitte | `@SEITENMITTE` |
| einen Satz allein auf einer Seite | `## @KERNSATZ Satz` oder `@MOTTO Satz` |
| eine kleine Verzierung | `@ZIER 12` (Breite in mm) |
| eine Verzierung unten, danach neue Seite | `@ZIER-UNTEN 10` |
| eine Verzierung zwischen zwei Abschnitten | `@ZIER-TRENNER` |
| ein eigenes Zierbild | in der Variablen-Datei `{zier}: meine-zier.png` (Bild in `bilder/`) |
| einen grossen Anfangsbuchstaben am Kapitelanfang (Initial, drei Zeilen hoch) | `{initial}: ja` – Farbe: `{initial-farbe}: akzent` (Gold) oder `haupt` (Blau). Ist der erste Absatz kürzer als drei Zeilen, läuft der nächste daneben weiter; folgt gleich ein Titel oder Foto, beginnt das Kapitel ohne Initial |
| das Initial anders: im Rand, im Feld, grösser, fett oder in einer Zierschrift | `{initial-stil}: rand` (links im Rand, Text volle Breite) oder `feld` (helles Feld mit Goldrahmen) · `{initial-zeilen}: 4` · `{initial-schrift}: fett` oder eine TTF-Datei aus `fonts/` (z. B. Cinzel Decorative, UnifrakturMaguntia, Playfair Display – frei auf fonts.google.com) |
| die ersten Wörter jedes Kapitels in Kapitälchen | `{kapitaelchen}: ja` – mit oder ohne Initial |
| Absätze eingerückt statt mit Abstand (wie viele Romane) | `{absatz-einzug}: ja` – der erste Absatz nach einem Titel bleibt bündig |

**Wann umbrechen?** Teile (`# Teil …`) und Kapitel oberster Ebene (`# Titel`) beginnen von selbst auf einer neuen Seite.
Sonst erst umbrechen, wenn der Text fertig ist – jede Änderung verschiebt die Seiten. Lieber `@PLATZ` als `---`:
es wirkt nur, wenn es nötig ist.

**Nicht innerhalb eines `:::`-Blocks:** `---` und `@ABSTAND` nach dem `:::` setzen.
**Ruhig bleiben:** nur eine Verzierung pro Seite.

## Inhaltsverzeichnis gestalten

`## @INHALTSVERZEICHNIS` im Buch setzt es an diese Stelle. Die Werte stehen in der Variablen-Datei unter
`### Inhaltsverzeichnis`.

| Ich will … | So |
|---|---|
| mehr oder weniger Ebenen | `{inhalt-tiefe}: 1–4` (Standard 2 = bis `##`; 3 = auch `###`) |
| einen Teil nie von seinen Kapiteln trennen | `{inhalt-teile}: zusammen` (Standard `fortlaufend`) |
| eine Seite weniger | `{inhalt-dichte}: 0.95` (enger 0.92, normal 1) – nur das Inhaltsverzeichnis, der Text bleibt |
| ohne Punktlinie | `{inhalt-punkte}: nein` |
| grössere Schrift | `{inhalt-schrift}: 10` (Standard 9.3 Punkt) |
| eine Dankesseite oder ein Nachwort darin | als Kapitel `## Danke` |
| ein Bilder- oder Tabellenverzeichnis | `{bilderverzeichnis}: ja` · `{tabellenverzeichnis}: ja` |

**Nur ein, zwei Zeilen auf der letzten Seite?** Zuerst `{inhalt-teile}: zusammen`, sonst `{inhalt-dichte}: 0.95`.
Im E-Book entsteht das Inhaltsverzeichnis von selbst.

## Stichwortverzeichnis

[← Gestalten: Ich will …](#Gestalten) · [Zum Kopieren](#Zum-Kopieren)

Das Verzeichnis am Schluss des Buchs listet Begriffe mit ihren Seiten. Es braucht drei Dinge:
`{stichworte}: ja` in der Variablen-Datei, eine eigene Zeile `@STICHWORTE` in der Buchdatei (meist vor `@RUECKSEITE`)
und die Liste `stichworte-<buch>.txt`. Neue Bücher (auch das Hallo-Buch) haben alles schon, mit Beispielen aus dem Demo.

**In 4 Schritten** (Menü: `w` → `i` Stichworte …):

```sh
sh build.sh stichworte              # 1. prüft die drei Dinge, schreibt stichworte-vorschlag.txt
                                    # 2. in stichworte-vorschlag.txt: [ ] durch [+] oder [x] ersetzen
sh build.sh stichworte uebernehmen  # 3. alle markierten unten an stichworte-<buch>.txt anhängen
sh build.sh schnell                 # 4. bauen – das Verzeichnis steht am Schluss
```

**stichworte-vorschlag.txt** – Begriffe aus dem Text, die mindestens zweimal vorkommen, mit Häufigkeit:

```text
[x] Emotionscode  (14)      steht schon in stichworte-<buch>.txt
[+] Bern  (9)               wird übernommen
[ ] Morgen  (7)             nur ein Vorschlag
```

**stichworte-<buch>.txt** – eine Zeile pro Stichwort, danach nach Wunsch verfeinern:

```text
Seele | Seelen | seelisch          die erste Schreibweise steht im Verzeichnis, gesucht werden alle
Quelle = göttliche Quelle | Urquelle   Eintrag links vom =, gesucht wird nur rechts
Gott -> Quelle                     Verweis «Gott, siehe Quelle» (ohne Seitenzahl)
# Kommentar                        wird nicht gelesen
```

- Übernehmen hängt nur an, doppelte lässt es weg, und sichert die Liste vorher nach `md-history/`.
  Markieren mit `[+]` oder `[x]` – beides geht; was schon in der Liste steht, wird nie doppelt angehängt.
  In der Vorschlagsliste wird aus `[+]` ein `[x]`. Markierte `[+]` bleiben, wenn du die Vorschläge neu machst.
- Stichwörter aus Geschichten (`stichworte:` im Kopf) kommen automatisch dazu.
- Ein einzelnes Wort allein oben auf der nächsten Seite? `{stichworte-gruppen}: zusammen` in der Variablen-Datei:
  Gruppen bis 3 Wörter bleiben beisammen, längere werden höchstens 2 + 2 getrennt (Standard: `fortlaufend`).
  Oft hilft auch, ein Stichwort wegzulassen, das kaum jemand sucht (Wohnort, Hauptthema des Buchs).
- `stichworte-vorschlag.txt` ist nur ein Hilfsblatt: `sh cleanup.sh` löscht es, die Stichwortdatei bleibt immer.

# Bauen und Drucken

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
sh build.sh stichworte      # Stichwortverzeichnis prüfen, Vorschläge → stichworte-vorschlag.txt ([+] = übernehmen)
sh build.sh stichworte uebernehmen   # alle [+] an stichworte-<buch>.txt anhängen (vorher gesichert)
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

[← Gestalten: Ich will …](#Gestalten) · [Zum Kopieren](#Zum-Kopieren)

Die Plattform-Datei enthält nur die **Technik** einer Druckerei. Ihre Werte gelten nur für Buchblock und Umschlag.
Lese-PDF, E-Book, Leseprobe, Korrektur und Mockup bleiben beim `{format}` der Variablen-Datei (Grundformat).

| In der Plattform-Datei | Bedeutung |
|---|---|
| `neu-berechnen` | `ja` = Seitenzahl hat sich geändert, im Coverrechner neu berechnen (der Bau erinnert daran) · `nein` = Werte passen |
| `berechnet-fuer-seiten` | Seiten des Buchblocks, für die Rücken und Umschlag berechnet sind; weicht der Buchblock ab, warnt `final` |
| `plattform` | `epubli`, `bod`, `tredition` oder `kdp` (bestimmt Strichcode-Platz und Füllseite; tredition und kdp wie bod) |
| `farbmodus` | `rgb` (Standard) oder `cmyk`: Buchblock und Umschlag werden bei `final` und `komplett` mit Ghostscript nach CMYK umgewandelt (z. B. für tredition); im Entwurf bleiben sie RGB (schneller). Jeder Bau rechnet neu aus den Originalbildern, es wird nie mehrfach umgewandelt. Braucht Ghostscript (Linux `sudo apt install ghostscript` · Mac `brew install ghostscript` · Windows: START-Windows, Schritt «Extras», holt den Installer). Lese-PDF, E-Book und Leseprobe bleiben RGB. |
| `format` | nur, wenn das Druckformat vom Grundformat abweicht; auch eigenes Mass `148 x 210` (Ränder und Schrift vom nächstliegenden Format) |
| `bindung`, `projekt`, `papier`, `extra-seiten` | `hardcover`/`softcover`/`beide` · `veroeffentlichen`/`privatdruck` · Papier zur Info · leere Notizseiten am Schluss |
| `ruecken-hardcover`, `ruecken-softcover` | Rücken in mm laut Coverrechner der Plattform |
| `beschnitt-buchblock`, `beschnitt-hardcover`, `beschnitt-softcover`, `deckel-hardcover` | Masse in mm (BoD: Buchblock 0, Deckel 153x216, Einschlag 17) |
| `isbn-position` | `links` · `mitte` · `rechts` (leer: epubli links frei, BoD rechts) |
| `isbn-groesse` | z. B. `40x20` (mm, 16 mm vom Rand seitlich, 8 mm von unten); leer = 60 × 35 mm ab der Ecke frei |
| `isbn-bild` | PNG aus `bilder/` auf weissem Feld; leer = nichts zeichnen (BoD: Strichcode aus der ISBN) |
| `isbn-rahmen` | leer = kein Rahmen · `gold` = Goldrahmen · `berge` = Goldrahmen, oben als Bergkette. Mit `isbn-bild` werden die Striche oben zu Gipfeln geschnitten (unten bleiben über 70 % frei, bleibt lesbar); beim eigenen BoD-Strichcode liegt die Bergkette darüber; bei epubli rahmt sie das freie Feld (Lage nach dem ersten Probedruck prüfen). Farbe = Akzentfarbe |
| `isbn-rahmen-farbe` | leer = `gold` (Akzentfarbe) · `schwarz` |
| `isbn-rahmen-abstand` | mm weiss zwischen Strichen und Linie, z. B. `2` – dann besteht der Code nur aus schwarzen Strichen auf Weiss (Vorgabe mancher Plattformen, z. B. tredition); leer = 0 |

Die `isbn-…`-Zeilen gelten für den **Strichcode mit der ISBN** auf der Rückseite (EAN-13, auch Barcode genannt). Bis 2.74 hiessen sie `barcode-…` – diese Namen gelten weiter.
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

## Umschlag: Rücken und Seitenzahl

Die Breite des Rückens hängt von Seitenzahl und Papier ab. Die Druckerei rechnet sie mit ihrem **Coverrechner** aus.

1. `sh build.sh final` – zeigt die **Seitenzahl des Buchblocks** (Seitenbilanz).
2. Im Coverrechner der Druckerei eingeben: Format, Bindung, Papier wie bestellt, Seitenzahl.
3. Das Ergebnis (Text, wie er kommt) in der Plattform-Datei `druck/<datei>.md` zuunterst unter
   `## Coverrechner (Rohdaten)` einfügen.
4. Oben eintragen: `{ruecken-hardcover}` bzw. `{ruecken-softcover}` (mm), bei Hardcover auch `{beschnitt-hardcover}`
   und `{deckel-hardcover}`; dazu `{berechnet-fuer-seiten}: <Seitenzahl>` und `{neu-berechnen}: nein`.
5. Nochmals `sh build.sh final`: Die Masse des Umschlags (z. B. 344 × 250 mm) müssen mit Gesamtbreite und
   Gesamthöhe im Coverrechner übereinstimmen.

Ändert sich die Seitenzahl später, warnt `final`, und das Menü zeigt oben «⚠ Coverrechner …» (ab 2.78) – `cv` öffnet
die Druckdatei. Dann Schritte 2–5 wiederholen; nach dem nächsten `final` verschwindet der Hinweis.
Die Texte auf dem Umschlag stehen in `<buch>-umschlag.md` (Vorderseite, Buchrücken, Rückseite).
[→ Plattform-Dateien](#Plattform-Dateien)

## Bei epubli

Ausgabeordner (z. B. `ausgabe-normal/`): `<kurz>_Buchblock.pdf` und `<kurz>_Umschlag_Hardcover.jpg`
bzw. `_Softcover.jpg` hochladen. Erst ein Testexemplar (`{projekt}: privatdruck` in der Plattform-Datei), dann
«Buch veröffentlichen»; die ISBN von epubli unter `## Ausgabe: Druck normal` bei `{isbn}:` eintragen und neu bauen.
E-Book (`.epub`): eigene ISBN unter `## Ausgabe: E-Book` bei `{isbn}:`, dann bei tolino media oder KDP hochladen.
Das E-Book enthält Angaben zur **Barrierefreiheit** (Gliederung, Inhaltsverzeichnis, Bildbeschreibungen);
`sh build.sh` warnt bei Fotos ohne `alt:` und ohne `text:`. Eigene Zusammenfassung: `ebook-barrierefreiheit:`. Die Akzentfarbe für Text wird im E-Book automatisch
lesbar dunkel gesetzt (Kontrast 4,5:1); eigene Farbe mit `farbe-akzent-ebook:`.

## Bei tredition

- **Druckdatei:** Muster `tredition-a5-hardcover` (CMYK ist dort schon eingestellt). In der Variablen-Datei unter
  `## Ausgabe: Druck …` bei `{druck-datei}:` eintragen.
- **Hardcover:** Einschlag und Deckel laut Coverrechner, z. B. `{beschnitt-hardcover}: 17` und `{deckel-hardcover}: 153x216`.
- **Coverrechner** von tredition: Seitenzahl aus `sh build.sh final` eingeben, das Ergebnis in der Druckdatei unter
  `## Coverrechner (Rohdaten)` einfügen, Rücken übernehmen («Umschlag: Rücken und Seitenzahl»).
- **ISBN und Strichcode:** tredition gibt jedem Buch eine ISBN und den Strichcode als SVG. Als PNG in `bilder/` legen
  und bei `{isbn-bild}:` eintragen. `{isbn-rahmen}: berge` und `{isbn-rahmen-abstand}: 2` setzen die Bergkette darüber,
  ohne dass Gold die Striche berührt.
- **Hochladen:** `<kurz>_Buchblock.pdf` und `<kurz>_Umschlag_Hardcover.pdf` – `00-UEBERSICHT.txt` zeigt sie.
- **Impressum:** tredition verlangt Druckerei und Kontakt nach EU-Produktsicherheit: `{impressum-herstellung}` und
  `{impressum-kontakt}` unter `## Ausgabe: Druck …`. Mehr: tredition.com/impressum-buch
- **Nur Exemplare, nicht im Handel:** Die Bestellung lässt sich vor der Veröffentlichung beenden – das Buch wird
  gedruckt, erscheint aber nie im Handel. In der Druckdatei dann `{projekt}: privatdruck` (ohne ISBN im Buch).

## Farben für den Druck: RGB oder CMYK

Bildschirm, Lese-PDF und E-Book arbeiten mit **RGB**. Viele Druckereien wollen **CMYK** (tredition: ja, epubli: RGB
geht). Einstellung in der Plattform-Datei (`druck/…md`):

```
{farbmodus}: cmyk
```

Dann wandelt `sh build.sh final` (und `komplett`) Buchblock und Umschlag mit Ghostscript nach CMYK um; alles andere
bleibt RGB:

| Datei | Farben |
|---|---|
| Buchblock und Umschlag für die Druckerei | CMYK mit `{farbmodus}: cmyk` (tredition), sonst RGB (epubli) |
| E-Book (EPUB) und Cover-Bilder | immer RGB |
| Lese-PDF, Leseprobe, Korrektur | immer RGB |
| Booklet zum Selberdrucken | RGB (entsteht vor der Umwandlung) |
| Werbebilder (Mockup) | RGB |

 Fotos selber in RGB liefern (nicht CMYK), JPG oder PNG – durchsichtige Stellen in PNG werden weiss.
Wirken Farben im Druck zu dunkel oder zu hell: Probedruck ansehen, bei Bedarf ein zweites Farbschema (siehe «Farbschemas»).

## Schwarz-weiss drucken (freiwillig)

Die feinen Farben (Kopfzeile, Bildunterschriften, Gold) wirken im eigenen Schwarz-weiss-Ausdruck sehr hell.
Mit `bildschirm-dunkler: ja` in der Variablen-Datei (Abschnitt «Weiteres») werden sie **nur im Bildschirm-PDF**
(und in Leseprobe, Korrektur, Booklet zum Selberdrucken) etwas dunkler. Druckdateien für epubli und das E-Book
bleiben unverändert.

## Druck bei KDP, Lulu und anderen

Für technisch Interessierte – der Motor kennt epubli und BoD, andere Druckereien gehen über eine eigene Druckdatei:

1. Eine Musterdatei kopieren, z. B. `druck/bod-a5-hardcover.md` als `druck/kdp-dein-format.md`.
2. Werte aus dem **Coverrechner** bzw. der Formatliste der Plattform eintragen: `{format}: 152,4 x 228,6`
   (eigenes Mass in mm), `ruecken-…`, `beschnitt-…`, `deckel-hardcover`, `papier`.
   Ohne Coverrechner: ein PDF hochladen – die Plattform nennt die Masse, die sie erwartet.
3. `plattform: bod` stehen lassen (Strichcode-Feld selbst bestimmen, keine epubli-Füllseite).
   Setzt die Plattform den Strichcode selbst (z. B. KDP), das Feld mit `isbn-position` / `isbn-groesse`
   frei lassen und `isbn-bild` leer.
4. Testen: `sh build.sh final druck=kdp-dein-format` → `ausgabe-test/kdp-dein-format/`, Masse in `00-UEBERSICHT.txt`
   mit dem Rechner der Plattform vergleichen. Passt alles: `{druck-datei}` unter `## Ausgabe: Druck …` umstellen.

**Grenzen:** Beschnitt gilt rundum. KDP will beim Buchblock keinen Beschnitt im Bund (nur oben, unten, aussen) –
das kann der Motor noch nicht. Masse nur in mm.

## Selber drucken: Booklet und Copyshop

- **Booklet:** `<kurz>_Probedruck_booklet.pdf` (nach `final`) bzw. `<datei>_booklet.pdf` (Entwurf):
  A4 quer, doppelseitig, an der kurzen Kante wenden, falten, ineinanderlegen, in der Mitte heften – ein
  Probeexemplar in Originalgrösse. Ein beliebiges PDF als Booklet: siehe «Skripte und Kurzbefehle».
- **Bildschirm-PDF** `<datei>.pdf` für den Copyshop (Klebebindung, Spiralbindung) oder zum Verschicken.
- **Korrektur-PDF** `<datei>_Korrektur.pdf` (`sh build.sh korrektur`): A4 mit Zeilennummern und Rand fürs Lektorat.
- Feine Farben im Schwarz-weiss-Druck zu hell: `bildschirm-dunkler: ja` (siehe «Schwarz-weiss drucken»).

## Veröffentlichen: ISBN, Preis, Pflichtexemplar

- **ISBN:** Jede Ausgabe braucht ihre eigene (Druck und E-Book getrennt). Die meisten Plattformen geben eine kostenlos
  (epubli, tredition, BoD); eine eigene gibt es in der Schweiz bei der ISBN-Agentur Schweiz, in Deutschland bei der MVB.
  Eintragen in der Variablen-Datei unter `## Ausgabe: Druck normal` bzw. `## Ausgabe: E-Book` bei `{isbn}:`, dann neu
  bauen – sie steht danach im Impressum und in `shop-angaben.txt` (bei BoD auch im Strichcode).
- **Preis:** gleich daneben bei `{preis}:`.
- **Impressum:** Was die Druckerei verlangt, steht in ihrer Plattform-Datei unter `## Notizen`; die Werte unter
  `## Ausgabe: …` ([Ausgaben](#Ausgaben)).
- **Bildrechte:** Bei jedem fremden Foto `quelle:` angeben – es erscheint im Bildnachweis. Personen im Buch vorher
  fragen ([Gegenlesen](#Personen-im-Buch)).
- **Pflichtexemplare:** Schweiz: Nationalbibliothek, Deutschland: DNB. Manche Druckereien übernehmen das – nachfragen.
- **Vor der Freigabe:** `sh build.sh komplett`, `CHECKLISTE.md` abhaken, Stand festhalten: `sh build.sh stand "Erstausgabe"`.

# E-Book

## E-Book: Ablauf

1. Umschlagtexte fürs E-Book prüfen: Zeilen `feld-ebook:` in `<buch>-umschlag.md` (sonst gelten die des Drucks).
2. Eigene ISBN und Preis unter `## Ausgabe: E-Book` (nicht die des Drucks).
3. `sh build.sh final` – oder nur das E-Book: `sh build.sh nur-ebook final`.
4. Im Ausgabeordner: `<datei>.epub` und `<datei>_Cover-vorne.jpg`; die Shop-Texte in `shop-angaben.txt`.
5. Hochladen (tolino media, KDP, XinXii …) und die Vorschau im Shop ansehen: Inhaltsverzeichnis, Fotos, Cover.

Keine E-Book-Fassung der zweiten Ausgabe: unter `## Ausgabe: E-Book unzensiert` `{erstellen}: nein`.

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

# Hörbuch (Linux, Testphase)

## Hörbuch: Ablauf

**0 · Einmalig** – Azure-Schlüssel eingeben (`hb` → `s`) und prüfen (`hb` → `c`), siehe «Einrichten».
Für den Verkauf das Hörbuch mit dem bezahlten Azure-Tarif erstellen: zweiter Schlüssel (`hb` → `s` → `2`), dann
`hb` → `x` auf S0 (siehe «Azure gratis oder bezahlt»).

**1 · Buch schreiben oder ändern** – wie immer in der Buch-MD.

**2 · Hörbuch erstellen** – alles in einem (Texte → vertonen → Paket → Hörprobe):

```
sh menu.sh → hb → a               # Menü
sh build.sh hoerbuch              # Terminal im Buchordner
cd audio && sh hb.sh komplett     # Terminal im Ordner audio/
```

Einzeln, Schritt für Schritt: `t` Texte → `v` vertonen → `f` Paket → `r` Hörprobe.

**3 · Anhören und weitergeben** – die Hörprobe spielt am Schluss von selbst:

```
mpv audio/verkauf/hoerprobe.mp3            # Hörprobe
ls audio/verkauf/                          # <Buch>-Hoerbuch_<Zeit>.zip: für Shop, Geschenk, Handy (M4B)
```

Nach einer Änderung im Buch einfach Schritt 2 wiederholen: Nur Geänderte werden neu vertont.
Bei einem Fehler hält der Ablauf an – die Meldung lesen, beheben, Schritt 2 nochmals.

## Hörbuch: Was es braucht

Aus dem Buch ein Hörbuch machen: eine MP3 pro Kapitel, vorgelesen von einer KI-Stimme von Microsoft Azure.
Getestet mit «Leben 1.0, 2.0, 3.0» und der Stimme **Ollie** (spricht Deutsch sehr angenehm). Vorerst **nur Linux**.

- Ein **kostenloses Azure-Konto** (Tarif F0: 0,5 Mio. Zeichen pro Monat gratis – ein Buch hat etwa 80'000;
  darüber blockiert Azure, es entstehen keine Kosten).
- ffmpeg (Pflicht) und mpv (zum Anhören), das Azure-Paket für Python – `hb` → `c` prüft alles.
- Für die Fremdwörter (`hb` → `u`, freiwillig): hunspell mit Wörterbüchern –
  `sudo apt install hunspell hunspell-de-ch hunspell-fr hunspell-es hunspell-it hunspell-en-gb`.
- Einmalig etwa 30 Minuten zum Einrichten.

## Hörbuch: Einrichten (einmalig)

1. portal.azure.com → Konto anlegen → «Speech-Dienst» (Speech service) erstellen: Tarif **F0**, Region z. B.
   `switzerlandnorth`. Unter «Schlüssel und Endpunkt» **Schlüssel 1** kopieren.
2. `sudo apt install ffmpeg mpv`
3. Im Buchordner `sh menu.sh` → `hb` → `s`: Schlüssel einfügen (Rechtsklick → Einfügen, es erscheint nichts), Region bestätigen.
   Er kommt nur in `~/.bashrc` (Sicherung `~/.bashrc.bak`) – nie in eine Datei im Buch und nie zu GitHub.
4. `hb` → `c` prüft alles und installiert das Azure-Paket.
5. Für den Verkauf (später): eine zweite Speech-Ressource mit Tarif **S0** anlegen, deren Schlüssel mit `hb` → `s` → `2`
   eingeben. Umschalten mit `hb` → `x` (siehe «Azure gratis oder bezahlt»).

Beim ersten `hb` entsteht der Ordner `audio/` mit `audio.conf`, `aussprache-ollie.txt`, `probe.txt` und `hb.sh`.
Danach zum Ausprobieren: `hb` → `p` (Probe) und `hb` → `w` (Wörter).

## Hörbuch: Das Menü hb

```
 Mein-Buch · pureSATZ 2.73.0 › Hörbuch      Ollie · -8% · 128 kbit · F0
 ── Probieren ─────────────────────   ── Hörbuch ───────────────────────
  p  Probe hören (probe.txt)          a  alles: Texte → vertonen → Paket → Hörprobe
  w  Wörter hören (KLINGEN FALSCH)    t  Texte aus dem Buch (zeigt Geänderte)
  u  Fremdwörter prüfen (Browser)     v  vertonen: was fehlt + geändert
                                      k  vertonen: Kapitel auswählen …
 ── Weitergeben ───────────────────   ── Bearbeiten · Ordner ──────────
  f  fertiges Paket: ZIP mit M4B      e  Wörter · Probe · Einstellungen
  r  Hörprobe (verkauf/)              s  Azure-Schlüssel eingeben
                                      x  Azure: F0 gratis ↔ S0 bezahlt
                                      $  Terminal in audio/
                                      o  Ordner audio/ öffnen
 ── Weiteres:  h hilfe · c prüfen · ↵ zurück
```

| Taste | Was passiert |
|---|---|
| `p` | `audio/probe.txt` vorlesen – fragt Stimme (Enter = eingestellt, `1`/`2` = Favorit, `l` = alle Stimmen von Azure mit ♀/♂, Nummer oder Name) und Tempo, spielt gleich ab. Danach: «als Standard-Stimme? [j/N]» (siehe «Andere Stimme») |
| `w` | Wörter unter `## KLINGEN FALSCH` vorlesen: Original, kurze Pause, Aussprache – spielt gleich ab |
| `u` | Fremdwörter prüfen: Scan + Prüfseite im Browser (siehe «Hörbuch: Fremdwörter»). Zurück ins Menü: Ctrl+C |
| `a` | **alles in einem:** Texte → vertonen → Paket → Hörprobe. Fragt das Tempo, hält beim ersten Fehler an, spielt am Schluss die Hörprobe |
| `t` | Texte aus der Buch-MD → `audio/txt-md/`. Nur geänderte werden ersetzt, die Liste steht danach da. Fragt dann «Jetzt vertonen?» (Enter = ja) |
| `v` | vertonen: MP3 für Kapitel ohne MP3 **oder** mit geändertem Text (Text neuer als MP3). Fertige bleiben. Fragt das Tempo. Abbruch = nochmals `v` |
| `k` | Kapitel vertonen: zeigt die Kapitel mit Kürzel, dann z. B. `0603,0605` oder `06` (ganzer Teil 6) und das Tempo – **immer neu**, MP3 wird ersetzt |
| `f` | Paket zum Weitergeben → `audio/verkauf/<Buch>-Hoerbuch_<Zeit>.zip` (siehe «Hörbuch: Weitergeben») |
| `r` | Hörprobe → `audio/verkauf/hoerprobe.mp3`, spielt gleich ab. `v` = Vergleich: dieselbe Stelle als 96, 128 und 192 kbit |
| `e` | öffnet `aussprache-<stimme>.txt`, `probe.txt` oder `audio.conf` im Editor |
| `s` | Azure-Schlüssel und Region eingeben (→ `~/.bashrc`, gilt sofort): `1` = F0 gratis, `2` = S0 bezahlt |
| `x` | Azure umschalten: F0 gratis ↔ S0 bezahlt. Was gilt, ist gold – oben in der Kopfzeile und in dieser Zeile; dazu in jeder Lauf-Linie |
| `$` | Terminal im Ordner `audio/` – dort `sh hb.sh` zeigt alle Befehle |
| `o` · `h` · `c` | Ordner `audio/` öffnen · diese Hilfe · Azure-Paket, Schlüssel, ffmpeg prüfen |

Oben steht, wo du bist (› Hörbuch) und was gerade gilt: Stimme, Tempo, Qualität (aus `audio.conf`).
Das Menü bleibt offen, bis Enter (oder `z`) – nach einem Lauf bleiben die Meldungen stehen. Bei jeder Frage
(Stimme, Tempo, Kürzel, Weiter?) heisst `z` zurück.

`v` oder `k`? **`v`** schaut selbst, was fehlt oder sich geändert hat – der Normalfall. **`k`** macht genau die Kapitel,
die du nennst, auch wenn sie aktuell sind – zum Vergleichen (anderes Tempo) oder nach einer neuen Aussprache-Regel.

## Hörbuch: So entsteht es

1. `hb` → `t` – Texte aus der Buch-MD (normale Ausgabe, mit Geschichten `@@`, Ansage am Anfang) → `audio/txt-md/`.
2. Enter (oder `hb` → `v`) – vertont alles nach `audio/mp3-md-azure-ollie-t-8-k128/`, mit Tracknummer, Titel,
   Album, Autor und dem Umschlag als Cover (`ausgabe-normal/…_Vorderseite.jpg`, entsteht beim Bau).
3. Anhören, Fehler notieren → Wörter verbessern ([Aussprache verfeinern](#Hörbuch-Aussprache-verfeinern)) →
   betroffene Kapitel mit `hb` → `k` neu.

**Der MP3-Ordner sagt, wie vertont wurde:** Stimme, Tempo (`t-8` = −8 %, `t0` = normal, `t5` = +5 %) und Qualität
(`k128`, `k192`). Ein anderes Tempo oder eine andere Qualität ergibt einen eigenen Ordner – der alte bleibt.
Aufs Handy: den MP3-Ordner kopieren.

## Hörbuch: Korrektur vertonen

Du hast im Buch etwas korrigiert, z. B. in zwei Kapiteln. So kommen nur diese ins Hörbuch:

1. Buch-MD speichern.
2. `hb` → `t` → Enter. Danach steht da: «Geändert: 2 Kapitel – 06.03.00_…, 06.05.00_…».
3. «Jetzt vertonen?» → Enter. Nur diese zwei MP3 werden neu gemacht – mit den Einstellungen aus `audio.conf`
   (Stimme, Tempo, Pausen, Aussprache), also gleich wie die anderen. Anhören: die `mpv …`-Zeilen stehen da.

Im Terminal (`hb` → `$`): `sh hb.sh texte` und dann `sh hb.sh vertonen`.

Änderungen an `aussprache-<stimme>.txt` erkennt `v` selbst (ab 2.73): Kapitel mit einem neuen, geänderten oder
gelöschten Wort werden neu vertont («Aussprache geändert (Chalet) → 2 Kapitel neu»). Dafür merkt sich jeder MP3-Ordner
in `regeln.json`, welche Regeln in welchem Kapitel stecken. Nicht erkannt werden die Pausen in `audio.conf` –
dann betroffene Kapitel mit `k` neu, oder alles in einem neuen Ordner (siehe nächster Abschnitt).
Kapitel umbenannt? `v` meldet «MP3 ohne Text» – die alte Datei von Hand löschen.

## Hörbuch: Anderes Tempo ausprobieren

| Was du willst | Tasten |
|---|---|
| 2 Kapitel mit −5 % zum Vergleichen | `hb` → `k` → `0603,0605` → Tempo `-5%` → Ordner `…-t-5-k128/` |
| ganzes Buch mit −5 % | `hb` → `v` → Tempo `-5%` – der neue Ordner ist leer, also entsteht alles |
| −5 % als neuer Standard | `hb` → `e` → Einstellungen → `AZURE_RATE="-5%"` |

Vergleichen: gleiche Datei in beiden Ordnern anhören, z. B. `mpv mp3-md-azure-ollie-t-8-k128/06.03*` und
`mpv mp3-md-azure-ollie-t-5-k128/06.03*`. Der Ordner, der nicht mehr gebraucht wird, kann weg.

## Hörbuch: Einstellungen (audio.conf)

| Zeile | Wirkung |
|---|---|
| `AZURE_STIMME="1"` | `1` = Favorit 1 (Ollie), `2` = Favorit 2 (Florian) oder ganzer Stimmname (z. B. `de-CH-LeniNeural`). Einmalig: `vertonen stimme=2` |
| `AZURE_SPRACHE="de-DE"` | fest Deutsch – ohne kippt Ollie bei englischen Wörtern ins Englische |
| `AZURE_RATE="-8%"` | Tempo, minus = langsamer. Einmalig: `vertonen tempo=-5%` (eigener Ordner `…-t-5-…`) |
| `AZURE_TITELPAUSE="2000ms"` | Pause vor und nach dem Kapitelnamen (dazu `AZURE_PAUSE`, `AZURE_SATZPAUSE`) |
| `AZURE_ANSAGE="…"` | Ansage am Anfang (`00.00.00_Ansage.mp3`) mit `{titel}`, `{untertitel}`, `{autor}`, `{jahr}`; leer = keine |
| `MP3_KBIT="128"` | `128` = Test · `192` = für Plattformen: 44,1 kHz, Lautstärke angeglichen, eigener Ordner `…-k192` |
| `ALBUM`, `ARTIST`, `COVER` | leer = aus dem Buch bzw. Umschlag vorne |
| `AZURE_STUFE="F0"` | `F0` = gratis (Test) · `S0` = bezahlt (Verkauf). Umschalten: `hb` → `x` |
| `AZURE_PREIS_S0="15"` | USD pro Mio. Zeichen – nur für die Kostenanzeige bei S0 (Preis im Azure-Portal prüfen) |

## Hörbuch: Aussprache verfeinern

Jede Stimme hat ihre Liste: `audio/aussprache-ollie.txt`, eine Zeile `Original = Aussprache`.

1. Neue Wörter unter `## KLINGEN FALSCH` eintragen – gern mehrere Varianten untereinander (`hb` → `e` → `w`).
2. `hb` → `w`: liest nur diesen Bereich vor (Original, kurze Pause, Aussprache) und spielt es ab.
3. Die beste Variante nach `## KLINGEN GUT` verschieben, die anderen löschen. Im Buch gelten beide Bereiche.

Regeln:

- Nur ganze Wörter, gross/klein egal. «Velo» gilt nicht für «Velofahrer» – eigene Zeile.
- **Lange vor kurzen:** `Sitting in the Power` vor `Power`, `www.…ch` vor `…ch` – sonst findet die lange nichts mehr.
- Ein Punkt am Ende des Originals greift nicht (`Dipl.`) – mit dem nächsten Wort schreiben: `Dipl. Techniker = …`.
- `# jahreszahlen: aus` oben: die Stimme spricht Jahreszahlen selbst (Ollie kann es).
- **In einer anderen Sprache sprechen:** `La Chaux-de-Fonds = {fr: La Chaux-de-Fonds}` – die Stimme spricht das Wort
  französisch. Kürzel: `fr`, `en`, `es`, `it` (oder genau, z. B. `fr-CH`). Gilt für Multilingual-Stimmen wie Ollie und
  Florian. Gibt es für das Wort schon eine Zeile (`Chalet = Scha-le`), diese ersetzen, nicht eine zweite dazuschreiben.

Was bei Ollie Korrektur brauchte (Beispiele aus «Leben 1.0, 2.0, 3.0»):

| Art | Beispiel |
|---|---|
| «Teil 2.» liest er als «zweiter» | `Teil 2 = Zweiter Teil` (steht schon in der Vorlage) |
| englisch | `Power = Pauer` · `Trance Healing = Tränss Hieling` · `Channeln = Tschenneln` |
| französisch | `Impératif = Äähnperatiff` · `Chalet = Scha-le` · `Française = Fran-sääs` – oder echt französisch: `Chalet = {fr: Chalet}` |
| Abkürzungen | `IT = Ei-Tii` · `RAV = R.A.V` |
| Web-Adressen | `www.thomasgsteiger.ch = w w w, Punkt, thomas gsteiger, Punkt, c h` |
| Zahl mit Buchstaben | `7x7 = Sieben mal Sieben` · `8ung = Achtung` |
| Namen, spanisch | `Guayaquil = Guajakiil` · `Krishna Das = Krischna Daas` |

Ganze Sätze im Zusammenhang prüfen: in `audio/probe.txt` schreiben (`#` = Zeile aus, Leerzeile = Absatz), dann
`hb` → `p`. Mehrere Probetexte: daneben `probe-namen.txt` usw., hören mit `sh hb.sh probe probe-namen.txt`.

Bewährt: zuerst alle Fremdwörter, Abkürzungen und Adressen im Buch zusammentragen (`hb` → `u`, siehe nächster
Abschnitt), mit `w` anhören, dann das ganze Buch einmal hören und den Rest notieren.

## Hörbuch: Fremdwörter

`hb` → `u` sucht Wörter, die das deutsche Wörterbuch nicht kennt, ein französisches, spanisches, italienisches oder
englisches aber schon, und öffnet eine Prüfseite im Browser. Benachbarte Fremdwörter werden eine Gruppe
(«Trance Healing», «La Chaux-de-Fonds»).

1. Einmalig die Wörterbücher: `sudo apt install hunspell hunspell-de-ch hunspell-fr hunspell-es hunspell-it hunspell-en-gb`
   (ohne: Scan nur nach Akzenten wie é, ñ).
2. `hb` → `u`. Oben die **Kandidaten**, darunter das ganze Buch, Fremdwörter farbig. Jedes Wort ist anklickbar,
   mehrere Wörter: mit der Maus markieren.
3. Pro Wort: `fr` · `en` · `es` · `it` (in dieser Sprache sprechen) · ✎ (eigene Aussprache) · ✗ deutsch (nie mehr
   vorschlagen) · ▶ (Original und Entscheid anhören) · – (Entscheid weg).
4. **💾 in Aussprache-Liste übernehmen**: schreibt unter `## KLINGEN FALSCH` (gleiche Wörter werden ersetzt,
   Sicherung `.bak`). Dann `w` anhören, die guten nach `## KLINGEN GUT`, dann `v` – die betroffenen Kapitel kommen neu.

Ins Buch kommt nichts: Die Regeln gelten für jedes Vertonen, auch nach Änderungen im Buch.
Ohne Server (`sh hb.sh fremd`): Seite `audio/fremdwoerter.html`, Entscheide mit 📋 kopieren und selbst einfügen.

Entschiedene Wörter zeigen die Farbe ihrer Sprache (✎ gold, deutsch durchgestrichen). Auch die **bestehenden Regeln**
unten auf der Seite (und jedes unterstrichene Wort im Text) haben die Knöpfe: z. B. `Française = Fran-sääs` → `fr`,
`Mallorca = Majorka` → `es`, ▶ vergleicht vorher, 🗑 löscht die Regel.

**Mithören mit Leuchtstift:** ▶ mithören beim Kapitel spielt dessen MP3 (unten in der Leiste). Das gesprochene Wort
leuchtet gold, die letzten verblassen über 20 Sekunden – klingt etwas falsch, auch nach ein paar Sekunden noch
draufklicken und entscheiden. Wortgenau mit den Zeiten, die beim Vertonen entstehen (`…zeiten.json`, ab 2.74);
bei älteren MP3s steht «≈» – dann ist die Stelle geschätzt, das Verblassen gleicht es aus. Scrollst du selbst,
folgt die Seite erst nach ein paar Sekunden wieder.

## Hörbuch: Andere Stimme

1. `hb` → `p` → `l`: alle deutschen und mehrsprachigen Stimmen von Azure, ♀ Frau · ♂ Mann.
2. Nummer oder Namen eingeben (z. B. `de-CH-LeniNeural`), Tempo – die Probe spielt.
3. «als Standard-Stimme? [j/N]» → `j`: steht dann in `audio.conf`. Die Aussprache-Liste der bisherigen Stimme kann
   übernommen werden (jede Stimme hat ihre eigene). Die MP3s kommen in einen eigenen Ordner.

Nur **Multilingual**-Stimmen (z. B. Ollie, Florian, Seraphina) können `{fr: …}` – andere sprechen solche Wörter
in ihrer Sprache.

## Hörbuch: Befehle zum Kopieren

Ohne Menü: `hb` → `$` öffnet ein Terminal im Ordner `audio/` (oder Rechtsklick auf `audio/` → «Im Terminal öffnen»).
Alle Zeilen gelten dort. `sh hb.sh` allein zeigt die Übersicht.

**Alles in einem**

```sh
sh hb.sh komplett                    # texte → vertonen → paket → hoerprobe
sh hb.sh komplett tempo=-5%          # dasselbe mit anderem Tempo
cd .. && sh build.sh hoerbuch        # dasselbe vom Buchordner aus
```

**Probieren**

```sh
sh hb.sh probe                       # probe.txt, eingestellte Stimme
sh hb.sh probe l                     # Stimmen mit Nummer
sh hb.sh probe 2                     # mit Stimme 2 (Florian)
sh hb.sh probe 1 -10%                # Ollie, Tempo −10 %
sh hb.sh probe alle                  # alle Stimmen nacheinander (eine MP3 pro Stimme)
sh hb.sh probe probe-namen.txt       # eigener Probetext
sh hb.sh woerter                     # KLINGEN FALSCH anhören
sh hb.sh fremd server                # Fremdwörter: Prüfseite mit Speichern und ▶ (Ctrl+C beendet)
sh hb.sh fremd                       # dasselbe ohne Server → fremdwoerter.html
mpv probe-ollie-t-8.mp3              # anhören (der Name steht nach jedem Lauf da)
ls -t *.mp3 | head                   # die neusten Proben
rm probe-*.mp3 aussprache-*.mp3      # Proben aufräumen
```

**Hörbuch**

```sh
sh hb.sh texte                       # Texte aus der Buch-MD (zeigt Geänderte)
sh hb.sh vertonen                    # MP3 für alles, was fehlt oder geändert ist
sh hb.sh liste                       # Kapitel mit Kürzel und Zeichen
sh hb.sh 000000                      # nur die Ansage neu
sh hb.sh 0603,0605                   # diese Kapitel neu vertonen
sh hb.sh 06                          # ganzer Teil 6 neu
sh hb.sh 0603,0605 tempo=-5%         # zum Vergleichen mit −5 % (eigener Ordner)
sh hb.sh vertonen tempo=-5%          # ganzes Buch mit −5 %
sh hb.sh vertonen stimme=2           # ganzes Buch einmalig mit Florian
sh hb.sh stufe                       # Azure umschalten: F0 gratis ↔ S0 bezahlt (stufe s0 / stufe f0)
```

**Nachsehen und anhören**

```sh
ls mp3-md-azure-ollie-t-8-k128/                         # alle MP3s
mpv mp3-md-azure-ollie-t-8-k128/02.01*                  # ein Kapitel
mpv mp3-md-azure-ollie-t-8-k128/                        # alle nacheinander
tail -40 mp3-md-azure-ollie-t-8-k128/einstellungen.txt  # letzter Lauf: Zeit, Aufruf, Einstellungen, Wörter
cat txt-md/02.01*                              # was die Stimme bekommt (vor den Aussprache-Regeln)
grep -n "Zeitstrahl" buch.txt                  # steht etwas im Hörbuch?
ls *.zip                                       # Sicherungen der ganzen Läufe
for f in mp3-md-azure-ollie-t-8-k128/*.mp3; do ffprobe -v error -show_entries format=duration -of csv=p=0 "$f"; done | awk '{s+=$1} END {printf "%d Dateien, %d:%02d:%02d\n", NR, s/3600, s%3600/60, s%60}'
```

**Vergleichen und neu machen**

```sh
mv mp3-md-azure-ollie-t-8-k128 mp3-alt   # alten Stand beiseite, dann: sh hb.sh vertonen
sed -i 's/^MP3_KBIT=.*/MP3_KBIT="192"/' audio.conf   # Produktion (eigener Ordner …-k192)
sed -i 's/^AZURE_STIMME=.*/AZURE_STIMME="2"/' audio.conf   # Stimme 2 fest einstellen
```

## Hörbuch: Was vorgelesen wird

Vorgelesen: Widmung, Kernsatz, Text, Geschichten (`@@`), Zitate, Tabellen Zeile für Zeile, Zeitstrahl,
Fotos als «Bild: Titel. Text.». Nicht: @TITEL, @IMPRESSUM, @HINWEIS, Inhaltsverzeichnis, übrige @-Befehle,
unzensierte Teile (das Hörbuch gibt es nur für die normale Ausgabe). Kontrolle: `audio/buch.txt` (vorgelesen),
`audio/buch-entfernt.txt` (weggelassen).

## Hörbuch: Was im Ordner audio liegt

- `audio.conf`, `aussprache-<stimme>.txt`, `probe.txt` (und eigene `probe-….txt`) – deine Einstellungen, Wörter und
  Probetexte (kommen zu GitHub, bleiben bei Updates).
- `hb.sh` – Starter für das Terminal: `sh hb.sh` zeigt alle Befehle.
- `probe-….mp3`, `aussprache-….mp3` – die letzten Proben (nicht zu GitHub).
- `txt-md/` – die Texte pro Kapitel (`t` ersetzt nur geänderte; ihr Datum zeigt `v`, was neu muss).
- `mp3-md-azure-<stimme>-t<tempo>-k<kbit>/` (z. B. `…-ollie-t-8-k128`) mit `einstellungen.txt`: jeder Lauf wird
  unten angehängt – Zeit, Aufruf, Einstellungen und die ganze Aussprache-Liste.
- `txt-md_<stimme>-t<tempo>-k<kbit>_<zeit>.zip` – wenn das ganze Buch vertont wird: Texte, Aussprache-Liste und
  `audio.conf` zur Sicherheit.

MP3, Texte und ZIPs kommen nicht zu GitHub.

## Hörbuch: Weitergeben (Paket und Hörprobe)

Für den eigenen Shop, als Geschenk oder zum Download. Zuerst Texte aktuell (`t`) und alles vertont (`v`) –
oder gleich alles mit `hb` → `a`. Die Original-MP3s bleiben unverändert. Fehlt zu einem Text die MP3, bricht
`paket` ab («zuerst vertonen»); MP3s ohne Text (alte Kapitel) kommen nicht ins Paket.

```
sh hb.sh paket               # → audio/verkauf/<Buch>-Hoerbuch_<Zeit>.zip
sh hb.sh hoerprobe           # → audio/verkauf/hoerprobe.mp3 (Ansage + erste Minuten, ausgeblendet)
sh hb.sh hoerprobe 0201 2    # anderes Kapitel, 2 Minuten
sh hb.sh hoerprobe vergleich # hoerprobe-96 / -128 / -192.mp3: dieselbe Stelle zum Vergleichen
```

Im ZIP: `MP3/01 Ansage.mp3` … (jedes Kapitel, Mono, `PAKET_KBIT`, mit Titel, Tracknummer, Album, Autor, Genre
«Hörbuch» und Cover) · eine **M4B** (AAC 96 kbit) mit Kapitelmarken (das ganze Hörbuch in einer Datei, für Handy und Hörbuch-Apps) ·
`playlist.m3u` · `cover.jpg` · `LIESMICH.txt` (mit Hinweis «Gelesen von einer KI-Stimme»).

In `audio.conf`: `PAKET_KBIT` (128 = Hörbuch-Standard, 96 = kleiner; zum Entscheiden `hb` → `r` → `v`), `HOERPROBE` (Kürzel und Minuten,
z. B. `0002 3` = Vorwort), `COVER_QUADRAT` (quadratisches Bild in `audio/`; leer = Umschlag vorne),
`AZURE_ABSPANN` (wird bei `t` als letztes Kapitel `99.00.00_Abspann` angelegt).

Qualität: Mit `MP3_KBIT="192"` liefert Azure verlustfrei (WAV 48 kHz), pureSATZ gleicht die Lautstärke an und
macht erst am Schluss MP3 – das ist der Master. Das Paket rechnet daraus `PAKET_KBIT`. 128 im Master ist nur zum Testen.

## Hörbuch: Azure gratis oder bezahlt

Der Klang ist gleich. **F0** = gratis, 0,5 Mio. Zeichen pro Monat, zum Testen. **S0** = bezahlt (rund 15 USD pro
Mio. Zeichen, ein Buch mit 80'000 Zeichen also etwa 1–2 Franken), für die Verkaufsfassung.

1. Im Azure-Portal eine zweite Speech-Ressource mit Tarif S0 anlegen (gleiche Region), Schlüssel 1 kopieren.
2. `hb` → `s` → `2`: als S0-Schlüssel eingeben (kommt als `AZURE_SPEECH_KEY_S0` in `~/.bashrc`).
3. `hb` → `x`: umschalten. Oben im Menü steht `F0` oder `S0`, ebenso in jeder Lauf-Linie und in `einstellungen.txt`.

Bei S0 zeigen `v` und `a` vor dem Vertonen die Höchstkosten fürs ganze Buch und fragen `[J/n]`.
Nach dem Verkaufslauf mit `x` zurück auf F0 – so kostet das Probieren nichts.

## Hörbuch: Kosten, Rechte, Verkauf

- F0 gratis bis 0,5 Mio. Zeichen pro Monat; Verbrauch: Azure-Portal → Speech-Ressource → Metriken.
  Die höhere Qualität (192) kostet nicht mehr – abgerechnet wird nach Zeichen.
- Für dich, Familie und Freunde: frei.
- **Verkauf:** `MP3_KBIT="192"`, die KI-Stimme angeben (Ansage), vorher die Azure-Bedingungen und die Regeln der
  Plattform prüfen – manche nehmen keine KI-Stimmen an. Die meisten wollen eine MP3 pro Kapitel (so wie hier).

## Hörbuch: Wenn etwas klemmt

| Meldung | Was tun |
|---|---|
| «S0 eingestellt, aber kein S0-Schlüssel» | `hb` → `s` → `2` (Schlüssel eingeben) oder `hb` → `x` zurück auf F0 |
| «AZURE_SPEECH_KEY fehlt» | `hb` → `s` (Schlüssel eingeben). Danach gilt er sofort, auch in offenen Menüs und Terminals. Prüfen: `grep -c AZURE_SPEECH ~/.bashrc` (2 = gut, mit S0-Schlüssel 3) |
| «Azure-Paket fehlt» | `hb` → `c` – installiert es in die `.venv` des Buchs |
| «Fehler» bei einem Kapitel | nochmals `v` – fertige Kapitel werden übersprungen |
| Kapitel klingt noch alt | zuerst `t` (Texte), dann `v`. Nur Aussprache geändert? Dann dieses Kapitel mit `k` |
| «MP3 ohne Text» | Kapitel umbenannt oder entfernt – die genannte alte MP3 von Hand löschen |
| Wort wird nicht ersetzt | ganzes Wort? Reihenfolge (lange vor kurzen)? Kein `$` oder Punkt am Ende? |
| Änderung in der Wörter-Datei ist weg | Editor hat überschrieben: Datei schliessen oder «Neu laden» |

# Werkzeuge

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

## Mit einer KI arbeiten

**Füttere deine Lieblings-KI mit `hilfe-ki.md` – und du bedienst pureSATZ im Flug.** Die KI kennt dann jede
Einstellung und sagt dir, was du wo eintragen musst. `hilfe-ki.md` ist dieselbe Hilfe als reiner Text (etwa halb so gross,
passt auch in kostenlose KI-Chats) und entsteht zusammen mit `hilfe.html` – am besten die aus dem Buchordner,
dort stehen auch die Variablen deines Buchs.

1. Neuen Chat öffnen (Claude, ChatGPT, Gemini …) und `hilfe-ki.md` hineinziehen – oder oben in der Hilfe
   **«📋 für KI kopieren»** drücken und im Chat einfügen (Ctrl+V).
2. Die Datei dazugeben, um die es geht, z. B. `Mein-Buch-variablen.md`, die Buch-MD oder eine Druckdatei aus `druck/`.
3. Fragen, z. B. «Wie bringe ich das Inhaltsverzeichnis auf zwei Seiten?» oder «Wie wird ein Foto so breit wie der Text?»
4. Vorschlag übernehmen, dann `sh build.sh pruefen` – der Motor meldet sofort, falls etwas nicht passt.

**Regel für die KI:** nur die Buchdateien ändern (MD, Variablen, Umschlag, `druck/`, Stichworte, Tabellen, Geschichten) –
**nie den Ordner `motor/`**.

Nimmt ein kostenloser KI-Chat auch `hilfe-ki.md` nicht ganz auf: `readme4ki.txt` (kurze Regeln) und deine Frage
geben und den passenden Abschnitt dieser Hilfe dazukopieren (oben suchen, Text markieren, kopieren).

## Skripte und Kurzbefehle

Im Buchordner (Windows: dieselben Namen mit `.bat`):

| Befehl | Wofür |
|---|---|
| `sh menu.sh` | Menü – alles mit einem Buchstaben |
| `sh build.sh …` | bauen, prüfen, Leseprobe, Stand … (alle Varianten: Abschnitt «Bauen») |
| `sh sync.sh` | mit GitHub abgleichen (mehrere Computer) |
| `sh update.sh` | neuen Motor holen |
| `sh sicherung.sh` | ganzes Buch als ZIP sichern |
| `sh cleanup.sh` | aufräumen (zeigt zuerst die Liste, fragt); `sh cleanup.sh ausgaben` = auch die Ausgabeordner |
| `sh neu.sh "Titel"` | neue Geschichte anlegen; ohne Titel: Übersicht der Geschichten |

**Von Hand**, für Spezielles:

| Befehl | Wofür |
|---|---|
| `python3 motor/manuskript.py` | Liste aller `@`-Befehle |
| `.venv/bin/python3 motor/booklet.py datei.pdf` | ein beliebiges PDF als Booklet zum Selberdrucken → `datei_booklet.pdf` |
| `.venv/bin/python3 motor/mockup.py ausgabe-normal/<datei>.pdf` | Werbebilder aus einem PDF (sonst `sh build.sh mockup`) |
| `python3 motor/epub2.py ausgabe-normal/<datei>.epub` | EPUB 2 aus einem fertigen E-Book |

## Das pureSATZ Handbuch

Diese Hilfe gibt es auch als Buch, gesetzt mit pureSATZ selbst. Einmal anlegen, im Ordner pureSATZ:

```sh
sh setup/setup.sh handbuch/handbuch.txt
cd ../pureSATZ-Handbuch && sh build.sh handbuch
```

Danach entsteht die Buch-MD bei jedem Bau neu aus der Hilfe (`{buch-aus-hilfe}: ja` in der Variablen-Datei). Darum
nie dort ändern, sondern in `START.md`, `motor/HILFE.md` und `handbuch/` (Einleitung, Stichworte). Text nur für die
Webseite steht zwischen `::: nur-webhilfe` und `:::`, Text nur fürs Buch zwischen `::: nur-handbuch` und `:::`.

## Werben: Leseprobe, Bilder, Shop-Texte

| Was | So |
|---|---|
| Leseprobe (PDF und EPUB) | `sh build.sh leseprobe` – welche Kapitel: `{leseprobe}` in der Variablen-Datei; einmalig bestimmte Seiten: `sh build.sh leseprobe normal 18,20-22` |
| Werbebilder | `…_Mockup.jpg` und `…_Vorderseite.jpg` nach `final` im Ausgabeordner; neu: `sh build.sh mockup` |
| Cover-Bilder | `…_Cover-vorne.jpg`, `…_Cover-hinten.jpg` – randlos, für Shop und Webseite |
| Texte für Shops | `shop-angaben.txt` nach `final`: Beschreibung, Schlagwörter, Kategorie aus `{shop-beschreibung}`, `{shop-schlagwoerter}`, `{shop-kategorie}` |
| Termine | Fahrplan unter «Erste Schritte»: Newsletter, Vernissage, Geschenke |

# Nachschlagen

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
- Inhaltsverzeichnis: siehe [Inhaltsverzeichnis gestalten](#Inhaltsverzeichnis-gestalten).

**Probedruck und Farben**
- Farben am Bildschirm nur grob beurteilen. Was zählt, ist der Probedruck auf dem echten Papier (matt/glänzend, weiss/creme).
- Seitenzahl geändert: im Coverrechner der Druckerei prüfen, ob Rücken und Umschlag gleich bleiben. Dann
  `{berechnet-fuer-seiten}` anpassen und `{neu-berechnen}: nein` setzen ([Umschlag](#Umschlag-Ruecken)).

## Glossar

| Begriff | Bedeutung |
|---|---|
| Ausgabe | ein Weg zum Leser: Druck normal, Druck unzensiert, E-Book … – je mit eigener ISBN und eigenem Impressum |
| Beschnitt | Rand, der beim Schneiden wegfällt; Bilder und Farben reichen bis dorthin |
| Booklet | A4-Blätter zum Falten – ein Probeexemplar zum Selberdrucken |
| Buchblock | der Innenteil des Buchs ohne Umschlag, eine PDF-Datei für die Druckerei |
| Coverrechner | Rechner der Druckerei: Rückenbreite und Umschlagmasse aus Seitenzahl und Papier |
| EAN-13 | der Strichcode mit der ISBN auf der Rückseite (auch Barcode) |
| EPUB | Dateiformat für E-Books |
| Fassung | normal oder unzensiert («uz»): zwei Varianten desselben Buchs |
| Füllseite | leere Seite am Schluss, damit die Seitenzahl für die Druckerei aufgeht |
| ISBN | Nummer eines Buchs, eine pro Ausgabe |
| Lese-PDF | Bildschirm-PDF zum Lesen und Verschicken, mit Umschlag |
| Motor | pureSATZ selbst (Ordner `motor/`) – setzt das Buch |
| Plattform-Datei | `druck/<datei>.md`: die Technik einer Druckerei |
| Probedruck | bestelltes Testexemplar vor der Freigabe |
| Rücken | schmale Seite des Umschlags zwischen Vorder- und Rückseite |
| Stand | festgehaltener Zwischenstand – zeigt später, was sich geändert hat |
| Variable | `{name}: wert` in der Variablen-Datei; im Buch erscheint der Wert an der Stelle `{name}` |
| Verzierung (Zier) | kleines Bild als Schmuck, z. B. der Lotus |
