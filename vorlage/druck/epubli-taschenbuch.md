# DRUCKANGABEN – epubli, Taschenbuch
Gilt nur für die Druckdateien (sh build.sh final / nur-druck). Die Werte hier haben Vorrang vor der
Variablen-Datei. Lese-PDF, E-Book, Leseprobe und Korrektur bleiben beim Grundformat der Variablen-Datei.
Verwenden: in <name>-variablen.md «- druck-normal: epubli-taschenbuch» oder «- druck-uz: epubli-taschenbuch».
Testen, ohne etwas umzustellen: sh build.sh final druck=epubli-taschenbuch
Leer = Vorgabe des Motors. Masse in mm. «name-normal» / «name-uz» gelten nur für diese Fassung.

## Plattform und Format
Plattform: epubli oder bod. Format: a5, taschenbuch, sachbuch, a4, quadrat (oder «seite: 148 x 210» für ein eigenes Mass).
Bindung: hardcover, softcover, beide. Projekt: veroeffentlichen (mit ISBN) oder privatdruck.
- plattform: epubli
- format: taschenbuch
- bindung: hardcover
- projekt:

## Rücken in mm laut epubli-Coverrechner
Ändert sich mit Seitenzahl und Papier!
- ruecken-hardcover:
- ruecken-softcover:

## Beschnitt, Deckel und Papier laut epubli-Coverrechner
Hardcover: 11 mm Einschlag rundum. Softcover-Umschlag und Innenseiten: 3 mm. Deckel leer = laut Format (134 x 208 mm).
Papier: wie bei der Bestellung gewählt (bestimmt die Rückenbreite).
- beschnitt-hardcover: 11
- beschnitt-softcover: 3
- beschnitt-buchblock: 3
- deckel-hardcover:
- papier:

## Zusätzliche Notizseiten
Falls epubli eine bestimmte Seitenzahl verlangt.
- extra-seiten:

## Barcode (Rückseite)
epubli druckt Strichcode und ISBN selbst unten links auf die Rückseite – alles leer lassen (60 x 35 mm bleiben frei).
Möglich: barcode-position links | mitte | rechts · barcode-groesse 40x20 · barcode-bild datei.png (aus bilder/)
- barcode-position:
- barcode-groesse:
- barcode-bild:
