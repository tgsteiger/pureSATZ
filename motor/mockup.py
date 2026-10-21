#!/usr/bin/env python3
"""
mockup.py – Werbebild des Buchs: Vorder- und Rückseite leicht gedreht, mit Schatten (pureSATZ ab 2.17).

Aus dem Bildschirm-PDF (erste Seite = Vorderseite, letzte Seite = Rückseite) entsteht im Ausgabeordner
    <datei>_Mockup.jpg          quadratisch, 1600 × 1600 Pixel – für Webseite, Newsletter, Shop, Social Media
    <datei>_Vorderseite.jpg     nur die Vorderseite, gerade, mit Schatten (z. B. für die Startseite)

Entsteht automatisch bei «sh build.sh final» und «sh build.sh nur-pdf final»,
oder jederzeit aus dem vorhandenen PDF mit «sh build.sh mockup».
Variable «mockup-hintergrund: #E9EEF4, #C9D3DF» (oben, unten) ändert den Hintergrund.
"""
import os
import sys


def _seite(doc, i, breite):
    from PIL import Image
    s = doc[i]
    w, _ = s.get_size()
    im = s.render(scale=breite / w * 1.0).to_pil().convert("RGB")
    return im.resize((breite, round(im.height * breite / im.width)), Image.LANCZOS)


def _mit_schatten(seite, winkel, unschaerfe=26, versatz=(14, 22), deckkraft=95):
    """Seite drehen, darunter einen weichen Schatten. Gibt RGBA zurück."""
    from PIL import Image, ImageFilter
    rand = unschaerfe * 3
    w, h = seite.size
    maske = Image.new("L", (w, h), 255)
    gross = (w + 2 * rand, h + 2 * rand)
    schatten = Image.new("L", gross, 0)
    schatten.paste(Image.new("L", (w, h), deckkraft), (rand + versatz[0], rand + versatz[1]))
    schatten = schatten.filter(ImageFilter.GaussianBlur(unschaerfe))
    bild = Image.new("RGBA", gross, (0, 0, 0, 0))
    bild.paste(Image.merge("RGBA", (*Image.new("RGB", gross, (40, 50, 70)).split(), schatten)), (0, 0))
    bild.paste(seite.convert("RGBA"), (rand, rand), maske)
    return bild.rotate(winkel, resample=Image.BICUBIC, expand=True)


def _hintergrund(groesse, oben, unten):
    from PIL import Image
    spalte = Image.new("RGB", (1, groesse))
    for y in range(groesse):
        t = y / (groesse - 1)
        spalte.putpixel((0, y), tuple(round(a + (b - a) * t) for a, b in zip(oben, unten)))
    return spalte.resize((groesse, groesse))


def _hex(h):
    h = h.strip().lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def erzeuge(pdf, hintergrund="#E9EEF4, #C9D3DF", groesse=1600):
    """Mockup und Vorderseite neben das PDF legen. Gibt die Pfade zurück."""
    import pypdfium2 as pdfium
    from PIL import Image
    doc = pdfium.PdfDocument(pdf)
    if len(doc) < 2:
        return []
    try:
        oben, unten = (_hex(x) for x in hintergrund.split(","))
    except ValueError:
        oben, unten = _hex("#E9EEF4"), _hex("#C9D3DF")
    breite = round(groesse * 0.42)
    vorne, hinten = _seite(doc, 0, breite), _seite(doc, len(doc) - 1, breite)

    bg = _hintergrund(groesse, oben, unten).convert("RGBA")
    h = _mit_schatten(hinten, 7)
    v = _mit_schatten(vorne, -3)
    xh = (groesse - round(h.width * 0.62) - v.width) // 2           # beide zusammen mittig
    bg.alpha_composite(h, (max(0, xh), max(0, (groesse - h.height) // 2 + round(groesse * 0.035))))
    bg.alpha_composite(v, (max(0, xh + round(h.width * 0.62)), max(0, (groesse - v.height) // 2 - round(groesse * 0.035))))
    stamm = os.path.splitext(pdf)[0]
    ziel = stamm + "_Mockup.jpg"
    bg.convert("RGB").save(ziel, quality=90, optimize=True)

    g2 = (round(breite * 1.5), round(vorne.height * 1.25))
    bg2 = _hintergrund(max(g2), oben, unten).crop((0, 0) + g2).convert("RGBA")
    v2 = _mit_schatten(vorne, 0)
    bg2.alpha_composite(v2, ((g2[0] - v2.width) // 2, (g2[1] - v2.height) // 2))
    ziel2 = stamm + "_Vorderseite.jpg"
    bg2.convert("RGB").save(ziel2, quality=90, optimize=True)
    return [ziel, ziel2]


if __name__ == "__main__":
    # python3 motor/mockup.py <Bildschirm-PDF>
    for p in erzeuge(sys.argv[1]):
        print("Mockup:", p)
