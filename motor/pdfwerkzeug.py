"""
pdfwerkzeug.py – PDF-Seiten als Bild (Cover-JPG, E-Book-Titelbild) und Textzeilen messen (Korrekturfassung).

Läuft auf Linux, macOS und Windows mit dem Python-Paket pypdfium2 (wird von einrichten.py installiert).
Fehlt es, wird – wie früher – poppler (pdftoppm, pdftotext) benutzt, falls installiert.
"""
import os
import re
import shutil
import subprocess
import tempfile

try:
    import pypdfium2 as pdfium
except ImportError:
    pdfium = None


def verfuegbar():
    return pdfium is not None or shutil.which("pdftoppm") is not None


def als_jpg(pdf, ziel, dpi=None, breite=None, qualitaet=95, seite=1):
    """Eine PDF-Seite als JPG speichern: mit dpi (z. B. 400) oder fester Breite in Pixeln. Gibt True/False."""
    if pdfium is not None:
        doc = pdfium.PdfDocument(pdf)
        s = doc[seite - 1]
        w, _ = s.get_size()
        massstab = (breite / w) if breite else (dpi or 300) / 72
        bild = s.render(scale=massstab).to_pil().convert("RGB")
        bild.save(ziel, quality=qualitaet, **({"dpi": (dpi, dpi)} if dpi else {}))
        doc.close()
        return True
    if shutil.which("pdftoppm"):
        groesse = ["-r", str(dpi)] if dpi else ["-scale-to-x", str(breite), "-scale-to-y", "-1"]
        subprocess.run(["pdftoppm", "-f", str(seite), "-l", str(seite)] + groesse +
                       ["-jpeg", "-jpegopt", f"quality={qualitaet}", "-singlefile", pdf, ziel[:-4]], check=True)
        return True
    return False


def zeilen_aller_seiten(pdf):
    """Pro Seite die Höhen (y von unten, in pt) aller Textzeilen, von oben nach unten."""
    roh = []
    if pdfium is not None:
        doc = pdfium.PdfDocument(pdf)
        for s in doc:
            tp = s.get_textpage()
            roh.append([tp.get_rect(i)[1] for i in range(tp.count_rects())])
        doc.close()
    else:
        with tempfile.TemporaryDirectory() as tmp:
            html = os.path.join(tmp, "z.html")
            subprocess.run(["pdftotext", "-bbox-layout", pdf, html], check=True)
            text = open(html, encoding="utf-8").read()
        for teil in text.split("<page ")[1:]:
            hoehe = float(re.search(r'height="([\d.]+)"', teil).group(1))
            roh.append([hoehe - float(m) for m in
                        re.findall(r'<line xMin="[\d.]+" yMin="[\d.]+" xMax="[\d.]+" yMax="([\d.]+)"', teil)])
    seiten = []
    for ys in roh:
        zeilen = []
        for y in sorted(ys, reverse=True):
            if not zeilen or zeilen[-1] - y > 6:          # Text auf derselben Höhe = eine Zeile
                zeilen.append(y)
        seiten.append(zeilen)
    return seiten


HINWEIS = ("Für Cover-JPG und E-Book-Titelbild fehlt pypdfium2. Einmalig im Buchordner: "
           "python3 motor/einrichten.py   (Windows: py motor\\einrichten.py)")
