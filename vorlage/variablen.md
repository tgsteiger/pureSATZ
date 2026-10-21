# VARIABLEN
Hier stehen alle Angaben zum Buch. Im Text und im Umschlag mit dem Namen in geschweiften Klammern verwenden, z. B. «© {jahr} {autor}». name-normal / name-uz: es gilt automatisch der Wert der Ausgabe, die gebaut wird. Eine Zeile, in der eine Variable leer ist, fällt im Buch weg. Überschriften und Sätze wie dieser sind nur Erklärungen.

## Buch
- titel: @@TITEL@@
- untertitel: @@UNTERTITEL@@
- autor: @@AUTOR@@
- website: @@WEBSITE@@
- ort: @@ORT@@
- jahr: @@JAHR@@
- auflage: 1. Auflage @@JAHR@@
- stand: @@JAHR@@
- verlag: Selbstverlag: @@AUTOR@@, @@ADRESSE@@

## Zwei Ausgaben
Zweite Ausgabe z. B. Director's Cut oder Unzensiert: ja / nein.
- zweite-ausgabe: @@ZWEITE@@
- ausgabe-name-normal: Normale Ausgabe
- ausgabe-name-uz: @@ZWEITNAME@@
- stempel-uz: @@ZWEITLABEL@@
- kasten-hinweis: darf übersprungen werden

## ISBN
Von epubli (Buch) bzw. eigene fürs E-Book. Leer = im Buch steht «ISBN folgt».
- isbn-buch:
- isbn-ebook:

## Shop
Angaben für epubli, tolino und KDP. Nach «sh build.sh final» stehen sie zum Kopieren in shop-angaben.txt (im Ausgabeordner). Beschreibung und Schlagwörter gehen auch ins E-Book. shop-link: Adresse des Shops (für den QR-Code der Leseprobe).
- shop-beschreibung: Worum geht es in diesem Buch? Zwei bis vier Sätze, die neugierig machen.
- shop-schlagwoerter: Stichwort 1, Stichwort 2, Stichwort 3
- shop-kategorie: z. B. Biografien & Erinnerungen
- preis-buch:
- preis-ebook:
- shop-link:

### Leseprobe
«sh build.sh leseprobe» macht eine Leseprobe: Umschlag, Titelei bis zum Inhaltsverzeichnis, dann die gewählten Seiten, Schlussseite, Rückseite. leseprobe-seiten: gedruckte Seitenzahlen, z. B. 14,16,17-20,22 (leseprobe-seiten-uz: eigene für die zweite Ausgabe). Sonst leseprobe: Anzahl Kapitel oder Titel des letzten Kapitels. Beides leer = die 4 Seiten nach dem Inhaltsverzeichnis. Text der Schlussseite: Variablen erlaubt, <br/> = neue Zeile, eine Zeile mit leerer Variable fällt weg. Der QR-Code führt zu «shop-link» (sonst zur Website). Auch als E-Book (…_Leseprobe.epub).
- leseprobe-seiten:
- leseprobe-seiten-uz:
- leseprobe:
- leseprobe-text: Das ganze Buch «{titel}» von {autor}<br/>ISBN {isbn}<br/>{website}

# TECHNIK

## Format und Druck bei epubli
Format: a5, taschenbuch, sachbuch, a4, quadrat. Bindung: hardcover, softcover, beide. Projekt: veroeffentlichen (mit ISBN) oder privatdruck. Andere Werte nur für die zweite Ausgabe gehen auch, z. B. «format-uz».
- format: @@FORMAT@@
- bindung: @@BINDUNG@@
- projekt-normal: veroeffentlichen
- projekt-uz: privatdruck

### Rückenbreite in mm laut epubli-Coverrechner
Ändert sich mit der Seitenzahl! Nach «sh build.sh final» die Seitenzahl im Coverrechner eingeben.
- ruecken: @@RUECKEN@@

### Beschnitt, Deckel und Papier laut epubli-Coverrechner
Beschnitt in mm. Hardcover: der Coverrechner nennt 11 mm (Einschlag rundum). Softcover-Umschlag und Innenseiten: 3 mm. Deckel: Breite x Höhe in mm, leer = laut Format. Papier: wie bei der Bestellung gewählt (bestimmt die Rückenbreite).
- beschnitt-hardcover: 11
- beschnitt-softcover: 3
- beschnitt-buchblock: 3
- deckel-hardcover:
- papier:

## Dateien und Ordner
- kurz-normal: @@KUERZEL@@
- kurz-uz: @@KUERZEL@@-@@ZWEITKURZ@@
- datei-normal: @@NAME@@
- datei-uz: @@NAME@@_@@ZWEITDATEI@@
- ordner-normal: ausgabe-normal
- ordner-uz: ausgabe-@@ZWEITORDNER@@

## Fotos
Fotos liegen in fotos/ (JPG), Porträt, Verzierung und Teil-Bilder in bilder/ (PNG). Ohne Angaben: jedes Foto so breit wie der Text, höchstens 75 mm hoch, am Seitenende etwas kleiner, damit keine Lücke entsteht. foto-format: alle Fotos auf dasselbe Seitenverhältnis zuschneiden, z. B. 3:2, 4:3, 16:9 oder quadrat (pro Foto «ausschnitt: oben / unten / links / rechts», Standard Mitte; Fotos mit «fluss» bleiben ungeschnitten). foto-breite: einheitliche Breite in mm (ein «breite:» im Foto geht vor). foto-anpassen: nein = nie verkleinern, alle Fotos immer gleich gross. Alle drei zusammen = alle Fotos genau gleich gross.
- foto-format:
- foto-breite:
- foto-anpassen: ja

## Weiteres
Stichwortverzeichnis aus stichworte-<name>.txt (ja / nein). Trennstellen: | = hier darf ein langes Wort getrennt werden. Zier: eigenes Bild der Verzierung im Ordner bilder/, leer = Standard. Kopfzeile: ohne-autor (Teil · Kapitel, Standard), autor (Autor · Teil · Kapitel) oder wechselnd (links Teil, rechts Kapitel). bildschirm-dunkler: ja = feine Farben nur im Bildschirm-PDF etwas dunkler (für Schwarz-weiss-Ausdrucke). mockup-hintergrund: Farbverlauf (oben, unten) des Werbebilds …_Mockup.jpg (entsteht bei «final» und mit «sh build.sh mockup»).
- stichworte: ja
- trennstellen: Welt|anschauung, Gedanken|karussell
- zier:
- zier-hell:
- kopfzeile: ohne-autor
- bildschirm-dunkler: nein
- mockup-hintergrund: #E9EEF4, #C9D3DF

## Sicherung
«sh sicherung.sh» sichert das ganze Buch als ZIP (Name mit Datum und Uhrzeit, ohne Zwischenspeicher; von den Ausgaben nur die Bildschirm-PDFs). «sh sicherung.sh lokal» oder «cloud» = nur dorthin, ohne Angabe = an beide. «sicherung-behalten»: nur die neuesten ZIPs behalten (leer = alle). Pfad relativ zum Buchordner oder mit ~ bzw. /. Bei jedem Bau kommen die MD-Dateien ausserdem mit Datum und Uhrzeit nach md-history/; «md-history-behalten»: pro Datei nur die neuesten Stände behalten (leer = alle).
- sicherung-lokal: ../Sicherungen
- sicherung-cloud:
- sicherung-behalten: 10
- md-history-behalten: 200


# LAYOUT
Aussehen des Buchs. Leer lassen = Vorgabe des Motors. Farben als #RRGGBB. Schriften: Dateien im Ordner fonts/ oder motor/fonts/, z. B. Lora-Regular.ttf, Lora-Bold.ttf, Lora-Italic.ttf, Lora-BoldItalic.ttf.

## Farben
- farbe-text: #2E2A26
- farbe-leise: #6E655C
- farbe-haupt: #1E428A
- farbe-akzent: #B8873B
- farbe-papier: #FBF6EC
- farbe-kasten: #EEF2F9
- farbe-stempel: #A8322A

## Schrift
Schriftgrösse und Zeilenabstand in Punkt; leer = passend zum Format.
- schrift-text: Lora
- schrift-titel: Poppins
- schriftgroesse:
- zeilenabstand:
- blocksatz: ja
