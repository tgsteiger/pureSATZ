"""
fassungen.py – Leseprobe und Korrekturfassung aus dem fertigen Bildschirm-PDF (wird von bauen.py benutzt).

Leseprobe:  Umschlag, Titelei bis zum Inhaltsverzeichnis, dann Seiten oder Kapitel, «Ende der Leseprobe», Rückseite.
            Variablen:  leseprobe-seiten: 14,16,17-20,22   (gedruckte Seitenzahlen; -uz = eigene für die zweite Ausgabe)
                        leseprobe: 3              (Anzahl Kapitel)  oder  leseprobe: Der Unfall  (bis und mit Kapitel)
                        beides leer: die 4 Seiten nach dem Inhaltsverzeichnis
                        leseprobe-text: …         (Text der Schlussseite, Variablen erlaubt; sonst Titel, ISBN, Website)
Korrektur:  jede Seite in Originalgrösse auf A4, links Zeilennummern (pro Seite), rechts Platz für Notizen.
"""
import io
import os
from datetime import datetime

from pypdf import PdfReader, PdfWriter, PageObject, Transformation
from pypdf.generic import NameObject, ArrayObject
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas


# --- Leseprobe -----------------------------------------------------------------------
def _eintraege(reader):
    """Inhalts-Einträge des PDFs: [(titel, seite, hat_unterkapitel)] in Lesereihenfolge (Seiten ab 1)."""
    liste = []

    def walk(o):
        for i, x in enumerate(o):
            if isinstance(x, list):
                walk(x)
                continue
            kinder = i + 1 < len(o) and isinstance(o[i + 1], list)
            liste.append((x.title, reader.get_destination_page_number(x) + 1, kinder))
    walk(reader.outline)
    return liste


def leseprobe_ende(reader, bis):
    """Letzte Seite der Leseprobe. bis = Anzahl Kapitel (Zahl) oder Titel des letzten Kapitels."""
    eintraege = _eintraege(reader)
    kapitel = [i for i, (_, _, kinder) in enumerate(eintraege) if not kinder]     # Teil-Seiten zählen nicht
    if not kapitel:
        return min(len(reader.pages), 12)
    bis = (bis or "3").strip()
    if bis.isdigit():
        letztes = kapitel[min(int(bis), len(kapitel)) - 1]
    else:
        treffer = [i for i in kapitel if bis.lower() in eintraege[i][0].lower()]
        if not treffer:
            raise SystemExit(f"Leseprobe: kein Kapitel mit «{bis}» gefunden (Variable «leseprobe»).")
        letztes = treffer[0]
    if letztes + 1 < len(eintraege):
        return max(eintraege[letztes][1], eintraege[letztes + 1][1] - 1)
    return len(reader.pages) - 1


def erste_inhaltsseite(reader):
    """Erste Seite nach Titelei und Inhaltsverzeichnis (= erster Eintrag im Inhalt), Seiten ab 1."""
    e = _eintraege(reader)
    return e[0][1] if e else min(len(reader.pages), 5)


def seiten_lesen(text):
    """«14,16,17-20,22» -> [14, 16, 17, 18, 19, 20, 22]. Falsche Angabe = Abbruch mit Meldung."""
    out = []
    for teil in (text or "").replace("–", "-").replace("—", "-").replace(" ", "").split(","):
        if not teil:
            continue
        m = __import__("re").fullmatch(r"(\d+)(?:-(\d+))?", teil)
        if not m:
            raise SystemExit(f"Leseprobe: «{teil}» verstehe ich nicht. Beispiel: leseprobe-seiten: 14,16,17-20,22")
        von, bis = int(m.group(1)), int(m.group(2) or m.group(1))
        if bis < von:
            raise SystemExit(f"Leseprobe: «{teil}» – die zweite Zahl muss grösser sein.")
        out += [n for n in range(von, bis + 1) if n not in out]
    return out


def seiten_text(seiten):
    """[14, 16, 17, 18, 19, 20, 22] -> «14, 16, 17–20, 22»."""
    teile, i = [], 0
    while i < len(seiten):
        j = i
        while j + 1 < len(seiten) and seiten[j + 1] == seiten[j] + 1:
            j += 1
        teile.append(str(seiten[i]) if i == j else f"{seiten[i]}–{seiten[j]}")
        i = j + 1
    return ", ".join(teile)


def kapitel_der_seiten(quelle, seiten):
    """Titel der Kapitel, in denen die Seiten liegen (für die E-Book-Leseprobe)."""
    r = PdfReader(io.BytesIO(open(quelle, "rb").read()))
    kap = [(t, s) for t, s, kinder in _eintraege(r) if not kinder]
    out = []
    for n in seiten:
        davor = [t for t, s in kap if s <= n]
        if davor and davor[-1] not in out:
            out.append(davor[-1])
    return out


def _ohne_interne_links(seite):
    """Interne Sprünge (Inhaltsverzeichnis) entfernen – ihre Ziele fehlen in der Leseprobe. Web-Links bleiben."""
    if "/Annots" not in seite:
        return
    bleiben = ArrayObject()
    for a in seite["/Annots"]:
        o = a.get_object()
        if o.get("/Subtype") == "/Link" and "/A" in o and o["/A"].get("/S") == "/URI":
            bleiben.append(a)
    seite[NameObject("/Annots")] = bleiben


def leseprobe_angaben(bk, fassung):
    """(Zeilen der Schlussseite, Link für den QR-Code) aus den Variablen «leseprobe-text» und «shop-link»."""
    import manuskript as M
    var = M.Ausgabe(bk.alle_variablen(), fassung, "druck")          # «druck»: {isbn} = ISBN des Buchs
    text = var("leseprobe-text") or "Das ganze Buch «{titel}» von {autor}<br/>ISBN {isbn}<br/>{website}"
    zeilen = [z for z in (var.ersetze(t) for t in text.replace("<br/>", "\n").split("\n")) if z]
    link = (var("shop-link") or var("website")).strip()
    if link and not link.startswith(("http://", "https://")):
        link = "https://" + link
    if link:                              # steht unter dem QR-Code bzw. als Link: nicht doppelt
        kurz = link.split("://", 1)[-1].rstrip("/")
        zeilen = [z for z in zeilen if z.strip().rstrip("/") not in (kurz, link)]
    return zeilen, link


def schlussseite(breite, hoehe, titel, zeilen, schrift_titel, schrift_text, farbe_titel, farbe_text, link=""):
    """Eine Seite «Ende der Leseprobe» als PDF-Seite, mit QR-Code zum Shop (link)."""
    puffer = io.BytesIO()
    c = canvas.Canvas(puffer, pagesize=(breite, hoehe))
    y = hoehe * (0.66 if link else 0.58)
    c.setFillColor(farbe_titel); c.setFont(schrift_titel, 17)
    c.drawCentredString(breite / 2, y, titel)
    y -= 14 * mm
    c.setFillColor(farbe_text); c.setFont(schrift_text, 10.5)
    for z in zeilen:
        c.drawCentredString(breite / 2, y, z); y -= 6 * mm
    if link:
        from reportlab.graphics.barcode.qr import QrCodeWidget
        from reportlab.graphics.shapes import Drawing
        from reportlab.graphics import renderPDF
        q = QrCodeWidget(link)
        x1, y1, x2, y2 = q.getBounds()
        gr = 30 * mm
        d = Drawing(gr, gr, transform=[gr / (x2 - x1), 0, 0, gr / (y2 - y1), 0, 0])
        d.add(q)
        y -= gr + 4 * mm
        renderPDF.draw(d, c, breite / 2 - gr / 2, y)
        c.linkURL(link, (breite / 2 - gr / 2, y, breite / 2 + gr / 2, y + gr), relative=0)
        c.setFont(schrift_text, 8.5)
        c.drawCentredString(breite / 2, y - 5 * mm, link.split("://", 1)[-1])
    c.showPage(); c.save()
    return PdfReader(io.BytesIO(puffer.getvalue())).pages[0]


def leseprobe(quelle, ziel, bis, schluss, mit_rueckseite=True, seiten=None):
    """quelle: Bildschirm-PDF; schluss: fertige Schlussseite (PageObject).
    seiten: Liste gedruckter Seitenzahlen (sonst bis = Kapitel). Gibt (seiten im PDF, Beschreibung)."""
    r = PdfReader(io.BytesIO(open(quelle, "rb").read()))   # Datei nicht offen halten (Windows)
    w = PdfWriter()
    if seiten is not None:
        start = erste_inhaltsseite(r)
        letzte = len(r.pages) - (1 if mit_rueckseite else 0)
        falsch = [n for n in seiten if n < 1 or n > letzte]
        if falsch:
            raise SystemExit(f"Leseprobe: Seite {', '.join(map(str, falsch))} gibt es nicht (Buch: 1–{letzte}).")
        auswahl = list(range(1, start)) + [n for n in seiten if n >= start]
        for n in auswahl:
            w.add_page(r.pages[n - 1])
            _ohne_interne_links(w.pages[-1])
        ende = max(auswahl)
        beschreibung = "Seiten " + seiten_text([n for n in seiten if n >= start])
        vorne = [n for n in seiten if n < start]
        if vorne:
            beschreibung += f"; Seite {seiten_text(vorne)} gehört zur Titelei und ist ohnehin dabei"
    else:
        ende = leseprobe_ende(r, bis)
        for i in range(ende):
            w.add_page(r.pages[i])
            _ohne_interne_links(w.pages[-1])
        beschreibung = f"Buch bis Seite {ende}"
    w.add_page(schluss)
    if mit_rueckseite and ende < len(r.pages) - 1:
        w.add_page(r.pages[-1])
    meta = dict(r.metadata or {})
    meta["/Title"] = str(meta.get("/Title", "")) + " – Leseprobe"
    w.add_metadata(meta)
    with open(ziel, "wb") as f:
        w.write(f)
    return len(w.pages), beschreibung


# --- Korrekturfassung ------------------------------------------------------------------
def _zeilen_aller_seiten(quelle):
    import pdfwerkzeug
    return pdfwerkzeug.zeilen_aller_seiten(quelle)


def korrektur(quelle, ziel, titel, schrift="Helvetica", markiert=None):
    """Korrekturfassung: Seite in Originalgrösse auf A4 hoch, Zeilennummern links, Notizrand rechts.
    markiert: {seite: [zeile, …]} – diese Zeilen mit rotem ▶ und roter Nummer (Gegenlesen)."""
    r = PdfReader(io.BytesIO(open(quelle, "rb").read()))   # Datei nicht offen halten (Windows)
    w = PdfWriter()
    aw, ah = A4
    datum = f"{datetime.now():%d.%m.%Y %H:%M}"
    alle_zeilen = _zeilen_aller_seiten(quelle)
    for nr, seite in enumerate(r.pages, 1):
        box = seite.cropbox
        sw, sh = float(box.width), float(box.height)
        massstab = min(1.0, (aw - 70 * mm) / sw, (ah - 24 * mm) / sh)
        x0, y0 = 18 * mm, (ah - sh * massstab) / 2
        zeilen = alle_zeilen[nr - 1] if nr <= len(alle_zeilen) else []
        blatt = PageObject.create_blank_page(width=aw, height=ah)
        blatt.merge_transformed_page(seite, Transformation().translate(-float(box.left), -float(box.bottom))
                                     .scale(massstab, massstab).translate(x0, y0))
        puffer = io.BytesIO()
        c = canvas.Canvas(puffer, pagesize=A4)
        c.setStrokeColorRGB(0.6, 0.6, 0.6); c.setLineWidth(0.4)
        c.rect(x0, y0, sw * massstab, sh * massstab)                 # Seitenrand des Buchs
        c.setFont(schrift, 6.5); c.setFillColorRGB(0.45, 0.45, 0.45)
        for i, y in enumerate(zeilen, 1):
            rot = i in (markiert or {}).get(nr, ())
            c.setFillColorRGB(*((0.8, 0.1, 0.1) if rot else (0.45, 0.45, 0.45)))
            c.drawRightString(x0 - 2.5 * mm, y0 + y * massstab + 1, str(i))
            if rot:                                     # Dreieck ▶ vor der Nummer
                ym = y0 + y * massstab + 3; p = c.beginPath()
                p.moveTo(x0 - 9 * mm, ym + 1.8); p.lineTo(x0 - 9 * mm, ym - 1.8); p.lineTo(x0 - 6.5 * mm, ym); p.close()
                c.drawPath(p, stroke=0, fill=1)
        c.setFillColorRGB(0.45, 0.45, 0.45)
        rechts = x0 + sw * massstab + 6 * mm                          # Notizrand mit feinen Linien
        c.setStrokeColorRGB(0.85, 0.85, 0.85)
        y = ah - 20 * mm
        while y > 15 * mm:
            c.line(rechts, y, aw - 10 * mm, y); y -= 7 * mm
        c.setFont(schrift, 7.5); c.setFillColorRGB(0.35, 0.35, 0.35)
        c.drawString(x0, ah - 10 * mm, f"KORREKTUR · {titel} · {datum}")
        c.drawRightString(aw - 10 * mm, ah - 10 * mm, f"Seite {nr} / {len(r.pages)}")
        c.showPage(); c.save()
        blatt.merge_page(PdfReader(io.BytesIO(puffer.getvalue())).pages[0])
        w.add_page(blatt)
    with open(ziel, "wb") as f:
        w.write(f)
    return len(r.pages)
