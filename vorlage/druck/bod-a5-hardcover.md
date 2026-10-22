# BoD – A5 Hardcover

#### UNGETESTET – Werte nach dem ersten Upload bei BoD prüfen
#### Test: sh build.sh final druck=bod-a5-hardcover
#### Rücken und Papier laut BoD-Coverrechner eintragen

## Plattform
- plattform: bod
#### default: epubli · optional: epubli | bod (bod auch für tredition, KDP und andere)
- format: a5
#### default: a5 · optional: a5 | taschenbuch | sachbuch | a4 | quadrat
- seite:
#### default: leer = Mass laut format · optional: eigenes Mass in mm, z. B. 148 x 210
- bindung: hardcover
#### default: hardcover · optional: hardcover | softcover | beide
- projekt:
#### default: veroeffentlichen (zweite Fassung: privatdruck) · optional: veroeffentlichen | privatdruck

## Innenteil
- beschnitt-buchblock: 0
#### default: epubli 3, bod 5 · optional: mm rundum, 0 = ohne Beschnitt
- extra-seiten:
#### default: 0 · optional: Anzahl leere Notizseiten am Schluss

## Umschlag
- ruecken-hardcover:
#### default: leer = 6 mm (Platzhalter) · optional: mm laut Coverrechner (ändert sich mit Seitenzahl und Papier)
- ruecken-softcover:
#### default: leer = 3 mm (Platzhalter) · optional: mm laut Coverrechner
- beschnitt-hardcover: 17
#### default: 11 · optional: Einschlag rundum in mm laut Coverrechner
- beschnitt-softcover:
#### default: 3 · optional: mm rundum
- deckel-hardcover: 153x216
#### default: leer = laut format (A5: 157 x 228) · optional: Breite x Höhe in mm
- papier:
#### default: leer · optional: Papier wie bestellt (nur zur Info)

## ISBN
- isbn-buch:
#### default: leer = «ISBN folgt» im Impressum · optional: ISBN der Plattform

## Strichcode
- barcode-position: rechts
#### default: leer = epubli links frei, bod rechts · optional: links | mitte | rechts
- barcode-groesse: 40x20
#### default: leer = 60 x 35 mm frei ab Ecke · optional: Breite x Höhe in mm, z. B. 40x20
- barcode-bild:
#### default: leer = nichts zeichnen (bod: Strichcode aus der ISBN) · optional: PNG aus bilder/
