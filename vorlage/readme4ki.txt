readme4ki.txt – Anleitung für eine KI, die an diesem Buch mitarbeitet
=====================================================================

AUFTRAG
Du hilfst beim Schreiben und Überarbeiten eines Buchs. Das Buch besteht aus Markdown-Dateien.
Ein Programm («Motor») macht daraus PDF, Druckdateien und E-Book. Du änderst nur Text und Werte
und hältst dich genau an die Regeln unten. Sonst kann der Motor das Buch nicht mehr bauen.

DATEIEN (nur diese darfst du ändern)
  @@NAME@@-buch.md        der Buchtext
  @@NAME@@-variablen.md   Werte: Titel, Autor, ISBN, Format, Shop-Texte, Farben …
  @@NAME@@-umschlag.md    Vorderseite, Buchrücken, Rückseite
  stichworte-@@NAME@@.txt Stichwortverzeichnis: ein Stichwort pro Zeile, Varianten mit |, # = Kommentar
  geschichten/*.md        einzelne Geschichten (falls es den Ordner gibt), siehe GESCHICHTEN unten
  tabellen/*.csv          Tabellen (falls es den Ordner gibt), siehe TABELLEN unten
  druck/*.md              Druckangaben pro Fassung (Plattform, Rücken, Beschnitt, Papier, Barcode), siehe DRUCK unten
NIE ändern: ausgabe-*/ (auch 00-UEBERSICHT.txt, wird bei jedem Bau neu erstellt), Ordner motor/, *.sh, *.bat, *.py, md-history/, geschichten/UEBERSICHT.md, geschichten-uebersicht.html.

GESCHICHTEN (nur wenn es den Ordner geschichten/ gibt)
- Eine Geschichte = eine Datei geschichten/name.md. Erste Zeile «## Titel», darunter freiwillig
  «- stand: idee|entwurf|ueberarbeiten|fertig», «- stichworte: …», «- quelle: …», dann Leerzeile und Text.
- Im Buch bindet eine eigene Zeile «@@name» die Geschichte ein. @@-Zeilen nie umbenennen, verschieben
  oder löschen ohne Auftrag. In einer Geschichte selbst gibt es kein @@.
- Überarbeitest du eine Geschichte, ändere nur ihre Datei. Den Stand nur ändern, wenn der Mensch es sagt.

TABELLEN (nur wenn es den Ordner tabellen/ gibt)
- Eine Tabelle = eine CSV-Datei tabellen/name.csv. Zeile 1 Bezeichnung, Zeile 2 Spaltenüberschriften,
  ab Zeile 3 Werte, optional letzte Zeile «Quelle: …». Trenner ; (wie in der Datei), Zeichensatz UTF-8.
- Im Buch bindet eine eigene Zeile «@#name» die Tabelle ein (optional «@#name quer» oder «@#name hoch»).
  @#-Zeilen nie ändern ohne Auftrag. Werte nur in der CSV ändern, nie als Text ins Buch kopieren.
- Jede Zeile braucht gleich viele Werte wie Spaltenüberschriften.

DRUCK (nur wenn es den Ordner druck/ gibt)
- Eine Datei pro Druckvariante, z. B. druck/epubli-a5-normal.md, druck/bod-a5-hardcover.md. Werte als «- name: wert».
- Erlaubte Namen: plattform, format, seite, bindung, projekt, ruecken-hardcover, ruecken-softcover,
  beschnitt-buchblock, beschnitt-hardcover, beschnitt-softcover, deckel-hardcover, papier, extra-seiten,
  isbn-buch, barcode-position, barcode-groesse, barcode-bild. Masse in mm, z. B. «seite: 148 x 210».
- Welche Datei gilt, steht in der Variablen-Datei: druck-normal / druck-uz (Name ohne .md).
- Werte nur aus dem Coverrechner der Plattform übernehmen, nie schätzen. Danach «sh build.sh pruefen».

LESEPROBE (Variablen-Datei)
- leseprobe-seiten: 14,16,17-20,22  = gedruckte Seitenzahlen; leseprobe-seiten-uz: eigene für die zweite Ausgabe.
- Sonst leseprobe: Anzahl Kapitel oder Titel. Beides leer = 4 Seiten nach dem Inhaltsverzeichnis.

GRUNDREGELN FÜR ALLE MD-DATEIEN
- Gliederung mit # / ## / ###. Werte als Listenzeile:  - name: wert
- Namen von Werten (vor dem Doppelpunkt) nie ändern, nie erfinden. Nur den Wert danach.
- {name} im Text = Wert aus der Variablen-Datei, z. B. {titel}, {autor}. So stehen lassen.
- Eine Zeile mit leerer Variable fällt im Buch weg.
- name-normal / name-uz: Wert je Ausgabe (normale und zweite Ausgabe).
- Erklärende Sätze ohne «- » davor sind erlaubt.

BUCHTEXT (@@NAME@@-buch.md)
  # Teil 1|Titel|Untertitel     neuer Teil mit eigener Seite (genau diese Form mit |)
  # Titel                       Kapitel oberster Ebene, z. B. Anhang, Über den Autor
  ## Kapitel                    Kapitel (erscheint im Inhaltsverzeichnis)
  ### Zwischentitel             kleiner Titel
  Leerzeile                     neuer Absatz.   <br/> = Zeilenumbruch im Absatz
  > Zitat   ~ Notiz an mich   - Listenpunkt   **fett**   [Text](https://…)
  1. Aufzählung (zählt selbst)   «  - Unterpunkt» (eingerückt)   «3\. Mai» = Zahl ohne Aufzählung
  ## @BEFEHL                    Befehl als Überschrift, wirkt wie @BEFEHL

Blöcke: beginnen mit «::: art Titel», enden mit «:::» (eigene Zeile)
  Arten: nur, mitte, foto (alt), zusammen, offen, offen-notiz, widmung, zeitstrahl, uz
  Endung = nur in einer Ausgabe/Medium: -normal, -uz, -bildschirm, -druck, -ebook, -buch, -privatdruck
  Beispiel:  ::: nur-uz        (dieser Text nur in der zweiten Ausgabe)
Foto (ohne «:::»):  «#### @FOTO Titel», darunter Zeilen «- datei: bild.jpg» / «- text: Bildunterschrift» /
  «- alt: Bildbeschreibung» / «- breite: 60» / «- fluss: rechts» / «- quelle: Foto: Name».
  Der Foto-Block endet an der ersten Leerzeile.  «#### @FOTO-UZ Titel» = nur zweite Ausgabe.

Befehle (eine eigene Zeile, GROSS, genau so geschrieben):
  @TITEL @IMPRESSUM @HINWEIS @WIDMUNG @KERNSATZ Satz @INHALTSVERZEICHNIS   (als «## @…» geschrieben)
  @ZITAT Text  @MOTTO Text  @UNTEN Text  @KOPF Text
  @UMBRUCH  @UMBRUCH-RECHTS  @PLATZ 40  @ABSTAND 8  @SEITENMITTE
  @ZIER 12  @ZIER-UNTEN  @ZIER-TRENNER
  @QR url | Text   @QR-PAAR url | Text ;; url | Text   @PORTRAIT bild.png | Text
  @BILDNACHWEIS  @STICHWORTE  @RUECKSEITE
Keine anderen @-Befehle erfinden. Befehle nicht übersetzen, nicht verschieben ohne Auftrag.

UMSCHLAG (@@NAME@@-umschlag.md)
  Abschnitte ## Vorderseite, ## Buchrücken, ## Rückseite. Werte als - schluessel: wert
  (titel, untertitel, autor, stempel, stempel-farbe, fuss, bild, slogan, foto, text, auszug).
  Endung am Schlüssel = nur dort: fuss-druck, fuss-bildschirm, text-ebook, auszug-uz. «> …» = Erklärung. Text der Rückseite kurz halten.

WAS DER MOTOR MACHT (zur Info)
  sh build.sh            Entwurf: Bildschirm-PDF, Druckdateien, E-Book (offene Stellen sichtbar)
  sh build.sh schnell    nur Lese-PDFs (beim Schreiben)
  sh build.sh final      Druckfassung für epubli, mit Seitenbilanz, Shop-Angaben, Kontrast-Prüfung
  sh build.sh komplett   final + Leseprobe + Korrektur in einem Durchgang
  sh build.sh final druck=bod-a5-normal   Test: nur Druckdateien mit dieser Datei aus druck/ -> ausgabe-test/
  sh build.sh pruefen    prüft die MD: unbekannte Variablen, Befehle, fehlende Fotos (mit Zeilennummer)
  sh build.sh leseprobe  Leseprobe · sh build.sh korrektur  Korrekturfassung mit Zeilennummern
  sh neu.sh "Titel"      neue Geschichte · sh neu.sh tabelle "Titel"  neue Tabelle (Windows: neu.bat)
  sh sicherung.sh        ZIP-Sicherung
  sh update.sh           Motor-Update von GitHub (ersetzt nur motor/; «pruefen» = nur nachsehen)
                         Bei Fragen zu Fehlern im Motor: nicht motor/ ändern, sondern sh update.sh empfehlen.
  sh build.sh hilfe      hilfe.html erzeugen und öffnen (ganze Anleitung mit Suche; Quelle motor/HILFE.md)

SO ARBEITEST DU
- Schreibe in der Sprache, Rechtschreibung und im Ton des Buchs (in der Schweiz: ss statt ß).
- Gib ganze Abschnitte zurück oder nenne genau, welche Zeile du ersetzt. Nichts stillschweigend löschen.
- Bist du unsicher, frage nach, statt Regeln zu raten.
- Danach soll der Mensch «sh build.sh pruefen» laufen lassen.
