#!/usr/bin/env python3
"""
stichworte-vorschlag.py – macht Vorschläge für das Stichwortverzeichnis.

Durchsucht das Manuskript nach Begriffen, die oft vorkommen (Namen, Orte,
Methoden, Fachwörter) und schreibt sie mit Häufigkeit nach stichworte-vorschlag.txt.
Bereits vorhandene Stichwörter (stichworte-<name>.txt) sind mit [x] markiert.

Aufruf:   python3 motor/stichworte-vorschlag.py
Danach:   gewünschte Begriffe in stichworte-<name>.txt übernehmen (eine Zeile pro Stichwort,
          Varianten mit | trennen, z. B.  Seele | Seelen ) und neu bauen.
"""
import os
import re
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
LISTE = os.path.join(BASE, "stichworte.txt")
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


def main():
    t = text_ohne_markup()
    # Einzelwörter mit Grossbuchstaben (Substantive, Namen) und Zwei-Wort-Namen
    woerter = re.findall(r"\b[A-ZÄÖÜ][\wäöüß'\-]{3,}\b", t)
    paare = re.findall(r"\b([A-ZÄÖÜ][\wäöüß\-]+ [A-ZÄÖÜ][\wäöüß\-]+)\b", t)
    zaehl = Counter(w for w in woerter if w not in STOPP)
    zaehl2 = Counter(p for p in paare if not set(p.split()) & STOPP)
    da = vorhandene()
    with open(AUS, "w", encoding="utf-8") as f:
        f.write("# Vorschläge fürs Stichwortverzeichnis (Häufigkeit im Text)\n")
        f.write("# [x] = steht schon in stichworte.txt\n\n# Namen und Begriffe aus zwei Wörtern\n")
        for p, n in zaehl2.most_common():
            if n >= 2:
                f.write(f"{'[x]' if p in da else '[ ]'} {p}  ({n})\n")
        f.write("\n# Einzelne Begriffe\n")
        for w, n in zaehl.most_common():
            if n >= 2:
                f.write(f"{'[x]' if w in da else '[ ]'} {w}  ({n})\n")
    print(f"Vorschläge gespeichert: {AUS}")


if __name__ == "__main__":
    main()
