# pureSATZ – Änderungen

pureSATZ ist das Satzsystem (der «Motor»), das aus Markdown-Dateien Buch, Umschlag und E-Book macht.
Der Name erinnert an pureRACE, die Zeitmess-Software des Autors von 1994. Bis 2.9.4 hiess es «Motor Leeres Buch».

## 2.40.0 (Oktober 2026)
- `{farbmodus}: cmyk`: Ghostscript läuft nur noch bei `final` und `komplett`. Im Entwurf (`sh build.sh`,
  `nur-druck` ohne final) bleiben die Druckdateien RGB – der Bau ist wieder so schnell wie vorher (Hinweis im Ablauf).
- Ghostscript fehlt: Hinweis mit dem passenden Befehl für Linux, Mac oder Windows. Unter Windows wird Ghostscript
  auch ohne PATH gefunden (`C:\Program Files\gs\…\bin\gswin64c.exe`).
- Einrichte-Skripte (`pc-einrichten/`): fragen, ob Ghostscript installiert werden soll (Linux apt, Mac brew oder
  MacPorts, Windows winget). INSTALLATION.md und HILFE.md ergänzt.

## 2.39.1 (Oktober 2026)
- E-Book: Teil-Titel zentriert (Apple Books setzte `h1` linksbündig); `---` / `@UMBRUCH` gibt jetzt auch im E-Book
  eine neue Seite.

## 2.39.0 (Oktober 2026)
- Neu in der Plattform-Datei: `{farbmodus}: rgb | cmyk`. Mit `cmyk` werden Buchblock und Umschlag (PDF) nach dem Bau
  mit Ghostscript nach CMYK umgewandelt (tredition verlangt CMYK). Ohne Ghostscript: Hinweis, Dateien bleiben RGB.
  Vorlage tredition: `{farbmodus}: cmyk`.

## 2.38.0 (Oktober 2026)
- Neu `{inhalt-dichte}` (# LAYOUT, Standard 1): Zeilenabstand im Inhaltsverzeichnis, z. B. 0.92 = etwas enger,
  damit es auf eine Seite weniger passt.
- Korrektur-PDF und Gegenlesen: Kopfzeile und Zeilennummern in Poppins (eingebettet) statt Helvetica –
  keine Schriftwarnung mehr.

## 2.37.0 (Oktober 2026)
- Personen: Steht ein Begriff im Kapiteltitel, kommt das ganze Kapitel dazu (Leseprobe-Seiten und Gegenlesen).
  Neu `+ uz: 59` / `+ normal: 41` unter einer Person in `personen-seiten.txt` = Seiten von Hand dazu (bleibt stehen).
  Die Kopfzeile «Teil · Kapitel» zählt nicht mehr als Fundstelle.

## 2.36.0 (Oktober 2026)
- Impressum: zwei freie Zeilen `{impressum-satz1}` und `{impressum-satz2}` direkt unter der Herstellung, in allen
  Ausgaben. Vorlage: `{impressum-satz1}: Gesetzt mit pureSATZ · github.com/tgsteiger/pureSATZ`.

## 2.35.3 (Oktober 2026)
- Gegenlesen: Die Stellen der Person sind links mit rotem ▶ und roter Zeilennummer markiert
  (`fassungen.korrektur(…, markiert=…)`; das normale Korrektur-PDF bleibt unverändert).

## 2.35.2 (Oktober 2026)
- Gegenlesen: `check_Name_Gegenlesen.pdf` im Format des Korrektur-PDFs (A4, Zeilennummern, Notizlinien) – für
  Rückmeldungen wie «S. 41, Z. 7». Kopfzeile: «Seitenzahl unten auf der Buchseite verwenden».

## 2.35.1 (Oktober 2026)
- Einheitlich `#` Titel · `>` Erklärung · `$` Befehl: `00-UEBERSICHT.txt` (neu mit Abschnitt GEGENLESEN, fehlende
  Dateien mit dem Befehl in eigener Zeile), `personen-seiten.txt` (Abschnitt «KEINE PERSONEN») und die Hinweise im
  Terminal (Stände, Personen, Update, «Neue PDFs»).

## 2.35.0 (Oktober 2026)
- **Personen gegenlesen:** `sh build.sh personen` sucht in den fertigen Lese-PDFs nach Personen (Vornamen, Rollen,
  Stichwörter) und schreibt `personen-seiten.txt` mit Seite, Zeile und Kapitel. Die Datei ist zugleich Eingabe:
  `Andrea | Medizinfrau` = eine Person, `--- Wort` = nie mehr vorschlagen. `sh build.sh personen Andrea` macht
  `check_Andrea_Gegenlesen.pdf` (und `-uz`) mit genau diesen Seiten – ohne neu zu bauen. Neues Modul `motor/personen.py`.

## 2.34.0 (Oktober 2026)
- Leseprobe: Seiten gehen auch in `{leseprobe}` (`17,18-22, 74, 88-92`; eine Zahl allein = Anzahl Kapitel).
  Neu `sh build.sh leseprobe [normal|uz] 18,20,23`: einmalig diese Seiten, ohne die Variablen zu ändern.
- Änderungs-PDF: Listenpunkte einzeln mit •, eingerückt und unter einer gemeinsamen Marke; **fett** bleibt fett
  bei neuen und gestrichenen Absätzen. Fehlt eine Datei in einem Stand (z. B. Umschlag), wird sie nicht verglichen.

## 2.33.1 (Oktober 2026)
- Stand nachträglich: `sh build.sh stand "Probedruck 1" 23.10.2026 15:00` nimmt die neueste Fassung bis zu diesem
  Zeitpunkt aus `md-history/` (Buch, Variablen, Umschlag, Stichwörter, Geschichten). Auch nur Datum oder nur Uhrzeit.

## 2.33.0 (Oktober 2026)
- **Was hat sich geändert?** Neu `sh build.sh stand "Name"` (Stand festhalten in `staende/`, ohne Name: Liste) und
  `sh build.sh aenderungen ["Name" ["Name2"]]`: `…_Aenderungen.pdf` mit allen geänderten, neuen und gestrichenen
  Absätzen nach Teil und Kapitel (Wörter grün/rot), Geschichten an ihrer Stelle, dazu geänderte Variablen,
  Umschlag-Werte und Stichwörter. Neues Modul `motor/staende.py`.
- `staende/` ist vor `sh cleanup.sh` geschützt; Hilfe, Spickzettel, readme4ki und Webseite ergänzt.

## 2.32.1 (Oktober 2026)
- Am Ende jedes Baus: Liste der neu erstellten PDFs (relativ zum Buchordner), zum Kopieren hinter `xreader `.
- `linux-einrichten.sh`: erkennt eine schon vorhandene xreader-Funktion oder einen alias in `~/.bashrc`
  (auch von Hand eingetragen) und trägt nichts doppelt ein.

## 2.32.0 (Oktober 2026)
- Impressum: `{auflage}` (z. B. «1. Auflage 2026») steht jetzt über der ISBN. Leer oder nicht vorhanden = Zeile fällt weg.
  Eigener Wert je Fassung mit `{auflage-normal}` / `{auflage-uz}`.
- `pc-einrichten/linux-einrichten.sh`: fragt, ob `xreader datei.pdf` im Hintergrund starten soll (Terminal bleibt frei).
  Trägt dafür einmalig eine kleine Funktion in `~/.bashrc` ein; mehrfaches Ausführen schadet nicht.

## 2.31.2 (Oktober 2026)
- Teil ohne Nummer (`# |Anhang|Zeitstrahl, Glossar, Klangportrait`): Inhaltsverzeichnis, PDF-Lesezeichen und E-Book
  zeigen jetzt «Anhang: …» statt «· Anhang: …»; im E-Book keine leere Nummernzeile mehr. Hilfe ergänzt.

## 2.31.1 (Oktober 2026)
- Neu `test/vergleich.py`: zwei Bauten Seite für Seite vergleichen (Text und Pixel jeder PDF-Seite, E-Books Datei für
  Datei). Damit lässt sich nach jeder Motor-Änderung prüfen, dass ein Buch gleich bleibt.
- Im Code die Versionsvermerke («(2.24)», «pureSATZ 2.19» …) entfernt – die Geschichte steht hier im CHANGELOG.
  Keine Änderung am Ergebnis (Leben123 mit vergleich.py geprüft: alles gleich).

## 2.31.0 (Oktober 2026)
- **`@ZITAT-ZIER Satz`**: Zitat mit Verzierung oben und unten – dasselbe wie `> Satz`, als Paar zu `@ZITAT Satz`
  (schlicht). `-ZIER` weglassen = Verzierung weg. `> Satz` geht im Buchtext weiter.
- Hilfe: jede Befehlszeile mit **Schreibweise** (die ganze Zeile, wie sie im Buch steht) und **Wirkung**;
  `@KOPF` unter «Seite, Umbruch, Kopfzeile»; «Text hervorheben» von leicht bis stark (`~`, `@ZITAT`, `@ZITAT-ZIER`,
  `@UNTEN`, `@MOTTO`). Neue Tabelle: `>` im Buchtext = Zitat, in den Einstellungs-Dateien = Erklärung.
- `python3 motor/manuskript.py` zeigt die Befehle ebenso mit Schreibweise und Wirkung.
- Vorlage und Leben123: Zitate als `@ZITAT-ZIER`. Geprüft: alle PDFs, Umschläge und E-Books gleich wie vorher.

## 2.30.3 (Oktober 2026)
- Hilfe: Befehle nach Aufgabe gruppiert (Titelei · Seiten und Umbruch · Text hervorheben · Verzierung ·
  Bilder, Links, Tabellen · Verzeichnisse), dazu «Seite sieht nicht gut aus? – Lösungen». Befehle stehen wieder
  ohne Klammern da (`@TITEL` statt `{@TITEL}`). Gleichbedeutende alte Namen (@LOTUS …, @ANHANG) nicht mehr aufgeführt.

## 2.30.2 (Oktober 2026)
- Der Bau zeigt am Anfang und am Ende das gewählte Farbschema, z. B. «Farben: Farbschema 2: dunkler für den Druck».

## 2.30.1 (Oktober 2026)
- Vorlage: Farbschema 3 für eigene Farben (leer, zum Ausfüllen).

## 2.30.0 (Oktober 2026)
- **Farbschemas**: unter `## Farben` Abschnitte `### Farbschema 1: …`, `### Farbschema 2: …` usw.; `{farbschema}: 2`
  wählt eines für alle Ausgaben. Schema 1 ist die Grundlage, das gewählte ersetzt nur seine Werte, andere werden
  übergangen. Fehlt das gewählte, meldet der Bau es und nimmt Schema 1. Ohne `{farbschema}` bleibt alles wie bisher.
- Vorlage und Leben123: Schema 1 = bisherige Farben, Schema 2 = dunkler für den Druck (Text, Kopfzeile, Gold).
- Geprüft: Leben123 mit Schema 1 Seite für Seite und Pixel für Pixel gleich wie mit 2.29.0.

## 2.29.0 (Oktober 2026)
- **Ein Abschnitt pro Ausgabe in der Variablen-Datei**: `## Ausgabe: PDF`, `## Ausgabe: Druck normal`,
  `## Ausgabe: Druck unzensiert` (auch «Druck zweite Ausgabe»), `## Ausgabe: E-Book`, `## Ausgabe: E-Book unzensiert`.
  Darin kurze Namen: `{druck-datei}`, `{isbn}`, `{preis}`, `{impressum-herstellung}`, `{impressum-kontakt}`,
  `{impressum-logo}`. Ein Wert dort gilt nur für diese Ausgabe und ersetzt den gemeinsamen.
- **Impressum automatisch**: Bleibt `## @IMPRESSUM` leer, setzt der Motor je Ausgabe © {jahr} {autor} · {website} ·
  {impressum-herstellung} · {impressum-rechte} · {impressum-kontakt} · ISBN {isbn} ein; leere Zeilen fallen weg.
- **E-Book je Fassung abschaltbar**: `{erstellen}: nein` unter `## Ausgabe: E-Book unzensiert`; alte E-Book-Dateien
  dieser Fassung werden entfernt, die Übersicht sagt «E-Book: keines».
- **Plattform-Dateien nur noch Technik**: oben `{neu-berechnen}` und `{berechnet-fuer-seiten}`, zuunterst
  `## Coverrechner (Rohdaten)` (wird nicht gelesen). `final` warnt, wenn der Buchblock eine andere Seitenzahl hat,
  und erinnert bei `{neu-berechnen}: ja`. `{format}` nur noch, wenn das Druckformat abweicht.
- `{format}` nimmt auch ein eigenes Mass in mm (`150 x 215`).
- `@SEITENMITTE` zentriert auch eine Seite, nach der ein Verzeichnis (z. B. Stichworte) beginnt.
- Leseprobe: auf der Schlussseite steht die ISBN der Druckausgabe (bisher «ISBN folgt», wenn sie in der
  Plattform-Datei stand); ohne ISBN fällt die Zeile weg.
- shop-angaben.txt: ISBN und Preis aus den Ausgaben.
- In allen Einstellungs-Dateien: zuerst die Werte, darunter die Erklärungen `> {name}: …`.
- Vorlage: Variablen mit Ausgabe-Abschnitten, Muster in vorlage/druck/ nur Technik (Impressum-Hinweise unter
  `## Notizen`), `tredition-ebook.md` entfällt. setup.sh trägt die gewählte Bindung in die Plattform-Datei ein.
- Hilfe, README und readme4ki.txt neu geschrieben; neuer Abschnitt «Ein neues Buch anlegen».
- Geprüft: Leben123 umgestellt – alle Dateien der normalen Fassung Seite für Seite und Pixel für Pixel gleich wie mit
  2.28.0; Unzensiert gleich bis auf die neue Seite «Was kommt danach?» und ohne E-Book. Alte Schreibweise baut gleich.

## 2.28.0 (Oktober 2026)
- **Eine Plattform-Datei pro Ausgabe, auch fürs E-Book**: neue Variable `{ebook}` (z. B. `tredition-ebook` →
  `druck/tredition-ebook.md`). Ihre Werte gelten nur im E-Book und ersetzen die gleichnamigen der Variablen-Datei –
  genau wie `{druck-normal}` / `{druck-uz}` fürs gedruckte Buch. `sh build.sh pruefen` meldet eine fehlende Datei.
- **Impressum gehört zur Plattform**: `{impressum-herstellung}`, `{impressum-logo}` (und ein eigener
  `{impressum-kontakt}`) stehen in der Plattform-Datei, kurze Namen ohne Endungen; gemeinsame Zeilen
  (`{impressum-rechte}`, `{impressum-kontakt}`) in der Variablen-Datei. Die Zuordnung «welche Ausgabe → welche
  Plattform» steht in der Variablen-Datei unter «Ausgaben – wer macht was».
- Muster in vorlage/druck/ wieder mit den Impressum-Zeilen ihrer Plattform; neues Muster `tredition-ebook.md`.
  Ohne Plattform-Datei gelten weiterhin `{impressum-herstellung-druck}` usw. aus der Variablen-Datei (Vorgabe epubli).
- Leben123: Normal gedruckt bei tredition, Unzensiert als Privatdruck bei epubli, E-Book bei tredition.

## 2.27.0 (Oktober 2026)
- **Eine Schreibweise für alle Einstellungs-Dateien** (Variablen, Druckdateien, Umschlag, Kopf der Geschichten, Fotos):
  `# / ##` Gliederung · `> …` Erklärung · `{name}: wert` setzt eine Variable · `feld: text` Feld des Umschlags,
  eines Fotos oder einer Geschichte. Kein `- ` mehr davor (nur echte Listen behalten es). Ältere Dateien mit
  `- name: wert` und erklärenden Sätzen ohne `>` gehen weiterhin.
- Vorlage, Word-Import (Fotos), neue Geschichten (`sh neu.sh`), Hilfe und readme4ki.txt auf die neue Schreibweise.
  hilfe.html liest Variablen mit und ohne `- `; Erklärungen mit `>` erscheinen dort als Text.
- Geprüft: Leben123 umgestellt (Variablen, Umschlag, Druckdateien, 12 Fotos) – alle PDFs, Umschläge und E-Books
  Seite für Seite und Pixel für Pixel gleich wie mit 2.26.0.

## 2.26.0 (Oktober 2026)
- **`{name}` auch dort, wo der Wert steht**: in Variablen- und Druckdateien darf (und soll) der Name in Klammern stehen:
  `- {impressum-kontakt}: …`. Die Suche nach `{impressum-kontakt}` findet so den Wert und die Stelle im Buch.
  `- name: wert` ohne Klammern geht weiterhin. Vorlage umgestellt; hilfe.html zeigt die Namen mit Klammern.
- **Der genauere Name gewinnt**: `{name-ebook}` / `{name-druck}` / `{name-bildschirm}` haben Vorrang vor `{name}`.
  Ein Wert in der Druckdatei schlägt auch `{name-druck}` der Variablen-Datei.
- **Regel: Texte in die Variablen-Datei, Technik in die Druckdatei.** Das Impressum steht vollständig in der
  Variablen-Datei (`impressum-herstellung-druck`, `-ebook`, `impressum-rechte`, `impressum-kontakt`,
  `impressum-logo-druck`); so bekommt auch das E-Book die Zeilen der Druckerei (z. B. tredition). Die Muster in
  vorlage/druck/ haben keinen Impressum-Abschnitt mehr (nur einen Hinweis, z. B. für den Privatdruck).
- Vorlage: Impressum wie Leben123 (©, Website, Herstellung, Rechte, Kontakt, ISBN); `verlag` entfällt (Adresse steht
  in `impressum-rechte`).
- **`plattform: tredition` und `kdp`**: verhalten sich wie `bod` (Strichcode-Feld rechts, keine epubli-Füllseite).
- **cleanup.sh** räumt zusätzlich `.backup`-Dateien auf, und mit `sh cleanup.sh ausgaben` auch alte Ausgabeordner,
  die zu keiner Fassung mehr gehören (z. B. `ausgabe-normal epubli`).

## 2.25.0 (Oktober 2026)
- **Markdown für Zeilenumbruch und neue Seite**:
  - `\` am Zeilenende = Zeilenumbruch im Absatz (wie `<br/>`); die nächste Zeile gehört zum selben Absatz.
    Gilt im Buch, in Blöcken und in der Umschlag-Datei. `<br/>` geht weiterhin (z. B. in Variablen).
  - Eine Zeile `---` = neue Seite (wie `@UMBRUCH`). Davor eine Leerzeile, sonst macht der Editor aus der Zeile
    darüber eine Überschrift.
- **Hilfe: die Regel der vier Formen** oben unter «Schreiben»: Markdown für alles, was Markdown kann; `@BEFEHL` für
  eine Zeile mit einer Wirkung; `## @…` / `#### @…` für Titelei und Elemente mit Angaben; `::: … :::` für
  Textbereiche mit Anfang und Ende. Vorlage und readme4ki.txt angepasst.
- Geprüft: Leben123 umgestellt (18 × `<br/>` → `\`, 4 × `@UMBRUCH` → `---`); alle PDFs, Umschläge und E-Books
  Seite für Seite und Pixel für Pixel gleich wie mit 2.24.2.

## 2.24.2 (Oktober 2026)
- **Widmung im Druck im unteren Drittel**: auf ihrer eigenen Seite (rechts) etwas kleiner (9 pt) und mittig im
  unteren Drittel statt in der Seitenmitte.

## 2.24.1 (Oktober 2026)
- **Logo im Impressum kleiner und näher beim Text**: Höhe 1,5 × Schriftgrösse des Impressums, zwei Zeilenabstände
  über dem ersten Absatz (statt 34 mm breit oben auf der Seite).

## 2.24.0 (Oktober 2026)
- **Titelei ohne `:::`-Blöcke**: `## @TITEL`, `## @IMPRESSUM`, `## @HINWEIS`, `## @WIDMUNG` stehen als eigene Abschnitte.
  - `@TITEL`: weitere Zeilen unter Titel und Untertitel werden mit « · » an den Untertitel gehängt
    (Vorlage: `{titel-zusatz}`, `titel-zusatz-uz` = Name der zweiten Ausgabe). PDF und E-Book.
  - **`## @HINWEIS`** (neu): direkt nach `@IMPRESSUM` oder `@WIDMUNG`; steht unten im Impressum, mit Abstand.
  - `## @WIDMUNG` als eigene Überschrift (bisher `### @WIDMUNG`, geht weiterhin).
- **Druck: Impressum und Widmung getrennt**: Seite 2 links = Impressum unten, Seite 3 rechts = Widmung allein,
  senkrecht mittig. Danach Kernsatz und Inhalt; das Vorwort beginnt so auf einer rechten Seite. Der Buchblock wird
  um eine Seite länger (oft fällt dafür eine Füllseite weg).
- **Logo im Impressum**: neue Variable `impressum-logo` (Druckdatei oder Variablen-Datei, PNG aus bilder/), oben links,
  34 mm breit (ab 2.24.1: über dem Text, 1,5 × Schrifthöhe). Leer = kein Logo. `sh build.sh pruefen` meldet ein fehlendes Bild.
- **Variablen je Medium**: gibt es `name-druck`, `name-ebook` oder `name-bildschirm`, nimmt `{name}` den Wert des
  Mediums (z. B. `impressum-herstellung-druck`). So braucht das Impressum keine `::: nur-buch`-Blöcke mehr.
  Neu in der Vorlage: `impressum-rechte` (Urheberrecht).
- **Foto ohne `:::`**: `#### @FOTO Titel`, darunter `- datei: …`, `- text: …` usw.; die erste Leerzeile beendet
  das Foto. `#### @FOTO-UZ` = nur zweite Ausgabe. Steht so in der Gliederung des Editors. Die alte Form
  `::: foto` … `:::` geht weiterhin. Vorlage, Import (Word/LibreOffice) und Hilfe auf die neue Form umgestellt.
- **Lese-PDF**: Impressum beginnt höher (25 statt 52 mm), damit ein längeres Impressum auf die Titelseite passt
  (vorher rutschte der letzte Absatz allein auf eine eigene Seite).
- **Umschlag-Datei im gleichen Aufbau wie die Druckdateien**: `## Vorderseite` / `## Buchrücken` / `## Rückseite`,
  Werte `- name: text`, Erklärungen `> …`. Neu: Endung am Namen statt `:::`-Block – `fuss-druck`, `fuss-bildschirm`,
  `text-ebook`, `auszug-uz` … gilt nur dort. Die alte Form (`# Vorderseite`, `::: nur-druck`) geht weiterhin.
- **Druckdateien**: Erklärungen mit `> ` statt `####` (ruhiger im Editor, der Motor übergeht beides).
  Muster in vorlage/druck/ mit Feld `impressum-logo`; tredition-Muster mit dem Impressumstext von tredition.
- Geprüft: Selbsttest; Leben123 Seite für Seite mit 2.23.0 verglichen – Unterschied nur in der Titelei
  (eine Seite weniger im Lese-PDF, weil das Impressum nicht mehr überläuft); `::: foto` und `#### @FOTO`
  ergeben Pixel für Pixel dasselbe PDF.

## 2.23.0 (Oktober 2026)
- **Rückseite im E-Book**: neue Variable `ebook-rueckseite` (Standard `bild`). Letzte Seite des E-Books ist die
  Rückseite des Covers als Bild – ohne Strichcode; Slogan, Klappentext, Zitate und Fuss stehen als Beschreibung (alt)
  für Vorleseprogramme dabei. `text` = dieselben Texte als Seite «Über dieses Buch», `nein` = wie bisher.
  Gilt für EPUB 3, EPUB 2 und die Leseprobe. EPUBCheck 5.1 und 4.2.6: 0 Fehler in allen drei Varianten.

## 2.22.0 (Oktober 2026)
- **Versatz im Buchblock**: `versatz-vertikal` und `versatz-horizontal` (mm) in der Druckdatei verschieben den ganzen
  Seiteninhalt – für die Korrektur nach dem Probeexemplar (vertikal + = nach oben, horizontal + = nach aussen, je nach
  linker/rechter Seite). Nur der Buchblock; Warnung, wenn der Versatz die Reserve des Beschnitts übersteigt.
  Leer/0 = Buchblock Seite für Seite unverändert. Alle Druck-Muster haben die zwei Felder.

## 2.21.3 (Oktober 2026)
- **EPUB 2 mit Angaben zur Barrierefreiheit**: schema.org-Metadaten (accessMode, accessibilityFeature, -Hazard,
  -Summary, accessModeSufficient) bleiben im EPUB 2 erhalten, als `<meta name="…" content="…"/>` – Ace by DAISY
  meldete sie als fehlend. EPUBCheck 4.2.6 und 5.1: weiterhin 0 Fehler.

## 2.21.2 (Oktober 2026)
- **Impressum je Druckerei**: `{impressum-herstellung}` und `{impressum-kontakt}` im Impressum (Vorlage); Werte in der
  Variablen-Datei (Vorgabe epubli) und in jeder Druckdatei (Abschnitt «Impressum»). Leer = Zeile fällt weg.
  Druckdateien erlauben eigene `impressum-…`-Namen. Muster: epubli mit echtem Text, BoD und tredition mit DEMO-Text.

## 2.21.1 (Oktober 2026)
- **Nur eingebettete Schriften im PDF**: Seiten, Tabellen, Aufzählungszeichen und QR-Codes starteten intern mit
  Helvetica bzw. Times-Roman (nicht eingebettet) – Druckereien wie tredition melden das. Jetzt überall die Buchschrift;
  einzige sichtbare Änderung: die Aufzählungspunkte sind nun in Lora statt Helvetica.
- **Prüfung bei jedem Bau**: Enthält ein PDF eine nicht eingebettete Schrift, erscheint eine WARNUNG mit Datei und Seiten.
- Strichcode aus der ISBN (BoD) ebenfalls mit eingebetteter Schrift.
- Druck-Muster (`vorlage/druck/`) übersichtlich: `##` Abschnitte, nur Werte, unter jedem Wert `#### default: … · optional: …`;
  neu `tredition-a5-hardcover.md` (Buchblock 15,8 x 22 cm).

## 2.21.0 (Oktober 2026)
- **Inhaltsverzeichnis als PDF**: `<datei>_Inhalt.pdf` – die Inhaltsseiten aus dem Lese-PDF (z. B. für XinXii),
  bei `sh build.sh`, `final`, `komplett` und `nur-pdf`.
- **Titelbild in mehreren Grössen**: `…_Cover-vorne_2000px.jpg`, `_1600px.jpg`, `_900px.jpg` (lange Seite) neben
  dem bisherigen `…_Cover-vorne.jpg` – für Shops mit Höchstgrössen. Beides in 00-UEBERSICHT.txt unter «E-Book».

## 2.20.1 (Oktober 2026)
- **`sh build.sh komplett`**: final + Leseprobe + Korrektur in einem Durchgang (Sicherung und Prüfung einmal,
  eine 00-UEBERSICHT.txt am Schluss) – für vor der Bestellung oder Veröffentlichung. `final` bleibt wie bisher.

## 2.20.0 (Oktober 2026)
- **E-Book zusätzlich als EPUB 2** («epub2-light», neues Modul `motor/epub2.py`): mit `ebook-epub2: ja` entsteht
  neben dem EPUB 3 auch `<datei>_EPUB2.epub` – für Shops und Prüfprogramme, die nur EPUB 2 annehmen (z. B. epubli).
  Gleicher Inhalt; content.opf 2.0, XHTML 1.1, Inhaltsverzeichnis über toc.ncx, ohne Barrierefreiheits-Angaben.
  EPUBCheck: 0 Fehler (Leben123 beide Fassungen und Leseprobe).
- Schriften im E-Book als `application/vnd.ms-opentype` statt `font/ttf` – keine CSS-007-Meldung mehr bei älteren Prüfprogrammen.
- 00-UEBERSICHT.txt zeigt das EPUB 2 unter «E-Book».

## 2.19.2 (Oktober 2026)
- **00-UEBERSICHT.txt** in jedem Ausgabeordner (auch `ausgabe-test/<datei>/`), bei jedem Bau neu: welche Datei
  wofür (Druckerei, E-Book, Lesen/Korrektur, Werbung, Selber drucken, Shop-Texte, weitere), oben FINAL oder ENTWURF,
  Art des Baus, Datum, Version und Druckdatei; bei jeder Datei Datum/Uhrzeit sowie Seiten und Masse bzw. Pixel.
  Fehlt etwas, steht der Befehl dazu. Alle Dateien entstehen wie bisher.
- **Hilfe neu gegliedert**: «Start» mit fünf Punkten (Erstes PDF in fünf Minuten, Computer einrichten, Hallo-PDF,
  Dein Buch bauen, Wenn etwas klemmt). Darunter Gruppen (gelbe Titel): Schreiben, Bauen, Drucken und veröffentlichen,
  **Andere Plattformen** (Druck bei KDP/Lulu, E-Book bei XinXii/tolino/KDP/BoD, Selber drucken/Copyshop),
  Sichern und mehrere Computer, Nachschlagen. In `HILFE.md` steuert «# Gruppe» die Gliederung.
- Hilfe ergänzt: alle Variablen der Vorlage auf einen Blick, `nur-ebook`, `sicherung`, neue Meldungen bei «Wenn etwas klemmt».
- Landingpage: Text in zwei Absätzen (Plattformen; Leseprobe, Korrektur, Booklet, Werbebilder), Hinweis auf 00-UEBERSICHT.txt.

## 2.19.1 (Oktober 2026)
- **Einfachere Ausgabeordner**: Ein normaler Bau legt die Druckdateien immer in `ausgabe-normal/` bzw. in den Ordner
  der zweiten Ausgabe – egal ob epubli, BoD oder eine andere Plattform. Die Ordner `BoD-<kurz>/` fallen weg.
- **Testlauf** `sh build.sh final druck=<datei>` baut nur Buchblock und Umschlag nach `ausgabe-test/<datei>/`
  (nicht zu GitHub, nicht in die Sicherung, `sh cleanup.sh ausgaben` löscht ihn mit).
- Hilfe: andere Plattformen (z. B. KDP) über eine kopierte Musterdatei mit Werten aus deren Coverrechner.
- Landingpage-Text: «druckfertiges Buch im gewünschten Format, mit Umschlag und E-Book».

## 2.19.0 (Oktober 2026)
- **Druckangaben in eigenen Dateien** (`druck/`): pro Fassung eine Datei mit allem, was nur den Druck betrifft
  (plattform, format, seite, bindung, projekt, ruecken-…, beschnitt-…, deckel-hardcover, papier, extra-seiten,
  isbn-buch, barcode-…). In der Variablen-Datei `druck-normal: epubli-a5-normal` / `druck-uz: …`. Die Werte gelten
  nur für Buchblock und Umschlag und haben dort Vorrang; Lese-PDF, E-Book, Leseprobe, Korrektur und Mockup bleiben
  beim Grundformat. Ohne `druck`-Zeile ändert sich nichts (Leben123 Seite für Seite gleich geprüft).
- **Testen ohne Umstellen**: `sh build.sh final druck=<datei>` (mit `normal` oder `uz`: nur diese Fassung).
  Der Bau zeigt «Druckangaben: druck/…md» und legt eine Kopie in den Ausgabeordner. `pruefen` meldet fehlende
  Druckdateien, unbekannte Namen und fehlende Barcode-Bilder.
- **Eigenes Seitenmass** `seite: 148 x 210` (mm): Ränder und Schrift vom nächstliegenden Format, Deckel = Seite +
  9 × 18 mm. Weicht das Druckformat vom Grundformat ab: Hinweis «Seitenzahlen im Druck anders als im Lese-PDF».
- **Barcode-Feld** auf der Rückseite: `barcode-position` (links, mitte, rechts), `barcode-groesse` (z. B. 40x20),
  `barcode-bild` (PNG aus bilder/, auf weissem Feld). Alles leer = wie bisher. Warnung, wenn Text ins Feld ragt.
- **Muster** in `vorlage/druck/`: epubli-a5, -taschenbuch, -sachbuch, -a4, -quadrat und bod-a5-hardcover
  (ungetestet). Neue Bücher bekommen sie in `druck/`.
- Meldungen nennen den Coverrechner der gewählten Plattform (epubli oder BoD); Umschlagmasse mit Nachkommastelle.
- Selbsttest: BoD-Druckdateien mit `druck=bod-a5-hardcover normal` (Buchblock 148 × 210 mm, Umschlag 250 mm hoch).

## 2.18.0 (Oktober 2026)
- **Cover-Bilder für E-Book-Shops**: Mit dem E-Book entstehen im Ausgabeordner `…_Cover-vorne.jpg` und
  `…_Cover-hinten.jpg`: Vorder- und Rückseite gerade, randlos, ohne Schatten (lange Seite 2560 Pixel, kurze
  mindestens 1600; bei A5 etwa 300 dpi). Passt für tolino media, neobooks, BoD und KDP (JPG, Hochformat,
  mind. 1600 Pixel breit). Anders als `…_Cover_Vorderseite.jpg` (Druck, mit Beschnitt) genau im Buchformat.
- **Umschlag im E-Book**: Texte aus `::: nur-ebook`; gibt es keine, die des Drucks (`::: nur-druck`). So steht auf
  Titelbild und Cover-Bildern z. B. «Erstausgabe 2027» statt «Stand 2027» (bisher wie im Bildschirm-PDF).
- Selbsttest prüft die beiden Cover-Bilder.

## 2.17.2 (Oktober 2026)
- **Windows**: Bilddateien unter Windows sofort schliessen. Die korrigierte build.py. Neue Hilfsfunktion _bild_laden() (mit bildgroesse()): Sie öffnet jedes Bild mit with, damit die Datei sofort wieder frei ist. Ist die Datei gerade gesperrt, wartet sie kurz 
-
## 2.17.1 (Oktober 2026)
- **Windows**: Meldungen zeigen jetzt Windows-Befehle (`.\build.bat final` statt `sh build.sh final`, ebenso
  setup, neu, update, sicherung, «py motor\…»). Neues Modul `motor/plattform.py`, in allen Skripten eingebunden.
- `neu.sh` / `neu.bat` ohne Titel zeigt unter der Übersicht, wie man eine Geschichte oder Tabelle anlegt.
- `readme.txt` und README beginnen mit «Zum Starten: hilfe.html → Start». Hinweis zum doppelten Ordner
  `pureSATZ-main` beim Entpacken unter Windows (START, Webseite).

## 2.17.0 (Oktober 2026)
- **Werbebilder (Mockup)**: Bei `sh build.sh final` und `nur-pdf final` entstehen aus dem Bildschirm-PDF jeder
  Ausgabe `…_Mockup.jpg` (Vorder- und Rückseite leicht gedreht, mit weichem Schatten, 1600 × 1600 Pixel) und
  `…_Vorderseite.jpg`. Jederzeit neu: `sh build.sh mockup`. Variable `mockup-hintergrund` (Farbverlauf oben, unten).
  Neues Modul `motor/mockup.py`.

## 2.16.2 (Oktober 2026)
- Hilfe: Aufräumen erklärt (was `sh cleanup.sh` löscht und was nie) und im Spickzettel; findet sich über die Suche
  mit «löschen», «entfernen», «delete», «alt», «aufräumen».
- Suche: mehrere Wörter – zuerst Abschnitte mit allen Wörtern, gibt es keinen, genügt eines. «ae/oe/ue» findet
  auch ä/ö/ü (z. B. «aufraeumen»).

## 2.16.1 (Oktober 2026)
- Hilfe: Fusszeile mit Links zu Webseite, GitHub, «Fehler melden» und E-Mail; neuer Abschnitt «pureSATZ im Netz
  (GitHub, Webseite)» unter «Nachschlagen» mit Webseite, GitHub, Download, Issues, Lizenz und Kontakt –
  findet sich auch über die Suche («github», «webseite», «download»).

## 2.16.0 (Oktober 2026)
- **Nummerierte Aufzählung**: Zeilen `1. …`, `2. …` werden eine Aufzählung mit bündigen Nummern in der
  Buchschrift. Der Motor zählt selbst (die erste Zahl ist der Start, Leerzeilen dazwischen unterbrechen nicht).
  Kurze Aufzählungen (bis 6 Punkte) werden nicht über zwei Seiten getrennt.
- **Unterpunkte**: `  - …` oder `  1. …` (2–4 Leerzeichen eingerückt), unter Listen und Aufzählungen.
- Auch in `::: zusammen`, im Kasten der zweiten Ausgabe und im E-Book (`<ol>`, `<ul>`).
- `3\. Mai` am Zeilenanfang = keine Aufzählung (gedruckt «3. Mai»); `pruefen` weist auf einzelne Zeilen wie
  «3. Mai war …» hin. Demo-Kapitel mit Beispiel.
- Bücher ohne `1.`-Zeilen bleiben gleich (geprüft mit Leben123).
- **Webseite** in `docs/` für GitHub Pages (tgsteiger.github.io/pureSATZ): Download, fünf Schritte je System,
  Bilder aus dem Hallo-Buch, Hilfe online. Erneuern: `python3 docs/landingpage.py`. Kontakt: puresatz@gsteiger.ch.

## 2.15.0 (Oktober 2026)
- **Fotos gleich gross** (Variablen, Abschnitt «Fotos», freiwillig): `foto-format: 3:2` schneidet alle Fotos auf
  dasselbe Seitenverhältnis zu (auch 4:3, 16:9, quadrat; pro Foto `ausschnitt: oben/unten/links/rechts`, Standard
  Mitte; Fotos mit `fluss` nicht), `foto-breite: 100` = einheitliche Breite in mm, `foto-anpassen: nein` = am
  Seitenende nie verkleinern. Zuschnitt im Zwischenspeicher `_bildcache/`, das Original bleibt. Auch im E-Book.
- **Prüfung**: Hinweis bei Fotos, die für ihre gedruckte Grösse zu wenig Pixel haben (unter etwa 200 dpi).
- **md-history-behalten: 200**: pro Datei nur die neuesten Stände in `md-history/` (leer = alle, wie bisher).
- Hilfe: neue Abschnitte «Bilder und Fotos» und «Sichern und zurückholen», in START.md der Punkt «Sichern».
  Unter «Nachschlagen» neu «Buchformate» (a5, taschenbuch, sachbuch, a4, quadrat: Seite, Textbreite, Schrift,
  nötige Pixel), direkt aus dem Motor, das Format des Buchs hervorgehoben.
  Demo-Kapitel mit einem Hochformat-Foto (`fotos/beispiel-hoch.jpg`), `fotos/readme.txt` ergänzt.
- Ohne die neuen Variablen bleibt alles wie bisher (geprüft mit Leben123).

## 2.14.1 (Oktober 2026)
- Demo-Kapitel jedes neuen Buchs (und das Hallo-Buch) zeigt eine kleine Tabelle: Abschnitt «Eine Tabelle» mit
  `@#muster`; `tabellen/muster.csv` heisst jetzt «Ein Buch entsteht». Bestehende Bücher bleiben unverändert.
- Kleine Tabellen (bis 12 Zeilen) werden nicht mehr über zwei Seiten getrennt, sondern rücken ganz auf die nächste.

## 2.14.0 (Oktober 2026)
- **Hallo-Buch**: `sh hallo.sh` (Windows: `hallo.bat` doppelklicken) im Ordner pureSATZ legt daneben ein Beispielbuch
  an (ohne Fragen, Werte aus `setup/hallo.txt`), baut es und öffnet das PDF. Gibt es es schon, wird es nur neu gebaut.
  Prüft vorher Python (3.10+) und sagt verständlich, was fehlt. Neu: `setup/hallo.py`.
- **START.md**: Checkliste für den Anfang (Terminal, Python, Computer einrichten, Hallo-Buch, selbst ändern,
  eigenes Buch) und «Wenn etwas nicht klappt». In der Hilfe ganz oben, mit Knopf **Start** neben Linux/Mac und
  Windows; Häkchen zum Anklicken, die der Browser sich merkt. Bücher neben pureSATZ zeigen sie auch.
- Hilfe: Gruppe «Schnellstart» heisst jetzt «Alltag»; Windows-Befehle für `pc-einrichten` und `python3 --version`.

## 2.13.0 (Oktober 2026)
- **Hilfe als Webseite**: `hilfe.html` im Buchordner, eine Datei, ohne Internet. Suche (Taste `/`, Treffer
  markiert, Umlaute egal), Schalter Linux/Mac ↔ Windows für alle Befehle, Kopier-Knopf, hell/dunkel.
  Inhalt: eigene Notizen aus `meine-hilfe.md` (freiwillig, ganz oben), `motor/HILFE.md`, alle Befehle und
  Blöcke, die Variablen des Buchs mit ihren Werten. `sh build.sh hilfe` erzeugt und öffnet sie; bei jeder
  Sicherung wird sie still neu erzeugt. Im Ordner pureSATZ: `python3 motor/hilfe.py`. Neues Modul `motor/hilfe.py`.
- `motor/HILFE.md` ist die eine Anleitung (früher `vorlage/README.md`); das README im Buch ist nur noch ein Hinweis.
- **bildschirm-dunkler: ja** (freiwillig): Bildschirm-PDF mit etwas dunklerer Akzent- und Leisefarbe, damit es
  auch schwarz-weiss gedruckt gut lesbar ist. Druck-PDF und E-Book bleiben gleich.
- `hilfe.html` kommt in die `.gitignore` der Bücher (automatisch beim nächsten Bau).

## 2.12.0 (Oktober 2026)
- **Tabellen** aus `tabellen/*.csv` (Zeile 1 Bezeichnung, Zeile 2 Spaltenüberschriften, dann Werte, optional
  «Quelle: …»; Trenner `;` oder `,`). Im Buch eine Zeile `@#name` (auch `@# name`, `@#name quer`, `@#name hoch`).
  Stil wie das Buch, Zahlen rechtsbündig, Kopfzeile wiederholt sich. Zu breit: umbrechen → kleiner (bis 7.5 pt) →
  quer auf eigener Seite (90° gedreht). E-Book: HTML-Tabelle, seitlich verschiebbar. `sh neu.sh tabelle "Titel"`.
  Prüfung: fehlende Tabelle (mit Vorschlag), Zeilen mit zu vielen Werten. Neues Modul `motor/tabellen.py`.
- **Leseprobe nach Seiten**: `leseprobe-seiten: 14,16,17-20,22` (gedruckte Seitenzahlen; `leseprobe-seiten-uz`
  für die zweite Ausgabe). Ohne Seiten gilt `leseprobe:` (Kapitel) wie bisher; beides leer = die 4 Seiten nach
  dem Inhaltsverzeichnis. Die E-Book-Leseprobe nimmt die Kapitel dieser Seiten.
- Bücher ohne `@#` und mit `leseprobe:` bleiben gleich (geprüft mit Leben123).

## 2.11.0 (Oktober 2026)
- **Geschichten sammeln**: Jede Geschichte kann eine eigene Datei in `geschichten/` sein; im Buch bindet eine
  eigene Zeile `@@name` sie ein (auch in `::: nur-…`-Blöcken). Kopf freiwillig: `stand` (idee · entwurf ·
  ueberarbeiten · fertig, nur für die Übersicht), `stichworte` (ins Stichwortverzeichnis), `quelle`.
- `sh neu.sh "Titel"` / `neu.bat` legt eine Geschichte an, `sh neu.sh` zeigt die Übersicht (`motor/geschichten.py`).
- `sh build.sh geschichten` = Sammel-PDF aller Geschichten (`…_Geschichten.pdf`, Stand im Titel); mit `uz` auch unzensiert.
- Übersicht bei jedem Bau: `geschichten-uebersicht.html` (Fortschritt, sortierbare Tabelle, Filter, Kanban) und
  `geschichten/UEBERSICHT.md`; beide in `.gitignore`.
- Prüfung: `@@` ohne Datei (mit Vorschlag), nicht oder doppelt eingebundene Geschichten; Fehlermeldungen nennen
  die Datei der Geschichte. Offene Stellen, md-history und Stichwort-Vorschläge berücksichtigen die Geschichten.
- Ältere Bücher bekommen `neu.sh`, `neu.bat` und die `.gitignore`-Einträge beim ersten Bau automatisch.
- Ohne Ordner `geschichten/` und ohne `@@` bleibt alles wie bisher (geprüft: PDFs von Leben123 Seite für Seite gleich).

## 2.10.1 (Oktober 2026)
- **Schreibweise pureSATZ** – wie das Vorbild pureRACE (Zeitmess-Software von 1994). Repository
  `tgsteiger/pureSATZ`, Ordner `pureSATZ`; `sh update.sh lokal` sucht `../pureSATZ`. Motor sonst unverändert.

## 2.10.0 (Oktober 2026)
- **Neuer Name: pureSATZ** (vorher «Motor Leeres Buch»). Repository und Ordner heissen `pureSATZ` / `pureSATZ`;
  in den PDF-Eigenschaften steht «pureSATZ <Version>». Die Vorlage für ein neues Buch liegt weiter in `vorlage/`.
- Kopfzeile: Standard ist jetzt `ohne-autor` («Teil · Kapitel»). Mit `kopfzeile: autor` wieder mit Autor.
- `update.sh`: holt den Motor von GitHub (`tgsteiger/pureSATZ`). Neu `sh update.sh lokal` = aus dem Ordner
  `../pureSATZ` neben dem Buch, ohne GitHub. Eigene Quelle: Umgebungsvariable `PURESATZ_QUELLE`
  (GitHub-Adresse oder Ordner).

## 2.9.4 (Oktober 2026)
- **Kopfzeile wählbar** mit der Variable `kopfzeile` (Abschnitt «Weiteres»): `autor` = «Autor · Teil · Kapitel»,
  `ohne-autor` = «Teil · Kapitel», `wechselnd` = links der Teil, rechts das Kapitel
  (klassisch, gut bei längeren Kapiteln).
- Tipp: Titel je Fassung über eine Variable, z. B. `# {zeitstrahl-titel}` vor den Blöcken `::: zeitstrahl-normal` /
  `::: zeitstrahl-uz` mit `zeitstrahl-titel-normal` und `zeitstrahl-titel-uz` (Werte nicht leer lassen).

## 2.9.3 (Oktober 2026)
- **Rückseite für epubli**: epubli setzt den ISBN-Strichcode unten links auf den Umschlag. Fusszeilen stehen
  darum im Druck rechtsbündig unten rechts, der Lotus in der Seitenmitte (sichtbare Unterkante
  mittig zwischen den Fusszeilen, berechnet aus Schrift und Bild, leerer Bildrand wird herausgerechnet); links unten bleiben ca. 60 x 35 mm frei. Warnung, wenn
  der Rückseitentext bis in diesen Bereich reicht. BoD (eigener Strichcode rechts) unverändert.

## 2.9.2 (Oktober 2026)
- **Keine Transparenzen mehr im Umschlag**: Der Stempel (z. B. «UNZENSIERT») wird deckend gezeichnet, die Farbe
  ist auf dem Papierton vorgemischt. Sieht gleich aus, epubli meldet keine Transparenz mehr. Bilder im Buchblock
  waren schon vorher ohne Transparenz (`_druckbilder/`).

## 2.9.1 (Oktober 2026)
- Leeres Buch aufgeräumt: `setup/` (setup.sh, setup.bat, setup.py), `import/` (import-text.*),
  `pc-einrichten/` (linux-, mac-, win-einrichten). Aufrufe im Ordner Leeres-Buch:
  `sh setup/setup.sh`, `sh setup/setup.sh motor ../Buch`, `sh import/import-text.sh …`, `bash pc-einrichten/linux-einrichten.sh`
  (Windows: `setup\setup.bat`, `import\import-text.bat`, `pc-einrichten\win-einrichten.bat`).
- `setup.sh motor ../Buch` findet den Buchordner auch, wenn man nicht im Ordner Leeres-Buch steht. Motor selbst unverändert.

## 2.9.0 (Oktober 2026)
- **Motor-Update aus dem Buch heraus**: `sh update.sh` / `update.bat` (`motor/update.py`) fragt GitHub nach dem
  neuesten Motor, zeigt die Neuerungen aus dem CHANGELOG und setzt ihn auf Wunsch ein. Ein lokaler Ordner
  Leeres-Buch ist dafür nicht nötig. `sh update.sh pruefen` = nur nachsehen, `sh update.sh ja` = ohne Rückfrage.
  Geholt wird mit git und der eigenen GitHub-Anmeldung (geht auch beim privaten Repository mit Einladung).
  Ersetzt wird nur `motor/`, der alte bleibt als `motor-alt-…`; fehlende Hilfsdateien werden ergänzt.
- `setup.sh` legt `update.sh` und `update.bat` im neuen Buch an; `setup.sh motor ../Buch` ergänzt sie in älteren Büchern.
- `linux-einrichten.sh` und `win-einrichten.bat` im Leeren Buch (wie `mac-einrichten.sh`): prüfen und installieren
  Python, venv und git (apt bzw. winget), GitHub **freiwillig** (Name/Mail, Anmeldung mit `gh`, Bücher holen),
  auf Wunsch neues Buch anlegen. Ohne GitHub geht alles ausser `sync` und `update`.

## 2.8.0 – Nachtrag Mac (Oktober 2026)
- `mac-einrichten.sh` im Leeren Buch: richtet einen Mac ein – Intel und Apple-Chip, **ohne Homebrew**
  (läuft auf Intel-Macs nicht mehr) und ohne `gh`: Apple-Werkzeuge, Python von python.org, git-Name/Mail,
  Schlüsselbund, GitHub-Zugang prüfen (mit Token-Anleitung), Bücher holen und einmal bauen. Motor unverändert.
- `INSTALLATION.md`, `GITHUB.md`, `ERSTES-BUCH.md`: Mac-Teil neu, mit GitHub-Token (classic, nur «repo») und häufigen Fehlern.

## 2.8.0 (Oktober 2026)
- **Buch auf mehreren Computern**: `sh sync.sh` / `sync.bat` (`motor/sync.py`) gleicht das Buch über ein privates
  GitHub-Repository ab: eigene Änderungen festhalten (Datum, Computername) → holen → hochladen. Bei Änderungen
  an derselben Stelle auf zwei Computern bleiben beide Versionen erhalten (`…_KONFLIKT-anderer-Computer_….md`).
- `setup.sh` legt im Buch `.gitignore` (ohne .venv, Ausgaben, Zwischenspeicher, md-history), `sync.sh`, `sync.bat` an.

## 2.7.2 (Oktober 2026)
- Windows: Wenn zwei parallele Läufe dasselbe Zwischenbild (`_druckbilder`, `_bildcache`) gleichzeitig anlegen,
  bricht der zweite nicht mehr ab (PermissionError), sondern nimmt die fertige Datei des ersten.

## 2.7.1 (Oktober 2026)
- GitHub-bereit: `.gitignore`, `.gitattributes` (Zeilenenden; .bat mit CRLF), `GITHUB.md` (Anleitung),
  Selbsttest `test/selbsttest.py` und GitHub Actions (`.github/workflows/selbsttest.yml`) (Linux, Mac, Windows; EPUBCheck).
- Windows: Zwischen-PDFs von Leseprobe und Korrektur werden nicht mehr offen gehalten (Löschen schlug fehl).

## 2.7.0 (Oktober 2026)
- **Linux, Mac und Windows**: poppler (pdftoppm, pdftotext) ist nicht mehr nötig. Cover-JPG, E-Book-Titelbild und
  die Zeilen der Korrekturfassung macht `pypdfium2` (Python-Paket, `motor/pdfwerkzeug.py`); fehlt es in einer
  älteren .venv, wird wie bisher poppler benutzt. Layout unverändert (PDFs Seite für Seite gleich, JPGs gleich gross, 400 dpi).
- Windows: `build.bat`, `cleanup.bat`, `sicherung.bat` im Buch, `setup.bat` im Leeren Buch; Ausgaben in UTF-8.

## 2.6.0 (Oktober 2026)
- `sh build.sh schnell`: nur die Lese-PDFs (alle Ausgaben parallel), ein Durchgang ohne Seitenausgleich,
  ohne Booklet, Statistik und Prüfung – etwa halb so lang wie `nur-pdf` (Leben123: ca. 8 statt 16 s).
- `sh build.sh final` prüft den **Kontrast** der Textfarben aus `# LAYOUT` auf Seite, Papier und Kasten
  (WCAG, mind. 4,5:1) und schlägt bei Bedarf eine dunklere Farbe vor; ändert nichts.
- `kontrast()` und `lesbare_farbe()` in `build.py` (auch fürs E-Book).
- Sicherung: Editor-Sicherungen (`*.backup`, `*~`) kommen nicht ins ZIP.

## 2.5.3 (Oktober 2026)
- E-Book: Akzentfarbe für Text (Links, Teil-Nummern, Jahreszahlen, Kasten-Kopf) automatisch so weit abgedunkelt,
  dass der Kontrast 4,5:1 erreicht (WCAG AA), z. B. #B8873B → #8C672D. Druck und PDF bleiben unverändert.
  Eigene Farbe: `farbe-akzent-ebook`.

## 2.5.2 (Oktober 2026)
- Neue Variablen unter `# TECHNIK`: `beschnitt-hardcover` (11 mm Einschlag laut Coverrechner),
  `beschnitt-softcover` (3), `beschnitt-buchblock` (3), `deckel-hardcover` (z. B. 157x228; leer = laut Format),
  `papier` (erscheint in der Ausgabe nach `final` und in `shop-angaben.txt`). Leer = bisherige Werte.
- Klarere Ausgabe nach `final`: Buchblock-Beschnitt «nur Innenseiten»; Hardcover-Umschlag mit Deckel, Rücken
  und Einschlag – zum direkten Vergleich mit dem Coverrechner (Gesamtbreite × Gesamthöhe).

## 2.5.1 (Oktober 2026)
- **Leseprobe auch als E-Book** (`…_Leseprobe.epub`, dieselben Kapitel, eigene Kennung) und **QR-Code** auf
  der Schlussseite: führt zu `shop-link:` (neu unter `## Shop`), sonst zur Website; im E-Book als Link.
- **Sicherung**: `sicherung-behalten: 10` behält pro Ziel nur die neuesten ZIPs dieses Buchs (leer = alle);
  Pfade mit Leerschlägen, Anführungszeichen erlaubt.
- Korrekturfassung: Kopfzeile «Seite n / N». Shop-Angaben mit Shop-Link.

## 2.5.0 (Oktober 2026)
- **Leseprobe**: `sh build.sh leseprobe` – Umschlag, Titelei, die ersten Kapitel (`leseprobe: 3` oder
  Kapiteltitel), Schlussseite (`leseprobe-text:`) und Rückseite → `<datei>_Leseprobe.pdf`.
- **Korrekturfassung**: `sh build.sh korrektur [final]` – jede Seite in Originalgrösse auf A4, Zeilennummern
  pro Seite, Notizlinien rechts → `<datei>_Korrektur.pdf` (`motor/fassungen.py`).
- **Sicherung**: `sh sicherung.sh [lokal] [cloud]` → `<name>_JJJJMMTTHHMMSS.zip` an die Ziele
  `sicherung-lokal` / `sicherung-cloud`; ohne .venv, Zwischenspeicher und Ausgaben, aber mit dem
  Bildschirm-PDF jeder Ausgabe (`motor/sicherung.py`).
- **E-Book barrierefrei**: `alt:` im Foto-Block (sonst Bildtext), Porträt mit Beschreibung, Sprache im
  Paket, Angaben nach EPUB Accessibility 1.1 (accessMode, accessibilityFeature, -Hazard, -Summary;
  eigene Zusammenfassung mit `ebook-barrierefreiheit:`); Hinweis bei Fotos ohne Beschreibung.
- **readme4ki.txt**: kurze Regeln für eine andere KI (von `setup.sh` angelegt).
- `build.py`: Zieldatei über `BUCH_ZIEL` wählbar; `cleanup.sh` entfernt liegengebliebene Zwischen-PDFs.
- Korrektur E-Book: dasselbe Foto zweimal im Buch ergab einen doppelten Eintrag im Paket (EPUBCheck-Fehler).

## 2.4.0 (Oktober 2026)
- **Bildnachweis**: Feld `quelle:` im Foto-Block; im Anhang entsteht die Seite «Bildnachweis» mit
  Seitenzahlen (an `@BILDNACHWEIS`, sonst vor dem Stichwortverzeichnis); auch im E-Book.
- **Shop-Angaben**: Abschnitt `## Shop` (shop-beschreibung, shop-schlagwoerter, shop-kategorie,
  preis-buch, preis-ebook); nach `final` als `shop-angaben.txt` im Ausgabeordner, Beschreibung und
  Schlagwörter auch im E-Book.
- **Statistik** nach jedem Bau: Wörter, Lesezeit, Wörter und Seiten pro Teil.
- `CHECKLISTE.md` im Buchordner (von `setup.sh` angelegt), `ERSTES-BUCH.md` im Leeren Buch.

## 2.3.0 (Oktober 2026)
- Booklets zum Selberdrucken entstehen automatisch beim Bauen (je ca. 1–2 Sekunden, parallel):
  im Entwurf und bei `nur-pdf` aus dem Bildschirm-PDF (`<datei>_booklet.pdf`), bei `sh build.sh final`
  als **Probedruck** aus der Druckfassung: Vorderseite + Buchblock + Rückseite, ohne Beschnittrand,
  genau wie das bestellte Buch (`<kurz>_Probedruck_booklet.pdf`).
- `booklet.py`: mehrere PDFs nacheinander und `--beschnitt MM`.
- **Seitenbilanz** nach `sh build.sh final`: Seiten mit Inhalt, Füllseiten (und warum), leere Seiten
  im Inhalt und ein Tipp, wenn eine Seite weniger eine Füllseite spart – Hilfe zum Kürzen vor der Bestellung.

## 2.2.2 (Oktober 2026)
- `cleanup.sh` (motor/aufraeumen.py): entfernt Zwischenspeicher, `_backup/`, alte Motoren und
  `stichworte-vorschlag.txt` – zeigt zuerst die Liste und fragt. `md-history/` bleibt immer.
  `sh cleanup.sh ausgaben` löscht zusätzlich die Ausgabeordner.

## 2.2.1 (Oktober 2026)
- Stichwörter wieder ganz einfach als Text: `stichworte-<name>.txt` (z. B. `stichworte-Leben123.txt`),
  sonst `stichworte.txt`; hat Vorrang vor dem Abschnitt `# STICHWORTE`. `setup.sh` legt sie mit wenig
  Demo-Inhalt an; die Sicherung nach `md-history/` umfasst sie.

## 2.2.0 (Oktober 2026)
- **Drei MD-Dateien** mit gleichen Regeln: `<name>-variablen.md`, `<name>-buch.md`, `<name>-umschlag.md`.
  (Eine Buch-MD mit `# BUCHSTART` oder `---`-Block geht weiterhin.)
- Stichwörter in der Variablen-Datei unter `# STICHWORTE` (statt `stichworte.txt`, das weiter gelesen wird).
- Layout in der Variablen-Datei unter `# LAYOUT`: `farbe-…`, `schrift-text`, `schrift-titel`,
  `schriftgroesse`, `zeilenabstand`, `blocksatz` (Vorrang vor `layout.py`).
- Sicherung nach `md-history/` umfasst alle drei Dateien.
- `setup.sh` / `setup.py` ersetzt `make-projekt.sh` / `.py`.

## 2.1.1 (Oktober 2026)
- Motor-Module haben Vorrang vor alten Skripten im Buchordner; `layout.py` des Buchs gilt weiterhin.
- Neue Variable `ebook-id` (je Ausgabe): feste E-Book-Kennung, z. B. nach dem Umbenennen eines Buchs.

## 2.1.0 (Oktober 2026)
- Übersichtlich im MD-Editor: Einstellungen oben unter `# VARIABLEN` / `# TECHNIK` (beliebig mit `##`, `###`
  gegliedert, Sätze = Erklärungen), Variablen als Liste `- name: wert`; das Buch beginnt nach `# BUCHSTART`.
  Die alte Form mit `---` funktioniert weiterhin.
- Befehle als Überschrift: `## @TITEL`, `## @IMPRESSUM`, `### @WIDMUNG`, `## @KERNSATZ …` erscheinen in der
  Navigation des Editors und wirken wie ohne `#`.
- Umschlag-MD ebenfalls als Liste `- schlüssel: text`, Erklärungen erlaubt, unbekannte Schlüssel werden gemeldet.

## 2.0.0 (Oktober 2026)
- **Alles Lesbare steht in der MD.** `einstellungen.py` entfällt: Angaben stehen oben in der Buch-MD
  als Variablen (`titel: …`), im Text mit `{titel}` einsetzbar; `name-normal` / `name-uz` je Ausgabe.
- Neue **Umschlag-MD** (`<buch>-umschlag.md`): Vorderseite, Buchrücken, Rückseite als `schlüssel: text`.
- Titelei in der MD: `@TITEL`, `@IMPRESSUM` (mit `::: widmung`), `@KERNSATZ`, `@INHALTSVERZEICHNIS`;
  `{isbn}` wird je nach Ausgabe gesetzt (Buch / E-Book / leer = «folgt»).
- `# Titel` ohne `|` = Kapitel oberster Ebene (Anhang, Zeitstrahl, Über den Autor).
- Neue Befehle: `@PORTRAIT`, `@QR`, `@QR-PAAR`, `@ZITAT`, `@UNTEN`, `@UMBRUCH-RECHTS`, `@ABSTAND`,
  `@ZIER` / `@ZIER-UNTEN` / `@ZIER-TRENNER` (`@LOTUS…` geht weiter), Block `::: zusammen`.
- Einheitliche Block-Endungen: `-normal`, `-uz` (`-dc`), `-bildschirm`, `-druck`, `-ebook`, `-buch`, `-privatdruck`.
- **Formate** `a5`, `taschenbuch`, `sachbuch`, `a4`, `quadrat` (Masse laut epubli) und **Bindung**
  `hardcover`, `softcover`, `beide`; Ränder, Schrift und Umschlag passen sich an.
- Verzierung frei wählbar: Variable `zier:` / `zier-hell:`.
- `manuskript.py`: gemeinsamer Leser für PDF, Druck und E-Book; Prüfung vor dem Bau
  (unbekannte Variablen/Befehle, fehlende Fotos, offene Blöcke) mit Zeilennummern.
- `bauen.py`: Optionen `final`, `nur-pdf`, `nur-druck`, `nur-ebook`, `pruefen`, `sicherung`;
  alle Schritte laufen parallel. E-Book-Titelbild ohne ganzes PDF (viel schneller).
- Ein Startskript `make-projekt.sh` statt `start-buch`, `make-buch-plattform`, `make-technische-plattform`.
- `::: seite` (Motor 1.x) entfällt: dafür `# Über den Autor` mit `@PORTRAIT` und `@QR-PAAR`.

## 1.0.1 (Oktober 2026)
- Neue Endung `-normal` (z. B. `::: nur-normal`) für die normale Ausgabe; `-v2` bleibt als alter Name.
- Neue Familie «offen»: `::: offen`, `offen-uz`, `offen-normal` (Buchtext, noch nicht entschieden:
  im Entwurf gelb, im Druck normaler Text) und `offen-notiz` (Notiz an dich, nie gedruckt; ersetzt `platzhalter`).
- Liste der offenen Stellen mit Zeilennummern nach jedem Bau.
- `sh build-pdfs.sh entwurf`: Bildschirm-PDFs als Entwurf.
- Neue Layout-Farben `offen` und `offen_linie`.

## 1.0.0 (Oktober 2026)
- Erste Fassung, entstanden aus dem Satzsystem von «Leben 1.0, 2.0, 3.0».
- Alle Buchangaben in `einstellungen.py`, das Aussehen in `layout.py`.
- Zwei Ausgaben aus einem Manuskript: A (offiziell) und B (z. B. Director's Cut).
- Blöcke: `uz`/`dc`, `nur-…`, `mitte`, `foto`, `platzhalter`, `zeitstrahl`, `seite` (mit `portrait:` und `qr:`).
- Stichwortverzeichnis mit Varianten, `=`-Einträgen und Verweisen (`->`).
- Druckdateien für epubli/BoD (Softcover, Hardcover), E-Book (EPUB 3), Booklets.
