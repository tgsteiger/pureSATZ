#!/usr/bin/env python3
"""
stichworte-vorschlag.py – Stichwortverzeichnis: Vorschläge machen und übernehmen.

Aufruf (im Buchordner):
    sh build.sh stichworte              prüft (stichworte: ja? @STICHWORTE im Buch? Stichwortdatei?)
                                        und schreibt stichworte-vorschlag.txt (Begriffe mit Häufigkeit)
    sh build.sh stichworte uebernehmen  alle mit [+] markierten Vorschläge unten an stichworte-<name>.txt anhängen

In stichworte-vorschlag.txt:  [ ] = Vorschlag · [+] = übernehmen · [x] = steht schon in der Stichwortdatei.
Markierte [+] bleiben beim nächsten Vorschlag erhalten. Vor dem Übernehmen wird die Stichwortdatei nach
md-history/ gesichert. Danach in stichworte-<name>.txt Varianten mit | ergänzen und neu bauen.
"""
import os
import re
import shutil
from collections import Counter

import sys
try:                                            # Windows: «sh build.sh» in Meldungen als «.\build.bat»
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "."))
    import plattform
    plattform.windows_befehle()
except ImportError:
    pass
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # Buchordner
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as bk      # findet die Buch-MD
import manuskript as M
TEXT = os.path.join(BASE, bk.TEXT)
AUS = os.path.join(BASE, "stichworte-vorschlag.txt")

# Häufige Wörter, die als Stichwort nichts taugen
STOPP = set("""
Ich Und Die Der Das Den Dem Des Ein Eine Einen Einem Einer Es Er Sie Wir Ihr Du Dein Deine Mein Meine
Meinen Meinem Meiner Mir Mich Dich Dir Uns Was Wie Wo Wer Wenn Dann Doch Aber Auch Als Am Im In An Auf
Aus Bei Mit Nach Von Vor Zu Zum Zur Um Über Unter Durch Für Ohne Gegen So Da Dort Hier Heute Damals Jetzt
Noch Nur Schon Immer Nie Oft Mal Einmal Erst Später Danach Dabei Darum Daher Also Nun Ja Nein Nicht
Kein Keine Alle Alles Viele Vieles Manche Manchmal Jede Jeder Jedes Diese Dieser Dieses Diesen Jahr
Jahre Jahren Zeit Tag Tage Woche Wochen Monate Mensch Menschen Leben Weg Teil Seite Mann Frau Kind
Herz Licht Welt Ende Anfang Moment Momente Gefühl Thema Themen Frage Fragen Antwort Sinn Kraft Ruhe
Sommer Winter Morgen Abend Nacht Hand Kopf Körper Bild Buch Bücher Blick Gedanken Freude Liebe Angst
Danke Vorschlag
""".split())


def text_ohne_markup():
    t = "\n".join(z for _, z in M.lies(TEXT)[1])          # mit eingebundenen Geschichten
    t = re.sub(r"^(:::.*|@.*|datei:.*|breite:.*|fluss:.*|Vorschlag:.*)$", " ", t, flags=re.M)
    t = re.sub(r"[#*>~|]", " ", t)
    return t


def vorhandene():
    w = set()
    for z in bk.stichwort_zeilen():      # stichworte-<name>.txt
        z = z.split("#", 1)[0].replace("->", "|").replace("=", "|")
        w |= {v.strip() for v in z.split("|") if v.strip()}
    return w


def markiert():
    """Begriffe, die in der alten stichworte-vorschlag.txt mit [+] markiert sind."""
    if not os.path.exists(AUS):
        return []
    m = [re.match(r"\[\+\]\s*(.+?)(?:\s+\(\d+\))?\s*$", z) for z in open(AUS, encoding="utf-8").read().splitlines()]
    return [x.group(1) for x in m if x]


def ziel():
    """Stichwortdatei: die vorhandene, sonst stichworte-<name>.txt (wird beim Übernehmen angelegt)."""
    return bk.stichwort_datei() or f"stichworte-{bk.NAME}.txt"


def pruefen():
    """Kurz zeigen, ob das Stichwortverzeichnis ins Buch kommt. Rückgabe: alles in Ordnung?"""
    gut = True
    if bk.ja("stichworte"):
        print("  ok  {stichworte}: ja")
    else:
        print(f"  !!  {{stichworte}}: nein – in {bk.VARIABLEN} auf «ja» setzen, sonst kein Verzeichnis"); gut = False
    if any(z.strip() == "@STICHWORTE" for _, z in M.lies(TEXT)[1]):
        print(f"  ok  @STICHWORTE steht in {bk.TEXT}")
    else:
        print(f"  !!  @STICHWORTE fehlt in {bk.TEXT} – eigene Zeile am Schluss (vor @RUECKSEITE), sonst kein Verzeichnis")
        gut = False
    if bk.stichwort_datei():
        n = sum(1 for z in bk.stichwort_zeilen() if z.split("#", 1)[0].strip())
        print(f"  ok  {bk.stichwort_datei()}: {n} Einträge")
    else:
        print(f"  ..  {ziel()} gibt es noch nicht – entsteht beim Übernehmen")
    return gut


def vorschlagen():
    pruefen()
    t = text_ohne_markup()
    # Einzelwörter mit Grossbuchstaben (Substantive, Namen) und Zwei-Wort-Namen
    woerter = re.findall(r"\b[A-ZÄÖÜ][\wäöüß'\-]{3,}\b", t)
    paare = re.findall(r"\b([A-ZÄÖÜ][\wäöüß\-]+ [A-ZÄÖÜ][\wäöüß\-]+)\b", t)
    zaehl = Counter(w for w in woerter if w not in STOPP)
    zaehl2 = Counter(p for p in paare if not set(p.split()) & STOPP)
    da = vorhandene()
    plus = set(markiert())

    def zeichen(w):
        return "[x]" if w in da else ("[+]" if w in plus else "[ ]")
    with open(AUS, "w", encoding="utf-8") as f:
        f.write("# Vorschläge fürs Stichwortverzeichnis (Häufigkeit im Text)\n")
        f.write(f"# [ ] = Vorschlag · [+] = übernehmen · [x] = steht schon in {ziel()}\n")
        f.write("# Gewünschte Begriffe: [ ] durch [+] ersetzen, speichern, dann: sh build.sh stichworte uebernehmen\n")
        f.write("\n# Namen und Begriffe aus zwei Wörtern\n")
        for p, n in zaehl2.most_common():
            if n >= 2:
                f.write(f"{zeichen(p)} {p}  ({n})\n")
        f.write("\n# Einzelne Begriffe\n")
        for w, n in zaehl.most_common():
            if n >= 2:
                f.write(f"{zeichen(w)} {w}  ({n})\n")
    print(f"\nVorschläge gespeichert: {os.path.basename(AUS)}"
          f"{f' ({len(plus - da)} mit [+] markiert)' if plus - da else ''}")
    print("Nächster Schritt: gewünschte Begriffe mit [+] markieren, dann: sh build.sh stichworte uebernehmen")


def uebernehmen():
    if not os.path.exists(AUS):
        sys.exit("Noch keine stichworte-vorschlag.txt – zuerst: sh build.sh stichworte")
    da = {w.lower() for w in vorhandene()}
    neu, doppelt = [], 0
    for w in markiert():
        if w.lower() in da or w.lower() in (x.lower() for x in neu):
            doppelt += 1
        else:
            neu.append(w)
    datei = ziel()
    pfad = os.path.join(BASE, datei)
    if not neu:
        print(f"Nichts zu übernehmen – keine neuen Begriffe mit [+] in stichworte-vorschlag.txt"
              f"{f' ({doppelt} stehen schon in {datei})' if doppelt else ''}.")
        return
    if os.path.exists(pfad):                     # zuerst sichern
        from datetime import datetime
        ordner = os.path.join(BASE, "md-history")
        os.makedirs(ordner, exist_ok=True)
        stamm, endung = os.path.splitext(datei)
        shutil.copy2(pfad, os.path.join(ordner, f"{stamm}_{datetime.now():%Y%m%d-%H-%M-%S}{endung}"))
        alt = open(pfad, encoding="utf-8").read()
    else:
        alt = ("# Stichwortverzeichnis – eine Zeile pro Stichwort, Varianten mit | trennen, # = Kommentar.\n"
               "#   Quelle = göttlichen Quelle | Urquelle   Eintrag links vom =, gesucht wird nur rechts\n"
               "#   Gott -> Quelle                          Verweis «Gott, siehe Quelle» (ohne Seitenzahl)\n")
    from datetime import date
    with open(pfad, "w", encoding="utf-8") as f:
        f.write(alt.rstrip("\n") + f"\n\n# --- übernommen {date.today():%d.%m.%Y}\n" + "\n".join(neu) + "\n")
    zeilen = open(AUS, encoding="utf-8").read().replace("[+]", "[x]")      # Vorschlagsliste nachführen
    open(AUS, "w", encoding="utf-8").write(zeilen)
    print(f"{len(neu)} Stichwort(e) übernommen nach {datei}"
          f"{f' ({doppelt} standen schon drin)' if doppelt else ''}:")
    print("  " + " · ".join(neu))
    print()
    pruefen()
    print(f"\nNächster Schritt: in {datei} Varianten mit | ergänzen (z. B. Seele | Seelen), dann: sh build.sh schnell")


def main():
    if any(a.lower() in ("uebernehmen", "übernehmen") for a in sys.argv[1:]):
        uebernehmen()
    else:
        vorschlagen()


if __name__ == "__main__":
    main()
