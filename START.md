# Start

## 1. Erstes PDF in fünf Minuten

Einmal von oben nach unten. Die Häkchen kannst du anklicken, der Browser merkt sie sich.
Oben rechts **Linux/Mac** oder **Windows** wählen, dann stimmen alle Befehle.

- [ ] **Terminal öffnen.** Linux: Strg+Alt+T · Mac: Cmd+Leertaste, «Terminal» · Windows: Start, «PowerShell».
  Dann in den Ordner pureSATZ wechseln (Ordner ins Fenster ziehen setzt den Pfad ein):

```sh
cd "Pfad/zu/pureSATZ"
```

- [ ] **Python da?** Es braucht Python 3.10 oder neuer. Fehlt es oder ist es älter: einfach weiter mit dem nächsten Punkt.

```sh
python3 --version
```

- [ ] **Computer einrichten** (einmalig). Prüft alles und installiert, was fehlt. Windows: die Datei im Ordner
  `pc-einrichten` auch einfach doppelklicken. Danach das Terminal schliessen und neu öffnen.

```sh
bash pc-einrichten/linux-einrichten.sh     # Linux
bash pc-einrichten/mac-einrichten.sh       # Mac
```

- [ ] **Hallo-Buch.** Legt neben pureSATZ ein Beispielbuch an, baut es und öffnet das PDF. Beim ersten Mal etwa
  eine Minute (Internet nötig), danach wenige Sekunden. Windows: `hallo.bat` auch einfach doppelklicken.

```sh
sh hallo.sh
```

- [ ] **Selbst ändern.** Im Ordner `Hallo-Buch` die Datei `Hallo-Buch-buch.md` öffnen, einen Satz ändern,
  speichern, dann neu bauen. Oder in `tabellen/muster.csv` eine Zahl ändern und die Tabelle im PDF ansehen. Das PDF liegt in `Hallo-Buch/ausgabe-normal/`.

```sh
cd ../Hallo-Buch
sh build.sh schnell
```

- [ ] **Sichern.** Dein Text wird bei jedem Bau automatisch nach `md-history/` gesichert (mit Datum und Uhrzeit).
  Das ganze Buch als ZIP nach `../Sicherungen`: im Buchordner

```sh
sh sicherung.sh
```

- [ ] **Eigenes Buch.** Zurück im Ordner pureSATZ: fragt Titel, Autor, Format und legt dein Buch an.
  Das Hallo-Buch darf danach gelöscht werden.

```sh
sh setup/setup.sh
```

Weiter geht es mit **Mein erstes Buch** (fünf Schritte bis zur Bestellung) und mit der Hilfe im Buchordner
(`hilfe.html`, neu mit `sh build.sh hilfe`).

## 2. Computer einrichten

Einmalig. Prüft Python und alles Nötige und installiert, was fehlt.
**Erfolg:** Am Schluss steht «alles bereit». Danach das Terminal schliessen und neu öffnen.

```sh
bash pc-einrichten/linux-einrichten.sh     # Linux
bash pc-einrichten/mac-einrichten.sh       # Mac
```

Windows: im Ordner `pc-einrichten` die Datei `win-einrichten.bat` doppelklicken.
Details: Punkt 1, «Computer einrichten».

## 3. Hallo-PDF

Ein Befehl im Ordner pureSATZ legt das Beispielbuch «Hallo-Buch» an, baut es und öffnet das PDF.
**Erfolg:** Das erste Buch-PDF ist offen. Beim ersten Mal etwa eine Minute (Internet nötig).

```sh
sh hallo.sh
```

Windows: `hallo.bat` doppelklicken. Das PDF liegt in `Hallo-Buch/ausgabe-normal/`.

## 4. Dein Buch bauen

1. **Anlegen** (im Ordner pureSATZ): fragt Titel, Autor, Format. `sh setup/setup.sh`
2. **Schreiben** in `<buch>-buch.md`, Angaben in `<buch>-variablen.md`, Umschlag in `<buch>-umschlag.md`.
3. **Ansehen** (im Buchordner): `sh build.sh schnell` – nur das Lese-PDF, in Sekunden.
4. **Alles bauen**: `sh build.sh` (Entwurf) bzw. `sh build.sh final` (Druckfassung).
5. **Welche Datei wofür?** Im Ausgabeordner zuoberst `00-UEBERSICHT.txt` öffnen: was zur Druckerei geht,
   was ins E-Book, was für Werbung und Probedruck.

**Erfolg:** Druckdateien, E-Book und Lese-PDF deines Buchs. Weiter: Hilfe «Bauen» und «Drucken und veröffentlichen».

```sh
sh build.sh final
```

## 5. Wenn etwas klemmt

| Meldung | Was tun |
|---|---|
| Windows: Ordner `pureSATZ-main` steckt in einem zweiten `pureSATZ-main` | Den inneren Ordner nehmen, an einen guten Ort verschieben (z. B. Dokumente) und in `pureSATZ` umbenennen. |
| `python3: command not found` / «nicht erkannt» | Punkt «Computer einrichten». Windows: Python von python.org, beim Installieren «Add python.exe to PATH» anhaken. |
| «Python … ist zu alt» | Neues Python installieren (3.10 oder neuer), Terminal neu öffnen. |
| Hängt beim ersten Mal / «keine Verbindung» | Der erste Bau lädt Pakete aus dem Internet. Verbindung prüfen, nochmals starten. |
| PDF öffnet sich nicht | Es liegt trotzdem da: `Hallo-Buch/ausgabe-normal/`. |
| Windows: «Ausführung von Skripts deaktiviert» | Die `.bat`-Dateien nehmen (z. B. `.\hallo.bat`), nicht `.sh`. |
| Welche Datei soll ich hochladen? | `00-UEBERSICHT.txt` im Ausgabeordner zeigt es, mit FINAL oder ENTWURF und Datum. |
| `sh build.sh pruefen` meldet einen Fehler | Die Meldung nennt Datei und Zeile. Meist ein Tippfehler bei `{variable}` oder `@BEFEHL`. |
| Druckdatei fehlt («Druckangaben: … fehlt») | Name bei `druck-normal` / `druck-uz` prüfen (ohne `.md`), Muster in `pureSATZ/vorlage/druck/`. |
| Etwas anderes | Die Meldung kopieren und in die Suche oben eingeben, oder einer KI zeigen (mit `readme4ki.txt`). |
