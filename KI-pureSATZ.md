# KI-pureSATZ – Wiedereinstieg für Claude (ab pureSATZ 3.5)

Stand: 21.11.2026 · Motor 3.5.1 · Zu Beginn einer Sitzung lesen. Gilt für den Motor und alle Bücher.
Regeln für die Zusammenarbeit (Sprache, «go», Befehle): `pureWORLD/CLAUDE-WIEDEREINSTIEGE.md` (privat).
Buchinhalt: `buecher/<Buch>/KI-<Buch>.md` (z. B. KI-Leben123.md). Grosser Umbau: `claude-modernisierung-puresatz.md`.
Diese Datei ist öffentlich (GitHub) – nichts Persönliches hineinschreiben.

## Was und wo
- pureSATZ = Satzsystem in Python (ReportLab, eigenes EPUB). Ein Buch = `<buch>-buch.md`, `-variablen.md`,
  `-umschlag.md`, dazu `druck/*.md` (Druckerei, Coverrechner), `stichworte-<buch>.txt`, `geschichten/`, `tabellen/`.
- Ordner: `~/Dokumente/pureWORLD/pureSATZ` (dieses Repo) und `~/Dokumente/pureWORLD/buecher/<Buch>/`.
  Jedes Buch hat eine eigene Kopie des Motors in `motor/` (holt sie mit `sh update.sh lokal`).
- Produktive Bücher: Leben123 (zwei Fassungen N + UC), Naehrstoffe, pureSATZ-Handbuch (Linux/Mac + Windows,
  entsteht aus der Hilfe). Hallo-Buch macht pureSATZ selbst (`sh hallo.sh`).
- Module in `motor/`: bauen.py (Ablauf, Befehle von build.sh) · manuskript.py (liest MD; `befehl()` zerlegt jeden
  @-Befehl, `zeilen()` liefert Text je Fassung) · build.py (PDF) · build-epub.py · build-broschuere.py · menu.py ·
  hilfe.py + HILFE.md (Hilfe) · update.py · staende.py · fassungen.py (Leseprobe, Korrektur) · audio/ (Hörbuch, md2txt.sh).

## Schreibweise 3.5 (Kurzfassung, ganz: hilfe.html → «Befehle (@)»)
- `@[FASSUNG-]NAME[-GRÖSSE][-ORT[-HÖHE]][-STIL][-FASSUNG] Text` · Bereiche `@NAME` … `@END` · Zahlen in mm.
- Fassung **vorne** = alles nur dort: `@UC-…`, `@NORMAL-…` / `@N-…`, `@EBOOK-…`, `@PRINT-…`, `@SCREEN-…`;
  `@UC` … `@END` = Text nur in UC.
- Fassung **hinten** (nur `@DECORATE`) = Text in beiden, Verzierung nur dort: `@DECORATE-REST-UPRIGHT-UC` … `@END`.
- Kein Bereich im Bereich. Unbekanntes bricht mit Zeilennummer ab.
- Begriffe: Fassung **normal** und **UC** (Ordner `ausgabe-unzensiert`, intern `uz`, Terminal `uc` oder `uz`) ·
  **Lese-PDF** (Bildschirm) · final = Druck + E-Book · komplett = final + Leseprobe + Korrektur.

## Prüfen – nach JEDER Motor-Änderung
1. Selbsttest (Cloud): `SELBSTTEST_OHNE_VENV=1 python3 test/selbsttest.py < /dev/null` → «SELBSTTEST IN ORDNUNG».
2. Testbuch: `python3 test/alle-befehle.py <leerer-ordner>` mit altem und neuem Motor bauen. Jeder Befehl aus
   manuskript.py (NAMEN, FASSUNG) muss darin vorkommen – neue Befehle dort ergänzen.
3. Bücher alt/neu: je eine Kopie mit altem und neuem Motor, `sh build.sh final`, dann
   `python3 test/vergleich.py <alt> <neu>` → «Alles gleich» (Druckbericht hat Datum und Version, ist nie gleich).
4. Hilfe/Webseite: `python3 motor/hilfe.py` · `python3 docs/landingpage.py ohne-bilder`.
5. VERSION + CHANGELOG nachführen.
- Cloud: pyphen und Ghostscript fehlen → Handbuch-PDF bricht ab (nur E-Book vergleichen), Silbentrennung anders.
  Hörtexte: md2txt.sh über eine Kopie des Buchs laufen lassen und alt/neu vergleichen (Azure-Kosten!).
- Menü testen mit Eingaben: `printf 'co\n\nj\n' | python3 motor/menu.py`.

## Dateien holen und zurückschreiben (Cowork)
- Zugriff auf `~/Dokumente/pureWORLD` anfragen. Holen (stage) → in der Cloud ändern → zurückschreiben (commit,
  mit expectedMtimeMs) → nochmals holen und vergleichen (cmp). Bilder (PNG/JPG) werden neu verpackt: Pixel vergleichen.
- Vorher immer den aktuellen Stand holen: Thomas ändert Buch-MDs selbst. Alte Fassung zuerst nach
  `md-history/<name>_JJJJMMTT-HH-MM-SS.md` (Bücher) bzw. `pureSATZ/_backup/vor-<version>/` (Motor).
- `device_list_dir` rekursiv auf pureSATZ bricht wegen .git bei 2000 Einträgen ab → Unterordner einzeln listen.
- Claude kann auf dem Computer keine Befehle ausführen: Befehle für Thomas in EINEM Block, Zeile für Zeile.

## Release
Claude: Motor ändern, VERSION + CHANGELOG, Selbsttest, zurückschreiben. Thomas (Selbsttest als eigener Block zuerst):
```
cd ~/Dokumente/pureWORLD/pureSATZ
python3 test/selbsttest.py
```
dann `sh release.sh` (git push, alle Bücher `update.sh lokal ja`) und in Leben123 bauen im Menü.

## Lehren
- Vor «es gab mal …» im Code und CHANGELOG suchen (grep), nicht annehmen. Bevor man den Motor verdächtigt: md-history vergleichen.
- Status-Dateien nur über das erste Wort lesen (`split()[0]`).
- Beide Fassungen bauen parallel: gemeinsame Druckdateien atomar schreiben.
- `@DECORATE-ABOVE-BOTTOM-N` braucht N mm Platz; Doppelseite: auf beiden Seiten denselben, kleineren Wert.
- Umflossene Bilder: Klasse `UmflossenesBild` (eigene wrap/split), immer mit Seitenbild prüfen (pdftoppm).
- update.py behält nur den letzten `motor-alt-…`; Starter (build.sh usw.) erneuert update ausser Dateien mit `# eigen`.

## Offen / Ideen
- Fassung hinten auch für weitere Befehle (Analyse 21.11., siehe CHANGELOG 3.5.2 falls umgesetzt).
- Hörbuch-Leser (md2txt.sh) auf manuskript.zeilen() umstellen, wenn das Hörbuch ohnehin neu aufgenommen wird.
- Ein einzelner Absatz, der allein auf eine neue Seite rutscht, nimmt den Absatz davor mit.
