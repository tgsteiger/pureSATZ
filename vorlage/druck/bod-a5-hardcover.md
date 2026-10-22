# DRUCKANGABEN – BoD, DIN A5 hoch, Hardcover
UNGETESTET – Werte nach dem ersten Test-Upload bei BoD prüfen und dann diese Zeile entfernen.
Gilt nur für die Druckdateien (sh build.sh final / nur-druck). Die Werte hier haben Vorrang vor der
Variablen-Datei. Lese-PDF, E-Book, Leseprobe und Korrektur bleiben beim Grundformat der Variablen-Datei.
Verwenden: in <name>-variablen.md «- druck-normal: bod-a5-hardcover» oder «- druck-uz: bod-a5-hardcover».
Testen, ohne etwas umzustellen: sh build.sh final druck=bod-a5-hardcover
Leer = Vorgabe des Motors. Masse in mm. «name-normal» / «name-uz» gelten nur für diese Fassung.

## Plattform und Format
Plattform: epubli oder bod. Format: a5, taschenbuch, sachbuch, a4, quadrat (oder «seite: 148 x 210»).
Bindung: hardcover, softcover, beide. Projekt: veroeffentlichen (mit ISBN) oder privatdruck.
- plattform: bod
- format: a5
- bindung: hardcover
- projekt:

## Rücken, Beschnitt und Deckel laut BoD-Coverrechner
BoD möchte den Buchblock ohne Beschnitt (148 x 210 mm). Hardcover: Deckel 153 x 216 mm, 17 mm Einschlag rundum.
Rücken: ändert sich mit Seitenzahl und Papier!
- ruecken-hardcover:
- beschnitt-buchblock: 0
- deckel-hardcover: 153x216
- beschnitt-hardcover: 17
- papier:

## ISBN
Bei BoD gibt es eine eigene ISBN (leer = im Impressum steht «ISBN folgt»; beim Privatdruck keine).
- isbn-buch:

## Barcode (Rückseite)
Feld unten rechts, 40 x 20 mm, mit 16 mm Abstand seitlich und 8 mm unten. barcode-bild: PNG aus bilder/
(leer = Strichcode aus der ISBN bzw. Platzhalter «Platz für ISBN-Strichcode»).
- barcode-position: rechts
- barcode-groesse: 40x20
- barcode-bild:
