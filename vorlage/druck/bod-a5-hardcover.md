# BoD – A5 Hardcover

{neu-berechnet}: nein
{berechnet-fuer-seiten}: 
{berechnet-am}: 
> {neu-berechnet}, {berechnet-fuer-seiten}, {berechnet-am}: setzt der Motor beim Bau der Druckdateien. nein = Seitenzahl geändert oder Rohdaten fehlen → Coverrechner rechnen, Text unten ersetzen.
> Nur Technik dieser Plattform. ISBN, Preis und Impressum stehen in der Variablen-Datei unter «## Ausgabe: …».
> Neue Werte: Text des Coverrechners unten unter «## Coverrechner (Rohdaten)» einfügen.
> UNGETESTET – Werte nach dem ersten Upload bei BoD prüfen
> Test: sh build.sh final druck=bod-a5-hardcover

## Plattform
{plattform}: bod
{bindung}: hardcover
{projekt}:
{farbmodus}:
> {plattform}: default: epubli · optional: epubli | bod | tredition | kdp (tredition und kdp verhalten sich wie bod)
> {bindung}: default: hardcover · optional: hardcover | softcover | beide
> {projekt}: default: veroeffentlichen (zweite Fassung: privatdruck) · optional: veroeffentlichen | privatdruck
> {farbmodus}: default: rgb · optional: rgb | cmyk (cmyk: Buchblock und Umschlag werden nach dem Bau mit Ghostscript umgewandelt; braucht gs)
> {format}: nur, wenn das Druckformat vom Grundformat in der Variablen-Datei abweicht: a5 | taschenbuch | sachbuch | a4 | quadrat oder Masse in mm, z. B. 150 x 215

## Innenteil
{beschnitt-buchblock}: 0
{extra-seiten}:
{versatz-vertikal}:
{versatz-horizontal}:
> {beschnitt-buchblock}: default: epubli 3, bod 5 · optional: mm rundum, 0 = ohne Beschnitt
> {extra-seiten}: default: 0 · optional: Anzahl leere Notizseiten am Schluss
> {versatz-vertikal}: default: 0 · optional: mm, + = ganzer Inhalt nach oben, − = nach unten (nach Messung am Probeexemplar, z. B. -1.5)
> {versatz-horizontal}: default: 0 · optional: mm, + = nach aussen, − = zum Bund hin

## Umschlag
{ruecken-hardcover}:
{ruecken-softcover}:
{beschnitt-hardcover}: 17
{beschnitt-softcover}:
{deckel-hardcover}: 153x216
{papier}:
> {ruecken-hardcover}: default: leer = 6 mm (Platzhalter) · optional: mm laut Coverrechner (ändert sich mit Seitenzahl und Papier)
> {ruecken-softcover}: default: leer = 3 mm (Platzhalter) · optional: mm laut Coverrechner
> {beschnitt-hardcover}: default: 11 · optional: Einschlag rundum in mm laut Coverrechner
> {beschnitt-softcover}: default: 3 · optional: mm rundum
> {deckel-hardcover}: default: leer = laut format (A5: 157 x 228) · optional: Breite x Höhe in mm
> {papier}: default: leer · optional: Papier wie bestellt (nur zur Info)

## Strichcode mit der ISBN (EAN-13, Barcode)
{isbn-position}: rechts
{isbn-groesse}: 40x20
{isbn-bild}:
{isbn-rahmen}:
{isbn-rahmen-farbe}:
{isbn-rahmen-abstand}:
> {isbn-position}: default: leer = epubli links frei, bod rechts · optional: links | mitte | rechts
> {isbn-groesse}: default: leer = 60 x 35 mm frei ab Ecke · optional: Breite x Höhe in mm, z. B. 40x20
> {isbn-bild}: default: leer = nichts zeichnen (bod: Strichcode aus der ISBN) · optional: PNG aus bilder/
> {isbn-rahmen}: default: leer = kein Rahmen · optional: gold = Goldrahmen · berge = Goldrahmen, oben als Bergkette (Striche eines PNG werden oben zu Gipfeln geschnitten)
> {isbn-rahmen-farbe}: default: leer = gold · optional: schwarz
> {isbn-rahmen-abstand}: default: leer = 0 (Linie berührt die Striche) · optional: mm weiss dazwischen, z. B. 2 (tredition: nur schwarze Striche auf Weiss)

## Coverrechner (Rohdaten)
> Text aus dem Coverrechner der Druckerei hier einfügen (wie er kommt). Der Motor liest ihn beim Bau selbst.

## Notizen
> Impressum und ISBN gehören in die Variablen-Datei unter «## Ausgabe: …». Beim Wechsel auf diese Plattform dort eintragen:
> DEMO-Texte – vor Gebrauch durch die Angaben von BoD ersetzen
> {impressum-herstellung}: Herstellung: BoD – Books on Demand GmbH, In de Tarpen 42, 22848 Norderstedt
> {impressum-kontakt}: Kontaktadresse nach EU-Produktsicherheitsverordnung: (Angabe von BoD eintragen)
