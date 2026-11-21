#!/usr/bin/env python3
"""
hilfe-bilder.py – Bilder für die Hilfe mit dem echten Motor erzeugen (pureSATZ 3.0).

    python3 test/hilfe-bilder.py            alle Bilder nach motor/bilder/hilfe/
    python3 test/hilfe-bilder.py decorate   nur dieses

Legt ein Musterbuch in einem Temp-Ordner an, baut jede Musterseite («schnell», Lese-PDF) und schneidet sie zu.
So stimmen die Bilder immer mit dem Motor überein. Braucht pypdfium2 und Pillow.
"""
import glob
import os
import shutil
import subprocess
import sys
import tempfile

import pypdfium2 as pdfium
from PIL import Image, ImageChops, ImageDraw, ImageFont

HIER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZIEL = os.path.join(HIER, "motor", "bilder", "hilfe")
SCHRIFT = os.path.join(HIER, "motor", "fonts", "Poppins-Medium.ttf")
BLAU = "#1E428A"
TEXT = ("Ein gewöhnlicher Absatz, damit man sieht, wie der Fliesstext daneben wirkt. "
        "Noch ein Satz, damit der Absatz etwas länger wird.")
KURZ = "Ein Absatz Fliesstext."

# name: (Fassung, Art, Markdown, Beschriftungen)  Art = «ausschnitt» oder Liste der Seiten (0 = erste Seite mit Text)
MUSTER = {
    "decorate": ("normal", "ausschnitt", f"""{TEXT}

@DECORATE Es ist so schön, hier zu sein.

{KURZ} Darüber: @DECORATE.

@DECORATE-TEXT Es ist so schön, hier zu sein.

{KURZ} Darüber: @DECORATE-TEXT.""", []),
    "aside": ("normal", "ausschnitt", f"""{TEXT}

@ASIDE Mein Tipp aus eigener Erfahrung: eine Randbemerkung mit @ASIDE – klein, kursiv, eingerückt.

{KURZ} Darüber: @ASIDE.""", []),
    "decorate-rest": ("normal", [0, 1, 2], f"""{TEXT}

@DECORATE-REST Es ist so schön, hier zu sein.

{TEXT}

@DECORATE-ABOVE-REST Es ist so schön, hier zu sein.

{TEXT}

@DECORATE-ABOVE-BOTTOM-34 Es ist so schön, hier zu sein.""",
                      ["@DECORATE-REST", "@DECORATE-ABOVE-REST", "@DECORATE-ABOVE-BOTTOM-34"]),
    "decorate-page": ("normal", [0, 1], f"""{TEXT}

@DECORATE-PAGE Es ist so schön, hier zu sein.""", ["davor", "@DECORATE-PAGE"]),
    "logo": ("normal", "ausschnitt", f"""{TEXT}

@LOGO-12

{KURZ} Darüber: @LOGO-12. Darunter: @LOGO-6-GAP vor dem Zwischentitel.

@LOGO-6-GAP

### Ein Zwischentitel

{KURZ}""", []),
    "logo-rest-bottom": ("normal", [0, 1], f"""{TEXT}

@LOGO-10-REST

{TEXT}

@LOGO-10-BOTTOM""", ["@LOGO-10-REST", "@LOGO-10-BOTTOM"]),
    "uc-block": ("uz", "ausschnitt", f"""{KURZ}

@UC-BLOCK Ein Kasten mit Titel
Dieser Kasten steht nur in der Fassung Unzensiert. In der normalen Fassung fehlt er ganz.
@END

{KURZ}""", []),
    "draft-note": ("normal", "ausschnitt", f"""@DRAFT
Über diesen Absatz ist noch nicht entschieden. Mit «s» gelb, mit «k» normal gedruckt.
@END

@NOTE Eine Notiz
Wird nie gedruckt – nur eine Erinnerung an dich.
@END""", []),
    "picture": ("normal", "ausschnitt", f"""#### @PICTURE-70 Ein Bild
datei: beispiel.jpg
text: @PICTURE-70: 70 mm breit, zentriert

#### @PICTURE-35-RIGHT Klein rechts
datei: beispiel.jpg
text: @PICTURE-35-RIGHT

{TEXT} Der Text fliesst links um das Bild herum, bis es zu Ende ist. {TEXT}""", []),
    "qr": ("normal", "ausschnitt", f"""@QR https://www.beispiel.ch | @QR mit Link: www.beispiel.ch

@QR https://www.beispiel.ch | Website ;; https://www.beispiel.ch/blog | Blog

@QR-RIGHT https://www.beispiel.ch

{TEXT} Der Text fliesst um den QR-Code (@QR-RIGHT).""", []),
    "timeline": ("normal", "ausschnitt", """@TIMELINE
1974 | Geboren
1990 | Lehre
2026 | Erstes Buch
@END""", []),
    "text": ("normal", "ausschnitt", """Ein Absatz mit **fett** und *kursiv*.\\
Nach dem Backslash beginnt eine neue Zeile im selben Absatz.

- Ein Punkt
- Noch ein Punkt
  - ein Unterpunkt

1. Erster Schritt
2. Zweiter Schritt

@ASIDE Eine Randbemerkung mit @ASIDE.""", []),
}


def musterbuch(tmp):
    """Musterbuch wie das Hallo-Buch anlegen (mit zweiter Fassung), Motor dazu."""
    sys.path.insert(0, os.path.join(HIER, "setup"))
    import setup as S
    w = S.lese_werte(os.path.join(HIER, "setup", "hallo.txt"))
    for k, _, vorgabe in S.FRAGEN:
        w.setdefault(k, vorgabe or "")
    w.update(NAME="Muster", TITEL="Muster", ZWEITE_AUSGABE="ja")
    ordner = os.path.join(tmp, "Muster")
    import contextlib
    import io
    with contextlib.redirect_stdout(io.StringIO()):
        S.buch(ordner, w)
        S.motor(ordner, venv=False)
    v = os.path.join(ordner, "Muster-variablen.md")              # Kasten wie bei Leben123: «UNZENSIERT»
    z = open(v, encoding="utf-8").read().split("\n")
    open(v, "w", encoding="utf-8").write("\n".join(z[:1] + ["{block-kopf}: UNZENSIERT"] + z[1:]))
    os.makedirs(os.path.join(ordner, "fotos"), exist_ok=True)
    shutil.copy(os.path.join(HIER, "motor", "bilder", "beispiel-foto.jpg"), os.path.join(ordner, "fotos", "beispiel.jpg"))
    return ordner


def bauen(ordner, md):
    with open(os.path.join(ordner, "Muster-buch.md"), "w", encoding="utf-8") as f:
        f.write("## @TITLE\n\n## Beispiel\n\n" + md + "\n")
    r = subprocess.run([sys.executable, os.path.join("motor", "bauen.py"), "schnell"], cwd=ordner,
                       capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stdout[-3000:] + r.stderr[-3000:])


def lese_pdf(ordner, fassung):
    """Lese-PDF der Fassung = kürzester PDF-Name im Ausgabeordner (ohne _Inhalt, _Booklet …)."""
    for d in sorted(glob.glob(os.path.join(ordner, "ausgabe-*"))):
        if (fassung == "uz") == (os.path.basename(d) == "ausgabe-normal"):
            continue
        pdfs = sorted(glob.glob(os.path.join(d, "*.pdf")), key=len)
        if pdfs:
            return pdfs[0]
    sys.exit(f"Kein Lese-PDF für {fassung}")


def seiten(pdf):
    dok = pdfium.PdfDocument(pdf)
    erste = next(i for i in range(len(dok)) if "Beispiel" in dok[i].get_textpage().get_text_range())
    return dok, erste


def bild(seite, scale):
    return seite.render(scale=scale).to_pil().convert("RGB")


def zuschneiden(img):
    """Kopf- und Fusszeile weg, dann auf den Inhalt zuschneiden (Hintergrund = Farbe der Ecke)."""
    w, h = img.size
    innen = img.crop((0, int(h * 0.085), w, int(h * 0.91)))
    grund = Image.new("RGB", innen.size, innen.getpixel((3, 3)))
    box = ImageChops.difference(innen, grund).convert("L").point(lambda v: 255 if v > 18 else 0).getbbox()
    if not box:
        return innen
    r = 18
    return innen.crop((max(0, box[0] - r), max(0, box[1] - r), min(w, box[2] + r), min(innen.height, box[3] + r)))


def rahmen(img, farbe="#C9C2B8"):
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, img.width - 1, img.height - 1], outline=farbe)
    return img


def nebeneinander(bilder, texte):
    luecke, oben = 22, 34 if texte else 0
    b = sum(i.width for i in bilder) + luecke * (len(bilder) - 1)
    neu = Image.new("RGB", (b, max(i.height for i in bilder) + oben), "white")
    x = 0
    for i, img in enumerate(bilder):
        neu.paste(rahmen(img), (x, oben))
        if texte:
            g = 17
            while g > 10 and ImageFont.truetype(SCHRIFT, g).getlength(texte[i]) > img.width:
                g -= 1
            ImageDraw.Draw(neu).text((x, 4), texte[i], fill=BLAU, font=ImageFont.truetype(SCHRIFT, g))
        x += img.width + luecke
    return neu


def speichern(img, name):
    os.makedirs(ZIEL, exist_ok=True)
    p = os.path.join(ZIEL, name + ".png")
    img.convert("P", palette=Image.ADAPTIVE, colors=96).save(p, optimize=True)
    return p


def main():
    nur = sys.argv[1:]
    tmp = tempfile.mkdtemp(prefix="hilfe-bilder-")
    try:
        ordner = musterbuch(tmp)
        for name, (fassung, art, md, texte) in MUSTER.items():
            if nur and name not in nur:
                continue
            bauen(ordner, md)
            dok, erste = seiten(lese_pdf(ordner, fassung))
            if art == "ausschnitt":
                img = rahmen(zuschneiden(bild(dok[erste], 1.6)))
            else:
                breite = 500 // len(art) - 16
                teile = []
                for n in art:
                    s = bild(dok[erste + n], 1.2)
                    teile.append(s.resize((breite, int(s.height * breite / s.width)), Image.LANCZOS))
                img = nebeneinander(teile, texte)
            p = speichern(img, name)
            print(f"{os.path.relpath(p, HIER)}  {img.width}×{img.height}  {os.path.getsize(p) // 1024} KB")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
