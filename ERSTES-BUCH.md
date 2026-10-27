# Mein erstes Buch – in fünf Schritten

*Nur schnell sehen, wie ein Buch aussieht?* Im Ordner pureSATZ `sh hallo.sh` (Windows: `hallo.bat`
doppelklicken). Klappt etwas nicht: Checkliste in `START.md`.

Für alle, die ein Buch schreiben möchten, auch ohne Erfahrung mit Linux. Ein Terminal öffnen
(Linux: Strg+Alt+T), dann die Befehle Zeile für Zeile eintippen und mit Enter bestätigen.

## 1. Einmalig vorbereiten
**Am einfachsten:** Windows `start.bat` · Mac `start.command` doppelklicken · Linux `sh start.sh` im Ordner
pureSATZ. Der Start erledigt die Schritte 1 und 2: fester Ort (`Buchprojekte`), Einrichten, Hallo-Buch, eigenes Buch.
Von Hand geht es so:
Im Ordner pureSATZ das Einrichte-Skript starten – es prüft alles, installiert, was fehlt, und fragt,
ob du mit GitHub arbeiten willst (freiwillig):
```sh
bash pc-einrichten/linux-einrichten.sh        # Linux
bash pc-einrichten/mac-einrichten.sh          # Mac
```
Windows: `pc-einrichten\win-einrichten.bat` doppelklicken. Danach `setup\setup.bat` und `build.bat` statt `sh setup/setup.sh` und `sh build.sh`. Alles Weitere, auch GitHub und ein zweiter Computer: **`INSTALLATION.md`**.

## 2. Ein neues Buch anlegen

*Schon in LibreOffice oder Word geschrieben?* Dann geht auch `sh import/import-text.sh manuskript.odt` (Testphase,
siehe `INSTALLATION.md`). Sonst:

```sh
cd "Pfad/zu/pureSATZ"
sh setup/setup.sh
```
Das Programm fragt Titel, Autor, einen kurzen technischen Namen (z. B. `Mein-Buch`), Format und
Bindung ab. Daneben entsteht der Ordner `Mein-Buch` mit vier Dateien:

- `Mein-Buch-variablen.md` – Angaben zum Buch (Titel, ISBN, Format, Farben)
- `Mein-Buch-buch.md` – hier schreibst du (ein Demo-Kapitel zeigt alle Möglichkeiten)
- `Mein-Buch-umschlag.md` – Texte für Vorder- und Rückseite
- `stichworte-Mein-Buch.txt` – Stichwortverzeichnis

## 3. Schreiben
Die MD-Dateien mit einem Markdown-Editor öffnen (z. B. ghostwriter, Typora oder einem einfachen
Texteditor). Erst das Demo ansehen, dann löschen und eigenen Text schreiben.
Fotos kommen in den Ordner `fotos/` (Hinweise zur Grösse: `fotos/readme.txt`).

*Eine Tabelle?* Das Demo-Kapitel zeigt eine (`tabellen/muster.csv`). `sh neu.sh tabelle "Titel"` legt in `tabellen/` eine CSV-Datei an (mit LibreOffice bearbeiten,
als «Text CSV» speichern); im Buch bindet eine Zeile `@#name` sie ein.

*Lieber einzelne Geschichten?* `sh neu.sh "Titel"` legt in `geschichten/` eine eigene Datei an; im Buch
bindet eine Zeile `@@name` sie ein. Übersicht: `sh neu.sh` oder `geschichten-uebersicht.html` im Browser.

## 4. Anschauen
```sh
cd "Pfad/zu/Mein-Buch"
sh build.sh
```
Beim ersten Mal wird einmalig eine Python-Umgebung eingerichtet (Internet nötig, ca. 1 Minute).
Danach liegt das PDF im Ordner `ausgabe-normal/`. Nach jeder Änderung: einfach wieder `sh build.sh`.
Welche Datei wofür ist (Druckerei, E-Book, Werbung, Probedruck), steht zuoberst in `ausgabe-normal/00-UEBERSICHT.txt`.

## 5. Drucken lassen
```sh
sh build.sh final
```
- Das **Probedruck-Booklet** ausdrucken (A4, doppelseitig, kurze Kante) und auf Papier lesen.
- Die `CHECKLISTE.md` im Buchordner Punkt für Punkt abhaken.
- Bei epubli: `…_Buchblock.pdf` und `…_Umschlag_Hardcover.jpg` (bzw. Softcover) hochladen – `00-UEBERSICHT.txt` zeigt sie unter «Bei der Druckerei hochladen».
- Andere Plattform (BoD, KDP …) oder nur E-Book (XinXii, tolino …): Hilfe, Gruppe «Andere Plattformen».
- Die Texte für den Shop stehen in `ausgabe-normal/shop-angaben.txt`.

Zwischendurch sichern: `sh sicherung.sh` (Ziele in der Variablen-Datei unter `# TECHNIK`).
Mit einer anderen KI arbeiten: ihr zuerst `readme4ki.txt` geben, dann die MD-Datei.

Mehr Hilfe: `README.md` im Buchordner. Wenn etwas nicht klappt, meldet `sh build.sh` den Fehler
mit Zeilennummer – meistens ist es ein Tippfehler in einer Variablen oder einem Befehl.
