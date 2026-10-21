# UMSCHLAG
Texte für Vorderseite, Buchrücken und Rückseite. Jede Zeile «- schlüssel: text». Variablen wie {titel} kommen aus der Variablen-Datei. Farben und Schriften stehen in der Variablen-Datei unter LAYOUT. Blöcke wie im Buch: ::: nur-druck, ::: nur-bildschirm, ::: nur-normal, ::: nur-uz. Eine Zeile, in der eine Variable leer ist, fällt weg.

# Vorderseite
- titel: {titel}
- untertitel: {untertitel}
- autor: {autor}
- stempel: {stempel}
- stempel-farbe: rot
- fuss: {ort} · {website}
::: nur-druck
- fuss: Erstausgabe {jahr}
:::
::: nur-bildschirm
- fuss: Stand {stand}
:::

# Buchrücken
Wird aus Titel, Untertitel, Autor und Stempel der Vorderseite gesetzt. Was nicht Platz hat, fällt automatisch weg.

# Rückseite
- slogan: Ein Satz, der neugierig macht.
- foto: autor-beispiel.png
- text: Hier steht der Klappentext: Worum geht es in diesem Buch?
- text: Ein zweiter Absatz, wenn nötig.
- auszug: «Ein kurzer Satz aus dem Buch.»
- auszug: «Noch einer.»
- fuss: {autor} · {ort}
- fuss: {website}
