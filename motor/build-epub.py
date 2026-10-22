"""
E-Book (EPUB 3) erstellen – für tolino, Kobo, Apple Books, Google Play, Kindle (via Amazon).
Aufruf (im Buchordner):  python3 motor/build-epub.py      (normale Ausgabe)
                         python3 motor/build-epub.py uz   (zweite Ausgabe)
Der Text passt sich jeder Bildschirmgrösse an (umfliessend). Titelbild = Vorderseite des Covers.
Benötigt: Pillow, pypdfium2 (sonst poppler) für das Titelbild.
"""
import html
import os
import re
import shutil
import sys
import subprocess
import uuid
import zipfile
from datetime import date
from xml.etree import ElementTree as ET
try:                                            # Windows: «sh build.sh» in Meldungen als «.\build.bat»
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "."))
    import plattform
    plattform.windows_befehle()
except ImportError:
    pass

from PIL import Image

import build as bk
E, L = bk.E, bk.L

bk.waehle(sys.argv[1] if len(sys.argv) > 1 else None)
ISBN_EBOOK = bk.V("isbn-ebook")   # eigene ISBN, nicht die des gedruckten Buchs
TITEL = E.TITEL
AUTOR = E.AUTOR
SPRACHE = E.SPRACHE
UNTERTITEL = bk.V("untertitel")

BASE = bk.BASE
OUT_DIR = os.path.join(BASE, bk.ausgabe()["ordner"])
os.makedirs(OUT_DIR, exist_ok=True)
LESEPROBE = os.environ.get("BUCH_LESEPROBE", "").strip()     # Leseprobe: Anzahl Kapitel oder Titel des letzten
EPUB = os.path.join(OUT_DIR, bk.ausgabe()["datei"] + ("_Leseprobe" if LESEPROBE else "") + ".epub")
TMP = os.path.join(OUT_DIR, "_epub_tmp" + ("_leseprobe" if LESEPROBE else ""))
shutil.rmtree(TMP, ignore_errors=True)
os.makedirs(os.path.join(TMP, "img"))


OHNE_ALT = []          # Fotos ohne «alt:» und ohne «text:» (Hinweis am Schluss)
PORTRAIT_ALT = f"Porträt von {AUTOR}"


def esc(t):
    t = html.escape(t, quote=False).replace("&lt;br/&gt;", "<br/>")
    t = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r'<a href="\2">\1</a>', t)
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)


# --- Bilder -----------------------------------------------------------------
# Titelbild: nur Vorder- und Rückseite zeichnen (viel schneller als das ganze Buch).
# Texte des Umschlags: Blöcke «::: nur-ebook», gibt es keine, dann wie im Druck («::: nur-druck»,
# z. B. «Erstausgabe {jahr}» statt «Stand …» des Bildschirm-PDFs) – pureSATZ 2.18.
def _umschlag_medium():
    try:
        text = open(os.path.join(BASE, bk.UMSCHLAG), encoding="utf-8").read()
    except OSError:
        return "druck"
    return "ebook" if re.search(r"^\s*:::\s*nur-ebook\b", text, re.M | re.I) else "druck"


from reportlab.pdfgen import canvas as _canvas
bk.MEDIUM = _umschlag_medium()
seiten_pdf = {}
for _name, _zeichnen in (("vorne", "cover"), ("hinten", "backpage")):
    seiten_pdf[_name] = os.path.join(TMP, f"_{_name}.pdf")
    _c = _canvas.Canvas(seiten_pdf[_name], pagesize=(bk.W, bk.H))
    getattr(bk.Doc(os.path.join(TMP, "_leer.pdf")), _zeichnen)(_c, None)
    _c.showPage(); _c.save()
bk.MEDIUM = "ebook"      # ab hier: Text und Blöcke der E-Book-Ausgabe
import pdfwerkzeug
if not pdfwerkzeug.als_jpg(seiten_pdf["vorne"], os.path.join(TMP, "img", "cover.jpg"), breite=1600, qualitaet=92):
    raise SystemExit(pdfwerkzeug.HINWEIS)
if not LESEPROBE:        # Cover-Bilder für E-Book-Shops: lange Seite 2560 Pixel, kurze mind. 1600 (pureSATZ 2.18)
    _breite = round(bk.W * max(2560 / max(bk.W, bk.H), 1600 / min(bk.W, bk.H)))
    for _name, _pdf in seiten_pdf.items():
        pdfwerkzeug.als_jpg(_pdf, os.path.join(OUT_DIR, f"{bk.ausgabe()['datei']}_Cover-{_name}.jpg"),
                            breite=_breite, qualitaet=92)
lot = Image.open(bk.LOTUS); lot.thumbnail((240, 240))
lot.save(os.path.join(TMP, "img", "lotus.png"))


def rundbild(datei):
    """Rundes Portrait als JPG ins E-Book übernehmen; gibt den Dateinamen zurück."""
    pfad = bk.finde(datei)
    if not pfad:
        return None
    por = Image.open(pfad).convert("RGBA"); por.thumbnail((600, 600))
    bg = Image.new("RGB", por.size, (255, 255, 255)); bg.paste(por, mask=por.getchannel("A"))
    name = "portrait_" + os.path.splitext(os.path.basename(pfad))[0] + ".jpg"
    bg.save(os.path.join(TMP, "img", name), quality=90)
    if name not in FOTOS:          # dasselbe Foto zweimal: nur einmal ins Paket
        FOTOS.append(name)
    return name

ORN = '<div class="orn"><img src="img/lotus.png" alt=""/></div>'

# --- Kapitel aus text.md ------------------------------------------------------
dateien = []          # (dateiname, titel, inhalt-html)
nav = []              # (ebene, titel, ziel)
aktuell = {"name": None, "titel": None, "html": []}
absatz = []
kapitelnr = 0
teilnr = 0
seitennr = 0


def flush_absatz():
    if absatz:
        aktuell["html"].append(f"<p>{esc(' '.join(absatz))}</p>"); absatz.clear()


def neue_datei(name, titel):
    flush_absatz()
    if aktuell["name"]:
        dateien.append((aktuell["name"], aktuell["titel"], "\n".join(aktuell["html"])))
    aktuell.update(name=name, titel=titel, html=[])


liste_offen = False      # offenes <ul>/<ol> im Haupttext: (tag, ebene) oder False
FOTOS = []        # zusätzliche Fotos aus dem Ordner fotos/


def liste_auf(art, ebene, nr=None):
    """Passendes <ul>/<ol> öffnen (Unterpunkte als eingerückte eigene Liste)."""
    global liste_offen
    tag = "ul" if art == "-" else "ol"
    if liste_offen != (tag, ebene):
        liste_zu()
        klasse = ' class="unter"' if ebene else ""
        start = f' start="{nr}"' if tag == "ol" and nr and nr != 1 else ""
        aktuell["html"].append(f"<{tag}{klasse}{start}>"); liste_offen = (tag, ebene)


def liste_zu():
    global liste_offen
    if liste_offen:
        aktuell["html"].append(f"</{liste_offen[0]}>"); liste_offen = False


def uz_html(titel, inhalt):
    """Unzensiert-Kasten als <aside>."""
    hinweis = getattr(E, "KASTEN_HINWEIS", "")
    h = [f'<aside class="uz"><p class="uzkopf">{esc(getattr(E, "KASTEN_KOPF", "UNZENSIERT"))}'
         + (f' <span>· {esc(hinweis)}</span>' if hinweis else "") + '</p>']
    if titel:
        h.append(f'<p class="uztitel">{esc(titel)}</p>')
    p, ul, zahl = [], False, bk.Nummerierung()
    for z in inhalt + [""]:
        t = z.strip()
        m = bk.LISTE.match(t) if t else None
        if m:
            if p: h.append(f"<p>{esc(' '.join(p))}</p>"); p = []
            _, art, text = zahl.punkt(m)
            tag = "ul" if art == "-" else "ol"
            if ul != tag:
                if ul: h.append(f"</{ul}>")
                h.append(f"<{tag}" + (f' start="{art}"' if tag == "ol" and art != 1 else "") + ">"); ul = tag
            h.append(f"<li>{esc(text)}</li>"); continue
        if ul: h.append(f"</{ul}>"); ul = False
        if not t:
            if p: h.append(f"<p>{esc(' '.join(p))}</p>"); p = []
        elif t.startswith("~ "):
            h.append(f'<p class="notiz">{esc(t[2:])}</p>')
        else:
            p.append(t)
    h.append("</aside>")
    return "".join(h)


vorspann = {"titel": [], "impressum": [], "widmung": "", "kernsatz": ""}
sammle = None
QUELLEN_E = []        # (bildtext, quelle) für den Bildnachweis
bn_gesetzt = False


def bildnachweis_datei():
    """Eigener Abschnitt «Bildnachweis» (ohne Seitenzahlen)."""
    global bn_gesetzt
    bn_gesetzt = True
    if not QUELLEN_E:
        return
    titel = E.WORT_BILDNACHWEIS or "Bildnachweis"
    neue_datei("bildnachweis.xhtml", titel)
    aktuell["html"].append(f"<h2 id='bn'>{esc(titel)}</h2>" + "".join(
        f"<p class='notiz'>{esc(t) + ' – ' if t else ''}{esc(q)}</p>" for t, q in QUELLEN_E))
    nav.append((1, titel, "bildnachweis.xhtml"))

def _norm(t):
    return re.sub(r"[^0-9a-zäöüß]+", "", re.sub(r"<[^>]+>|\*\*", "", t).lower())


# Leseprobe nach Seiten: nur die Kapitel, in denen die gewählten Seiten liegen (Titel aus dem PDF)
LP_KAPITEL = {_norm(t) for t in os.environ.get("BUCH_LESEPROBE_KAPITEL", "").split("\n") if t.strip()}
lp_teil_aktiv = {}
if LESEPROBE == "seiten":
    _teil = None
    for _z in bk.text_zeilen():
        if isinstance(_z, tuple) or not _z.startswith(("# ", "## ")):
            continue
        if _z.startswith("# ") and "|" in _z:
            _teil = _z; lp_teil_aktiv.setdefault(_teil, False)
        elif _teil and _norm(_z.lstrip("# ")) in LP_KAPITEL:
            lp_teil_aktiv[_teil] = True
lp_aktiv = True
def tabelle_html(zeile):
    """Tabelle als HTML (im E-Book nie gedreht; zu breit = seitlich verschiebbar)."""
    import tabellen as T
    v = T.verweis(zeile)
    pfad = T.alle(bk.BASE).get(v[0]) if v else None
    if not pfad:
        raise SystemExit("; ".join(T.pruefe(bk.BASE, zeile)))
    d = T.lies(pfad)
    a = bk.var()
    ein = lambda t: (a.ersetze(t) if "{" in t else t) or ""
    reihen = [[ein(x) for x in r] for r in d["zeilen"]]
    rechts = [all(T.ist_zahl(r[i]) for r in reihen if r[i].strip()) and any(r[i].strip() for r in reihen)
              for i in range(len(d["kopf"]))]
    kl = lambda i: ' class="zahl"' if rechts[i] else ""
    kopf = "".join(f"<th{kl(i)}>{esc(ein(k))}</th>" for i, k in enumerate(d["kopf"]))
    zeilen = "".join("<tr>" + "".join(f"<td{kl(i)}>{esc(x)}</td>" for i, x in enumerate(r)) + "</tr>" for r in reihen)
    quelle = f'<p class="tabquelle">{esc(ein(d["quelle"]))}</p>' if d["quelle"] else ""
    return (f'<div class="tabelle"><p class="tabtitel">{esc(ein(d["titel"]))}</p>'
            f'<table class="daten"><thead><tr>{kopf}</tr></thead><tbody>{zeilen}</tbody></table>{quelle}</div>')


lp_zahl, lp_fertig = 0, False
NUM = bk.Nummerierung()
for zeile in bk.text_zeilen():
    if LESEPROBE == "seiten" and sammle is None:
        if not isinstance(zeile, tuple) and zeile.startswith(("# ", "## ")):
            if zeile.startswith("# ") and "|" in zeile:
                lp_aktiv = lp_teil_aktiv.get(zeile, False)
            else:
                lp_aktiv = _norm(zeile.lstrip("# ")) in LP_KAPITEL
        if not lp_aktiv:
            continue
    elif LESEPROBE and not isinstance(zeile, tuple) and zeile.startswith(("# ", "## ")) and sammle is None:
        if lp_fertig:
            break                         # Leseprobe: hier hört sie auf
        if not (zeile.startswith("# ") and "|" in zeile):       # Teil-Seiten zählen nicht als Kapitel
            lp_zahl += 1
            lp_fertig = lp_zahl >= int(LESEPROBE) if LESEPROBE.isdigit() else LESEPROBE.lower() in zeile.lower()
    if sammle is not None:
        if isinstance(zeile, tuple) and zeile[0] == "WIDMUNG":
            vorspann["widmung"] = " ".join(t.strip() for t in zeile[2] if t.strip()); continue
        if not isinstance(zeile, tuple) and zeile.strip() == "@WIDMUNG" and sammle == "impressum":
            sammle = "widmung_z"; vorspann["widmung_z"] = []; continue
        if isinstance(zeile, tuple) or zeile.lstrip().startswith(("#", "@")):
            sammle = None
        else:
            vorspann[sammle].append(zeile); continue
    if isinstance(zeile, tuple) and zeile[0] == "ZEITSTRAHL":
        flush_absatz()
        zeilen_z = "\n".join(f"<tr><td class='jahr'>{esc(a)}</td><td>{esc(b)}</td></tr>"
                             for a, b in bk.zeitstrahl_zeilen(zeile[2]))
        aktuell["html"].append(f"<table>{zeilen_z}</table>")
        continue
    if isinstance(zeile, tuple) and zeile[0] == "ZUSAMMEN":     # im E-Book: normaler Text
        flush_absatz()
        for z in zeile[2] + [""]:
            t = z.strip()
            if not t: flush_absatz()
            elif bk.LISTE.match(z.rstrip()):
                e, art, text = NUM.punkt(bk.LISTE.match(z.rstrip()))
                tag = "ul" if art == "-" else "ol"
                aktuell["html"].append(f"<{tag}" + (' class="unter"' if e else "")
                                       + (f' start="{art}"' if tag == "ol" and art != 1 else "") + f"><li>{esc(text)}</li></{tag}>")
            elif t.startswith("> "): aktuell["html"].append(f'{ORN}<p class="zitat">{esc(t[2:])}</p>{ORN}')
            else: absatz.append(t)
        flush_absatz()
        continue
    if isinstance(zeile, tuple):
        flush_absatz()
        liste_zu(); NUM = bk.Nummerierung()
        if zeile[0] == "UZ":
            aktuell["html"].append(uz_html(zeile[1], zeile[2]))
        elif zeile[0] == "OFFEN":        # nur im Entwurf: gelb markiert
            aktuell["html"].append(uz_html("", zeile[2]).replace('class="uz"', 'class="uz offen"', 1)
                                   .replace(esc(getattr(E, "KASTEN_KOPF", "UNZENSIERT")), "OFFEN", 1))
        elif zeile[0] == "SEITE":        # eigene Seite (z. B. «Über den Autor»)
            seitennr += 1
            name = f"seite{seitennr}.xhtml"
            neue_datei(name, zeile[1])
            aktuell["html"].append(f'<h2 id="s{seitennr}">{esc(zeile[1])}</h2>')
            nav.append((1, zeile[1], name))
        elif zeile[0] == "PORTRAIT":
            datei, _, text = zeile[2][0].partition("|")
            name = rundbild(datei.strip())
            if name:
                aktuell["html"].append(f'<div class="bild"><img class="portrait" src="img/{name}" alt="{esc(text.strip() or PORTRAIT_ALT)}"/></div>'
                                       + (f'<p class="bildtext">{esc(text.strip())}</p>' if text.strip() else ""))
        elif zeile[0] == "QR":           # im E-Book als Links statt QR-Codes
            for z in zeile[2]:
                url, _, label = z.partition("|")
                aktuell["html"].append(f'<p class="mitte"><a href="{esc(url.strip())}">{esc(label.strip().replace("<br/>", " · "))}</a></p>')
        elif zeile[0] == "ZEIT":         # Zeitstrahl als eigene Datei
            seitennr += 1
            titel_z = zeile[1] or getattr(E, "WORT_ZEITSTRAHL", "Zeitstrahl")
            name = f"seite{seitennr}.xhtml"
            neue_datei(name, titel_z)
            zeilen_z = "\n".join(f"<tr><td class='jahr'>{esc(a)}</td><td>{esc(b)}</td></tr>"
                                 for a, b in bk.zeitstrahl_zeilen(zeile[2]))
            aktuell["html"].append(f"<h2 id='z{seitennr}'>{esc(titel_z)}</h2><table>{zeilen_z}</table>")
            nav.append((1, titel_z, name))
        elif zeile[0] == "MITTE":         # zentrierter Block zwischen zwei Lotusblüten
            absaetze, p = [], []
            for z in zeile[2] + [""]:
                if z.strip(): p.append(z.strip())
                elif p: absaetze.append(" ".join(p)); p = []
            aktuell["html"].append(ORN + "".join(f'<p class="mitte">{esc(a)}</p>' for a in absaetze) + ORN)
        elif zeile[0] == "FOTO":          # nur echte Fotos, keine Vorschläge im E-Book
            pfad, text, _, datei = bk.foto_info(zeile[2])
            if pfad and bk.foto_quelle(zeile[2]):
                QUELLEN_E.append((text or zeile[1], bk.foto_quelle(zeile[2])))
            if pfad:
                alt = bk.foto_alt(zeile[2]) or text
                if not alt:
                    OHNE_ALT.append(datei)
                alt = alt or zeile[1]
                im = Image.open(pfad).convert("RGB"); im.thumbnail((1400, 1400))
                name = "foto_" + os.path.splitext(datei)[0] + ".jpg"
                im.save(os.path.join(TMP, "img", name), quality=88)
                if name not in FOTOS:          # dasselbe Foto zweimal: nur einmal ins Paket
                    FOTOS.append(name)
                opt = bk.foto_optionen(zeile[2])
                if opt.get("fluss") in ("rechts", "links"):
                    seite = "right" if opt["fluss"] == "rechts" else "left"
                    aktuell["html"].append(f'<div class="fluss fluss-{seite}"><img class="foto" src="img/{name}" alt="{esc(alt)}"/>'
                                           + (f'<p class="bildtext">{esc(text)}</p>' if text else "") + '</div>')
                else:
                    breite = f' style="max-width:{min(100, int(float(opt["breite"]) / 1.2))}%"' if opt.get("breite") else ""
                    aktuell["html"].append(f'<div class="bild"><img class="foto" src="img/{name}"{breite} alt="{esc(alt)}"/></div>'
                                           + (f'<p class="bildtext">{esc(text)}</p>' if text else ""))
        continue
    s = zeile.rstrip()
    m = bk.LISTE.match(s)
    if m:
        flush_absatz()
        e, art, text = NUM.punkt(m)
        liste_auf(art, e, art if art != "-" else None)
        aktuell["html"].append(f"<li>{esc(text)}</li>"); continue
    liste_zu()
    if s.strip():
        NUM = bk.Nummerierung()
    if re.match(r"^\d{1,3}\\\.", s):                 # «3\. Mai» = keine Aufzählung
        s = s.replace("\\.", ".", 1)
    if not s.strip():
        flush_absatz(); continue
    if s.startswith("# ") and "|" not in s:      # Kapitel oberster Ebene: eigene Datei
        seitennr += 1
        t = s[2:].strip()
        name = f"seite{seitennr}.xhtml"
        neue_datei(name, t)
        aktuell["html"].append(f'<h2 id="s{seitennr}">{esc(t)}</h2>')
        nav.append((1, t, name))
    elif s.startswith("# "):
        num, titel, sub = [x.strip() for x in s[2:].split("|")][:3]
        teilnr += 1
        name = f"teil{teilnr}.xhtml"
        neue_datei(name, f"{num} · {titel}")
        aktuell["html"].append(f'<section class="teil"><img class="teillotus" src="img/lotus.png" alt=""/>'
                               f'<p class="teilnr">{esc(num)}</p><h1>{esc(titel)}</h1>'
                               f'<p class="teilsub">{esc(sub)}</p></section>')
        nav.append((1, f"{num} · {titel}: {sub}", name))
    elif s.startswith("### "):
        flush_absatz(); aktuell["html"].append(f'<h3>{esc(s[4:])}</h3>')
    elif s.startswith("## "):
        flush_absatz()
        if aktuell["name"] is None:
            neue_datei("vorwort.xhtml", s[3:])
        kapitelnr += 1
        anker = f"k{kapitelnr}"
        aktuell["html"].append(f'<h2 id="{anker}">{esc(s[3:])}</h2>')
        nav.append((2 if any(n[0] == 1 for n in nav) else 1, s[3:], f"{aktuell['name']}#{anker}"))
    elif s.startswith("> "):
        flush_absatz()
        aktuell["html"].append(f'{ORN}<p class="zitat">{esc(s[2:])}</p>{ORN}')
    elif s.startswith("~ "):
        flush_absatz(); aktuell["html"].append(f'<p class="notiz">{esc(s[2:])}</p>')
    elif s.startswith("@MOTTO "):
        flush_absatz()
        aktuell["html"].append(f'<div class="motto">{ORN}<p class="zitat">{esc(s[7:])}</p>{ORN}</div>')
    elif s.startswith("@ZITAT "):
        flush_absatz(); aktuell["html"].append(f'<p class="zitat">{esc(s[7:])}</p>')
    elif s.startswith("@UNTEN "):
        flush_absatz(); aktuell["html"].append(f'<p class="zitat" style="margin-top: 3em;">{esc(s[7:])}</p>')
    elif s == "@TITEL":
        flush_absatz(); sammle = "titel"
    elif s == "@IMPRESSUM":
        flush_absatz(); sammle = "impressum"
    elif s.startswith("@KERNSATZ"):
        flush_absatz(); vorspann["kernsatz"] = s[9:].strip()
    elif s.startswith("@PORTRAIT "):
        flush_absatz()
        datei, _, text = s[10:].partition("|")
        name = rundbild(datei.strip())
        if name:
            aktuell["html"].append(f'<div class="bild"><img class="portrait" src="img/{name}" alt="{esc(text.strip() or PORTRAIT_ALT)}"/></div>'
                                   + (f'<p class="bildtext">{esc(text.strip())}</p>' if text.strip() else ""))
    elif s.startswith(("@QR-PAAR ", "@QR ")):     # im E-Book: Links statt QR-Codes
        flush_absatz()
        for x in s.split(" ", 1)[1].split(";;"):
            url, _, label = x.partition("|")
            label = (label.strip() or url.strip()).replace("<br/>", ": ")
            aktuell["html"].append(f'<p><a href="{esc(url.strip())}">{esc(label)}</a></p>')
    elif s.startswith(("@BILDNACHWEIS", "@STICHWORTE", "@RUECKSEITE")):
        flush_absatz()
        if not bn_gesetzt:
            bildnachweis_datei()
    elif s.startswith("@#"):                     # Tabelle aus tabellen/*.csv (pureSATZ 2.12)
        flush_absatz(); aktuell["html"].append(tabelle_html(s))
    elif s.startswith("@"):
        flush_absatz()      # Steuerzeilen für das Seitenlayout gelten im E-Book nicht
    else:
        absatz.append(s.strip())
liste_zu()
if not bn_gesetzt:
    bildnachweis_datei()
if LESEPROBE:                             # Schlussseite wie im PDF, mit Link statt QR-Code
    import fassungen
    zeilen_lp, link_lp = fassungen.leseprobe_angaben(bk, bk.FASSUNG)
    neue_datei("leseprobe-ende.xhtml", "Ende der Leseprobe")
    aktuell["html"].append('<section class="titel"><h2 id="lp">Ende der Leseprobe</h2>'
                           + "".join(f'<p class="mitte">{esc(z)}</p>' for z in zeilen_lp)
                           + (f'<p class="mitte"><a href="{esc(link_lp)}">{esc(link_lp)}</a></p>' if link_lp else "")
                           + "</section>")
    nav.append((1, "Ende der Leseprobe", "leseprobe-ende.xhtml"))
neue_datei(None, None)

# Titelseite mit Impressum (vorne), alles aus @TITEL / @IMPRESSUM / @KERNSATZ der MD
titelz = [z.strip() for z in vorspann["titel"] if z.strip()]


def absaetze_html(zeilen):
    """Zeilen untereinander, Leerzeile = neuer Absatz."""
    out, akt = [], []
    for z in zeilen + [""]:
        if getattr(z, "nr", 0) == -1:
            continue
        if z.strip():
            akt.append(esc(z.strip()))
        elif akt:
            out.append("<p>" + "<br/>".join(akt) + "</p>"); akt = []
    return "\n".join(out)


vorspann["widmung"] = vorspann["widmung"] or " ".join(z.strip() for z in vorspann.get("widmung_z", []) if z.strip())
widmung_html = ('<p style="margin-top: 2em;"><i>' + esc(vorspann["widmung"]) + '</i></p>') if vorspann["widmung"] else ""
kernsatz_html = ('<div class="motto">' + ORN + '<p class="zitat">' + esc(vorspann["kernsatz"]) + '</p>' + ORN + '</div>') if vorspann["kernsatz"] else ""
titel_html = f"""
<section class="titel">
<img class="titellotus" src="img/lotus.png" alt=""/>
<h1 class="haupttitel">{esc(titelz[0] if titelz else TITEL)}</h1>
<p class="untertitel">{esc(titelz[1] if len(titelz) > 1 else UNTERTITEL)}</p>
<p class="autor">{esc(AUTOR)}</p>
</section>
<div class="impressum">
{absaetze_html(vorspann["impressum"])}
{widmung_html}
</div>""" + kernsatz_html
dateien.insert(0, ("titel.xhtml", TITEL, titel_html))

# --- CSS ----------------------------------------------------------------------
CSS = """
p.mitte { text-align: center; text-indent: 0; }
div.motto { margin: 30% 0; page-break-before: always; page-break-after: always; }

img.foto { max-width: 100%; max-height: 60vh; }
div.fluss { width: 40%; margin: 0.2em 0 0.6em 0; }
div.fluss-right { float: right; margin-left: 1em; }
div.fluss-left { float: left; margin-right: 1em; }
div.fluss img.foto { width: 100%; }
aside.uz { background: @@kasten@@; border-left: 3px solid @@akzent@@; padding: 0.6em 1em; margin: 1em 0; font-size: 0.93em; }
aside.uz p { text-indent: 0; }
aside.offen { background: @@offen@@; border-left-color: @@offen_linie@@; }
p.uzkopf { font-size: 0.7em; color: @@akzenttext@@; letter-spacing: 0.08em; margin: 0 0 0.3em 0; font-weight: bold; }
p.uzkopf span { color: @@leise@@; font-style: italic; font-weight: normal; letter-spacing: 0; }
p.uztitel { color: @@haupt@@; font-weight: bold; margin: 0 0 0.4em 0; }
@font-face { font-family: "Text"; src: url(fonts/@@f_text@@); }
@font-face { font-family: "Text"; font-style: italic; src: url(fonts/@@f_text_kursiv@@); }
@font-face { font-family: "Text"; font-weight: bold; src: url(fonts/@@f_text_fett@@); }
@font-face { font-family: "Titel"; font-weight: 500; src: url(fonts/@@f_titel@@); }
body { font-family: "Text", serif; line-height: 1.5; color: @@text@@; margin: 0 4%; }
p { margin: 0 0 0.7em 0; text-align: left; }
h1, h2 { font-family: "Titel", sans-serif; font-weight: 500; color: @@haupt@@; }
h2 { font-size: 1.25em; margin: 1.6em 0 0.6em 0; page-break-after: avoid; }
.teil { text-align: center; margin-top: 18%; page-break-after: always; }
.teillotus { width: 30%; max-width: 160px; opacity: 0.35; }
.teilnr { font-family: "Titel", sans-serif; color: @@akzenttext@@; letter-spacing: 0.15em;
          text-transform: uppercase; font-size: 0.8em; margin-top: 1em; text-align: center; }
.teil h1 { font-size: 2em; margin: 0.2em 0; }
.teilsub { font-style: italic; color: @@leise@@; text-align: center; }
.orn { text-align: center; margin: 0.6em 0; }
.orn img { width: 1.6em; }
.zitat { text-align: center; font-style: italic; color: @@haupt@@; font-size: 1.1em; margin: 0.4em 8%; }
.notiz { font-style: italic; color: @@leise@@; margin-left: 5%; }
ul, ol { padding-left: 1.4em; } li { margin-bottom: 0.4em; } ul.unter, ol.unter { margin-top: 0; padding-left: 2.8em; }
table { border-collapse: collapse; width: 100%; font-size: 0.9em; }
td { padding: 0.3em 0.4em 0.3em 0; vertical-align: top; border-bottom: 1px solid @@linie@@; }
td.jahr { font-family: "Titel", sans-serif; color: @@akzenttext@@; white-space: nowrap; width: 5.5em; }
.bild { text-align: center; } .portrait { width: 45%; max-width: 260px; border-radius: 50%; }
.bildtext { text-align: center; font-style: italic; color: @@leise@@; font-size: 0.85em; }
.titel { text-align: center; margin-top: 15%; }
.titellotus { width: 35%; max-width: 200px; }
.haupttitel { font-size: 2em; margin: 0.8em 0 0.2em 0; }
.untertitel { font-style: italic; color: @@leise@@; text-align: center; }
.autor { font-family: "Titel", sans-serif; text-align: center; margin-top: 1.5em; }
.impressum { page-break-before: always; font-size: 0.8em; color: @@leise@@; margin-top: 40%; }
a { color: @@akzenttext@@; }
"""


SCHRIFT_DATEI = {r: L.SCHRIFTDATEIEN[bk.schrift(r)] for r in ("text", "text_kursiv", "text_fett", "titel")}
for _k in list(L.FARBEN) + list(SCHRIFT_DATEI):
    pass
CSS = re.sub(r"@@f_(\w+)@@", lambda m: SCHRIFT_DATEI[m.group(1)], CSS)
AKZENT_TEXT = bk.V("farbe-akzent-ebook") or bk.lesbare_farbe(bk.hexfarbe("akzent"), ["#FFFFFF", bk.hexfarbe("kasten")])
CSS += """
div.tabelle { overflow-x: auto; margin: 1em 0; }
p.tabtitel { font-family: "Titel", sans-serif; color: @@haupt@@; margin: 0 0 0.3em 0; text-indent: 0; }
table.daten { width: auto; min-width: 60%; font-size: 0.85em; }
table.daten th { text-align: left; color: @@haupt@@; border-bottom: 1.5px solid @@akzent@@; padding: 0.25em 0.5em; }
table.daten td { padding: 0.2em 0.5em; border-bottom: 0.5px solid @@linie@@; vertical-align: top; }
table.daten .zahl { text-align: right; }
table.daten tbody tr:nth-child(even) td { background: @@kasten@@; }
p.tabquelle { font-size: 0.8em; font-style: italic; margin: 0.3em 0 0 0; text-indent: 0; }
"""
CSS = CSS.replace("@@akzenttext@@", AKZENT_TEXT)
CSS = re.sub(r"@@(\w+)@@", lambda m: bk.hexfarbe(m.group(1)), CSS)


def xhtml(titel, inhalt):
    return f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="{SPRACHE}" lang="{SPRACHE}">
<head><meta charset="utf-8"/><title>{esc(titel)}</title><link rel="stylesheet" href="style.css"/></head>
<body>
{inhalt}
</body>
</html>"""


# --- Navigation ----------------------------------------------------------------
def nav_html():
    out, ebene = ["<ol>"], 1
    for i, (lv, titel, ziel) in enumerate(nav):
        if lv > ebene:
            out[-1] = out[-1][:-5] + "<ol>"          # in den vorherigen <li> verschachteln
            ebene = lv
        elif lv < ebene:
            out.append("</ol></li>"); ebene = lv
        out.append(f'<li><a href="{ziel}">{esc(titel)}</a></li>')
    if ebene == 2:
        out.append("</ol></li>")
    out.append("</ol>")
    return "\n".join(out)


nav_doc = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="{SPRACHE}" lang="{SPRACHE}">
<head><meta charset="utf-8"/><title>Inhalt</title><link rel="stylesheet" href="style.css"/></head>
<body>
<nav epub:type="toc" id="toc"><h2>Inhalt</h2>
{nav_html()}
</nav>
<nav epub:type="landmarks" hidden="hidden"><ol>
<li><a epub:type="cover" href="cover.xhtml">Titelbild</a></li>
<li><a epub:type="toc" href="nav.xhtml">Inhalt</a></li>
<li><a epub:type="bodymatter" href="{dateien[1][0]}">Beginn</a></li>
</ol></nav>
</body></html>"""

# Kennung des E-Books: «ebook-id» (fest, z. B. nach einer Umbenennung), sonst aus buch-id/Website, Titel und Kurzname
_kennung = bk.V("ebook-id") or ((bk.V("buch-id") or (E.WEBSITE + "/" + E.TITEL)) + "/" + bk.ausgabe()["kuerzel"])
ident = f"urn:isbn:{ISBN_EBOOK.replace('-', '')}" if ISBN_EBOOK else f"urn:uuid:{uuid.uuid5(uuid.NAMESPACE_URL, _kennung)}"
if LESEPROBE:                             # Leseprobe: eigene Kennung, nie die ISBN des Buchs
    ident = f"urn:uuid:{uuid.uuid5(uuid.NAMESPACE_URL, _kennung + '/leseprobe')}"

# toc.ncx (für ältere Lesegeräte)
ncx_points, order = [], 0
for lv, titel, ziel in nav:
    order += 1
    ncx_points.append(f'<navPoint id="n{order}" playOrder="{order}"><navLabel><text>{esc(titel)}</text>'
                      f'</navLabel><content src="{ziel}"/></navPoint>')
ncx = f"""<?xml version="1.0" encoding="utf-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
<head><meta name="dtb:uid" content="{ident}"/></head>
<docTitle><text>{esc(TITEL)}</text></docTitle>
<navMap>{''.join(ncx_points)}</navMap></ncx>"""

cover_doc = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="{SPRACHE}" lang="{SPRACHE}">
<head><meta charset="utf-8"/><title>Titelbild</title>
<style>body{{margin:0;padding:0;text-align:center;}} img{{max-width:100%;max-height:100%;}}</style></head>
<body epub:type="cover"><img src="img/cover.jpg" alt="Titelbild: {esc(TITEL)}"/></body></html>"""

# --- Barrierefreiheit (EPUB Accessibility 1.1, schema.org) -------------------------------
def barrierefrei():
    """Angaben zur Barrierefreiheit für Shops und Vorlesegeräte. Ehrlich: nur, was das E-Book wirklich hat."""
    m = ['<meta property="schema:accessMode">textual</meta>']
    if FOTOS:
        m.append('<meta property="schema:accessMode">visual</meta>')
    m.append(f'<meta property="schema:accessModeSufficient">{"textual" if not OHNE_ALT else "textual,visual"}</meta>')
    merkmale = ["structuralNavigation", "tableOfContents", "readingOrder", "displayTransformability"]
    if FOTOS and not OHNE_ALT:
        merkmale.append("alternativeText")
    m += [f'<meta property="schema:accessibilityFeature">{x}</meta>' for x in merkmale]
    m.append('<meta property="schema:accessibilityHazard">none</meta>')
    zusammenfassung = bk.V("ebook-barrierefreiheit") or (
        "Umfliessender Text mit Inhaltsverzeichnis und Überschriften-Gliederung; Schrift und Grösse sind einstellbar. "
        + ("Alle Bilder haben eine Textbeschreibung." if FOTOS and not OHNE_ALT else
           "Einzelne Bilder haben keine Textbeschreibung." if OHNE_ALT else "Keine inhaltlichen Bilder."))
    m.append(f'<meta property="schema:accessibilitySummary">{esc(zusammenfassung)}</meta>')
    return "\n".join(m)


# --- content.opf -----------------------------------------------------------------
fonts = sorted(set(SCHRIFT_DATEI.values()))
manifest = [
    '<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>',
    '<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>',
    '<item id="css" href="style.css" media-type="text/css"/>',
    '<item id="coverimg" href="img/cover.jpg" media-type="image/jpeg" properties="cover-image"/>',
    '<item id="cover" href="cover.xhtml" media-type="application/xhtml+xml"/>',
    '<item id="lotus" href="img/lotus.png" media-type="image/png"/>',
] + [f'<item id="foto{i}" href="img/{n}" media-type="image/jpeg"/>' for i, n in enumerate(FOTOS)] + [
] + [f'<item id="f{i}" href="fonts/{f}" media-type="application/vnd.ms-opentype"/>' for i, f in enumerate(fonts)] \
  + [f'<item id="d{i}" href="{n}" media-type="application/xhtml+xml"/>' for i, (n, _, _) in enumerate(dateien)]
spine = ['<itemref idref="cover" linear="yes"/>', f'<itemref idref="d0"/>', '<itemref idref="nav"/>'] + \
        [f'<itemref idref="d{i}"/>' for i in range(1, len(dateien))]
opf = f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid" xml:lang="{SPRACHE}">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:identifier id="bookid">{ident}</dc:identifier>
<dc:title>{esc(TITEL + (" – Leseprobe" if LESEPROBE else ""))}</dc:title>
<dc:creator>{esc(AUTOR)}</dc:creator>
<dc:language>{SPRACHE}</dc:language>
<dc:description>{esc(bk.V("shop-beschreibung") or UNTERTITEL)}</dc:description>
{"".join(f"<dc:subject>{esc(w.strip())}</dc:subject>" for w in bk.V("shop-schlagwoerter").split(",") if w.strip())}
<dc:publisher>{esc(AUTOR)}, {esc(E.ORT)}</dc:publisher>
<dc:date>{date.today().isoformat()}</dc:date>
<meta property="dcterms:modified">{date.today().isoformat()}T00:00:00Z</meta>
<meta name="cover" content="coverimg"/>
{barrierefrei()}
</metadata>
<manifest>
{chr(10).join(manifest)}
</manifest>
<spine toc="ncx">
{chr(10).join(spine)}
</spine>
</package>"""

# --- Schreiben + Prüfen ------------------------------------------------------------
dateien_xml = {"nav.xhtml": nav_doc, "cover.xhtml": cover_doc, "toc.ncx": ncx, "content.opf": opf}
for n, t, inhalt in dateien:
    dateien_xml[n] = xhtml(t, inhalt)
for n, inhalt in dateien_xml.items():
    ET.fromstring(inhalt.encode("utf-8"))      # wirft einen Fehler, falls das XML nicht sauber ist

with zipfile.ZipFile(EPUB, "w") as z:
    z.writestr(zipfile.ZipInfo("mimetype"), "application/epub+zip", compress_type=zipfile.ZIP_STORED)
    z.writestr("META-INF/container.xml", """<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
<rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles>
</container>""", compress_type=zipfile.ZIP_DEFLATED)
    for n, inhalt in dateien_xml.items():
        z.writestr("OEBPS/" + n, inhalt, compress_type=zipfile.ZIP_DEFLATED)
    z.writestr("OEBPS/style.css", CSS, compress_type=zipfile.ZIP_DEFLATED)
    for f in fonts:
        z.write(bk.finde(f, ("fonts",)), "OEBPS/fonts/" + f, compress_type=zipfile.ZIP_DEFLATED)
    for f in os.listdir(os.path.join(TMP, "img")):
        z.write(os.path.join(TMP, "img", f), "OEBPS/img/" + f, compress_type=zipfile.ZIP_DEFLATED)
shutil.rmtree(TMP, ignore_errors=True)
print(f"Fertig: {os.path.relpath(EPUB, BASE)}  ({len(dateien)} Abschnitte, {len(nav)} Einträge im Inhalt)")
if OHNE_ALT:
    print(f"Hinweis Barrierefreiheit: {len(OHNE_ALT)} Foto(s) ohne Beschreibung – im Foto-Block «alt: …» oder «text: …» ergänzen: "
          + ", ".join(OHNE_ALT))
if not ISBN_EBOOK and not LESEPROBE:
    print("Hinweis: Noch keine E-Book-ISBN eingetragen.")
if bk.ja("ebook-epub2", "nein") and not LESEPROBE:      # «epub2-light» für Shops, die nur EPUB 2 annehmen (2.20)
    import epub2
    print(f"Fertig: {os.path.relpath(epub2.wandle(EPUB, EPUB[:-5] + '_EPUB2.epub'), BASE)}  (EPUB 2)")
