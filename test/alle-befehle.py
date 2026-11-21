#!/usr/bin/env python3
"""
alle-befehle.py – Testbuch mit jedem Befehl (pureSATZ 3.0), Teil des Selbsttests.

    python3 test/alle-befehle.py            Testbuch im Temp-Ordner bauen (final), prüfen, wieder löschen
    python3 test/alle-befehle.py <ordner>   Testbuch in <ordner> anlegen und bauen – bleibt stehen

Grundlage ist das Demo-Kapitel der Vorlage (vorlage/buch.md), dazu ein Kapitel mit allem, was dort fehlt.
Prüft, dass jeder Befehl aus manuskript.py (NAMEN, FASSUNG) im Buch steht – ein neuer Befehl gehört auch hierher.
Für Motor-Änderungen: einmal mit altem, einmal mit neuem pureSATZ in zwei Ordner bauen, dann
    python3 test/vergleich.py <ordner-alt> <ordner-neu>
"""
import contextlib
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile

HIER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))     # Ordner pureSATZ
sys.path.insert(0, os.path.join(HIER, "setup"))
sys.path.insert(0, os.path.join(HIER, "motor"))
import setup as S            # noqa: E402
import manuskript as M       # noqa: E402

WERTE = dict(TITEL="Alle Befehle", UNTERTITEL="Testbuch für den Motor", AUTOR="Vorname Nachname", NAME="Alle",
             FORMAT="a5", BINDUNG="beide", ZWEITE_AUSGABE="ja", ZWEITE_NAME="Unzensiert", ORT="Bern", JAHR="2027",
             WEBSITE="www.beispiel.ch", ADRESSE="Strasse 1, 3000 Bern")
TEXT = ("Ein gewöhnlicher Absatz, damit man sieht, wie der Fliesstext daneben wirkt. "
        "Noch ein Satz, damit der Absatz etwas länger wird und mehrere Zeilen füllt.")

# Was die Vorlage nicht zeigt (Reihenfolge = im Buch). Kein Bereich im Bereich.
KAPITEL = f"""## Alle Befehle

@HEADER Kopfzeile von Hand

{TEXT}

@NORMAL-ASIDE Randbemerkung nur in der normalen Ausgabe.

@UC-ASIDE Randbemerkung nur in der zweiten Ausgabe.

@PRINT
Dieser Absatz steht nur im Druck.
@END

@SCREEN
Dieser Absatz steht nur im Lese-PDF.
@END

@EBOOK-SPACER-6

@UC-DECORATE Ein Satz mit Linien, nur in der zweiten Ausgabe.

@DECORATE-LOGO

@DECORATE-TEXT-BOTTOM Ein Satz unten auf der Seite.

@HEADER

@NEWPAGE

### Logos

{TEXT}

@LOGO

{TEXT}

@LOGO-6-GAP

### Nach der Lücke

{TEXT}

@LOGO-8-REST

{TEXT}

@LOGO-10-BOTTOM

@UC-HEADER Nur Unzensiert

### Bilder und QR

#### @PICTURE-35-LEFT Klein links
datei: beispiel.jpg
text: @PICTURE-35-LEFT
quelle: Foto: Test

{TEXT} {TEXT}

#### @UC-PICTURE-70 Nur in der zweiten Ausgabe
datei: beispiel-hoch.jpg
text: @UC-PICTURE-70

@QR https://www.beispiel.ch | Ein QR-Code

@QR-RIGHT https://www.beispiel.ch/blog

{TEXT} {TEXT}

@UC-HEADER

@NEWPAGE-60

### Tabellen und Geschichte

@#breit

@@eine-geschichte

@NEWPAGE

@PAGE-CENTER

@DECORATE-REST-UPRIGHT Mitte des Rests, aufrecht.

{TEXT}

@DECORATE-REST-UPRIGHT-MAIN Mitte des Rests, in der Hauptfarbe.

{TEXT}

@UC-DECORATE-ABOVE-REST Schlusssatz mit Linie oben, nur Unzensiert.

{TEXT}

@DECORATE-ABOVE-REST Schlusssatz mit Linie oben.

{TEXT}

@DECORATE-ABOVE-BOTTOM-34 Schlusssatz auf fester Höhe, \\
mit Zeilenumbruch.

@UC-TIMELINE
2020 | Nur in der zweiten Ausgabe
2027 | Noch eine Zeile
@END

@KEEP-TOGETHER
{TEXT}
@DECORATE Ein Satz im Bereich.
@ASIDE Eine Randbemerkung im Bereich.
@END

@UC
#### @PICTURE-30 Bild im Bereich
datei: beispiel.jpg
text: Bild in @UC … @END

Ein Absatz nur in der zweiten Ausgabe, nach dem Bild.
@END

@NEWPAGE

Fassung hinten: der Text steht in beiden Ausgaben, verziert nur in einer.

@DECORATE-UC Ein Satz mit Linien nur in UC, in Normal ein Absatz.

@N-ASIDE Randbemerkung nur normal (Kurzform @N).

@DECORATE-REST-ITALIC-NORMAL
**Rückblick**

Verziert nur in Normal, in UC gewöhnliche Absätze.
@END

{TEXT}

@DECORATE-ABOVE-REST-UC Schlusssatz mit Linie nur in UC, Text in beiden.

"""

GESCHICHTE = f"""## Eine Geschichte
- stand: fertig
- stichworte: Geschichte, Test
- quelle: alle-befehle.py

{TEXT}

@DECORATE Ein Satz in der Geschichte.
"""

VERZEICHNISSE = "@LIST-PICTURES\n\n@LIST-TABLES\n\n@PICTURE-CREDITS\n\n"


def anlegen(ordner):
    """Buch aus der Vorlage, Motor dazu, Kapitel, Geschichte und breite Tabelle ergänzen."""
    with contextlib.redirect_stdout(io.StringIO()):
        S.buch(ordner, dict(WERTE))
        S.motor(ordner, venv=False)
    md = os.path.join(ordner, "Alle-buch.md")
    t = open(md, encoding="utf-8").read()
    for alt, neu in (("# Teil 2|", KAPITEL + "# Teil 2|"), ("@INDEX\n", VERZEICHNISSE + "@INDEX\n")):
        if alt not in t:
            sys.exit(f"FEHLER: «{alt.strip()}» fehlt in vorlage/buch.md")
        t = t.replace(alt, neu, 1)
    open(md, "w", encoding="utf-8").write(t)
    open(os.path.join(ordner, "geschichten", "eine-geschichte.md"), "w", encoding="utf-8").write(GESCHICHTE)
    open(os.path.join(ordner, "tabellen", "breit.csv"), "w", encoding="utf-8").write(
        "Breite Tabelle\n" + ";".join(f"Spalte {i}" for i in range(10)) + "\n"
        + "\n".join(";".join(f"Inhalt {r}-{i}" for i in range(10)) for r in range(4)) + "\nQuelle: Test\n")
    return t


def fehlende(t):
    """Befehle aus manuskript.py, die im Buch nicht am Zeilenanfang stehen."""
    da = set()
    for z in t.split("\n"):
        b = M.befehl(z)
        if b:
            da.add(b.name)
            da.update(k for k in M.FASSUNG if z.lstrip("# ").startswith((f"@{k}-", f"@{k} ")) or z.strip() == f"@{k}")
    return [n for n in list(M.NAMEN) + list(M.FASSUNG) if n not in da]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    tmp = None if args else tempfile.mkdtemp(prefix="alle-befehle-")
    ordner = os.path.abspath(args[0]) if args else os.path.join(tmp, "Alle")
    try:
        if os.path.exists(ordner):
            sys.exit(f"FEHLER: {ordner} gibt es schon – leeren Ordner angeben.")
        t = anlegen(ordner)
        fehlt = fehlende(t)
        if fehlt:
            sys.exit("FEHLER: Diese Befehle fehlen im Testbuch: " + ", ".join("@" + n for n in fehlt))
        r = subprocess.run([sys.executable, os.path.join("motor", "bauen.py"), "final"], cwd=ordner,
                           capture_output=True, text=True, encoding="utf-8", errors="replace",
                           env=dict(os.environ, PYTHONIOENCODING="utf-8"))
        if r.returncode or "FEHLER" in r.stdout:
            sys.exit(r.stdout[-3000:] + r.stderr[-3000:] + "\nFEHLER: Testbuch «alle Befehle» lässt sich nicht bauen.")
        soll = [os.path.join("ausgabe-normal", f) for f in ("Alle.pdf", "Alle.epub", "ALLE_Buchblock.pdf",
                                                            "ALLE_Umschlag_Hardcover.pdf", "ALLE_Umschlag_Softcover.pdf")]
        soll += [os.path.join("ausgabe-unzensiert", f) for f in ("Alle_Unzensiert.pdf", "Alle_Unzensiert.epub")]
        weg = [f for f in soll if not os.path.exists(os.path.join(ordner, f))]
        if weg:
            sys.exit("FEHLER: Testbuch «alle Befehle»: es fehlt " + ", ".join(weg))
        print(f"Testbuch «alle Befehle» in Ordnung ({len(M.NAMEN)} Befehle, {len(M.FASSUNG)} Fassungen).")
    finally:
        if tmp:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
