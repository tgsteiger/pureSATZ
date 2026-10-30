# Start

## 1. Erstes PDF in fünf Minuten

Einmal von oben nach unten. Die Häkchen kannst du anklicken, der Browser merkt sie sich.
Oben rechts **Linux/Mac** oder **Windows** wählen, dann stimmen alle Befehle.

- [ ] **Starten.** ZIP auspacken (Windows: Rechtsklick → «Alle extrahieren …»), dann im Ordner pureSATZ:
  Windows `START-Windows.bat` doppelklicken · Mac `START-Mac.command` doppelklicken (blockiert der Mac es: Rechtsklick →
  Öffnen, oder Systemeinstellungen → Datenschutz & Sicherheit → «Dennoch öffnen») · Linux: Rechtsklick in den Ordner →
  «Im Terminal öffnen», dann `sh START-Linux.sh` eintippen. Er führt in fünf Schritten durch: Technik (Python), Ort für die Bücher (`Buchprojekte` im Benutzerordner – nicht Downloads, nicht in einer Cloud), Hallo-Buch, dein eigenes Buch (Titel, Untertitel, Autor, Format) und Extras (GitHub, freiwillig). Enter nimmt jeweils den Vorschlag.

Danach sieht es so aus – geschrieben und gebaut wird immer im Ordner deines Buchs, nie in pureSATZ:

```
Buchprojekte/
  pureSATZ/      die Werkstatt – hier nichts schreiben
  Hallo-Buch/    zum Ausprobieren, darf weg
  Mein-Buch/     dein Buch – hier schreibst und baust du
```

- [ ] **Terminal im Buchordner.** Windows und Mac: im Buchordner `Terminal hier` doppelklicken – das Befehlsfenster
  öffnet sich genau dort (Windows: cmd). Linux: Rechtsklick in den Ordner → «Im Terminal öffnen».

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

- [ ] **Eigenes Buch.** Fragt der Start nach dem Hallo-Buch schon (Enter = ja). Sonst im Ordner pureSATZ:
  fragt Titel, Autor, Format und legt dein Buch neben pureSATZ an. Das Hallo-Buch darf danach gelöscht werden.

```sh
sh setup/setup.sh
```

Weiter geht es mit **Mein erstes Buch** (fünf Schritte bis zur Bestellung) und mit der Hilfe im Buchordner
(`hilfe.html`, neu mit `sh build.sh hilfe`).

### Von Hand, falls der Start nicht klappt

- **Terminal öffnen.** Linux: Strg+Alt+T · Mac: Cmd+Leertaste, «Terminal» · Windows: im Explorer in die Adresszeile `cmd` tippen, Enter.
  Dann in den Ordner pureSATZ wechseln (Ordner ins Fenster ziehen setzt den Pfad ein):

```sh
cd "Pfad/zu/pureSATZ"
```

- **Python da?** Es braucht Python 3.10 oder neuer. Fehlt es oder ist es älter: einfach weiter mit dem nächsten Punkt.

```sh
python3 --version
```

- **Computer einrichten** (einmalig). Prüft alles und installiert, was fehlt. Windows: die Datei im Ordner
  `pc-einrichten` auch einfach doppelklicken. Danach das Terminal schliessen und neu öffnen.

```sh
bash pc-einrichten/linux-einrichten.sh     # Linux
bash pc-einrichten/mac-einrichten.sh       # Mac
```

- **Hallo-Buch.** Legt neben pureSATZ ein Beispielbuch an, baut es und öffnet das PDF. Beim ersten Mal etwa
  eine Minute (Internet nötig), danach wenige Sekunden. Windows: `hallo.bat` auch einfach doppelklicken.

```sh
sh hallo.sh
```

## 2. Computer einrichten

Einmalig – macht der Start (Punkt 1) automatisch. Prüft Python und alles Nötige und installiert, was fehlt.
GitHub ist freiwillig und kommt am Schluss. **Erfolg:** Am Schluss steht «=== Fertig ===».

```sh
bash pc-einrichten/linux-einrichten.sh     # Linux
bash pc-einrichten/mac-einrichten.sh       # Mac
```

Windows: im Ordner `pc-einrichten` die Datei `win-einrichten.bat` doppelklicken. Fehlt Python, installiert sie es und
macht gleich weiter (wenn nötig in einem neuen Fenster). Details: Punkt 1, «Von Hand».

## 3. Dein Buch bauen

1. **Anlegen** (macht der Start, sonst im Ordner pureSATZ): fragt Titel, Autor, Format. `sh setup/setup.sh`
   Ab dann arbeitest du im Buchordner – `Terminal hier` doppelklicken öffnet das Befehlsfenster dort.
2. **Schreiben** in `<buch>-buch.md`, Angaben in `<buch>-variablen.md`, Umschlag in `<buch>-umschlag.md`.
3. **Ansehen** (im Buchordner): `sh build.sh schnell` – nur das Lese-PDF, in Sekunden.
4. **Alles bauen**: `sh build.sh` (Entwurf) bzw. `sh build.sh final` (Druckfassung).
   Vor Bestellung oder Veröffentlichung: `sh build.sh komplett` (dazu Leseprobe und Korrektur-PDF).
5. **Welche Datei wofür?** Im Ausgabeordner zuoberst `00-UEBERSICHT.txt` öffnen: was zur Druckerei geht,
   was ins E-Book, was für Werbung und Probedruck.
6. **Stand festhalten** an wichtigen Punkten, z. B. bei einer Bestellung: `sh build.sh stand "Probedruck 1"`.
   Später zeigt `sh build.sh aenderungen` als PDF, was sich seither geändert hat.

**Erfolg:** Druckdateien, E-Book und Lese-PDF deines Buchs. Weiter: Hilfe «Bauen» und «Drucken und veröffentlichen».

```sh
sh build.sh final
```

## 4. Gestalten: Ich will …

Die häufigsten Fälle beim Gestalten – nachsehen, wenn etwas nicht so aussieht wie gewünscht.
Danach mit `sh build.sh schnell` ansehen.

| Ich will … | So geht es |
|---|---|
| eine **neue Seite** | `---` auf einer eigenen Zeile, davor eine Leerzeile. **Nicht innerhalb eines `:::`-Blocks**, sondern nach dem `:::`. Steht `---` schon oben auf einer Seite, entsteht keine leere Seite. |
| **mehr Abstand** | `@ABSTAND 8` (in mm). Mehrere Leerzeilen geben *nicht* mehr Abstand. Nicht innerhalb eines `:::`-Blocks. |
| einen Satz **ganz unten** auf der Seite | `@UNTEN Satz` – zentriert und kursiv, z. B. für einen Hinweis |
| einen **schönen Schluss** (Gruss, Zitat) | `@ZITAT Schön, dass du da bist.<br/>Herzlich, Name`, darunter `@ZIER 10` |
| ein Zitat **mit Verzierung** | `@ZITAT-ZIER Satz` (kurz `> Satz`). Nur eine Verzierung pro Seite – sonst wird es unruhig. |
| einen kurzen **Abschluss am Teil-Ende** | `::: mitte` … `:::` |
| eine **Dankesseite oder ein Nachwort** im Inhaltsverzeichnis | als Kapitel `## Danke`, Text im Blocksatz, zum Schluss `@ZITAT` und `@ZIER 10` |
| einen **Zwischentitel** ohne Eintrag im Inhaltsverzeichnis | `### Titel` (`## Titel` erscheint im Inhalt) |
| eine **Randbemerkung** | `~ Satz` (klein, kursiv) |
| eine **Zeile umbrechen**, ohne neuen Absatz | `\` am Zeilenende (in Variablen: `<br/>`) |
| Text **nur in einer Fassung** | `::: nur-uz` … `:::` oder `::: nur-normal` … `:::` |
| ein **Foto** | `#### @FOTO Titel`, darunter `datei: bild.jpg` – eine Leerzeile beendet das Foto |
| einen **QR-Code** | `@QR https://… \| Text`, zwei nebeneinander mit `@QR-PAAR` |
| sehen, **ob es passt** | `sh build.sh schnell`, dann das PDF öffnen (der Befehl steht am Ende des Baus) |

Alle Befehle: Hilfe «Befehle (@)» und «Blöcke (:::)».

## 5. Wenn etwas klemmt

| Meldung | Was tun |
|---|---|
| Windows: Ordner `pureSATZ-main` steckt in einem zweiten `pureSATZ-main` | Im inneren Ordner `START-Windows.bat` doppelklicken – er kopiert pureSATZ an den richtigen Ort (`Buchprojekte`) und benennt ihn richtig. |
| Windows: Python nach der Installation «nicht erkannt» | Fenster schliessen, `START-Windows.bat` nochmals doppelklicken. Hilft das nicht: Computer neu starten. |
| Mac: «START-Mac.command kann nicht geöffnet werden» | Rechtsklick → Öffnen, oder Systemeinstellungen → Datenschutz & Sicherheit → «Dennoch öffnen». Oder im Terminal `sh START-Linux.sh`. |
| `python3: command not found` / «nicht erkannt» | Punkt «Computer einrichten». Windows: Python von python.org, beim Installieren «Add python.exe to PATH» anhaken. |
| «Python … ist zu alt» | Neues Python installieren (3.10 oder neuer), Terminal neu öffnen. |
| Hängt beim ersten Mal / «keine Verbindung» | Der erste Bau lädt Pakete aus dem Internet. Verbindung prüfen, nochmals starten. |
| PDF öffnet sich nicht | Es liegt trotzdem da: `Hallo-Buch/ausgabe-normal/`. |
| Windows: «Ausführung von Skripts deaktiviert» | Das ist PowerShell. cmd nehmen (`Terminal hier` doppelklicken) und die `.bat`-Dateien starten (z. B. `hallo.bat`), nicht `.sh`. |
| Welche Datei soll ich hochladen? | `00-UEBERSICHT.txt` im Ausgabeordner zeigt es, mit FINAL oder ENTWURF und Datum. |
| `sh build.sh pruefen` meldet einen Fehler | Die Meldung nennt Datei und Zeile. Meist ein Tippfehler bei `{variable}` oder `@BEFEHL`. |
| Plattform-Datei fehlt («Druckangaben: … fehlt») | Name bei `{druck-datei}` unter `## Ausgabe: Druck …` prüfen (ohne `.md`), Muster in `pureSATZ/vorlage/druck/`. |
| Druckerei meldet «nicht eingebettete Schriften» | Motor aktualisieren und neu bauen (`sh update.sh`, dann `sh build.sh final`). Der Bau warnt selbst, falls noch eine Schrift fehlt. |
| Meine Änderung ist wieder weg | Editor: «Auto save» aus. Beim Hinweis «Datei geändert» neu laden. Ändert eine KI oder ein Skript die Datei, sie vorher im Editor schliessen. Ältere Fassungen liegen in `md-history/`. |
| Abstand oder neue Seite wirkt nicht | Steht der Befehl innerhalb eines `:::`-Blocks? Dann nach das `:::` setzen. |
| Farben am Bildschirm unsicher | Am Probedruck auf Papier beurteilen, nicht am Bildschirm. |
| Etwas anderes | Die Meldung kopieren und in die Suche oben eingeben, oder einer KI zeigen (mit `readme4ki.txt`). |

## 6. Fahrplan: vom Manuskript zum fertigen Buch

Zum Abhaken – der Browser merkt sich die Häkchen. «drucken» oben rechts druckt nur diesen Fahrplan.
Mit einem Zieldatum (freiwillig, z. B. Erscheinen oder Vernissage) zeigt jede Kachel, bis wann der Schritt spätestens
fertig sein sollte. Dauer und Wochen stehen in `pureSATZ/START.md`, z. B. `{⏱ 3–6 Wochen · fertig −8}` = 8 Wochen vor
dem Ziel; die Zahlen sind grobe Erfahrungswerte und lassen sich anpassen.
**Zwei Probedrucke** sind eingeplant: Der zweite kommt ca. 10 Tage nach Erhalt des ersten, mit allen Korrekturen.

::: kacheln
1. [ ] **Lektorat durch einen Menschen:** Jemand liest Sprache, Stil und Logik – nicht nur Rechtschreibung. Nicht vergessen! Dafür das Korrektur-PDF: `sh build.sh korrektur`. {⏱ 3–6 Wochen · fertig −10}
2. [ ] **Gegenlesen:** Personen im Buch fragen und ihre Stellen schicken: `sh build.sh personen Name`. Einwilligungen einholen. {⏱ 2–3 Wochen · fertig −10}
3. [ ] **Ort reservieren:** Raum für Vernissage oder Lesung – früh, beliebte Orte sind schnell weg. {⏱ 2–3 Monate vorher · fertig −12}
4. [ ] **Gäste und Moderation:** Wer führt durch den Anlass? Gäste oder Referenten anfragen und bestätigen lassen. {⏱ 1–2 Wochen · fertig −10}
5. [ ] **Newsletter 1:** Ankündigung, Leseprobe (`sh build.sh leseprobe`), Einladung mit Anmeldung. {⏱ 1–2 Tage · fertig −8}
6. [ ] **Probedruck 1 bestellen:** `sh build.sh final`, hochladen, bestellen. Stand festhalten: `sh build.sh stand "Probedruck 1"`. {⏱ Lieferung 1–2 Wochen · fertig −65 Tage}
7. [ ] **Sichtbar werden:** Buchseite auf der Webseite, Mockup und Shop-Texte (`shop-angaben.txt`), soziale Medien. {⏱ laufend · fertig −6}
8. [ ] **Probedruck 1 lesen und korrigieren:** auf Papier lesen – Farben, Umschlag und Rücken, Ränder, Bilder, Trennungen. Korrekturen eintragen, mit `sh build.sh aenderungen` kontrollieren. {⏱ ca. 10 Tage · fertig −45 Tage}
9. [ ] **Probedruck 2 bestellen:** ca. 10 Tage nach Erhalt des ersten, mit allen Korrekturen: `sh build.sh final`, hochladen, bestellen. {⏱ Lieferung 1–2 Wochen · fertig −45 Tage}
10. [ ] **Probedruck 2 prüfen:** nur noch kontrollieren, ob die Korrekturen sitzen. Ist alles gut: freigeben. {⏱ ca. 1 Woche · fertig −30 Tage}
11. [ ] **Druckfreigabe und Bücher bestellen:** Seitenzahl im Coverrechner prüfen, ISBN und Preis kontrollieren, `final` hochladen, freigeben. Menge für Geschenke, Anlass und Reserve. {⏱ bis die Bücher da sind 2–3 Wochen · fertig −4}
12. [ ] **E-Book:** hochladen; die Leseprobe (PDF/EPUB) auf die eigene Webseite stellen. {⏱ bis sichtbar in den Shops 1–3 Wochen · fertig −4}
13. [ ] **Newsletter 2 «Es ist da»:** Buchseite sichtbar, wie man das Buch bekommt, Erinnerung an den Anlass. {⏱ 1 Tag · fertig −2}
14. [ ] **Geschenke verteilen:** Exemplare an Familie, Personen im Buch, Helfende; Beitrag im Google-Unternehmensprofil. {⏱ 1–2 Wochen · fertig −2}
15. [ ] **Erinnerung an die Angemeldeten:** kurzes Mail mit Zeit, Ort, Anfahrt. {⏱ 1 Stunde · fertig −1}
16. [ ] **Vernissage oder Lesung:** Ablauf und Rollen (Moderation, Büchertisch und Kasse, Fotos, Apéro), Lesestellen laut üben, genug Bücher, Bezahlung (bar/TWINT), Stift zum Signieren. {⏱ der grosse Tag · fertig 0}
17. [ ] **Pflichtexemplare:** Schweiz: zwei Exemplare an die Nationalbibliothek; Deutschland: an die DNB. Prüfen, ob die Druckerei das übernimmt. {⏱ 1 Woche · fertig +1}
18. [ ] **Danach:** Dank-Mail an die Gäste, Rückmeldungen und Rezensionen sammeln, nachbestellen, Fehler für eine zweite Auflage notieren (`stand`). {⏱ laufend · fertig +4}
:::

## Tipp: Menü statt Befehle

Im Buchordner `sh menu.sh` (Windows: `menu.bat` doppelklicken). Dann genügt ein Buchstabe – geordnet nach
Schreiben (`m` MD öffnen, `g` Geschichten, `t` Tabellen, `c` gegenlesen), Bauen (`s` schnell, `k` komplett,
`w` weitere), Ansehen (`p` PDF, `o` Ordner) und Abgleichen (`sy` sync, `u` update); `n` neu (neues Buch,
Hallo-Buch, `v` Lotus-Starter). `:` zeigt Befehle zum Tippen, `h` oder `?` die Hilfe.
Mit ↑ holst du die letzten Befehle zurück, `q` beendet.

Mehr dazu in der Hilfe unter «Bauen → Menü».
