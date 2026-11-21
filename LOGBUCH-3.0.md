# Logbuch pureSATZ 3.0 – neue Schreibweise

Stand: 21.11.2026 02:30 · Motor **3.0.1** freigegeben (release.sh) · Naehrstoffe und Leben123 umgestellt.
Ziel: **jeder Name sagt, was er heute tut** – einfacher, ohne Funktion zu verlieren.
Bedingung: Bücher bleiben **pixelgleich** (vergleich.py «Alles gleich»).

## Regeln (entschieden 20.11., Thomas)

1. **Alles, was pureSATZ ist, beginnt mit `@`** – Steuerzeichen englisch (wie in jeder Software), Hilfe deutsch.
   Markdown bleibt für Text: `**fett**`, `*kursiv*`, `\` (Zeilenumbruch), Titel `#`.
2. **Bauplan:** `@[FASSUNG-]NAME[-GRÖSSE][-ORT[-HÖHE]][-STIL] Text` – alles vor dem ersten Leerzeichen ist der Befehl
   (gross geschrieben), danach der Text. Zahlen immer in mm.
3. **Ortswörter:** (ohne) = hier im Text · `REST` = Mitte des Rests der Seite, dann neue Seite · `BOTTOM` = unten
   (`BOTTOM-34` = Oberkante 34 mm über dem Ende des Textbereichs) · `GAP` = in der Lücke vor der nächsten Überschrift ·
   `PAGE` = eigene Seite (z. B. `@DECORATE-PAGE`) · `RIGHT`/`LEFT` = daneben, Text fliesst herum.
4. **Fassung als Vorsilbe:** `@UC-…` (Unzensiert) · `@NORMAL-…` · `@EBOOK-…` · `@PRINT-…` (Druck) · `@SCREEN-…` (Lese-PDF).
   Im Bereich `@UC` … `@END` gilt alles automatisch nur für UC.
5. **Bereich** = Befehl allein auf der Zeile (oder mit Titel), endet mit `@END`. Kein Bereich im Bereich.
6. **Standard nicht angeben** – nur, was abweicht (z. B. `-UPRIGHT`).
7. **Alte Namen gehen weiter** (gleiche Wirkung). Die Hilfe zeigt nur 3.0 – 3.0 ist der neue Standard.
8. Variablen bleiben deutsch (`{titel}`, `-uz` …); nur die fünf unten bekommen neue Namen.

## Tabelle alt → neu

### Seite
| alt | neu |
|---|---|
| `---` · `@UMBRUCH` | `@NEWPAGE` |
| `@UMBRUCH-RECHTS` | `@NEWPAGE-RIGHT` |
| `@PLATZ 40` | `@NEWPAGE-40` (nur wenn weniger als 40 mm frei) |
| `@ABSTAND 8` | `@SPACER-8` (nur Leerraum) |
| `@SEITENMITTE` | `@PAGE-CENTER` (wirkt nur mit `k`) |
| `@KOPF Text` … `@KOPF` | `@HEADER Text` … `@HEADER` |

### Logo und DECORATE (Linie-Logo-Linie)
| alt | neu | Wirkung |
|---|---|---|
| `@ZIER 12` · `@LOTUS` | `@LOGO-12` | Logo im Text, 12 mm breit |
| `@ZIER-UNTEN 10` | `@LOGO-10-BOTTOM` | unten auf der Seite, dann neue Seite |
| `@ZIER-UNTEN 8 mitte` | `@LOGO-8-REST` | Mitte des Rests, dann neue Seite |
| `@ZIER-TRENNER` | `@LOGO-6-GAP` | Lücke vor der nächsten Überschrift |
| `@ZIER-LINIE` | `@DECORATE-LOGO` | Linie-Logo-Linie |
| `@ZITAT-ZIER Satz` · `> Satz` | `@DECORATE Satz` | Linie-Logo, Satz, Linie-Logo |
| `@ZITAT Satz` | `@DECORATE-TEXT Satz` | nur Text (kursiv, zentriert) |
| `@UNTEN Satz` | `@DECORATE-TEXT-BOTTOM Satz` | Text unten auf der Seite |
| `@MOTTO Satz` · `## @KERNSATZ Satz` | `@DECORATE-PAGE Satz` · `## @DECORATE-PAGE Satz` | eigene Seite (Titelei mit `##`) |
| `::: mitte` (1 Absatz) | `@DECORATE-REST Satz` | Mitte des Rests (Kapitelende) |
| `::: mitte` … `:::` | `@DECORATE-REST` … `@END` | mehrere Absätze |
| `::: mitte oben` | `@DECORATE-ABOVE-REST Satz` | Schlusssatz, Linie nur oben |
| `::: mitte oben fest 34` | `@DECORATE-ABOVE-BOTTOM-34 Satz` | Schlusssatz auf fester Höhe |
| `::: mitte aufrecht` / `blau` | `…-UPRIGHT` / `…-UPRIGHT-MAIN` | Schrift wie Fliesstext / in Hauptfarbe |
| `~ Satz` | `@ASIDE Satz` | Randbemerkung |

Zeilenumbruch im Satz: `\` (z. B. `@DECORATE-ABOVE-BOTTOM-34 Schön, dass du auch da bist. \` + nächste Zeile).

### Bereiche
| alt | neu |
|---|---|
| `::: nur-uz` · `nur-normal` · `nur-ebook` · `nur-druck` · `nur-bildschirm` | `@UC` · `@NORMAL` · `@EBOOK` · `@PRINT` · `@SCREEN` … `@END` |
| `::: uz Titel` (Kasten «Unzensiert») | `@UC-BLOCK Titel` … `@END` (nur in UC) |
| `::: offen` | `@DRAFT` … `@END` (mit `s` gelb, mit `k` normal gedruckt) |
| `::: platzhalter` · `offen-notiz` | `@NOTE` … `@END` (wird nie gedruckt) |
| `::: zusammen` | `@KEEP-TOGETHER` … `@END` |
| `::: zeitstrahl` | `@TIMELINE` … `@END` |
| `:::` | `@END` |

### Bilder, QR, Titelei, Verzeichnisse
| alt | neu |
|---|---|
| `#### @FOTO Titel` + `breite: 60` + `fluss: rechts` | `#### @PICTURE-60-RIGHT Titel` (darunter weiter `datei:` `text:` `quelle:`) |
| `#### @FOTO-UZ` | `#### @UC-PICTURE` |
| `@QR-PAAR a ;; b` | `@QR a ;; b` |
| `@QR-FLUSS url` | `@QR-RIGHT url` |
| `@TITEL` `@IMPRESSUM` `@HINWEIS` `@WIDMUNG` `@INHALTSVERZEICHNIS` | `@TITLE` `@IMPRINT` `@NOTICE` `@DEDICATION` `@CONTENTS` |
| `@STICHWORTE` `@BILDERVERZEICHNIS` `@TABELLENVERZEICHNIS` `@BILDNACHWEIS` `@RUECKSEITE` | `@INDEX` `@LIST-PICTURES` `@LIST-TABLES` `@PICTURE-CREDITS` `@BACK-COVER` |
| `@PORTRAIT`, `@#tabelle`, `@@geschichte` | bleiben |

### Variablen
| alt | neu |
|---|---|
| `{zier}` · `{zier-hell}` | `{logo}` · `{logo-light}` |
| `{mitte-stil}` | `{decorate-stil}` |
| `{kasten-kopf}` · `{kasten-hinweis}` | `{block-kopf}` · `{block-hinweis}` |

### Standards (nur angeben, was abweicht)
- Fliesstext: aufrecht, Textfarbe, Blocksatz.
- `@DECORATE …`, `@DECORATE-TEXT`, `-BOTTOM`: kursiv, Zitatfarbe, zentriert. `@DECORATE-PAGE`: kursiv 14 pt.
- `@ASIDE`: klein, kursiv, eingerückt.
- `@PICTURE`: zentriert, ganze Breite, höchstens 75 mm hoch (oder `{foto-breite}`); `-RIGHT`/`-LEFT` 45 mm.
- `@LOGO` ohne Zahl: im Text 12, `BOTTOM` 10, `REST` 10, `GAP` 6 mm.

## Technik (so gebaut, KISS)
- **manuskript.py `v3()`**: übersetzt beim Lesen (`lies()`) jede neue Zeile in die alte interne Form.
  build.py, build-epub.py, Hörbuch, Stichworte usw. sehen weiter die alten Formen → **pixelgleich ohne Änderung am Zeichnen**.
  Code-Blöcke bleiben unberührt. Fehler mit Zeilennummer bei falschem Bauplan.
- `VAR_NEU` in manuskript.py: neue Variablennamen gelten wie die alten (auch mit Endungen `-uz`, `-druck`).
- **motor/umbenennen.py**: stellt ein Buch um (Buch-MD, Geschichten, Umschlag nur `:::`, Variablen); zeigt zuerst,
  `ja` schreibt (Sicherung md-history/). Kurze Bereiche werden eine Zeile (`::: nur-uz` / `@KOPF` / `:::` → `@UC-HEADER`).
  Druckdateien (druck/*.md) stellt es nicht um – dort gibt es keine Befehle.
- **3.0.1 Menü `um`**: Hat ein Buch noch alte Namen, steht oben «⚠ Alte Schreibweise (vor 3.0) → um». `um` zeigt die
  Änderungen, Hinweis «Andere Computer zuerst mit ss auf 3.0 bringen», fragt «Umstellen? [J/n]», sichert, stellt um
  (umbenennen.aenderungen/schreiben). `bp` meldet kurz «alte Schreibweise → Menü um». umbenennen.py bleibt im Motor.

## Prüfung (20.11. nachts, in der Cloud)
| Buch | alt 2.86 ↔ neu 3.0 |
|---|---|
| Naehrstoffe (alte Namen, neuer Motor) | Alles gleich |
| Naehrstoffe (umgestellt) | Alles gleich |
| Leben123 normal + UZ (Kopie, umgestellt inkl. Variablen) | **Alles gleich** (Lese-PDF, Buchblock, Umschlag, E-Book) |
| Hallo-Buch aus umgestellter Vorlage | Alles gleich (danach Erklärtexte der Vorlage angepasst) |
| Selbsttest | IN ORDNUNG |
Nur der Druckbericht unterscheidet sich (Uhrzeit). In der Cloud fehlen pyphen/Ghostscript – bei alt und neu gleich.

## Ablauf (Reihenfolge Thomas, 20.11.)
1. ✓ pureSATZ umbauen (3.0.0) · Naehrstoffe testen · Vorlage umgestellt.
2. ✓ **Hilfe neu** (21.11. früh): HILFE.md, START.md, readme4ki, Befehlsliste/Bereiche in hilfe.py und handbuch.py,
   11 Bilder (test/hilfe-bilder.py), Suchwörter alt → neu, `bp`-Hinweis, Menü `in` → `{decorate-stil}`, staende.py.
   Geprüft: Leben123 (alte und neue Namen), Naehrstoffe: «Alles gleich» (nur Druckbericht-Kopf); Selbsttest grün.
3. ✓ Handbuch: bei Thomas lokal mit 3.0 gebaut (nach HB-Fix `{isbn-bild}`), in Ordnung. Notiz von damals: In der Cloud bricht der Bau ab («LayoutError: Splitting error» beim Absatz
   «Das machen auch final und komplett …», Seite ~80) – **auch schon mit 2.86**, also kein 3.0-Fehler. In der Cloud fehlt
   pyphen (andere Trennung) → zuerst bei Thomas lokal bauen; bricht es dort auch ab, eigene Runde.
4. ✓ 3.0.1 (21.11. 01:25): Menü `um` (siehe Technik). Getestet an Naehrstoffe-Kopie: alles gleich, Selbsttest grün.
5. ✓ Naehrstoffe (21.11. 01:31, Thomas): `ul`, `um`, `s` – alles in Ordnung.
6. ✓ Leben123 (21.11. 01:33, Thomas): `ul`, `um` – in Ordnung. Danach **Probedruck 2** ansehen; wenn gut, keine Änderung
   mehr. Offiziell kaufbar ab **21.12.2026**, Thomas kauft schon vorher.
   Zeitstrahl normal hatte eine Zeile mehr (neue Seite): **nicht von 3.0** (Übersetzung Zeile für Zeile gleich, build.py
   gleich wie 2.86), sondern vom Gegenlesen: 1996 in zwei Zeilen geteilt (1996 / 1997–1998).
7. **Andere Computer** haben noch 2.8x: dort zuerst `ss`, bevor ein umgestelltes Buch gebaut wird.

## Offen / später
- **Weiter in LOGBUCH-3.1.md:** Motor bereinigen (Auftrag für neuen Chat, Plan G0–G6, Menü U1–U9).
- Neue Funktionen (nicht pixelrelevant, je mit Testseite): `@DECORATE-LOGO-30` (Logo-Grösse in der Linie) ·
  `@DECORATE-LINE` (Linie ohne Logo) · `@DECORATE-ABOVE/-BELOW Satz` im Text · `@LOGO-8-BOTTOM-10` (Abstand) ·
  Stil `-BOLD` · `@PICTURE-S/M/L` · `{logo-light}: 30` (Deckkraft statt eigenes Bild).
- `@NEWPAGE` ersetzt `---` (umbenennen.py stellt um); `---` geht still weiter. (G4 «weglassen» = `@---` verworfen.)
- BuchGeschichen: nur Test, kann gelöscht werden (Thomas).
- Fehlermeldung, wenn `@UC-…` in einem `@UC`-Bereich steht (heute: «Block wird nicht geschlossen»).

- Leben123 Zeitstrahl (nur normal), wartet auf go – gemessen mit Lora 8,6 pt, Platz pro Zeile ca. 91 mm:
  A 1974 `Geboren am Dreikönigstag in Bern, Kindheit in Muri-Gümligen` (1 Zeile) ·
  B 2017 `Teilnahme am ersten Emotionscode-Seminar in der Schweiz` (1 Zeile) ·
  C 2018 `Zertifizierter Emotionscode-Anwender, Einsatz BodyCode, neue Website, regelmässig Schwitzhütte` (2 Zeilen wie bisher) ·
  D heute: «Informatiker, Autor und Praxis» lassen (Praxis am Schluss) oder «Informatiker, Praxis, Autor» (zeitlich) – Thomas entscheidet.
  Spalte A schmaler: nicht empfohlen (Motor, alle Bücher, bringt höchstens 4 mm).
- ✓ Leben123: CLAUDE-WIEDEREINSTIEG(-BUCH).md und readme4ki.txt auf 3.0 nachgeführt (21.11. 02:45).
- Leben123 S. 58/59: «Es ist so schön …» steht tiefer als «Schön, dass du auch da bist.» – S. 58 hat keine 34 mm Platz mehr
  (nach dem Gegenlesen voller) → auf beiden Seiten denselben kleineren Wert (z. B. 28). Kein neuer Code nötig.
- Druckdateien: `{neu-berechnen}: ja` (bis 2.81 = von Hand neu rechnen) heisst seit 2.82.0 `{neu-berechnet}: ja|nein`
  (Motor rechnet aus den Rohdaten, ja = Werte passen); alter Name wird beim Bau der Druckdatei umgestellt.
  Leben123 `epubli-a5-uz.md` hat noch den alten Namen (seither nicht gebaut). Sicherung beim Ändern: md-history/druck/.
- Zurückschreiben aus der Cloud: Vergleich sofort nach dem Schreiben reicht (3 s statt 90 s, 21.11. geprüft).

## Notizen
- 20.11. 22:55: Bilder DECORATE / DECORATE-TEXT / DECORATE-PAGE angesehen: PAGE ist ein Ortswort (gleiche Zier, eigene Seite, 14 pt).
- Idee Thomas: Hilfe 3.0 mit solchen Bildern (vom Motor erzeugt) – Struktur, Suche, Register, Windows/Mac, Brotkrumen bleiben.
- 20.11.: Idee nach «::: mitte-uz oben fest 37 – sieht gebastelt aus».
- 20.11. abends: Logo statt Lotus/Zier, Zahl im Namen, englische Steuerzeichen, Fassung als Vorsilbe (UC), DECORATE-Familie,
  REST statt mitte, GAP statt TRENNER, Motto/Kernsatz = DECORATE-PAGE, Bereiche mit @END.
