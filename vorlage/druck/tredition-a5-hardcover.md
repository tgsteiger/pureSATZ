# tredition – A5 Hardcover

{neu-berechnen}: ja
{berechnet-fuer-seiten}: 
> {neu-berechnen}: ja = Seitenzahl hat sich geändert, Rücken und Umschlag im Coverrechner neu berechnen · nein = Werte passen
> {berechnet-fuer-seiten}: Seiten des Buchblocks, für die die Werte unten berechnet sind. Weicht der Buchblock ab, warnt «sh build.sh final».
> Nur Technik dieser Plattform. ISBN, Preis und Impressum stehen in der Variablen-Datei unter «## Ausgabe: …».
> Neue Werte vom Coverrechner: unten unter «## Coverrechner (Rohdaten)» einfügen und Claude sagen: «Coverwerte übernehmen».
> UNGETESTET beim Umschlag – Buchblock 15,8 x 22 cm (A5 + 5 mm Beschnitt) laut tredition
> Test: sh build.sh final druck=tredition-a5-hardcover

## Plattform
{plattform}: tredition
{bindung}: hardcover
{projekt}:
> {plattform}: default: epubli · optional: epubli | bod | tredition | kdp (tredition und kdp verhalten sich wie bod)
> {bindung}: default: hardcover · optional: hardcover | softcover | beide
> {projekt}: default: veroeffentlichen (zweite Fassung: privatdruck) · optional: veroeffentlichen | privatdruck
> {format}: nur, wenn das Druckformat vom Grundformat in der Variablen-Datei abweicht: a5 | taschenbuch | sachbuch | a4 | quadrat oder Masse in mm, z. B. 150 x 215

## Innenteil
{beschnitt-buchblock}: 5
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
{beschnitt-hardcover}:
{beschnitt-softcover}: 5
{deckel-hardcover}:
{papier}:
> {ruecken-hardcover}: default: leer = 6 mm (Platzhalter) · optional: mm laut Coverrechner (ändert sich mit Seitenzahl und Papier)
> {ruecken-softcover}: default: leer = 3 mm (Platzhalter) · optional: mm laut Coverrechner
> {beschnitt-hardcover}: default: 11 · optional: Einschlag rundum in mm laut Coverrechner
> {beschnitt-softcover}: default: 3 · optional: mm rundum
> {deckel-hardcover}: default: leer = laut format (A5: 157 x 228) · optional: Breite x Höhe in mm
> {papier}: default: leer · optional: Papier wie bestellt (nur zur Info)

## Strichcode
{barcode-position}: rechts
{barcode-groesse}: 40x19
{barcode-bild}:
> {barcode-position}: default: leer = epubli links frei, bod rechts · optional: links | mitte | rechts
> {barcode-groesse}: default: leer = 60 x 35 mm frei ab Ecke · optional: Breite x Höhe in mm, z. B. 40x20
> {barcode-bild}: default: leer = nichts zeichnen (bod: Strichcode aus der ISBN) · optional: PNG aus bilder/

## Offen
> Umschlag: Rücken, Deckelmass und Einschlag von tredition

## Coverrechner (Rohdaten)
> Hier die Angaben aus dem Coverrechner der Plattform einfügen (Text, wie er kommt). Der Motor liest diesen Abschnitt nicht.
> Rücken, Deckel und Einschlag laut tredition eintragen; Strichcode von tredition als PNG nach bilder/

## Notizen
> Impressum und ISBN gehören in die Variablen-Datei unter «## Ausgabe: …». Beim Wechsel auf diese Plattform dort eintragen:
> {impressum-herstellung}: Druck und Distribution im Auftrag des Autors: tredition GmbH, Heinz-Beusen-Stieg 5, 22926 Ahrensburg, Deutschland
> {impressum-kontakt}: Kontaktadresse nach EU-Produktsicherheitsverordnung: (eigene E-Mail eintragen)
> E-Book über tredition («## Ausgabe: E-Book»): {impressum-herstellung}: Distribution im Auftrag des Autors: tredition GmbH, Heinz-Beusen-Stieg 5, 22926 Ahrensburg, Deutschland
> Logo: {impressum-logo}: PNG von tredition in bilder/
