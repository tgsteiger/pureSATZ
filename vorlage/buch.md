## @TITEL
{titel}
{untertitel}
{titel-zusatz}

## @IMPRESSUM
© {jahr} {autor}
{website}
Satzsystem: pureSATZ

{verlag}
{impressum-herstellung}

{impressum-rechte}

{impressum-kontakt}

ISBN {isbn}
{auflage}
::: nur-privatdruck
Privatdruck {jahr} · nicht im Handel erhältlich
:::

## @HINWEIS
Hier steht ein Hinweis unten im Impressum, z. B. «Dieses Buch ersetzt keine Beratung». Keiner gewünscht? Diese zwei Zeilen löschen.

## @WIDMUNG
Hier steht eine Widmung. Im gedruckten Buch steht sie allein auf der rechten Seite neben dem Impressum. Keine gewünscht? Diese zwei Zeilen löschen.

## @KERNSATZ Ein Satz, der das ganze Buch zusammenfasst.

## @INHALTSVERZEICHNIS

## Vorwort

Dieses Demo-Kapitel zeigt alle Möglichkeiten. Schau dir das PDF an und vergleiche es mit dieser Datei: So siehst du, welche Zeile was bewirkt. Danach einfach alles ab hier löschen und dein Buch schreiben.

Ein neuer Absatz beginnt nach einer leeren Zeile. **Fett** steht zwischen zwei Sternchen. Ein Link sieht so aus: [{website}](https://{website}).<br/>Ein Zeilenumbruch innerhalb des Absatzes geht mit br in spitzen Klammern.

~ Eine Zeile mit Tilde ist eine kursive Randbemerkung.

> Eine Zeile mit > ist ein Zitat, eingerahmt von der Verzierung.

@ZITAT Ein Zitat mit @ZITAT, ohne Verzierung.

{autor}, {ort}

# Teil 1|Grundlagen|Text, Listen und Kästen

## Ein Kapitel

Ein Teil beginnt mit einer Raute und zwei senkrechten Strichen: Nummer, Titel, Untertitel. Kapitel beginnen mit zwei Rauten und stehen im Inhaltsverzeichnis. Die Kopfzeile zeigt Autor, Teil und Kapitel.

### Ein Zwischentitel

Zwischentitel beginnen mit drei Rauten. Sie stehen nicht im Inhaltsverzeichnis und rutschen nie allein ans Seitenende.

- Ein Punkt einer Liste
- Noch ein Punkt
  - ein Unterpunkt (zwei Leerzeichen eingerückt)
- Und ein dritter

Eine nummerierte Aufzählung zählt selbst weiter:

1. Erster Schritt
2. Zweiter Schritt
   - ein Unterpunkt
3. Dritter Schritt

Beginnt ein Satz mit einer Zahl und einem Punkt, aber es ist keine Aufzählung: «3\. Mai» schreiben.

## Zwei Ausgaben aus einer Datei

Blöcke beginnen mit drei Doppelpunkten und enden mit drei Doppelpunkten. Die Endung sagt, wo der Block erscheint: -normal, -uz (zweite Ausgabe), -bildschirm, -druck, -ebook, -buch, -privatdruck.

::: uz Ein Kasten mit eigenem Titel
Dieser Kasten erscheint nur in der zweiten Ausgabe, «{ausgabe-name-uz}». In der normalen Ausgabe fehlt er ganz.

- Auch Aufzählungen gehen im Kasten.
~ Und Randbemerkungen.
:::

::: nur-uz
Dieser normale Absatz steht nur in der zweiten Ausgabe.
:::

::: nur-normal
Dieser normale Absatz steht nur in der normalen Ausgabe.
:::

::: nur-ebook
Dieser Absatz steht nur im E-Book.
:::

## Noch offen

Beim Schreiben ist nicht alles entschieden. Dafür gibt es die Familie «offen». Im Entwurf (sh build.sh) ist sie farbig markiert, und am Ende des Bauens steht eine Liste mit Zeilennummern.

::: offen
Dieser Absatz ist noch offen: Im Entwurf gelb, in der Druckfassung normaler Text in beiden Ausgaben.
:::

::: offen-uz
Dieser Absatz ist offen und gehört eher in die zweite Ausgabe. Entschieden? Aus offen-uz wird nur-uz.
:::

::: offen-notiz Hier fehlt noch etwas
Eine Notiz an dich selbst: erscheint nur im Entwurf als roter Kasten und wird nie gedruckt.
:::

## Bilder

Ein Foto beginnt mit «#### @FOTO Titel» (so steht es auch in der Gliederung des Editors), darunter die Angaben als Liste. Die erste Leerzeile beendet den Foto-Block. Ein Foto über die ganze Breite (ohne «fluss»):

#### @FOTO Landschaft
- datei: beispiel.jpg
- text: Ein Bild mit Bildunterschrift
- quelle: Foto: Vorname Nachname
- alt: Weite Landschaft mit Hügeln unter blauem Himmel
- breite: 80

Ein Hochformat wird bei gleicher Breite höher; der Motor begrenzt Fotos auf 75 mm Höhe, darum wird es schmaler. Sollen alle Fotos gleich gross sein: in der Variablen-Datei «foto-format: 3:2» (alle gleich zugeschnitten), «foto-breite» und «foto-anpassen: nein».

#### @FOTO Hochformat
- datei: beispiel-hoch.jpg
- text: Ein Hochformat: gleich hoch, aber schmaler
- alt: Ein Baum vor einem Abendhimmel

#### @FOTO Ein Foto, das noch fehlt
- Vorschlag: Hier könnte ein Foto vom Garten stehen. Im Entwurf ein Kasten, im Druck nichts.
- datei: garten.jpg

#### @FOTO Klein mit Textfluss
- datei: beispiel.jpg
- fluss: rechts
- breite: 40
- text: Text fliesst um das Bild

Dieser Absatz fliesst links um das kleine Bild herum. Das ist praktisch für Porträts oder kleine Erinnerungsstücke. Die folgenden Absätze (bis zu fünf) umfliessen das Bild, bis es zu Ende ist.

Fotos mit «quelle:» erscheinen automatisch im Bildnachweis im Anhang, mit Seitenzahl.

Noch ein Absatz, damit man den Textfluss gut sieht. Mit «fluss: links» steht das Bild links. Ein Buch lebt von Abwechslung: lange Absätze, kurze Absätze, Bilder, Zitate.

## Eine Tabelle

Tabellen stehen als CSV-Datei im Ordner tabellen/ (mit LibreOffice bearbeiten, als «Text CSV» speichern). Im Buch genügt eine eigene Zeile mit @# und dem Dateinamen, hier @#muster:

@#muster

Zahlen stehen rechtsbündig. Ist eine Tabelle zu breit, wird sie kleiner oder quer gestellt. Eine neue Tabelle legt «sh neu.sh tabelle "Titel"» an.

@UMBRUCH-RECHTS

## Seiten steuern

Eine Zeile mit @UMBRUCH beginnt eine neue Seite. @UMBRUCH-RECHTS beginnt im Druck immer auf einer rechten Seite. @PLATZ 60 beginnt eine neue Seite nur, wenn weniger als 60 mm Platz bleiben. @ABSTAND 8 lässt 8 mm frei.

@ABSTAND 8

::: zusammen
Ein Block «zusammen» wird nie auf zwei Seiten getrennt.

- zum Beispiel eine Liste,
- die zusammenbleiben soll.
:::

@ZIER 12

::: mitte
Ein zentrierter Block zwischen zwei Verzierungen,

zum Beispiel für einen Dank oder ein Gedicht.
:::

@MOTTO Ein Satz allein auf einer Seite.

# Teil 2|Anhang|Zeitstrahl, Autor und Verzeichnis|beispiel.jpg

## Ein Teil mit eigenem Bild

Dieser Teil hat oben ein eigenes Bild: Es steht als vierte Angabe in der Teil-Zeile. Eine Raute ohne senkrechte Striche ergibt ein Kapitel auf oberster Ebene, zum Beispiel für den Anhang.

# Zeitstrahl

::: zeitstrahl
1974 | Geboren
1990 | Lehre
{jahr} | Erstes Buch
heute | {ort}
:::

# Über den Autor

@PORTRAIT autor-beispiel.png | {autor}

**{autor}** lebt in {ort}. Hier steht ein kurzer Text über den Autor.

::: nur-normal
«{titel}» ist das erste Buch.
:::
::: nur-uz
Dies ist die Ausgabe «{ausgabe-name}» von «{titel}».
:::

@QR-PAAR https://{website} | Website<br/>{website} ;; https://{website}/blog | Blog<br/>{website}/blog

@STICHWORTE

@MOTTO Danke.

@RUECKSEITE
