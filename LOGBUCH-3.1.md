# Logbuch pureSATZ 3.1 – Motor bereinigen

Stand: 21.11.2026 12:30 · **3.5.0 im Original** (K4 erledigt: G0–G6, U1–U9, D, N; D2 verworfen) · offen: `sh release.sh` (Thomas) · Vorgänger: LOGBUCH-3.0.md (neue Schreibweise, erledigt).

## Auftrag (für einen neuen Chat)

**Start im neuen Chat:**
«Verbinde die Ordner ~/Dokumente/pureWORLD-umbau und ~/Dokumente/pureWORLD. Lies pureWORLD-umbau/pureSATZ/LOGBUCH-3.1.md
und pureWORLD/buecher/Leben123/CLAUDE-WIEDEREINSTIEG.md (Abschnitt 1). Dann Umbau starten mit go G0 G1.»

**Arbeitsort = Kopie `~/Dokumente/pureWORLD-umbau/`** (entschieden 21.11., Thomas):
- Darin: `pureSATZ/` (ohne .git, _backup) und `buecher/Leben123`, `Naehrstoffe`, `pureSATZ-Handbuch` (ohne .git,
  motor-alt-*, md-history; mit ausgabe-* = Vergleich «vorher», Motor 3.0.1).
- **Claude schreibt nur in die Kopie, nie ins Original `~/Dokumente/pureWORLD/`.** Das Original nur lesen.
- Ohne .git: `sync`/`release.sh` können nichts nach GitHub schicken; Menü `s` baut ohne sync.
- Thomas baut in der Kopie lokal (mit Silbentrennung und CMYK) und schaut an; Claude prüft in der Cloud (vergleich.py).
- Dieses Logbuch liegt in der Kopie (pureWORLD-umbau/pureSATZ/) und wird dort nachgeführt.
- **K4 auch:** in Leben123/CLAUDE-WIEDEREINSTIEG.md (Original) beim Prüfen ergänzen: «Testbuch: `python3 test/alle-befehle.py
  <leerer-ordner>` je mit altem und neuem pureSATZ bauen, dann `test/vergleich.py <alt> <neu>` → «Alles gleich».» (W, 21.11.)
- **Am Schluss (K4):** nur `pureSATZ` zurück ins Original kopieren (ohne .git zu überschreiben), dann `sh release.sh`.
  Bücher nicht zurückkopieren (Thomas ändert sie weiter); zum Schluss das aktuelle Leben123 nochmals «Alles gleich» prüfen.
- Während des Umbaus **keine Motor-Änderung im Original**. Falls doch nötig: hier unter «Verlauf» festhalten und beim
  Zurückkopieren übernehmen.

Kopie anlegen (Thomas, einmal):
```
mkdir -p ~/Dokumente/pureWORLD-umbau/buecher
cd ~/Dokumente/pureWORLD
rsync -a --exclude .git --exclude _backup pureSATZ ../pureWORLD-umbau/
rsync -a --exclude .git --exclude 'motor-alt-*' --exclude md-history buecher/Leben123 buecher/Naehrstoffe buecher/pureSATZ-Handbuch ../pureWORLD-umbau/buecher/
```

**Ziel:** Den Motor (ca. 14'000 Zeilen, build.py 3'100) aufräumen: weniger Code, eine Sprache innen und aussen,
jede Sache nur an einer Stelle. **Ohne Funktion zu verlieren.**

**Bedingung bei JEDEM Schritt** (sonst nicht zurückschreiben):
1. **Selbsttest grün:** `SELBSTTEST_OHNE_VENV=1 python3 test/selbsttest.py < /dev/null` → «SELBSTTEST IN ORDNUNG».
2. **Pixelgleich:** `python3 test/vergleich.py <alt> <neu>` → «Alles gleich» für Leben123 (normal + UZ), Naehrstoffe,
   pureSATZ-Handbuch und das Testbuch aus G0. Jeweils `sh build.sh final`, alter Motor = Stand vor dem Schritt
   (`_backup/vor-<version>/`). Testbuch: `python3 test/alle-befehle.py <leerer-ordner>` je mit altem und neuem pureSATZ.
   Nur Druckbericht (Uhrzeit) und Datum im E-Book dürfen sich unterscheiden.
3. Menü-Test mit Eingaben, wenn menu.py betroffen ist (z. B. `printf 'um\nn\n\nj\n' | python3 motor/menu.py`).
4. VERSION + CHANGELOG nachführen, dieses Logbuch nachführen (Tabelle «Verlauf» unten).

**Leben123 schützen:** Gearbeitet wird nur in der Kopie. `sh release.sh` erst am Schluss im Original, nach der Freigabe
von Probedruck 2, geprüft mit «Alles gleich».
Alte Bücher und andere Computer brauchen keine Rücksicht: alles liegt auf GitHub, Bücher werden neu geholt
(andere Computer: Menü `ss`). Alte Bücher stellt `um` / `motor/umbenennen.py` um.

**Regeln (Thomas):**
- Erst Plan mit Buchstaben, ändern erst nach «go». KISS: vorhandenen Code nutzen, keine neuen Sonderfälle.
- Antworten kurz. Befehle nur Linux, alle in EINEM Codeblock, Zeile für Zeile, nie `&&`.
- Thomas ändert Dateien zwischendurch: immer die aktuelle Datei vom Computer holen und vergleichen.
- Kein Schritt ändert, was im Buch steht oder wie es aussieht. Neue Funktionen: nicht in dieser Runde.

**Arbeitsweise in der Cloud (bewährt):**
- Ganzes pureSATZ **aus der Kopie** holen (auch import/ und docs/, sonst bricht der Selbsttest ab).
  Bücher Leben123, Naehrstoffe, pureSATZ-Handbuch aus der Kopie holen (ohne ausgabe-*, .venv).
- In der Cloud fehlen pyphen und Ghostscript (bei alt und neu gleich). `.venv/bin/python3` = Link auf System-Python.
- Vor dem Zurückschreiben (in die Kopie): bisherige Dateien nach `pureWORLD-umbau/pureSATZ/_backup/vor-<version>/`, dann aus neuem outputs/-Ordner mit
  expectedMtimeMs schreiben, danach nochmals holen und mit cmp vergleichen (sofort genügt).
- Ein Schritt = eine Version (3.1.0, 3.1.1 …). Thomas macht am Schluss `sh release.sh` (Selbsttest läuft darin).

## Befund (21.11., kurze Bestandesaufnahme)
- Toter Code fast keiner: nur `zeitstrahl_block` und `seite_kopf` in build.py werden nie aufgerufen.
- **Innen alte Namen:** `manuskript.v3()` übersetzt 3.0 beim Lesen zurück in die alten Formen; build.py und
  build-epub.py arbeiten weiter mit `@ZITAT-ZIER`, `@ZIER`, `@LOTUS…`, `::: mitte`, `::: uz`, `kasten`, `zier`.
- **Doppelt:** build.py (PDF, ca. 11 Befehls-Zweige ab Zeile ~2429) und build-epub.py (ab ~485) werten jeden Befehl
  je selbst aus. Zitat mit Verzierung an 4 Stellen; `zeitstrahl_block`/`zeitstrahl_tabelle` fast gleich;
  `druck_datei`/`ebook_datei`.
- **Altlasten:** `-dc`, `-v2`, `offiziell`, `isbn-buch`, `barcode-…` (30× in build.py, heute `isbn-…`),
  `{neu-berechnen}` (bis 2.81), Variablenblock zwischen `---`, `- name:` mit Strich, `::: foto`, `@ANHANG`, `@LOTUS…`.
- Rund 70 Kommentare mit Versionsgeschichte («2.84.6: …») in build/menu/bauen/epub → gehören in den CHANGELOG.
- **Bleiben (nach G1):** `barcode-…` (Naehrstoffe-Druckdateien) und `{neu-berechnen}` (Druckdateien aller drei Bücher) –
  `um` stellt Druckdateien nicht um. Später: Druckdateien in `um` mit umstellen, dann weg.
- **Handbuch in der Cloud:** PDF-Bau bricht ab (LayoutError S. ~81, «Das machen auch final und komplett …») – mit 3.0.1
  genauso (fehlendes pyphen). Vergleich dort nur E-Books + «gleicher Fehler». Bei Thomas lokal bauen.

## Plan (Reihenfolge)
| | Was | Gewinn | Aufwand | Risiko |
|---|---|---|---|---|
| **G0** ✓ | **Testbuch «alle Befehle»** (aus test/hilfe-bilder.py ableiten): jeder 3.0-Befehl, jeder Bereich, jede Fassung, Foto, QR, Tabelle, Geschichte, Zeitstrahl, Verzeichnisse. Wird Teil des Selbsttests oder test/alle-befehle.py | Sicherheit für alles | klein | – |
| **G1** ✓ | Altlasten weg (Liste oben), tote Funktionen, Versionskommentare kürzen | weniger Code | klein | klein |
| **G2** ✓ | **Innen 3.0:** build.py/build-epub.py werten die 3.0-Namen direkt aus; `v3()` entfällt; Variablen intern `logo`, `block-kopf` … `umbenennen.py` bleibt (alte Bücher) | **am grössten** | mittel | mittel |
| **G4** ✓ | Doppeltes zusammenführen: Zitat mit Verzierung, Zeitstrahl, druck_datei/ebook_datei | mittel | klein | klein |
| **G3** ✓* | **Ein Leser für alle:** manuskript.py liest jeden Befehl einmal in eine Liste (Art, Werte, Text); PDF, E-Book, Hörbuch, Stände nutzen sie | gross | gross | mittel |
| **G5** ✓ | Menü und Begriffe U1–U9 (unten; alle erledigt); alte Tasten gehen weiter | Bedienung | klein | klein |
| **G6** ✓ | Hilfe kürzen (Ausnahmen, alte Namen), Bilder neu (test/hilfe-bilder.py) | weniger lesen | klein | – |

Vorgehen: G0 → G1 → G2 + G4 → G3 → G5 → G6.
\* **G3 Entscheid (21.11.):** PDF, E-Book, Prüfung und Stände lesen seit G2 über denselben Leser (`zeilen()` + `befehl()`).
Das Hörbuch behält seinen awk-Leser (md2txt.sh, auf 3.0 umgestellt): Ein gemeinsamer Leser würde die 18 Zeilen mit `\`
in Leben123 anders umbrechen → Kapiteltexte ändern sich → Azure nimmt sie neu auf (Kosten). Umstellen, wenn das Hörbuch
ohnehin neu aufgenommen wird. build.py **nicht** in mehrere Dateien aufteilen (Risiko > Gewinn).

## Menü und Begriffe (G5) – Unstimmigkeiten
| | Heute | Vorschlag |
|---|---|---|
| U1 ✓ | `k` «komplett» = final · `f` = final · `sh build.sh komplett` = final + Leseprobe + Korrektur | `f` final, `k` komplett (wie Terminal) |
| U2 ✓ | `w` «weitergeben» = `lp` + `ko` | fällt weg (in `k`), Taste geht weiter |
| U3 ✓ | Cover: Menü `co`, Terminal `cover-stand` (anzeigen) und `covers` (bauen), «Coverrechner» | einheitlich `co` / `covers` |
| U4 ✓ | Stände: `sm` merken · `zh` zurückholen · `a` änderungen · Terminal `stand`, `aenderungen` | ein Muster |
| U5 ✓ | `a` änderungen ↔ `au` aufräumen | klarer trennen |
| U6 ✓ | `in` = Gestaltung (von «Initial») | sprechendes Kürzel |
| U7 ✓ | Lese-PDF · Bildschirm-PDF · `nur-pdf` · SCREEN | ein Wort |
| U8 ✓ | Unzensiert · UZ · uz · zweite Ausgabe · UC | klären (im Buch UC, Ordner uz) |
| U9 ✓ | Gruppen «1 Schreiben, 2 Bauen, 3 Ansehen», andere ohne Nummer | einheitlich |

Umgesetzt (3.4.0): `f` final, `k` komplett · `w` aus dem Menü · Cover `co` (Menü und `sh build.sh co`), `cv`/`cover-stand` gehen weiter ·
`cl` aufräumen (`au` geht weiter) · überall «Lese-PDF» · Gruppen ohne Nummern.
3.5.0: U4 Stände zusammen unter «Ansehen» (`sm` `a` `zh`), `db` zu «Prüfen» · U6 `ge` Gestaltung (`in` geht weiter) ·
U8 überall «Fassung UC», Terminal `uc` = `uz`, Ordner bleibt · D Fassung hinten bei @DECORATE (Text in beiden, Verzierung nur dort) · N `@N-` = `@NORMAL-`.

Übersicht «welcher Befehl baut was» (für die Hilfe, mit G5/G6): schnell = nur Lese-PDF (Entwurf) · ohne Wort = alles
Entwurf · **final = Druckfassung** (Buchblock + Umschlag CMYK, Cover aus Rohdaten, E-Book, Mockup, Druckbericht) ·
komplett = final + Leseprobe + Korrektur · nur-pdf / nur-druck / nur-ebook [final] · covers = nur-druck final.

## Verlauf
| Datum | Version | Schritt | Selbsttest | Vergleich |
|---|---|---|---|---|
| 21.11. | 3.0.1 | Ausgangslage (Leben123 + Naehrstoffe auf 3.0 umgestellt) | grün | – |
| 21.11. | – | Entscheid: Umbau in der Kopie pureWORLD-umbau (K1–K4) | – | – |
| 21.11. | 3.1.0 | **G0** test/alle-befehle.py (im Selbsttest) · **G1** @LOTUS…, @ANHANG, dc/v2/offiziell, isbn-buch, ::: foto, `---`-Variablenblock, `- name:`, zeitstrahl_block, seite_kopf weg; ~80 Versionskommentare gekürzt; umbenennen.py versteht dc/v2/offiziell selbst | grün | Leben123 N+UZ, Naehrstoffe, Testbuch: Alles gleich (nur Druckbericht) · Handbuch: E-Book gleich bis auf Versionsnummer, PDF wie vorher Cloud-Fehler |
| 21.11. | 3.2.0 | **G2** innen 3.0: `manuskript.befehl()` zerlegt jeden Befehl, v3() weg, build/epub/md2txt/staende/import auf 3.0, alte Schreibweise → Meldung mit `um` · **G4** zier_satz, _plattform_datei · Korrekturen: Bild in @UC, E-Book @ASIDE in @KEEP-TOGETHER, Hörbuch ohne @NOTE | grün | Leben123 N+UZ, Naehrstoffe, Handbuch (E-Book), Testbuch: Alles gleich · Hörbuch-Texte gleich · erweitertes Testbuch: nur die Korrekturen |
| 21.11. | 3.3.0 | **G6** Hilfe: jede Sache an einer Stelle (Gestalten = Leitfaden, Befehle (@) = Tabelle inkl. Bereiche), doppelte Listen und Versionsangaben weg · **build.sh**: Befehlsliste nur in bauen.py (`sh build.sh befehle`), update erneuert Starter (ausser `# eigen`, update.*, menu.*), release ruft `update.py hilfsdateien` · Webseite (docs) nachgeführt | grün | Leben123, Naehrstoffe, Testbuch: Alles gleich · Handbuch-E-Book: neue Hilfe (gewollt) · Hilfebilder gleich · keine toten Verweise |
| 21.11. | 3.4.0 | **G5** Menü: `f` final, `k` komplett (+ Leseprobe, Korrektur), `w` nur noch als alte Taste, Cover `co` überall, `cl` aufräumen, «Lese-PDF» statt «Bildschirm-PDF», Gruppen ohne Nummern · Hilfe: Menütext, Menübild, Tasten-Tabelle, Spickzettel · **S** Erste Schritte: zwei Anfangsabschnitte zu einem | grün | Leben123 N+UZ, Naehrstoffe, Testbuch: Alles gleich (nur Druckbericht) · Menü getestet: co, cv, f, k, cl, au, `:` |
| 21.11. | 3.5.0 | **D** Fassung hinten bei @DECORATE (Text in beiden Fassungen, Verzierung nur in einer; PDF, E-Book, Hörbuch) · **N** `@N-` · **U8** Fassung UC (Begriffe, `uc` im Terminal) · **U6** `ge` · **U4** Stände zusammen, `db` zu Prüfen | grün | Leben123 N+UZ, Naehrstoffe: gleich (nur Druckbericht) · Leben123-Hörtexte gleich · Testbuch: neue Seite mit D/N, beide Fassungen angesehen |
| 21.11. | 3.5.0 | **K4** 41 Dateien ins Original-pureSATZ (Original war seit der Kopie unverändert; Sicherung `_backup/vor-3.5.0-umbau/`) · D2 (zwei DECORATE für einen Text) verworfen | grün | aktuelles Leben123 mit 3.0.1 und 3.5.0: Alles gleich (nur Druckbericht; Doppelblock Z. 135–151 für den Test entfernt, er baut mit beiden Motoren nicht) |
