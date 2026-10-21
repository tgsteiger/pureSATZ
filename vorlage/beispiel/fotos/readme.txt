FOTOS – kurz zur Bildqualität
=============================

Format:      JPG (Fotos). PNG geht auch, aber ohne Transparenz.
Farben:      RGB, wie aus Kamera oder Handy. Nicht in CMYK umwandeln.

Auflösung für den Druck: 300 dpi in der gedruckten Grösse.
Faustregel: Breite in mm x 12 = nötige Pixel.

  Bild über die ganze Textbreite (A5, ca. 115 mm)   ->  mind. 1400 Pixel breit
  halbe Breite (breite: 60)                         ->  mind.  700 Pixel
  kleines Bild mit Textfluss (breite: 40)           ->  mind.  500 Pixel
  A4 oder Quadrat, ganze Breite (ca. 160 mm)        ->  mind. 1900 Pixel

Grösser schadet nicht: Der Motor verkleinert automatisch auf höchstens 1800 Pixel
(Zwischenspeicher _bildcache/). Handyfotos (3000–4000 Pixel) sind also ideal.

Zu klein (z. B. aus WhatsApp oder vom Web, unter ca. 800 Pixel) wird im Druck unscharf.
Im Bildschirm-PDF sieht man das oft nicht – im Probedruck-Booklet schon eher.

Dateinamen: ohne Leerzeichen und Umlaute, z. B. sommer-1980.jpg
Im Buch:    ::: foto Titel / datei: sommer-1980.jpg / text: Bildunterschrift / :::

Gleich gross:  Ohne Angaben ist jedes Foto so breit wie der Text und höchstens 75 mm hoch
               (Querformat breit, Hochformat schmaler). Alle Fotos gleich gross: in der
               Variablen-Datei  foto-format: 3:2  ·  foto-breite: 100  ·  foto-anpassen: nein
               Zuschnitt aus der Mitte; pro Foto «ausschnitt: oben» (oder unten, links, rechts).
               Das Original hier bleibt immer unverändert.

Zu wenig Pixel meldet  sh build.sh pruefen  mit einem Hinweis.
