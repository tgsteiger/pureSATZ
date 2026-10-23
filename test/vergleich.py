#!/usr/bin/env python3
"""
vergleich.py – zwei Bauten Seite für Seite vergleichen (Text und Pixel), dazu E-Books Datei für Datei.

Gedacht für Motor-Änderungen: dasselbe Buch einmal mit dem alten und einmal mit dem neuen Motor bauen
(je in einer eigenen Kopie des Buchordners), dann:

    python3 test/vergleich.py <alter-Buchordner> <neuer-Buchordner>
    python3 test/vergleich.py <alt> <neu> --text      zusätzlich die geänderten Textzeilen zeigen

Verglichen werden alle Ordner «ausgabe-…»: PDFs (Seitenzahl, Text und Bild jeder Seite) und EPUBs
(jede enthaltene Datei). JPGs und TXT-Dateien nicht (enthalten Datum bzw. werden neu verpackt).
Ausgabe pro Datei «gleich» oder die abweichenden Seiten: T12 = Text anders, P12 = nur Bild anders.
Das Korrektur-PDF trägt Datum und Uhrzeit in der Kopfzeile und ist darum nie «gleich».
Rückgabewert 0 = alles gleich, 1 = Unterschiede. Braucht pypdfium2 und Pillow (in .venv vorhanden).
"""
import difflib
import glob
import os
import sys
import zipfile

try:
    import pypdfium2 as pdfium
    from PIL import ImageChops
except ImportError:
    sys.exit("Braucht pypdfium2 und Pillow – mit .venv/bin/python3 test/vergleich.py … aufrufen.")


def seiten_text(dok):
    return [dok[i].get_textpage().get_text_range() for i in range(len(dok))]


def pdf_vergleich(a, b, text_zeigen):
    da, db = pdfium.PdfDocument(a), pdfium.PdfDocument(b)
    ta, tb = seiten_text(da), seiten_text(db)
    diffs, details = [], []
    if len(ta) != len(tb):
        diffs.append(f"Seiten {len(ta)}->{len(tb)}")
    for i in range(min(len(ta), len(tb))):
        if ta[i] != tb[i]:
            diffs.append(f"T{i + 1}")
            if text_zeigen:
                details += [f"      S. {i + 1}: {z}" for z in difflib.unified_diff(
                    ta[i].split("\n"), tb[i].split("\n"), lineterm="", n=0) if z[:1] in "+-" and z[:3] not in ("+++", "---")]
            continue
        ia, ib = da[i].render(scale=0.7).to_pil(), db[i].render(scale=0.7).to_pil()
        if ia.size != ib.size or ImageChops.difference(ia.convert("RGB"), ib.convert("RGB")).getbbox():
            diffs.append(f"P{i + 1}")
    return diffs, details


def epub_vergleich(a, b):
    za, zb = zipfile.ZipFile(a), zipfile.ZipFile(b)
    na, nb = set(za.namelist()), set(zb.namelist())
    return [x for x in sorted(na | nb) if x not in na or x not in nb or za.read(x) != zb.read(x)]


def main():
    args = [x for x in sys.argv[1:] if not x.startswith("--")]
    if len(args) != 2:
        sys.exit(__doc__)
    alt, neu = (os.path.abspath(x) for x in args)
    text_zeigen = "--text" in sys.argv
    unterschied = False
    ordner = sorted({os.path.basename(p) for p in glob.glob(os.path.join(alt, "ausgabe-*")) + glob.glob(os.path.join(neu, "ausgabe-*"))
                     if os.path.isdir(p)})
    if not ordner:
        sys.exit("Keine Ordner «ausgabe-…» gefunden – zuerst in beiden Ordnern bauen.")
    for o in ordner:
        fa = {os.path.basename(f) for f in glob.glob(os.path.join(alt, o, "*")) if f.endswith((".pdf", ".epub"))}
        fb = {os.path.basename(f) for f in glob.glob(os.path.join(neu, o, "*")) if f.endswith((".pdf", ".epub"))}
        print(f"== {o}")
        for n in sorted(fa - fb):
            print(f"  {n}: nur im alten Bau"); unterschied = True
        for n in sorted(fb - fa):
            print(f"  {n}: nur im neuen Bau"); unterschied = True
        for n in sorted(fa & fb):
            pa, pb = os.path.join(alt, o, n), os.path.join(neu, o, n)
            if n.endswith(".pdf"):
                diffs, details = pdf_vergleich(pa, pb, text_zeigen)
            else:
                diffs, details = epub_vergleich(pa, pb), []
            print(f"  {n}: {'gleich' if not diffs else ' '.join(diffs[:40])}")
            for d in details[:60]:
                print(d)
            unterschied = unterschied or bool(diffs)
    print("\nAlles gleich." if not unterschied else "\nEs gibt Unterschiede (siehe oben).")
    sys.exit(1 if unterschied else 0)


if __name__ == "__main__":
    main()
