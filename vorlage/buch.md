## @TITLE
{titel}
{untertitel}
{titel-zusatz}

## @IMPRINT

## @NOTICE
Hier steht ein Hinweis unten im Impressum, z. B. «Dieses Buch ersetzt keine Beratung». Keiner gewünscht? Diese zwei Zeilen löschen.

## @DEDICATION
Hier steht eine Widmung. Im gedruckten Buch steht sie allein auf der rechten Seite neben dem Impressum. Keine gewünscht? Diese zwei Zeilen löschen.

## @DECORATE-PAGE Ein Satz, der das ganze Buch zusammenfasst.

## @CONTENTS

## Vorwort

Dieses Demo-Kapitel zeigt alle Möglichkeiten. Schau dir das PDF an und vergleiche es mit dieser Datei: So siehst du, welche Zeile was bewirkt. Danach einfach alles ab hier löschen und dein Buch schreiben.

Ein neuer Absatz beginnt nach einer leeren Zeile. **Fett** steht zwischen zwei Sternchen. Ein Link sieht so aus: [{website}](https://{website}).\
Diese Zeile beginnt neu, gehört aber zum selben Absatz: In der MD steht am Ende der Zeile davor ein umgekehrter Schrägstrich (Backslash).

@ASIDE Eine Randbemerkung: klein und kursiv.

@DECORATE Ein Satz mit @DECORATE, zwischen zwei Linien mit Logo.

@DECORATE-TEXT Ein Satz mit @DECORATE-TEXT, schlicht, ohne Linien.

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

Ein Bereich beginnt mit einem @-Befehl allein auf der Zeile und endet mit @END. @UC (zweite Ausgabe), @NORMAL, @EBOOK, @PRINT (Druck) und @SCREEN (Lese-PDF) sagen, wo er erscheint. Für eine einzelne Zeile genügt die Vorsilbe: @UC-SPACER-14.

@UC-BLOCK Ein Kasten mit eigenem Titel
Dieser Kasten erscheint nur in der zweiten Ausgabe, «{ausgabe-name-uz}». In der normalen Ausgabe fehlt er ganz.

- Auch Aufzählungen gehen im Kasten.
@ASIDE Und Randbemerkungen.
@END

@UC
Dieser normale Absatz steht nur in der zweiten Ausgabe.
@END

@NORMAL
Dieser normale Absatz steht nur in der normalen Ausgabe.
@END

@EBOOK
Dieser Absatz steht nur im E-Book.
@END

## Noch offen

Beim Schreiben ist nicht alles entschieden. Dafür gibt es @DRAFT und @NOTE. Im Entwurf (sh build.sh) sind sie farbig markiert, und am Ende des Bauens steht eine Liste mit Zeilennummern.

@DRAFT
Dieser Absatz ist noch offen: Im Entwurf gelb, in der Druckfassung normaler Text in beiden Ausgaben.
@END

@UC-DRAFT
Dieser Absatz ist offen und gehört eher in die zweite Ausgabe. Entschieden? Aus @UC-DRAFT wird @UC.
@END

@NOTE Hier fehlt noch etwas
Eine Notiz an dich selbst: erscheint nur im Entwurf als roter Kasten und wird nie gedruckt.
@END

## Bilder

Ein Foto beginnt mit «#### @PICTURE Titel» (so steht es auch in der Gliederung des Editors), darunter die Angaben, eine pro Zeile. Die erste Leerzeile beendet den Foto-Block. Eine Zahl im Namen ist die Breite in mm: «#### @PICTURE-80 Titel».

#### @PICTURE-80 Landschaft
datei: beispiel.jpg
text: Ein Bild mit Bildunterschrift
quelle: Foto: Vorname Nachname
alt: Weite Landschaft mit Hügeln unter blauem Himmel

Ein Hochformat wird bei gleicher Breite höher; der Motor begrenzt Fotos auf 75 mm Höhe, darum wird es schmaler. Sollen alle Fotos gleich gross sein: in der Variablen-Datei «foto-format: 3:2» (alle gleich zugeschnitten), «foto-breite» und «foto-anpassen: nein».

#### @PICTURE Hochformat
datei: beispiel-hoch.jpg
text: Ein Hochformat: gleich hoch, aber schmaler
alt: Ein Baum vor einem Abendhimmel

#### @PICTURE Ein Foto, das noch fehlt
Vorschlag: Hier könnte ein Foto vom Garten stehen. Im Entwurf ein Kasten, im Druck nichts.
datei: garten.jpg

#### @PICTURE-40-RIGHT Klein mit Textfluss
datei: beispiel.jpg
text: Text fliesst um das Bild

Dieser Absatz fliesst links um das kleine Bild herum. Das ist praktisch für Porträts oder kleine Erinnerungsstücke. Die folgenden Absätze (bis zu fünf) umfliessen das Bild, bis es zu Ende ist.

Fotos mit «quelle:» erscheinen automatisch im Bildnachweis im Anhang, mit Seitenzahl.

Noch ein Absatz, damit man den Textfluss gut sieht. Mit «@PICTURE-40-LEFT» steht das Bild links. Ein Buch lebt von Abwechslung: lange Absätze, kurze Absätze, Bilder, Zitate.

Auch der Strichcode auf der Rückseite darf schön sein: Mit «isbn-rahmen: berge» in der Druckdatei bekommt er einen goldenen Rahmen, oben als Bergkette (mit «gold» ein schlichter Goldrahmen). Er bleibt lesbar. Das Beispiel zeigt eine erfundene Nummer.

#### @PICTURE-60 Strichcode mit Goldrahmen
datei: strichcode-bergkette.png
text: Strichcode mit Bergkette – isbn-rahmen: berge
alt: Strichcode mit goldenem Rahmen, oben als Bergkette

## Eine Tabelle

Tabellen stehen als CSV-Datei im Ordner tabellen/ (mit LibreOffice bearbeiten, als «Text CSV» speichern). Im Buch genügt eine eigene Zeile mit @# und dem Dateinamen, hier @#muster:

@#muster

Zahlen stehen rechtsbündig. Ist eine Tabelle zu breit, wird sie kleiner oder quer gestellt. Eine neue Tabelle legt «sh neu.sh tabelle "Titel"» an.

@NEWPAGE-RIGHT

## Seiten steuern

@NEWPAGE beginnt eine neue Seite. @NEWPAGE-RIGHT beginnt im Druck immer auf einer rechten Seite. @NEWPAGE-60 beginnt eine neue Seite nur, wenn weniger als 60 mm Platz bleiben. @SPACER-8 lässt 8 mm frei.

@SPACER-8

@KEEP-TOGETHER
Ein Bereich @KEEP-TOGETHER wird nie auf zwei Seiten getrennt.

- zum Beispiel eine Liste,
- die zusammenbleiben soll.
@END

@LOGO-12

@DECORATE-REST
Mit @DECORATE-REST steht der Text zwischen zwei Linien mitten im Rest der Seite,

zum Beispiel für einen Dank oder ein Gedicht.
@END

@DECORATE-PAGE Ein Satz allein auf einer Seite.

# Teil 2|Anhang|Zeitstrahl, Autor und Verzeichnis|beispiel.jpg

## Ein Teil mit eigenem Bild

Dieser Teil hat oben ein eigenes Bild: Es steht als vierte Angabe in der Teil-Zeile. Eine Raute ohne senkrechte Striche ergibt ein Kapitel auf oberster Ebene, zum Beispiel für den Anhang.

# Zeitstrahl

@TIMELINE
1974 | Geboren
1990 | Lehre
{jahr} | Erstes Buch
heute | {ort}
@END

# Über den Autor

@PORTRAIT autor-beispiel.png | {autor}

**{autor}** lebt in {ort}. Hier steht ein kurzer Text über den Autor.

@NORMAL
«{titel}» ist das erste Buch.
@END
@UC
Dies ist die Ausgabe «{ausgabe-name}» von «{titel}».
@END

@QR https://{website} | Website<br/>{website} ;; https://{website}/blog | Blog<br/>{website}/blog

@INDEX

@DECORATE-PAGE Danke.

@BACK-COVER
