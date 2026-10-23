# epubli – Sachbuch

> Test: sh build.sh final druck=epubli-sachbuch
> Verwenden: in <buch>-variablen.md «{druck-normal}: epubli-sachbuch» (bzw. {druck-uz})
> Rücken und Papier laut epubli-Coverrechner eintragen; Deckel 144 x 223 mm

## Plattform
{plattform}: epubli
> default: epubli · optional: epubli | bod | tredition | kdp (tredition und kdp verhalten sich wie bod)
{format}: sachbuch
> default: a5 · optional: a5 | taschenbuch | sachbuch | a4 | quadrat
{seite}:
> default: leer = Mass laut format · optional: eigenes Mass in mm, z. B. 148 x 210
{bindung}: hardcover
> default: hardcover · optional: hardcover | softcover | beide
{projekt}:
> default: veroeffentlichen (zweite Fassung: privatdruck) · optional: veroeffentlichen | privatdruck

## Innenteil
{beschnitt-buchblock}: 3
> default: epubli 3, bod 5 · optional: mm rundum, 0 = ohne Beschnitt
{extra-seiten}:
> default: 0 · optional: Anzahl leere Notizseiten am Schluss
{versatz-vertikal}:
> default: 0 · optional: mm, + = ganzer Inhalt nach oben, − = nach unten (nach Messung am Probeexemplar, z. B. -1.5)
{versatz-horizontal}:
> default: 0 · optional: mm, + = nach aussen, − = zum Bund hin

## Umschlag
{ruecken-hardcover}:
> default: leer = 6 mm (Platzhalter) · optional: mm laut Coverrechner (ändert sich mit Seitenzahl und Papier)
{ruecken-softcover}:
> default: leer = 3 mm (Platzhalter) · optional: mm laut Coverrechner
{beschnitt-hardcover}: 11
> default: 11 · optional: Einschlag rundum in mm laut Coverrechner
{beschnitt-softcover}: 3
> default: 3 · optional: mm rundum
{deckel-hardcover}:
> default: leer = laut format (A5: 157 x 228) · optional: Breite x Höhe in mm
{papier}:
> default: leer · optional: Papier wie bestellt (nur zur Info)

## ISBN
{isbn-buch}:
> default: leer = «ISBN folgt» im Impressum · optional: ISBN der Plattform

## Impressum
> Impressum-Zeilen dieser Plattform. Sie ersetzen die gleichnamigen der Variablen-Datei. Leer = Zeile fällt weg.
{impressum-herstellung}: Herstellung: epubli – ein Service der neopubli GmbH, Köpenicker Strasse 154a, 10997 Berlin
{impressum-kontakt}: Kontaktadresse nach EU-Produktsicherheitsverordnung: produktsicherheit@epubli.com
{impressum-logo}:
> Privatdruck: z. B. «{impressum-herstellung}: Privatdruck · nicht im Handel erhältlich · Herstellung: epubli …»

## Strichcode
{barcode-position}:
> default: leer = epubli links frei, bod rechts · optional: links | mitte | rechts
{barcode-groesse}:
> default: leer = 60 x 35 mm frei ab Ecke · optional: Breite x Höhe in mm, z. B. 40x20
{barcode-bild}:
> default: leer = nichts zeichnen (bod: Strichcode aus der ISBN) · optional: PNG aus bilder/
