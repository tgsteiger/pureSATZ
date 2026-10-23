# Umschlag

> Texte für Vorderseite, Buchrücken und Rückseite. Jede Zeile «name: text».
> Variablen wie {titel} kommen aus der Variablen-Datei. Farben und Schriften stehen dort unter LAYOUT.
> Endung am Namen = nur dort: «-druck» gedruckter Umschlag · «-bildschirm» Lese-PDF · «-ebook» E-Book-Cover · «-normal» / «-uz» Ausgabe.
> Eine Zeile, in der eine Variable leer ist, fällt weg.

## Vorderseite
titel: {titel}
untertitel: {untertitel}
autor: {autor}
stempel: {stempel}
stempel-farbe: rot
fuss: {ort} · {website}
fuss-druck: Erstausgabe {jahr}
fuss-bildschirm: Stand {stand}
> stempel-farbe: rot = schräger Stempel (Farbe: {farbe-stempel} im LAYOUT) · zeile = feine Zeile über dem Titel · keine
> fuss: Fusszeilen unten auf der Vorderseite, höchstens zwei (die ersten zwei, die gelten)

## Buchrücken
> Wird aus Titel, Untertitel, Autor und Stempel der Vorderseite gesetzt. Was nicht Platz hat, fällt automatisch weg.

## Rückseite
slogan: Ein Satz, der neugierig macht.
foto: autor-beispiel.png
text: Hier steht der Klappentext: Worum geht es in diesem Buch?
text: Ein zweiter Absatz, wenn nötig.
auszug: «Ein kurzer Satz aus dem Buch.»
auszug: «Noch einer.»
fuss: {autor} · {ort}
fuss: {website}
> slogan: Satz oben auf der Rückseite; «\» = neue Zeile
> foto: rundes Foto aus bilder/
> text: Klappentext, ein Absatz pro Zeile
> auszug: kurze Sätze aus dem Buch
> fuss: Fusszeilen unten auf der Rückseite, höchstens zwei (die ersten zwei, die gelten)
