# pureSATZ – Änderungen

pureSATZ ist das Satzsystem (der «Motor»), das aus Markdown-Dateien Buch, Umschlag und E-Book macht.
Der Name erinnert an pureRACE, die Zeitmess-Software des Autors von 1994. Bis 2.9.4 hiess es «Motor Leeres Buch».

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
