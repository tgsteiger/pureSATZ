# CHECKLISTE vor der Bestellung
Zum Abhaken: «- [ ]» wird zu «- [x]». Reihenfolge von oben nach unten.

## 1. Text
- [ ] Ganzes Buch einmal am Stück gelesen (Bildschirm-PDF)
- [ ] Probedruck-Booklet ausgedruckt und auf Papier gelesen (`sh build.sh final`, Datei `…_Probedruck_booklet.pdf`)
- [ ] Korrekturfassung gelesen oder weitergegeben (`sh build.sh korrektur`, Zeilennummern für Rückmeldungen)
- [ ] Jemand anderes hat gegengelesen
- [ ] Keine offenen Stellen mehr (Liste am Ende von `sh build.sh`)
- [ ] Stichwortverzeichnis angeschaut (`stichworte-<buch>.txt`)

## 2. Seiten und Bilder
- [ ] Seitenbilanz angeschaut (am Ende von `sh build.sh final`): wenige Füll- und Leerseiten
- [ ] Fotos scharf genug (siehe `fotos/readme.txt`), im Probedruck kontrolliert
- [ ] Bildrechte geklärt: eigene Fotos oder Erlaubnis; fremde Fotos mit `quelle:` (Bildnachweis)
- [ ] Personen auf Fotos und im Text einverstanden

## 3. Angaben (Variablen-Datei)
- [ ] Titel, Untertitel, Autor, Jahr, Auflage stimmen
- [ ] Impressum geprüft (Verlag, Adresse, Hinweis)
- [ ] Format und Bindung gewählt
- [ ] Rückenbreite laut epubli-Coverrechner eingetragen (Seitenzahl des Buchblocks eingeben)
- [ ] Shop-Angaben: Beschreibung, Schlagwörter, Kategorie, Preis

## 4. epubli
- [ ] Testexemplar als Privatdruck bestellt und geprüft (`projekt-normal: privatdruck`)
- [ ] «Buch veröffentlichen»: Buchblock und Umschlag hochgeladen
- [ ] ISBN von epubli bei `isbn-buch:` eingetragen, neu gebaut, Buchblock ersetzt (gleiche Seitenzahl!)
- [ ] Vorschau bei epubli kontrolliert (Umschlag, Rücken, Strichcode)

## 5. E-Book
- [ ] Eigene ISBN fürs E-Book bei `isbn-ebook:` (oder bewusst ohne)
- [ ] E-Book auf einem Lesegerät oder in einer App angeschaut
- [ ] Hochgeladen: eigener Shop / tolino media / KDP

## 6. Nach dem Erscheinen
- [ ] Belegexemplare an die Schweizerische Nationalbibliothek: **2 Exemplare**, selbst schicken
      (epubli schickt nichts). Für Bücher mit Schweizer Bezug, als Schenkung.
      Adresse: Schweizerische Nationalbibliothek, Erwerbung, Hallwylstrasse 15, 3003 Bern
- [ ] Bei Verkauf in Deutschland: Ablieferung an die Deutsche Nationalbibliothek klären (epubli macht es nicht)
- [ ] Website / Shop / Newsletter: Buch eintragen, Leseprobe verlinken (`sh build.sh leseprobe`)
- [ ] Sicherung: `sh sicherung.sh` (lokal und cloud)
