# Erste Schritte

## 1. Erstes PDF in fünf Minuten

ZIP ganz auspacken (Windows: Rechtsklick → «Alle extrahieren …»), dann im Ordner pureSATZ den Start aufrufen:

- **Linux:** Rechtsklick in den Ordner → «Im Terminal öffnen», dann `sh START-Linux.sh`
- **Mac:** Terminal öffnen (Cmd+Leertaste, «Terminal»), `sh ` tippen, `START-Mac-imTerminal.sh` ins Fenster ziehen, Enter
- **Windows:** `START-Windows.bat` doppelklicken

Der Start führt in fünf Schritten zum eigenen Buch. Enter nimmt immer den Vorschlag; er darf beliebig oft laufen.

1. **Technik.** Prüft Python (3.10 oder neuer) und installiert, was fehlt. Beim ersten Mal braucht es Internet.
2. **Ort.** Schlägt einen festen Ordner für deine Bücher vor: `Buchprojekte` im Benutzerordner – nicht Downloads,
   Schreibtisch oder eine Cloud. pureSATZ wird dorthin kopiert; den ausgepackten Ordner darfst du danach löschen.
   `n` lässt pureSATZ, wo es ist.
3. **Hallo-Buch.** Legt ein Beispielbuch an, baut es und öffnet das PDF. So siehst du, was pureSATZ macht.
4. **Dein Buch.** Fragt Titel, Untertitel, Autor und Format, legt den Buchordner neben pureSATZ an und öffnet ihn.
5. **Extras.** GitHub (freiwillig: Sicherung im Netz, Abgleich zwischen Computern) und Ghostscript (empfohlen).
   Beides geht auch später.

Klemmt etwas: [→ Wenn etwas klemmt](#Wenn-etwas-klemmt) oder unten «Von Hand».

Danach sieht es so aus (steht auch in `00-UEBERSICHT.txt`) – geschrieben und gebaut wird immer im Ordner deines
Buchs, nie in pureSATZ:

```
Buchprojekte/
  pureSATZ/      die Werkstatt – hier nichts schreiben
  Hallo-Buch/    zum Ausprobieren, darf weg
  Mein-Buch/     dein Buch – hier schreibst und baust du
```

Im Ordner deines Buchs das Menü öffnen – ein Buchstabe genügt, `s` baut das Lese-PDF in Sekunden:

```sh
sh menu.sh
```

::: nur-webhilfe
Zum Abhaken einmal von oben nach unten (die Häkchen merkt sich der Browser). Oben rechts **Linux/Mac** oder
**Windows** wählen, dann stimmen alle Befehle.
:::

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

**Erfolg:** Druckdateien, E-Book und Lese-PDF deines Buchs. Weiter: Hilfe «Bauen und Drucken».

```sh
sh build.sh final
```

## 4. Wenn etwas klemmt

| Meldung | Was tun |
|---|---|
| Windows: Ordner `pureSATZ-main` steckt in einem zweiten `pureSATZ-main` | Im inneren Ordner `START-Windows.bat` doppelklicken – er kopiert pureSATZ an den richtigen Ort (`Buchprojekte`) und benennt ihn richtig. |
| Windows: Python nach der Installation «nicht erkannt» | Fenster schliessen, `START-Windows.bat` nochmals doppelklicken. Hilft das nicht: Computer neu starten. |
| Mac: Doppelklick auf eine Startdatei geht nicht («kann nicht geöffnet werden») | Der Mac sperrt heruntergeladene Dateien. Im Terminal starten: `sh ` tippen, `START-Mac-imTerminal.sh` ins Fenster ziehen, Enter. Danach gehen `Terminal hier` und der Lotus per Doppelklick. |
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
| Abstand oder neue Seite wirkt nicht | Steht der Befehl innerhalb eines `@DECORATE-REST`- oder `@UC-BLOCK`-Bereichs? Dann nach das `@END` setzen. |
| Farben am Bildschirm unsicher | Am Probedruck auf Papier beurteilen, nicht am Bildschirm. |
| Etwas anderes | Die Meldung kopieren und in die Suche oben eingeben (im Menü: `hf wort`), oder einer KI zeigen (mit `hilfe-ki.md`). |

## 5. Fahrplan: vom Manuskript zum fertigen Buch

::: nur-webhilfe
Zum Abhaken – der Browser merkt sich die Häkchen. «drucken» oben rechts druckt nur diesen Fahrplan.
Mit einem Zieldatum (freiwillig, z. B. Erscheinen oder Vernissage) zeigt jede Kachel, bis wann der Schritt spätestens
fertig sein sollte. Dauer und Wochen stehen in `pureSATZ/START.md`, z. B. `{⏱ 3–6 Wochen · fertig −8}` = 8 Wochen vor
dem Ziel; die Zahlen sind grobe Erfahrungswerte und lassen sich anpassen.
:::
::: nur-handbuch
Zum Abhaken. Die Hilfe (`hilfe.html`) zeigt zu jedem Schritt Dauer und spätestes Datum, wenn du ein Zieldatum eingibst.
:::
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
Schreiben (`m` MD öffnen, `g` Geschichten, `t` Tabellen, `c` gegenlesen), Bauen (`s` schnell, `f` final,
`k` komplett), Ansehen (`p` PDF, `o` Ordner) und Abgleichen / Prüfen (`sy` sync, `u` update, `bp` Buch prüfen); `n` neu (neues Buch,
Hallo-Buch, `v` Lotus-Starter für Menü und Hilfe). `:` zeigt Befehle zum Tippen, `h` oder `?` die Hilfe.
Mit ↑ holst du die letzten Befehle zurück, Enter (oder `z`) = eine Stufe zurück (im Hauptmenü: «beenden? [j/N]»).

Mehr dazu in der Hilfe unter «Erste Schritte → Menü».

# Gestalten

## Gestalten: Ich will …

Die häufigsten Fälle beim Gestalten. Danach mit `s` (Menü) bzw. `sh build.sh schnell` ansehen.
Ganze Bausteine: [Zum Kopieren](#Zum-Kopieren).

::: nur-webhilfe
**Klick auf einen Code = kopiert.** Suchen: Taste `/`.
:::

**So sind alle Befehle gebaut:** `@NAME-GRÖSSE-ORT Text` – alles vor dem ersten Leerzeichen ist der Befehl
(gross geschrieben), danach kommt der Text. Zahlen sind immer mm. Angeben musst du nur, was vom Standard abweicht.

| Ortswort | heisst |
|---|---|
| (keins) | hier im Text |
| `REST` | in die Mitte des Rests der Seite, danach neue Seite |
| `BOTTOM` | unten auf die Seite (`BOTTOM-34` = 34 mm über dem Ende des Textes), danach neue Seite |
| `PAGE` | auf eine eigene Seite |
| `GAP` | in die Lücke vor der nächsten Überschrift |
| `RIGHT` · `LEFT` | daneben, der Text fliesst herum |

### Text

| Ich will … | So |
|---|---|
| Text **hervorheben** | `**fett**` · `*kursiv*` mitten im Text. [→ fett und kursiv](#Text-hervorheben) |
| eine **Zeile umbrechen**, ohne neuen Absatz | `\` am Zeilenende (in Variablen: `<br/>`) |
| eine **Randbemerkung** | `@ASIDE Satz` (klein, kursiv, eingerückt) · nur in UC als Randbemerkung, in normal als Absatz: `@ASIDE-UC Satz` |
| einen **Zwischentitel** | `### Titel`, kleiner `#### Titel` (ins Inhaltsverzeichnis mit `{inhalt-tiefe}: 3` bzw. `4`) |
| eine **Aufzählung** | `- Punkt` oder `1. Schritt`, Unterpunkt zwei Leerzeichen eingerückt |

![Text, Liste und Randbemerkung](bilder/hilfe/text.png)

![@ASIDE: Randbemerkung](bilder/hilfe/aside.png)

### Sätze mit Linie und Logo (DECORATE)

| Ich will … | So |
|---|---|
| einen Satz **zwischen zwei Linien mit Logo**, der Text geht danach weiter | `@DECORATE Satz` |
| denselben Satz **ohne Linien** | `@DECORATE-TEXT Satz` |
| einen Satz **ganz unten** auf der Seite (z. B. ein Hinweis) | `@DECORATE-TEXT-BOTTOM Satz` |
| einen Satz **allein auf einer Seite** | `@DECORATE-PAGE Satz` (in der Titelei: `## @DECORATE-PAGE Satz`) |
| nur **Linie mit Logo**, ohne Text | `@DECORATE-LOGO` |

![@DECORATE und @DECORATE-TEXT](bilder/hilfe/decorate.png)

![@DECORATE-PAGE: eigene Seite](bilder/hilfe/decorate-page.png)

### Ein Kapitel schön abschliessen

| Ich will … | So |
|---|---|
| einen Satz **mitten in den Rest der Seite**, danach neue Seite | `@DECORATE-REST Satz` |
| mehrere Absätze so | `@DECORATE-REST` … `@END` |
| einen **Schlusssatz** mit Linie nur oben | `@DECORATE-ABOVE-REST Satz` |
| den Schlusssatz **auf beiden Seiten einer Doppelseite gleich hoch** | `@DECORATE-ABOVE-BOTTOM-34 Satz` – Oberkante 34 mm über dem Ende des Textes. Auf beiden Seiten dieselbe Zahl; reicht der Platz nicht, setzt der Motor mittig |
| die Schrift wie der Fliesstext statt kursiv | am Befehl `-UPRIGHT` (in der Hauptfarbe: `-UPRIGHT-MAIN`), z. B. `@DECORATE-REST-UPRIGHT` · für das ganze Buch: `{decorate-stil}` |

Zeilenumbruch im Satz mit `\` am Zeilenende, z. B. `@DECORATE-ABOVE-REST Schön, dass du da bist. \` und darunter `Herzlich, Name`.

![@DECORATE-REST, -ABOVE-REST, -ABOVE-BOTTOM-34](bilder/hilfe/decorate-rest.png)

### Logo

| Ich will … | So |
|---|---|
| das **Logo** im Text | `@LOGO-12` (12 mm breit) |
| das Logo **in die Lücke vor der nächsten Überschrift** (ohne eigenen Platz) | `@LOGO-6-GAP` |
| das Logo **mitten in den Rest der Seite**, danach neue Seite | `@LOGO-10-REST` |
| das Logo **unten auf die Seite**, danach neue Seite | `@LOGO-10-BOTTOM` |
| ein **eigenes Logo** | in der Variablen-Datei `{logo}: mein-logo.png` (Bild in `bilder/`), hell: `{logo-light}` |

![@LOGO-12 und @LOGO-6-GAP](bilder/hilfe/logo.png)

![@LOGO-10-REST und @LOGO-10-BOTTOM](bilder/hilfe/logo-rest-bottom.png)

### Seiten und Abstand

| Ich will … | So |
|---|---|
| eine **neue Seite** | `@NEWPAGE` (im Druck immer rechts: `@NEWPAGE-RIGHT`) |
| eine neue Seite **nur, wenn unten zu wenig Platz** bleibt | `@NEWPAGE-60` (weniger als 60 mm frei) – gut vor einem Foto oder Zwischentitel |
| **mehr Abstand** | `@SPACER-8` (mm). Mehrere Leerzeilen geben keinen Abstand |
| einen Abschnitt **nie trennen** | `@KEEP-TOGETHER` … `@END` |
| den Inhalt einer Seite **senkrecht in die Mitte** | `@PAGE-CENTER` (wirkt beim Bauen mit `k`) |
| in der **Kopfzeile** ein anderes Wort | `@HEADER Ecuador` … `@HEADER` (allein = wieder normal) |

### Zwei Fassungen (normal und Unzensiert)

| Ich will … | So |
|---|---|
| Text **nur in einer Fassung** | `@UC` … `@END` (nur Unzensiert) · `@NORMAL` … `@END` |
| **einen Befehl** nur in einer Fassung | Vorsilbe: `@UC-SPACER-14`, `@NORMAL-NEWPAGE`, `#### @UC-PICTURE Titel` |
| einen **Kasten «Unzensiert»** mit Titel | `@UC-BLOCK Titel` … `@END` |
| Text nur im **E-Book**, nur im **Druck**, nur im **Lese-PDF** | `@EBOOK` · `@PRINT` · `@SCREEN` … `@END` |

![@UC-BLOCK](bilder/hilfe/uc-block.png)

### Noch offen

| Ich will … | So |
|---|---|
| eine Stelle, über die ich **noch nicht entschieden** habe | `@DRAFT` … `@END` – mit `s` gelb markiert, mit `f` normal gedruckt |
| eine **Notiz**, die nie gedruckt wird | `@NOTE Titel` … `@END` (in einer Geschichte: Zeile `notiz: …`) |

![@DRAFT und @NOTE](bilder/hilfe/draft-note.png)

### Bilder, Tabellen, QR

| Ich will … | So |
|---|---|
| ein **Foto** | `#### @PICTURE Titel`, darunter `datei: bild.jpg` und `text: Bildtext` – eine Leerzeile beendet das Foto. [→ alle Angaben](#Bilder-und-Fotos) |
| das Foto **60 mm breit** | `#### @PICTURE-60 Titel` |
| ein Foto, das der **Text umfliesst** | `#### @PICTURE-40-RIGHT Titel` (oder `-LEFT`) |
| eine **Tabelle** | `@#name` (CSV im Ordner tabellen/) – Menü `t` → `n` legt sie an. [→ Tabellen](#Tabellen) |
| eine **Geschichte** einbinden | `##### @@name` – Menü `g` → `b` macht es selbst. [→ Geschichten](#Geschichten-sammeln) |
| einen **QR-Code** | `@QR https://… \| Text`, mehrere nebeneinander: `@QR a \| Text ;; b \| Text` |
| einen QR-Code **rechts, der Text fliesst herum** | `@QR-RIGHT url` direkt vor den Absatz (im E-Book weggelassen) |
| einen **Zeitstrahl** | `@TIMELINE` … `@END`, jede Zeile `1974 \| Geboren` |

![@PICTURE-70 und @PICTURE-35-RIGHT](bilder/hilfe/picture.png)

![@QR, zwei nebeneinander, @QR-RIGHT](bilder/hilfe/qr.png)

![@TIMELINE](bilder/hilfe/timeline.png)

### Aussehen des ganzen Buchs

| Ich will … | So |
|---|---|
| einen **grossen Anfangsbuchstaben** am Kapitelanfang | Menü `ge` oder `{initial}: ja` in der Variablen-Datei. [→ Seitengestaltung](#Seitengestaltung) |
| Absätze **eingerückt** statt mit Abstand | `{absatz-einzug}: ja` |
| den Druck in **CMYK** (z. B. tredition) | in der Druckdatei `{farbmodus}: cmyk`. [→ RGB oder CMYK](#Farben-fuer-den-Druck) |
| den **Strichcode** mit Goldrahmen oder Bergkette | in der Druckdatei `{isbn-rahmen}: berge` oder `gold`. [→ Druckangaben](#Plattform-Dateien) |
| sehen, **ob es passt** | Menü `s` (schnell) – für den Druck: `f` (final) |

Alle Befehle auf einen Blick: Hilfe «Befehle (@)».
