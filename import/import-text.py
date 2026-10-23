#!/usr/bin/env python3
"""
import-text.py – macht aus einem LibreOffice- oder Word-Dokument ein neues Buch (wie setup.sh, aber mit echtem Text).

TESTPHASE: funktioniert für einfache Dokumente (Formatvorlagen, Text, fett, Listen, Links, Bilder), ist aber
noch nicht voll ausgereift. Das Ergebnis immer im PDF kontrollieren; IMPORT-BERICHT.txt nennt, was fehlt.

    sh import/import-text.sh manuskript.odt          (Windows: import\\import-text.bat manuskript.odt)
    sh import/import-text.sh manuskript.docx --autor "Vorname Nachname" --name Mein-Buch --ziel ../Mein-Buch

Regeln für das Dokument (LibreOffice Writer oder Word):
  Formatvorlagen  Titel, Untertitel, Überschrift 1–3, Standard/Textkörper, Zitat, Beschriftung.
  Fett, Aufzählungen, Links, Bilder (mit Beschriftung oder Alternativtext), manueller Seitenumbruch.
  Speichern als .odt oder .docx (alte .doc: wird mit LibreOffice umgewandelt, falls installiert).

Ergebnis: Buchordner neben pureSATZ (wie setup.sh) mit dem Text in <name>-buch.md, Bildern in fotos/
und IMPORT-BERICHT.txt (was übernommen wurde, was nicht). Motor und Vorlage werden nicht verändert.
Läuft nur mit Python (keine zusätzlichen Pakete) auf Linux, Mac und Windows.
"""
import os
import re
import shutil
import statistics
import subprocess
import sys
import tempfile
import zipfile
from datetime import date
from xml.etree import ElementTree as ET
try:                                            # Windows: «sh build.sh» in Meldungen als «.\build.bat»
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "motor"))
    import plattform
    plattform.windows_befehle()
except ImportError:
    pass

HIER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))     # Ordner pureSATZ (import-text.py liegt in import/)
sys.path.insert(0, os.path.join(HIER, "setup"))
import setup as S          # noqa: E402  (pureSATZ: legt den Buchordner an)

NS = {
    "office": "urn:oasis:names:tc:opendocument:xmlns:office:1.0",
    "text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0",
    "style": "urn:oasis:names:tc:opendocument:xmlns:style:1.0",
    "fo": "urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0",
    "draw": "urn:oasis:names:tc:opendocument:xmlns:drawing:1.0",
    "xlink": "http://www.w3.org/1999/xlink",
    "svg": "urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0",
    "meta": "urn:oasis:names:tc:opendocument:xmlns:meta:1.0",
    "dc": "http://purl.org/dc/elements/1.1/",
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
    "pr": "http://schemas.openxmlformats.org/package/2006/relationships",
    "cp": "http://schemas.openxmlformats.org/package/2006/metadata/core-properties",
}


def q(tag):
    p, n = tag.split(":")
    return "{%s}%s" % (NS[p], n)


# Ein Block = (art, inhalt):  ("titel", t) ("untertitel", t) ("h", (stufe, t)) ("p", t) ("zitat", t)
# ("liste", t) ("bild", dict) ("beschriftung", t) ("umbruch", None) ("leer", None)
class Bericht(list):
    def __call__(self, text):
        self.append(text)


BERICHT = Bericht()


def sauber(t):
    t = re.sub(r"[ \t]+", " ", t).strip()
    # aufgeteilte Links (z. B. «Herzmauer.» + «ch» mit gleicher Adresse) wieder zu einem Link verbinden
    alt = None
    while alt != t:
        alt, t = t, re.sub(r"\[([^\]]*)\]\(([^)\s]+)\)\[([^\]]*)\]\(\2\)", r"[\1\3](\2)", t)
    return t


# --------------------------------------------------------------------------- LibreOffice (.odt)
def lies_odt(pfad):
    z = zipfile.ZipFile(pfad)
    inhalt = ET.fromstring(z.read("content.xml"))
    stile = ET.fromstring(z.read("styles.xml")) if "styles.xml" in z.namelist() else None
    info = {}
    if "meta.xml" in z.namelist():
        m = ET.fromstring(z.read("meta.xml"))
        for k, tag in (("titel", "dc:title"), ("autor", "meta:initial-creator"), ("autor2", "dc:creator")):
            e = m.find(".//" + q(tag))
            if e is not None and (e.text or "").strip():
                info[k] = e.text.strip()

    # Stile: Name -> (Elternstil, fett, kursiv, Seitenumbruch davor)
    stil = {}
    for wurzel in (stile, inhalt):
        if wurzel is None:
            continue
        for s in wurzel.iter(q("style:style")):
            name = s.get(q("style:name"))
            tp = s.find(q("style:text-properties"))
            pp = s.find(q("style:paragraph-properties"))
            stil[name] = dict(
                eltern=s.get(q("style:parent-style-name")),
                fett=tp is not None and tp.get(q("fo:font-weight")) in ("bold", "600", "700", "800", "900"),
                kursiv=tp is not None and tp.get(q("fo:font-style")) == "italic",
                umbruch=pp is not None and pp.get(q("fo:break-before")) == "page")

    auto = inhalt.find(q("office:automatic-styles"))
    automatisch = {s.get(q("style:name")) for s in (auto if auto is not None else [])}

    def grundstil(name):
        """Benannter Stil hinter einem automatischen Stil (P1 -> Title)."""
        if name in automatisch and stil.get(name, {}).get("eltern"):
            name = stil[name]["eltern"]
        return (name or "").replace("_20_", " ")

    def eigenschaft(name, k):
        seen = 0
        while name and seen < 10:
            if stil.get(name, {}).get(k):
                return True
            name = stil.get(name, {}).get("eltern"); seen += 1
        return False

    bilder = {}

    def text_von(el, fett=False):
        """Text eines Absatzes mit **fett**, Links und <br/>; Bilder werden gesammelt."""
        teile = [el.text or ""] if el.text else []
        for k in el:
            tag = k.tag
            if tag == q("text:span"):
                sn = k.get(q("text:style-name"))
                f = eigenschaft(sn, "fett") and not fett
                inner = text_von(k, fett or f)
                teile.append(f"**{inner.strip()}** " if f and inner.strip() else inner)
            elif tag == q("text:s"):
                teile.append(" " * int(k.get(q("text:c"), "1")))
            elif tag == q("text:tab"):
                teile.append(" ")
            elif tag == q("text:line-break"):
                teile.append("<br/>")
            elif tag == q("text:a"):
                href = k.get(q("xlink:href"), "")
                t = text_von(k, fett)
                teile.append(f"[{t}]({href})" if href.startswith("http") else t)
            elif tag == q("draw:frame"):
                bilder.setdefault("neu", []).append(k)
            elif tag in (q("text:soft-page-break"), q("text:bookmark"), q("text:bookmark-start"),
                         q("text:bookmark-end"), q("office:annotation")):
                if tag == q("office:annotation"):
                    BERICHT("Kommentar weggelassen.")
            elif tag == q("text:note"):
                BERICHT("Fussnote weggelassen (der Motor kennt noch keine Fussnoten): «"
                        + sauber("".join(k.itertext()))[:60] + "…»")
            else:
                teile.append(text_von(k, fett))
            if k.tail:
                teile.append(k.tail)
        return "".join(teile)

    def bild(frame):
        img = frame.find(q("draw:image"))
        titel = frame.find(q("svg:title")); desc = frame.find(q("svg:desc"))
        href = img.get(q("xlink:href")) if img is not None else None
        d = dict(name=frame.get(q("draw:name")) or "bild",
                 alt=sauber((titel.text if titel is not None else "") or (desc.text if desc is not None else "") or ""),
                 daten=None, endung=".jpg")
        if href and href in z.namelist():
            d["daten"] = z.read(href); d["endung"] = os.path.splitext(href)[1].lower() or ".png"
        return d

    blocks = []

    def absatz(el, liste=False):
        sn = el.get(q("text:style-name")) or ""
        art = grundstil(sn).lower()
        if eigenschaft(sn, "umbruch"):
            blocks.append(("umbruch", None))
        bilder.clear()
        t = sauber(text_von(el))
        for fr in bilder.get("neu", []):
            blocks.append(("bild", bild(fr)))
        if el.tag == q("text:h"):
            blocks.append(("h", (int(el.get(q("text:outline-level"), "1")), t))); return
        if not t:
            blocks.append(("leer", None)); return
        if liste:
            blocks.append(("liste", t))
        elif art == "title":
            blocks.append(("titel", t))
        elif art == "subtitle":
            blocks.append(("untertitel", t))
        elif art.startswith("heading ") and art[8:].isdigit():
            blocks.append(("h", (int(art[8:]), t)))
        elif art in ("quotations", "zitat", "quote"):
            blocks.append(("zitat", t))
        elif art in ("caption", "illustration", "figure", "drawing", "abbildung", "beschriftung") or \
                el.find(".//" + q("text:sequence")) is not None:
            blocks.append(("beschriftung", t))
        else:
            blocks.append(("p", t))

    def gehe(el):
        for k in el:
            if k.tag in (q("text:p"), q("text:h")):
                absatz(k)
            elif k.tag == q("text:list"):
                for li in k.iter(q("text:list-item")):
                    for p in li.findall(q("text:p")):
                        absatz(p, liste=True)
            elif k.tag.endswith("}table"):
                BERICHT("Tabelle übernommen als einfacher Text (Zeile für Zeile).")
                for p in k.iter(q("text:p")):
                    absatz(p)
            elif k.tag.endswith("}section"):
                gehe(k)
    body = inhalt.find(".//" + q("office:text"))
    gehe(body)
    return blocks, info


# --------------------------------------------------------------------------- Word (.docx)
def lies_docx(pfad):
    z = zipfile.ZipFile(pfad)
    doc = ET.fromstring(z.read("word/document.xml"))
    rels = {}
    if "word/_rels/document.xml.rels" in z.namelist():
        for r in ET.fromstring(z.read("word/_rels/document.xml.rels")):
            rels[r.get("Id")] = (r.get("Target"), r.get("TargetMode"))
    namen = {}
    if "word/styles.xml" in z.namelist():
        for s in ET.fromstring(z.read("word/styles.xml")).iter(q("w:style")):
            n = s.find(q("w:name"))
            namen[s.get(q("w:styleId"))] = (n.get(q("w:val")) if n is not None else "").lower()
    info = {}
    if "docProps/core.xml" in z.namelist():
        c = ET.fromstring(z.read("docProps/core.xml"))
        for k, tag in (("titel", "dc:title"), ("autor", "dc:creator")):
            e = c.find(q(tag))
            if e is not None and (e.text or "").strip():
                info[k] = e.text.strip()

    def an(el):        # w:b / w:i an?
        return el is not None and el.get(q("w:val"), "true") not in ("0", "false", "none")

    blocks = []
    for p in doc.find(q("w:body")):
        if p.tag == q("w:tbl"):
            BERICHT("Tabelle übernommen als einfacher Text (Zeile für Zeile).")
            ps = list(p.iter(q("w:p")))
        elif p.tag == q("w:p"):
            ps = [p]
        else:
            continue
        for p in ps:
            ppr = p.find(q("w:pPr"))
            sid = ppr.find(q("w:pStyle")).get(q("w:val")) if ppr is not None and ppr.find(q("w:pStyle")) is not None else ""
            art = namen.get(sid, sid.lower())
            liste = (ppr is not None and ppr.find(q("w:numPr")) is not None) or \
                art.startswith(("list bullet", "list number", "aufzählungszeichen", "listennummer"))
            if ppr is not None and an(ppr.find(q("w:pageBreakBefore"))):
                blocks.append(("umbruch", None))
            teile, bilder = [], []

            def lauf(r, link=None):
                rpr = r.find(q("w:rPr"))
                fett = rpr is not None and an(rpr.find(q("w:b")))
                t = ""
                for k in r:
                    if k.tag == q("w:t"):
                        t += k.text or ""
                    elif k.tag == q("w:tab"):
                        t += " "
                    elif k.tag == q("w:br"):
                        if k.get(q("w:type")) == "page":
                            bilder.append("UMBRUCH")
                        else:
                            t += "<br/>"
                    elif k.tag == q("w:footnoteReference"):
                        BERICHT("Fussnote weggelassen (der Motor kennt noch keine Fussnoten).")
                    elif k.tag == q("w:drawing"):
                        blip = k.find(".//" + q("a:blip"))
                        pr = k.find(".//" + q("wp:docPr"))
                        d = dict(name=(pr.get("name") if pr is not None else "bild"),
                                 alt=sauber((pr.get("descr") or pr.get("title") or "") if pr is not None else ""),
                                 daten=None, endung=".jpg")
                        rid = blip.get(q("r:embed")) if blip is not None else None
                        if rid and rid in rels:
                            ziel = "word/" + rels[rid][0].lstrip("/").replace("word/", "")
                            if ziel in z.namelist():
                                d["daten"] = z.read(ziel); d["endung"] = os.path.splitext(ziel)[1].lower()
                        bilder.append(d)
                if fett and t.strip():
                    t = f"**{t.strip()}** "
                teile.append(t)

            for k in p:
                if k.tag == q("w:r"):
                    lauf(k)
                elif k.tag == q("w:hyperlink"):
                    vorher = len(teile)
                    for r in k.iter(q("w:r")):
                        lauf(r)
                    txt = "".join(teile[vorher:]); del teile[vorher:]
                    ziel = rels.get(k.get(q("r:id")), ("", ""))[0]
                    teile.append(f"[{txt.strip()}]({ziel})" if ziel.startswith("http") else txt)
                elif k.tag in (q("w:ins"), q("w:smartTag"), q("w:sdt")):
                    for r in k.iter(q("w:r")):
                        lauf(r)
            for b in bilder:
                blocks.append(("umbruch", None) if b == "UMBRUCH" else ("bild", b))
            t = sauber("".join(teile))
            if not t:
                blocks.append(("leer", None)); continue
            m = re.match(r"(heading|überschrift)\s*(\d)", art)
            if m:
                blocks.append(("h", (int(m.group(2)), t)))
            elif art in ("title", "titel"):
                blocks.append(("titel", t))
            elif art in ("subtitle", "untertitel"):
                blocks.append(("untertitel", t))
            elif art in ("quote", "intense quote", "zitat", "intensives zitat", "quotations"):
                blocks.append(("zitat", t))
            elif art in ("caption", "beschriftung"):
                blocks.append(("beschriftung", t))
            elif liste:
                blocks.append(("liste", t))
            else:
                blocks.append(("p", t))
    if z.namelist() and any(n.startswith("word/comments") for n in z.namelist()):
        BERICHT("Kommentare weggelassen.")
    return blocks, info


# --------------------------------------------------------------------------- Umwandeln in Buch-MD
ENDE = (".", "!", "?", ":", "»", "«", '"', "“", "”", ")", "…")


def zeilen_zusammenfuegen(blocks):
    """Text, der Zeile für Zeile als eigene Absätze kam (z. B. aus PDF kopiert), zu Absätzen verbinden."""
    ps = [t for a, t in blocks if a == "p"]
    if len(ps) < 6:
        return blocks
    offen = sum(1 for t in ps if not t.rstrip("*").endswith(ENDE))
    if offen / len(ps) < 0.3:
        return blocks
    median = statistics.median(len(t) for t in ps)
    neu = []
    for a, t in blocks:
        if a == "p" and neu and neu[-1][0] == "p":
            vorher = neu[-1][1]
            letzte = vorher.split("\n")[-1]
            absatzende = letzte.rstrip("*").endswith(ENDE) and len(letzte) < 0.8 * median
            kurz_allein = not t.rstrip("*").endswith(ENDE) and len(t) < 0.75 * median and letzte.endswith(ENDE)
            if not absatzende and not kurz_allein:
                neu[-1] = ("p", vorher + "\n" + t); continue
        neu.append((a, t))
    BERICHT(f"Der Text kam Zeile für Zeile (wie aus einem PDF kopiert): Zeilen zu Absätzen verbunden – "
            f"bitte die Absätze im PDF kontrollieren ({len(ps)} Zeilen → "
            f"{sum(1 for a, _ in neu if a == 'p')} Absätze).")
    return [(a, t.replace("\n", " ") if a == "p" else t) for a, t in neu]


def geschuetzt(t):
    """Text darf nicht wie ein Befehl der Buch-MD aussehen und keine {Variablen} enthalten."""
    if "{" in t or "}" in t:
        BERICHT(f"Geschweifte Klammern ersetzt durch runde: «{t[:50]}…»")
        t = t.replace("{", "(").replace("}", ")")
    if re.match(r"^(#|>|~|@|:::|- |\d+\. )", t):
        t = "​" + t          # unsichtbares Zeichen davor: bleibt normaler Text
    return t


def slug_datei(n):
    n = re.sub(r"[^A-Za-z0-9äöüÄÖÜ_-]+", "-", n).strip("-")
    return n or "bild"


def buch_md(blocks, fotos_ordner):
    blocks = zeilen_zusammenfuegen(blocks)
    h = [t for a, t in blocks if a == "h"]
    h1 = sum(1 for s, _ in h if s == 1)
    teile = h1 >= 2 and any(s == 2 for s, _ in h)
    if teile:
        BERICHT(f"Aufbau: {h1}× Überschrift 1 mit Überschrift 2 darunter → Teile (eigene Teil-Seite) mit Kapiteln.")
    elif h:
        BERICHT("Aufbau: Überschrift 1 → Kapitel, Überschrift 2 → Zwischentitel, Überschrift 3 → fetter Titel.")
    zeilen, teilnr, bildnr, hat_kapitel = [], 0, 0, False
    namen = set()
    i = 0
    while i < len(blocks):
        art, inhalt = blocks[i]
        if art in ("titel", "untertitel"):
            pass
        elif art == "h":
            stufe, t = inhalt
            t = t.replace("|", "/").replace("**", "")
            if teile and stufe == 1:
                teilnr += 1; zeilen += [f"# Teil {teilnr}|{t}|", ""]; hat_kapitel = True
            elif (teile and stufe == 2) or (not teile and stufe == 1):
                zeilen += [f"## {t}", ""]; hat_kapitel = True
            elif (teile and stufe == 3) or (not teile and stufe == 2):
                zeilen += [f"### {t}", ""]
            else:
                zeilen += [f"**{t}**", ""]
        elif art in ("p", "beschriftung"):
            if not hat_kapitel:
                zeilen += ["## Einleitung", ""]; hat_kapitel = True
                BERICHT("Text vor der ersten Überschrift → Kapitel «Einleitung» (Titel im Buch-MD anpassen).")
            zeilen += [geschuetzt(inhalt), ""]
        elif art == "zitat":
            zeilen += ["> " + inhalt.replace("**", ""), ""]
        elif art == "liste":
            zeilen.append("- " + inhalt)
            if i + 1 >= len(blocks) or blocks[i + 1][0] != "liste":
                zeilen.append("")
        elif art == "umbruch":
            zeilen += ["@UMBRUCH", ""]
        elif art == "bild":
            bildnr += 1
            d = inhalt
            name = slug_datei(os.path.splitext(d["name"])[0])
            while name in namen:
                name += "-2"
            namen.add(name)
            datei = name + (d["endung"] if d["daten"] else ".jpg")
            # Beschriftung direkt danach (Formatvorlage Beschriftung/Caption)?
            text = ""
            j = i + 1
            while j < len(blocks) and blocks[j][0] == "leer":
                j += 1
            if j < len(blocks) and blocks[j][0] == "beschriftung":
                text = blocks[j][1].replace("**", ""); blocks[j] = ("leer", None)
            zeilen.append(f"#### @FOTO {name}")
            if d["daten"]:
                with open(os.path.join(fotos_ordner, datei), "wb") as f:
                    f.write(d["daten"])
            else:
                zeilen.append(f"Bild «{d['name']}» war im Dokument ohne Bilddaten (verknüpft?). "
                              f"Bitte als fotos/{datei} ablegen.")
                BERICHT(f"Bild «{d['name']}»: keine Bilddaten im Dokument – Platzhalter gesetzt (fotos/{datei}).")
            zeilen.append(f"datei: {datei}")
            if text:
                zeilen.append(f"text: {text}")
            if d["alt"]:
                zeilen.append(f"alt: {d['alt']}")
            if not text and not d["alt"]:
                BERICHT(f"Bild «{d['name']}»: ohne Beschriftung und ohne Alternativtext (fürs E-Book «alt:» ergänzen).")
            zeilen += [""]                    # Foto-Block endet an der Leerzeile
        i += 1
    return zeilen, bildnr


def titelei(vorlage_md):
    """Titelei aus der Vorlage (bis @INHALTSVERZEICHNIS), ohne Demo-Widmung, Demo-Hinweis und Demo-Kernsatz."""
    aus, weg = [], False
    for z in vorlage_md.split("\n"):
        if z.startswith("## Vorwort"):
            break
        if re.match(r"#{2,3} @(WIDMUNG|HINWEIS)\b", z):
            weg = True; continue
        if z.startswith("## @KERNSATZ"):
            continue
        if weg and z.startswith("#"):
            weg = False
        if not weg:
            aus.append(z)
    return "\n".join(aus).rstrip() + "\n\n"


# --------------------------------------------------------------------------- Ablauf
def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__); sys.exit(0)
    opt = {}
    for k in ("--autor", "--name", "--ziel", "--format", "--bindung"):
        if k in a:
            i = a.index(k); opt[k[2:]] = a[i + 1]; del a[i:i + 2]
    venv = "--ohne-venv" not in a
    a = [x for x in a if not x.startswith("--")]
    quelle = os.path.abspath(a[0])
    if not os.path.exists(quelle):
        sys.exit(f"Datei nicht gefunden: {quelle}")
    endung = os.path.splitext(quelle)[1].lower()
    tmp = None
    if endung in (".doc", ".rtf"):
        soffice = shutil.which("soffice") or shutil.which("libreoffice")
        if not soffice:
            sys.exit("Alte .doc/.rtf-Datei: bitte in LibreOffice oder Word öffnen und als .odt oder .docx speichern.")
        tmp = tempfile.mkdtemp()
        subprocess.run([soffice, "--headless", "--convert-to", "odt", "--outdir", tmp, quelle], check=True,
                       capture_output=True)
        quelle = os.path.join(tmp, os.path.splitext(os.path.basename(quelle))[0] + ".odt"); endung = ".odt"
        BERICHT("Alte Word-Datei mit LibreOffice in .odt umgewandelt.")
    if endung == ".odt":
        blocks, info = lies_odt(quelle)
    elif endung == ".docx":
        blocks, info = lies_docx(quelle)
    else:
        sys.exit("Bitte eine .odt- (LibreOffice) oder .docx-Datei (Word) angeben.")

    titel = next((t for k, t in blocks if k == "titel"), "") or info.get("titel", "")
    untertitel = next((t for k, t in blocks if k == "untertitel"), "")
    autor = opt.get("autor") or info.get("autor") or info.get("autor2", "")
    if not titel:
        titel = next((t for k, t in blocks if k == "h"), (0, os.path.splitext(os.path.basename(quelle))[0]))[1]
        BERICHT(f"Kein Titel (Formatvorlage «Titel») gefunden – genommen: «{titel}».")
    if not autor:
        autor = S.frage("Autor", "Vorname Nachname") if sys.stdin.isatty() else "Vorname Nachname"
        if autor == "Vorname Nachname":
            BERICHT("Kein Autor im Dokument – «Vorname Nachname» eingesetzt (Variablen-Datei: autor).")
    name = S.slug(opt.get("name") or titel)
    werte = dict(TITEL=titel.replace("**", ""), UNTERTITEL=untertitel.replace("**", ""), AUTOR=autor, NAME=name,
                 FORMAT=opt.get("format", "a5"), BINDUNG=opt.get("bindung", "hardcover"),
                 ZWEITE_AUSGABE="nein", ORT="", JAHR=str(date.today().year), WEBSITE="", ADRESSE="")
    ordner = os.path.abspath(opt.get("ziel") or os.path.join(HIER, "..", name))
    if os.path.exists(os.path.join(ordner, f"{name}-buch.md")):
        sys.exit(f"Es gibt schon ein Buch in {ordner} – nichts überschrieben. Anderer Name: --name Neuer-Name")

    print(f"Import (Testphase): {os.path.basename(a[0])} → {ordner}")
    name = S.buch(ordner, werte)
    zeilen, bilder = buch_md(blocks, os.path.join(ordner, "fotos"))
    vorlage = S.fuelle(open(os.path.join(S.VORLAGE, "buch.md"), encoding="utf-8").read(), S.platzhalter(werte))
    text = titelei(vorlage) + "\n".join(zeilen).rstrip() + "\n\n@RUECKSEITE\n"
    with open(os.path.join(ordner, f"{name}-buch.md"), "w", encoding="utf-8") as f:
        f.write(text)
    # Stichwortverzeichnis aus: die Demo-Stichworte passen nicht zum neuen Text
    with open(os.path.join(ordner, f"stichworte-{name}.txt"), "w", encoding="utf-8") as f:
        f.write("# Stichwortverzeichnis: ein Stichwort pro Zeile, Varianten mit |  (danach @STICHWORTE ins Buch)\n")
    for demo in ("beispiel.jpg",):
        p = os.path.join(ordner, "fotos", demo)
        if os.path.exists(p) and demo not in text:
            os.remove(p)
    S.motor(ordner, venv)

    kap = sum(1 for z in zeilen if z.startswith("## "))
    teile = sum(1 for z in zeilen if z.startswith("# Teil"))
    woerter = len(re.findall(r"\w+", " ".join(z for z in zeilen if not z.startswith(("::: ", "datei:", "alt:")))))
    kopf = [f"IMPORT-BERICHT – {os.path.basename(a[0])} → {name}  ({date.today():%d.%m.%Y})",
            "(Import in der Testphase – bitte das Ergebnis im PDF kontrollieren)", "",
            f"Titel: {werte['TITEL']}", f"Untertitel: {werte['UNTERTITEL'] or '–'}", f"Autor: {autor}",
            f"Teile: {teile} · Kapitel: {kap} · Bilder: {bilder} · Wörter: {woerter}", "", "Hinweise:"]
    hinweise = list(dict.fromkeys(BERICHT)) or ["keine – alles übernommen."]
    weiter = ["", "Weiter:", f"  cd \"{ordner}\"", "  sh build.sh schnell      (Windows: build.bat schnell)",
              f"  Text und Angaben anpassen in {name}-buch.md und {name}-variablen.md (z. B. ort, website)."]
    with open(os.path.join(ordner, "IMPORT-BERICHT.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(kopf + ["  - " + h for h in hinweise] + weiter) + "\n")
    print("\n" + "\n".join(kopf + ["  - " + h for h in hinweise] + weiter))
    if tmp:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
