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


def teil_seiten(pdf):
    """Seiten der Teile (und des Anhangs): Lesezeichen der obersten Ebene, die Unterpunkte haben."""
    from pypdf import PdfReader
    r = PdfReader(pdf)
    o, seiten = list(r.outline), []
    for i, e in enumerate(o):
        if not isinstance(e, list) and i + 1 < len(o) and isinstance(o[i + 1], list):
            seiten.append(r.get_destination_page_number(e) + 1)
    return seiten


def doppelseiten(pdf, ziel, titel="", schrift=None, breite=120):
    """3.7: Alle Seiten als Doppelseiten auf einem PNG (Seite 1 allein rechts). Teil-Seiten mit Rahmen:
    grün = rechts, rot = links. Gibt (teile, rechts) zurück; None, wenn kein Werkzeug zum Rendern da ist."""
    from PIL import Image, ImageDraw, ImageFont
    seiten = []
    if pdfium is not None:
        doc = pdfium.PdfDocument(pdf)
        for s in doc:
            seiten.append(s.render(scale=breite / s.get_size()[0]).to_pil().convert("RGB"))
        doc.close()
    elif shutil.which("pdftoppm"):
        with tempfile.TemporaryDirectory() as t:
            subprocess.run(["pdftoppm", "-scale-to-x", str(breite), "-scale-to-y", "-1", "-png", pdf,
                            os.path.join(t, "s")], check=True)
            seiten = [Image.open(os.path.join(t, f)).convert("RGB") for f in sorted(os.listdir(t))]
    else:
        return None
    teile = teil_seiten(pdf)
    w, h = seiten[0].size
    try:
        f1 = ImageFont.truetype(schrift, 15) if schrift else ImageFont.load_default()
        f2 = ImageFont.truetype(schrift, 12) if schrift else ImageFont.load_default()
    except OSError:
        f1 = f2 = ImageFont.load_default()
    paare = [[None, 1]] + [[i, i + 1 if i + 1 <= len(seiten) else None] for i in range(2, len(seiten) + 1, 2)]
    pro, sw, sh = 7, 2 * w + 14, h + 24
    C = Image.new("RGB", (pro * sw + 20, ((len(paare) + pro - 1) // pro) * sh + 46), (225, 225, 225))
    D = ImageDraw.Draw(C)
    rechts = sum(1 for t in teile if t % 2)
    D.text((10, 12), f"{titel} · {len(seiten)} Seiten · Teile rechts: {rechts} von {len(teile)} "
                     "(grün = rechts, rot = links)", fill="black", font=f1)
    for k, paar in enumerate(paare):
        x0, y0 = 10 + (k % pro) * sw, 42 + (k // pro) * sh
        for j, n in enumerate(paar):
            if n is None:
                continue
            x = x0 + j * w
            C.paste(seiten[n - 1], (x, y0))
            if n in teile:
                D.rectangle([x, y0, x + w - 1, y0 + h - 1], outline=(0, 150, 0) if n % 2 else (210, 0, 0), width=4)
        D.text((x0 + w - 14, y0 + h + 4), "–".join(str(n) for n in paar if n), fill=(60, 60, 60), font=f2)
    C.save(ziel)
    return teile, rechts
