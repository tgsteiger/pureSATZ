# Anleitung für Claude: Hilfe (hilfe.html) aufräumen und verbessern

Zweck: Claude prüft die Hilfe selbständig, **zeigt Verbesserungen als Liste mit Kürzeln** und setzt sie erst nach
«go …» um. Erprobt beim Umbau 3.x (Hilfe G6, 21.11.2026). Technik: `KI-pureSATZ.md`. Datei ist öffentlich.

## Woraus die Hilfe entsteht
| Quelle | Was |
|---|---|
| `START.md` | Erste Schritte, «Gestalten: Ich will …» (Tabellen, Bilder der Befehle) |
| `motor/HILFE.md` | alles Weitere (Menü, Bauen, Variablen, Druck, Hörbuch, Glossar …) |
| `motor/hilfe.py` | baut hilfe.html + hilfe-ki.md; Listen darin: `BEFEHL_GRUPPEN` (Abschnitt «Befehle (@)»), `SPICKZETTEL` (Befehle zum Kopieren, Menü `:`), `LOESUNGEN` |
| `test/hilfe-bilder.py` | Bilder `motor/bilder/hilfe/*.png` mit dem echten Motor (`python3 test/hilfe-bilder.py <name>`) |
| `docs/landingpage.py` | Webseite (docs/index.html, docs/hilfe.html) |
| pureSATZ-Handbuch | Buch, entsteht beim Bau aus der Hilfe – ändert sich mit |
Massgebend für Befehle ist der Code: `motor/manuskript.py` (`NAMEN`, `FASSUNG`, `HINTEN`, `ORT`, `STIL`, `_pruefe`).

## Regeln für gute Hilfe
- Jede Sache steht **an einer Stelle**; anderswo nur ein Link `[→ Titel](#Titel)`.
- Kurz. Erst das Häufige, dann Ausnahmen. Tabellen «Ich will … | So». Ein Bild sagt mehr als drei Sätze.
- Keine Versionsgeschichte («seit 2.84», «früher …») – die steht im CHANGELOG.
- Ein Wort pro Sache: Fassung **normal** / **UC**, **Lese-PDF**, final, komplett. Menütasten = Terminal-Befehle.
- Alte Schreibweisen nur im Abschnitt zum Umstellen (`um`), nirgends sonst.
- Schweizer Schreibweise (ss, «»), keine Doppelformen («Leser»).

## Ablauf
1. **Holen:** ganzes pureSATZ (Unterordner einzeln), neuestes `hilfe.html` erzeugen: `python3 motor/hilfe.py`.
2. **Bestandesaufnahme** (alles mit Zahlen festhalten):
   - Jeder Befehl aus `NAMEN` und jede Fassung: kommt er in «Befehle (@)» vor? Steht er doppelt (grep `@NAME` in START.md, HILFE.md, hilfe.py)?
     Ist die Schreibweise wie im Code (`_pruefe` erlaubt sie)? Fassung vorne/hinten richtig beschrieben?
   - Veraltetes: `grep -nE "[0-9]\.[0-9]{2}|früher|alt:|Bildschirm-PDF|Unzensiert|UZ\b|zweite Ausgabe"` (Fundstellen einzeln beurteilen).
   - Menü: Tasten in der Hilfe gegen `motor/menu.py` (Menütext, Untermenüs) – Menütext aus der echten Ausgabe.
   - Längste Abschnitte (Zeilen je `##`), Abschnitte ohne Bild, die eins bräuchten, Bilder ohne Verwendung.
   - Tote Links (Skript unten), Links der Webseite auf hilfe.html.
3. **Vorschläge zeigen** – Tabelle mit Kürzel, Was, Gewinn für den Leser, Aufwand, Empfehlung. Beispiel:
   | | Was | Gewinn | Aufwand |
   |---|---|---|---|
   | H1 | «Befehle (@)» als eine Übersicht: Befehl · Wirkung · Fassung vorne/hinten · Bild | alles auf einen Blick | mittel |
   | H2 | Doppelte Liste in «Schreiben» → Link | weniger lesen | klein |
   Dann auf «go …» warten. Nichts umsetzen, was nicht freigegeben ist.
4. **Umsetzen** in START.md / HILFE.md / hilfe.py, Bilder mit `test/hilfe-bilder.py` (neues Muster in `MUSTER`).
5. **Prüfen:**
   - `python3 motor/hilfe.py` · `python3 docs/landingpage.py ohne-bilder` · Linkprüfer → «tote Links: keine».
   - Seite ansehen (HTML im Browser oder als PDF/PNG), Suche nach einem Befehl ausprobieren.
   - Selbsttest (baut auch das Hallo-Buch und prüft die Hilfe mit).
   - Handbuch: E-Book bauen und alt/neu vergleichen – Unterschiede nur dort, wo die Hilfe geändert wurde.
6. **Zurückschreiben** wie in KI-pureSATZ.md (holen, sichern, schreiben, vergleichen), CHANGELOG-Zeile, Thomas macht Release.

## Linkprüfer
Anker entstehen im Browser: `#Text` trifft den ersten Abschnitt (`<h2>`), dessen Titel – klein, ohne Akzente,
ä→a, nur Buchstaben/Ziffern – diesen Text enthält.
```python
import re, sys, unicodedata, html
def k(t):
    t = unicodedata.normalize("NFD", t.lower()); t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    for a, b in (("ae", "a"), ("oe", "o"), ("ue", "u"), ("ß", "ss")): t = t.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "", t)
for f in sys.argv[1:]:                      # python3 anker.py hilfe.html docs/hilfe.html
    s = open(f, encoding="utf-8").read()
    ids = set(re.findall(r'id="([^"]+)"', s))
    h2 = [k(html.unescape(re.sub(r"<[^>]+>", "", t))) for t in re.findall(r"<h2[^>]*>(.*?)</h2>", s, re.S)]
    tot = sorted({z for z in re.findall(r'href="#([^"]+)"', s)
                  if z not in ids and not any(k(z) in t for t in h2) and not z.startswith("suche=")})
    print(f"{f}: {len(h2)} Abschnitte, tote Links: {tot or 'keine'}")
```
