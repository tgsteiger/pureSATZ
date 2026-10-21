#!/usr/bin/env python3
"""
booklet.py – ordnet ein PDF als Broschüre (Booklet) neu an.

Je zwei Originalseiten werden verkleinert nebeneinander auf ein
A4-Querformat-Blatt gesetzt, in der richtigen Reihenfolge zum Falten.
Danach einfach doppelseitig drucken: Wenden an der KURZEN Kante.

Aufruf:
    python3 booklet.py eingabe.pdf            -> eingabe_booklet.pdf
    python3 booklet.py eingabe.pdf ausgabe.pdf
    python3 booklet.py --beschnitt 3 ausgabe.pdf vorne.pdf buchblock.pdf hinten.pdf
        mehrere PDFs nacheinander, ringsum 3 mm Beschnitt wegschneiden (Probedruck)

Fehlende Seiten (auf ein Vielfaches von 4) werden als Leerseiten VOR der
letzten Seite eingefügt, damit die Rückseite des Umschlags aussen bleibt.
Mit der Option --leer-am-ende kommen sie wie früher ganz ans Ende.

Benötigt: pypdf  (ist in der Python-Umgebung .venv des Buchs enthalten)
"""

import sys
from pathlib import Path

try:
    from pypdf import PdfReader, PdfWriter, PageObject, Transformation
    from pypdf.generic import RectangleObject, ContentStream
except ImportError:
    PdfReader = None

# A4 quer in Punkt (1 pt = 1/72 Zoll)
SHEET_W, SHEET_H = 841.89, 595.28
HALF_W = SHEET_W / 2
MM = 72 / 25.4


def place(sheet, page, slot):
    """Setzt eine Seite skaliert und zentriert in die linke (0) oder rechte (1) Hälfte."""
    page.transfer_rotation_to_content()          # gedrehte Seiten korrekt behandeln
    box = page.cropbox
    w, h = float(box.width), float(box.height)
    scale = min(HALF_W / w, SHEET_H / h)
    x = slot * HALF_W + (HALF_W - w * scale) / 2
    y = (SHEET_H - h * scale) / 2
    t = (Transformation()
         .translate(-float(box.left), -float(box.bottom))
         .scale(scale, scale)
         .translate(x, y))
    sheet.merge_transformed_page(page, t)


def erstelle(eingaben, ziel, beschnitt_mm=0.0, leer_am_ende=False, leise=False):
    """Booklet aus einer oder mehreren PDF-Dateien (in dieser Reihenfolge).
    beschnitt_mm: ringsum wegschneiden (Buchblock und Cover für epubli haben 3 mm)."""
    if PdfReader is None:
        raise SystemExit("pypdf fehlt (python3 motor/einrichten.py richtet es ein).")
    seiten = []
    for pfad in eingaben:
        mm_rand = beschnitt_mm
        if isinstance(pfad, tuple):              # (datei, beschnitt in mm) je Datei
            pfad, mm_rand = pfad
        for p in PdfReader(str(pfad)).pages:
            if mm_rand:
                b = mm_rand * MM
                box = p.mediabox
                l, u, r, o = float(box.left) + b, float(box.bottom) + b, float(box.right) - b, float(box.top) - b
                p.cropbox = RectangleObject([l, u, r, o])
                # Inhalt auf den Endformat-Bereich begrenzen (sonst ragt der Beschnitt ins Nachbarbild)
                inhalt = p.get_contents()
                daten = inhalt.get_data() if inhalt is not None else b""
                clip = f"q {l:.3f} {u:.3f} {r - l:.3f} {o - u:.3f} re W n\n".encode()
                neu = ContentStream(None, None)
                neu.set_data(clip + daten + b"\nQ")
                p.replace_contents(neu)
            seiten.append(p)
    count = len(seiten)
    n = -(-count // 4) * 4                       # auf Vielfaches von 4 aufrunden
    leer = [None] * (n - count)
    if leer_am_ende or count < 2:
        seiten += leer
    else:
        seiten = seiten[:-1] + leer + seiten[-1:]
    writer = PdfWriter()
    for s in range(n // 4):
        # Vorderseite: [letzte, erste], Rückseite: [zweite, vorletzte]
        for left, right in ((n - 1 - 2 * s, 2 * s), (2 * s + 1, n - 2 - 2 * s)):
            sheet = PageObject.create_blank_page(width=SHEET_W, height=SHEET_H)
            for slot, idx in ((0, left), (1, right)):
                if seiten[idx] is not None:
                    place(sheet, seiten[idx], slot)
            writer.add_page(sheet)
    with open(ziel, "wb") as f:
        writer.write(f)
    if not leise:
        print(f"{count} Seiten -> {n // 4} Blätter ({n // 2} PDF-Seiten)")
        if n != count:
            wo = "am Ende" if leer_am_ende else "vor der letzten Seite"
            print(f"Hinweis: {n - count} Leerseite(n) {wo} eingefügt.")
        print(f"Gespeichert: {ziel}")
        print("Drucken: doppelseitig, Wenden an der KURZEN Kante, Grösse 100 %.")
    return n // 4


def main():
    argv = sys.argv[1:]
    beschnitt = 0.0
    if "--beschnitt" in argv:
        i = argv.index("--beschnitt"); beschnitt = float(argv[i + 1]); del argv[i:i + 2]
    leer_am_ende = "--leer-am-ende" in argv
    args = [a for a in argv if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    if len(args) > 2 or beschnitt:               # ausgabe.pdf eingabe1.pdf eingabe2.pdf …
        ziel, eingaben = Path(args[0]).expanduser(), [Path(a).expanduser() for a in args[1:]]
    else:
        src = Path(args[0]).expanduser()
        ziel = Path(args[1]).expanduser() if len(args) > 1 else src.with_name(src.stem + "_booklet.pdf")
        eingaben = [src]
    erstelle(eingaben, ziel, beschnitt, leer_am_ende)


if __name__ == "__main__":
    main()
