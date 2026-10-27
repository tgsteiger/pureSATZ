# VARIABLEN
> Hier stehen alle Angaben zum Buch. Jeder Wert steht als «{name}: wert»; im Buch und im Umschlag erscheint er mit demselben Namen {name}, z. B. «© {jahr} {autor}». So findet die Suche nach {name} beide Stellen. name-normal / name-uz: es gilt automatisch der Wert der Ausgabe, die gebaut wird. Eine Zeile, in der eine Variable leer ist, fällt im Buch weg. Zeilen mit «>» und Überschriften sind nur Erklärungen.

## Buch
{titel}: @@TITEL@@
{untertitel}: @@UNTERTITEL@@
{titel-zusatz-normal}:
{titel-zusatz-uz}: @@ZWEITNAME@@
{autor}: @@AUTOR@@
{website}: @@WEBSITE@@
{ort}: @@ORT@@
{jahr}: @@JAHR@@
{auflage}: 1. Auflage @@JAHR@@
{stand}: @@JAHR@@
{format}: @@FORMAT@@
> {format}: Grundformat für Lese-PDF, E-Book, Leseprobe, Korrektur und Druck: a5 | taschenbuch | sachbuch | a4 | quadrat oder Masse in mm, z. B. 150 x 215. Eine Plattform-Datei braucht {format} nur, wenn ihr Druckformat abweicht.

## Zwei Ausgaben
{zweite-ausgabe}: @@ZWEITE@@
{ausgabe-name-normal}: Normale Ausgabe
{ausgabe-name-uz}: @@ZWEITNAME@@
{stempel-uz}: @@ZWEITLABEL@@
{kasten-hinweis}: darf übersprungen werden
> {zweite-ausgabe}: zweite Ausgabe, z. B. Director's Cut oder Unzensiert: ja | nein

## Impressum
{impressum-rechte}: Das Werk, einschliesslich seiner Teile, ist urheberrechtlich geschützt. Jede Verwertung ist ohne Zustimmung des Autors unzulässig. Zu erreichen unter: @@AUTOR@@, @@ADRESSE@@.
{impressum-hinweis}:
{impressum-kontakt}:
{impressum-satz1}: Gesetzt mit pureSATZ · github.com/tgsteiger/pureSATZ
{impressum-satz2}:
> Gilt für alle Ausgaben. Steht in der Buch-MD unter «## @IMPRESSUM» nichts, setzt der Motor das Impressum selbst zusammen: © {jahr} {autor} · {website} · {impressum-herstellung} · {impressum-satz1} · {impressum-satz2} · {impressum-rechte} · {impressum-hinweis} · {impressum-kontakt} · {auflage} · ISBN {isbn}. Leere Zeilen fallen weg.
> Was nur für eine Ausgabe gilt (Herstellung, Logo, eigene Kontaktzeile, ISBN, Preis), steht unten bei der Ausgabe und ersetzt dort die Zeile von hier.
> {impressum-hinweis}: eigener Absatz vor der Kontaktadresse, z. B. «… ersetzt keine medizinische Beratung» (leer = fällt weg).
> {impressum-satz1}, {impressum-satz2}: zwei freie Zeilen direkt unter der Herstellung, z. B. womit gesetzt wurde oder wer begleitet hat (leer = Zeile fällt weg).

## Ausgabe: PDF
> Lese-PDF, Leseprobe, Korrektur und Booklet zum Selberdrucken – ohne Herstellung, Logo und ISBN.

## Ausgabe: Druck normal
{druck-datei}: epubli-@@FORMAT@@
{isbn}:
{preis}:
{impressum-herstellung}: Herstellung: epubli – ein Service der neopubli GmbH, Köpenicker Strasse 154a, 10997 Berlin
{impressum-kontakt}: Kontaktadresse nach EU-Produktsicherheitsverordnung: produktsicherheit@epubli.com
{impressum-logo}:
> {druck-datei}: Plattform-Datei in druck/ (Name ohne .md) mit der Technik: Bindung, Rücken, Beschnitt, Strichcode. Muster: epubli-a5, epubli-taschenbuch, bod-a5-hardcover, tredition-a5-hardcover … Testen ohne Umstellen: sh build.sh final druck=bod-a5-hardcover
> {isbn}: von der Plattform; leer = keine ISBN-Zeile
> {impressum-herstellung}, {impressum-kontakt}: Angaben der Plattform (hier: epubli)
> {impressum-logo}: Logo der Plattform über dem Impressum, 1,5 × Schrifthöhe, PNG aus bilder/

## Ausgabe: Druck zweite Ausgabe
{druck-datei}: epubli-@@FORMAT@@
{isbn}:
{impressum-herstellung}: Privatdruck · nicht im Handel erhältlich · Herstellung: epubli – ein Service der neopubli GmbH, Köpenicker Strasse 154a, 10997 Berlin
{impressum-kontakt}: Kontaktadresse nach EU-Produktsicherheitsverordnung: produktsicherheit@epubli.com
> Gedrucktes Buch der zweiten Ausgabe (@@ZWEITNAME@@), hier als Privatdruck ohne ISBN. Ohne zweite Ausgabe wird dieser Abschnitt nicht gebraucht.

## Ausgabe: E-Book
{isbn}:
{preis}:
{impressum-herstellung}:
> Eigene ISBN, nicht die des gedruckten Buchs. {impressum-herstellung}: z. B. die Distribution der Plattform

## Ausgabe: E-Book zweite Ausgabe
{erstellen}: ja
> {erstellen}: ja = E-Book der zweiten Ausgabe bauen · nein = keines

## E-Book
{ebook-epub2}: nein
{ebook-rueckseite}: bild
> {ebook-epub2}: zusätzlich <datei>_EPUB2.epub für Shops, die nur EPUB 2 annehmen (z. B. epubli): ja | nein
> {ebook-rueckseite}: letzte Seite des E-Books (und der Leseprobe): bild = Rückseite des Covers als Bild (ohne Strichcode, Texte als Beschreibung für Vorleseprogramme) · text = dieselben Texte als Seite «Über dieses Buch» · nein = keine

## Shop
{shop-beschreibung}: Worum geht es in diesem Buch? Zwei bis vier Sätze, die neugierig machen.
{shop-schlagwoerter}: Stichwort 1, Stichwort 2, Stichwort 3
{shop-kategorie}: z. B. Biografien & Erinnerungen
{shop-link}:
> Angaben für epubli, tolino und KDP. Nach «sh build.sh final» stehen sie zum Kopieren in shop-angaben.txt (im Ausgabeordner), mit ISBN und Preis der Ausgaben oben. Beschreibung und Schlagwörter gehen auch ins E-Book.
> {shop-link}: Adresse des Shops (für den QR-Code der Leseprobe)

### Leseprobe
{leseprobe-seiten}:
{leseprobe-seiten-uz}:
{leseprobe}: 3
> oder einzelne Seiten angeben: 17,18-22, 74, 88-92, 95
{leseprobe-text}: Das ganze Buch «{titel}» von {autor}<br/>ISBN {isbn}<br/>{website}
> «sh build.sh leseprobe» macht eine Leseprobe: Umschlag, Titelei bis zum Inhaltsverzeichnis, dann die gewählten Seiten, Schlussseite, Rückseite. Auch als E-Book (…_Leseprobe.epub).
> {leseprobe-seiten}: gedruckte Seitenzahlen, z. B. 14,16,17-20,22 ({leseprobe-seiten-uz}: eigene für die zweite Ausgabe)
> {leseprobe}: Anzahl Kapitel (eine Zahl), Titel des letzten Kapitels oder Seiten (mit Komma oder Strich, z. B. 17,18-22). Beides leer = die 4 Seiten nach dem Inhaltsverzeichnis. Einmalig andere Seiten: sh build.sh leseprobe uz 18,20,23
> {leseprobe-text}: Text der Schlussseite. Variablen erlaubt, <br/> = neue Zeile, eine Zeile mit leerer Variable fällt weg. Der QR-Code führt zu {shop-link} (sonst zur Website).

# TECHNIK

## Dateien und Ordner
{kurz-normal}: @@KUERZEL@@
{kurz-uz}: @@KUERZEL@@-@@ZWEITKURZ@@
{datei-normal}: @@NAME@@
{datei-uz}: @@NAME@@_@@ZWEITDATEI@@
{ordner-normal}: ausgabe-normal
{ordner-uz}: ausgabe-@@ZWEITORDNER@@

## Fotos
{foto-format}:
{foto-breite}:
{foto-anpassen}: ja
> Fotos liegen in fotos/ (JPG), Porträt, Verzierung und Teil-Bilder in bilder/ (PNG). Ohne Angaben: jedes Foto so breit wie der Text, höchstens 75 mm hoch, am Seitenende etwas kleiner, damit keine Lücke entsteht. Alle drei zusammen = alle Fotos genau gleich gross.
> {foto-format}: alle Fotos auf dasselbe Seitenverhältnis zuschneiden, z. B. 3:2, 4:3, 16:9 oder quadrat (pro Foto «ausschnitt: oben / unten / links / rechts», Standard Mitte; Fotos mit «fluss» bleiben ungeschnitten)
> {foto-breite}: einheitliche Breite in mm (ein «breite:» im Foto geht vor)
> {foto-anpassen}: nein = nie verkleinern, alle Fotos immer gleich gross

## Weiteres
{stichworte}: ja
{trennstellen}: Welt|anschauung, Gedanken|karussell
{zier}:
{zier-hell}:
{kopfzeile}: ohne-autor
{bildschirm-dunkler}: nein
{mockup-hintergrund}: #E9EEF4, #C9D3DF
> {stichworte}: Stichwortverzeichnis aus stichworte-<name>.txt: ja | nein
> {trennstellen}: | = hier darf ein langes Wort getrennt werden
> {zier}: eigenes Bild der Verzierung im Ordner bilder/, leer = Standard
> {kopfzeile}: ohne-autor (Teil · Kapitel, Standard) | autor (Autor · Teil · Kapitel) | wechselnd (links Teil, rechts Kapitel)
> {bildschirm-dunkler}: ja = feine Farben nur im Bildschirm-PDF etwas dunkler (für Schwarz-weiss-Ausdrucke)
> {mockup-hintergrund}: Farbverlauf (oben, unten) des Werbebilds …_Mockup.jpg (entsteht bei «final» und mit «sh build.sh mockup»)

## Sicherung
{sicherung-lokal}: ../Sicherungen
{sicherung-cloud}:
{sicherung-behalten}: 10
{md-history-behalten}: 200
> «sh sicherung.sh» sichert das ganze Buch als ZIP (Name mit Datum und Uhrzeit, ohne Zwischenspeicher; von den Ausgaben nur die Bildschirm-PDFs). «sh sicherung.sh lokal» oder «cloud» = nur dorthin, ohne Angabe = an beide. Pfade relativ zum Buchordner oder mit ~ bzw. /.
> {sicherung-behalten}: nur die neuesten ZIPs behalten (leer = alle)
> {md-history-behalten}: bei jedem Bau kommen die MD-Dateien mit Datum und Uhrzeit nach md-history/; pro Datei nur die neuesten Stände behalten (leer = alle)


# LAYOUT
> Aussehen des Buchs. Leer lassen = Vorgabe des Motors.

## Farben
{farbschema}: 1
> {farbschema}: 1 = Standard · 2 = dunkler für den Druck · weitere Schemas unten möglich (z. B. «### Farbschema 3: …»)
> Schema 1 gilt immer als Grundlage, das gewählte Schema ersetzt nur die Werte, die darin stehen. Gilt für alle Ausgaben.
> Farben als #RRGGBB.

### Farbschema 1: Standard
{farbe-text}: #2E2A26
{farbe-leise}: #6E655C
{farbe-haupt}: #1E428A
{farbe-akzent}: #B8873B
{farbe-papier}: #FBF6EC
{farbe-kasten}: #EEF2F9
{farbe-stempel}: #A8322A
> {farbe-text}: Fliesstext · {farbe-leise}: Kopfzeile, Seitenzahl, Bildtexte · {farbe-haupt}: Titel, Linien · {farbe-akzent}: Gold (Teil-Nummern, Jahre)

### Farbschema 2: dunkler für den Druck
{farbe-text}: #1A1714
{farbe-leise}: #4E4741
{farbe-akzent}: #8C672D
> Falls kleine Schrift im Druck unscharf oder zu hell wirkt. {farbe-text} ganz schwarz wäre #000000.

### Farbschema 3: deine eigenen Farben
> Hier kannst du deine eigenen Farben angeben. Viel Spass.

## Schrift
{schrift-text}: Lora
{schrift-titel}: Poppins
{schriftgroesse}:
{zeilenabstand}:
{inhalt-dichte}: 1
{blocksatz}: ja
> {schrift-text}, {schrift-titel}: Dateien im Ordner fonts/ oder motor/fonts/, z. B. Lora-Regular.ttf, Lora-Bold.ttf, Lora-Italic.ttf, Lora-BoldItalic.ttf
> {schriftgroesse}, {zeilenabstand}: in Punkt; leer = passend zum Format
> {inhalt-dichte}: Zeilenabstand im Inhaltsverzeichnis, 1 = normal, 0.92 = etwas enger (passt z. B. auf eine Seite weniger)
