#!/usr/bin/env python3
"""
staende.py – Stände markieren und vergleichen: «Was hat sich geändert?» (pureSATZ ab 2.33).

Im Buchordner (über build.sh / build.bat):
    sh build.sh stand "Probedruck 1"          jetzigen Stand unter diesem Namen festhalten
    sh build.sh stand "Probedruck 1" 23.10.2026 15:00   nachträglich: Fassung aus md-history/ bis zu diesem Zeitpunkt
    sh build.sh stand                         alle Stände zeigen
    sh build.sh aenderungen                   was sich seit dem letzten Stand geändert hat
    sh build.sh aenderungen "Probedruck 1"    … seit diesem Stand
    sh build.sh aenderungen "Probedruck 1" "Probedruck 2"   zwei Stände miteinander vergleichen

Ein Stand ist eine Kopie der Texte (Buch-, Variablen-, Umschlag-MD, Stichwörter, Geschichten) im Ordner
staende/<datum>_<name>/. Der Ordner kommt mit sh sync.sh auch auf die anderen Computer.
Ergebnis von «aenderungen»: <Datei>_Aenderungen.pdf im Ausgabeordner der normalen Fassung –
Absatz für Absatz, Neues grün und unterstrichen, Gestrichenes rot und durchgestrichen.
"""
import difflib
import html
import os
import re
import shutil
import sys
from datetime import datetime

ORDNER = "staende"
INFO = "stand.txt"


# --- Stände speichern und finden -------------------------------------------------
def _slug(name):
    s = name.strip().lower()
    for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss"), ("é", "e"), ("è", "e"), ("à", "a")):
        s = s.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-") or "stand"


def _info(pfad):
    d = {}
    try:
        for z in open(os.path.join(pfad, INFO), encoding="utf-8"):
            k, _, w = z.partition(":")
            if w:
                d[k.strip().lower()] = w.strip()
    except OSError:
        pass
    d.setdefault("name", os.path.basename(pfad).partition("_")[2] or os.path.basename(pfad))
    d.setdefault("datum", "")
    return d


def alle(base):
    """[(ordnerpfad, info)] – älteste zuerst."""
    o = os.path.join(base, ORDNER)
    if not os.path.isdir(o):
        return []
    return [(os.path.join(o, d), _info(os.path.join(o, d))) for d in sorted(os.listdir(o))
            if os.path.isdir(os.path.join(o, d)) and not d.startswith((".", "_"))]


def finde(base, name):
    """Stand nach Name (Gross/klein egal), Ordnername oder eindeutigem Teil davon."""
    staende = alle(base)
    if not staende:
        raise SystemExit('> Noch kein Stand festgehalten.\n$ sh build.sh stand "Probedruck 1"')
    if name is None:
        return staende[-1]
    n = name.strip().lower()
    for p, i in staende:
        if i["name"].lower() == n or os.path.basename(p).lower() == n:
            return p, i
    treffer = [(p, i) for p, i in staende if n in i["name"].lower() or n in os.path.basename(p).lower()]
    if len(treffer) == 1:
        return treffer[0]
    namen = "\n  ".join(f"{i['name']}  ({i['datum']})" for _, i in staende)
    raise SystemExit(f"Stand «{name}» {'ist nicht eindeutig' if treffer else 'nicht gefunden'}. Vorhanden:\n  {namen}")


def speichern(base, name, dateien, geschichten, motor_version="", zeit=None, notiz=""):
    """dateien: Namen im Buchordner oder {Name im Stand: Quellpfad}; geschichten: {name: pfad}."""
    for _, i in alle(base):
        if i["name"].lower() == name.strip().lower():
            raise SystemExit(f"Den Stand «{name}» gibt es schon ({i['datum']}). Anderen Namen wählen oder den Ordner "
                             f"staende/…_{_slug(name)}/ löschen.")
    jetzt = zeit or datetime.now()
    ziel = os.path.join(base, ORDNER, f"{jetzt:%Y-%m-%d}_{_slug(name)}")
    n = 2
    while os.path.exists(ziel):
        ziel = os.path.join(base, ORDNER, f"{jetzt:%Y-%m-%d}_{_slug(name)}-{n}"); n += 1
    os.makedirs(ziel)
    quellen = dateien if isinstance(dateien, dict) else {d: os.path.join(base, d) for d in dateien if d}
    for d, q in quellen.items():
        if os.path.exists(q):
            shutil.copy2(q, os.path.join(ziel, d))
    for g, p in geschichten.items():
        z = os.path.join(ziel, "geschichten", g + ".md")
        os.makedirs(os.path.dirname(z), exist_ok=True)
        shutil.copy2(p, z)
    with open(os.path.join(ziel, INFO), "w", encoding="utf-8") as f:
        f.write(f"name: {name.strip()}\ndatum: {jetzt:%d.%m.%Y %H:%M}\nmotor: {motor_version}\n"
                + (f"notiz: {notiz}\n" if notiz else ""))
    return ziel


# --- Stand nachträglich aus md-history/ -------------------------------------------
ZEIT = re.compile(r"_(\d{8}-\d{2}-\d{2}-\d{2})$")


def zeit_aus(argumente):
    """Datum/Uhrzeit am Ende der Argumente: «23.10.2026 15:00», «23.10.2026», «2026-10-23», «15:00» (heute).
    Gibt (übrige Argumente, datetime | None)."""
    rest, datum, uhr = list(argumente), None, None
    while rest:
        a = rest[-1].strip()
        if uhr is None and re.fullmatch(r"\d{1,2}[:.]\d{2}", a) and datum is None:
            uhr = a.replace(".", ":"); rest.pop(); continue
        m = re.fullmatch(r"(\d{1,2})\.(\d{1,2})\.(\d{4})", a) or re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", a)
        if m and datum is None:
            g = m.groups()
            datum = (int(g[2]), int(g[1]), int(g[0])) if len(g[0]) <= 2 else (int(g[0]), int(g[1]), int(g[2]))
            rest.pop(); continue
        break
    if datum is None and uhr is None:
        return argumente, None
    j, mo, t = datum or (datetime.now().year, datetime.now().month, datetime.now().day)
    h, mi = (int(x) for x in (uhr or "23:59").split(":"))
    return rest, datetime(j, mo, t, h, mi, 59)


def aus_history(base, dateien, bis):
    """Neueste Kopie jeder Datei in md-history/ bis zum Zeitpunkt «bis». ({Name: Pfad}, {Geschichte: Pfad}, Zeit)"""
    o = os.path.join(base, "md-history")
    if not os.path.isdir(o):
        raise SystemExit("Kein Ordner md-history/ – ein Stand in der Vergangenheit geht nur mit md-history.")

    def neueste(ordner, stamm, endung):
        best = None
        for f in os.listdir(ordner):
            s, e = os.path.splitext(f)
            m = ZEIT.search(s)
            if e != endung or not m or s[:m.start()] != stamm:
                continue
            z = datetime.strptime(m.group(1), "%Y%m%d-%H-%M-%S")
            if z <= bis and (best is None or z > best[0]):
                best = (z, os.path.join(ordner, f))
        return best
    quellen, zeiten = {}, []
    for d in dateien:
        if not d:
            continue
        b = neueste(o, *os.path.splitext(d))
        if b:
            quellen[d] = b[1]; zeiten.append(b[0])
    if not quellen or dateien[0] not in quellen:
        raise SystemExit(f"In md-history/ gibt es keine Fassung von {dateien[0]} vor dem {bis:%d.%m.%Y %H:%M}.")
    geschichten = {}
    og = os.path.join(o, "geschichten")
    if os.path.isdir(og):
        namen = {ZEIT.sub("", os.path.splitext(f)[0]) for f in os.listdir(og) if f.endswith(".md")}
        for n in sorted(namen):
            b = neueste(og, n, ".md")
            if b:
                geschichten[n] = b[1]
    return quellen, geschichten, max(zeiten)


def zeigen(base):
    staende = alle(base)
    if not staende:
        print('> Noch kein Stand.\n$ sh build.sh stand "Probedruck 1"   (festhalten)')
        return
    print("Stände (älteste zuerst):")
    for p, i in staende:
        print(f"  {i['name']:<30} {i['datum']:<17} {os.path.relpath(p, base)}/")
    print('\n$ sh build.sh aenderungen   (seit dem letzten Stand)\n$ sh build.sh aenderungen "Name"   (seit diesem Stand)')


# --- Text in Absätze zerlegen ----------------------------------------------------
BLOCK = re.compile(r"^\s*:::\s*(\S*)")
LISTE = re.compile(r"^\s*(?:[-*]|\d{1,3}\.)\s+\S")


def _fassung(art):
    a = art.lower()
    if a.endswith("-uz") or a == "uz" or a.startswith("nur-uz"):
        return "nur Unzensiert"
    if a.endswith("-normal"):
        return "nur normale Fassung"
    return ""


def _kapitelname(z):
    s = z.strip()
    m = re.match(r"^(#{1,3})\s+(.*)$", s)
    if not m:
        return None
    t = m.group(2).strip()
    if t.startswith("@"):
        return None
    if len(m.group(1)) == 1 and "|" in t:                 # # Teil 1|Leben 1.0|Der Suchende
        teile = [x.strip() for x in t.split("|")]
        t = ": ".join(x for x in teile[:2] if x) or t
    return len(m.group(1)), t


def absaetze(buchtext, geschichten_text):
    """[(text, ort, fassung)] – Absätze in Buch-Reihenfolge; @@-Geschichten an ihrer Stelle eingesetzt."""
    import geschichten as G
    zeilen = []
    for z in buchtext.split("\n"):
        m = G.VERWEIS.match(z)
        if m and m.group(1) in geschichten_text:
            zeilen += geschichten_text[m.group(1)].split("\n") + [""]
        else:
            zeilen.append(z)
    out, para, ort, kap, teil, offen = [], [], "", "", "", []

    def fertig():
        if para:
            out.append((" ".join(x.strip() for x in para).strip(), ort, next((f for f in reversed(offen) if f), "")))
            para.clear()

    for z in zeilen:
        s = z.strip()
        b = BLOCK.match(z)
        if b:
            fertig()
            if b.group(1):
                offen.append(_fassung(b.group(1)))
            elif offen:
                offen.pop()
            continue
        k = _kapitelname(z)
        if k:
            fertig()
            if k[0] == 1:
                teil, kap = k[1], ""
            elif k[0] == 2:
                kap = k[1]
            ort = " · ".join(x for x in (teil, kap) if x)
            out.append((s, ort, next((f for f in reversed(offen) if f), "")))
            continue
        if LISTE.match(z):                                 # jeder Listenpunkt ist ein eigener Absatz
            fertig()
        if not s or s in ("---",) or s.startswith(("#### @FOTO",)):
            fertig()
            if s.startswith("#### @FOTO"):
                para.append(s)
            continue
        para.append(z)
    fertig()
    return out


def _werte(text):
    """{(abschnitt, name): wert} aus Variablen- oder Umschlag-MD (Erklärungen mit «>» zählen nicht)."""
    d, abschnitt = {}, ""
    for z in text.split("\n"):
        s = z.strip()
        if s.startswith("#"):
            abschnitt = s.lstrip("#").strip()
            continue
        if not s or s.startswith(">"):
            continue
        m = re.match(r"^\{?([A-Za-z0-9@][A-Za-z0-9_.-]*)\}?\s*:\s*(.*)$", s)
        if m:
            d[(abschnitt, m.group(1))] = m.group(2)
    return d


# --- Vergleich ------------------------------------------------------------------
def _woerter(t):
    return re.findall(r"\S+\s*", t)


def _markiert(alt, neu, gruen, rot):
    """Absatz mit Wortänderungen als Paragraph-Markup."""
    a, b = _woerter(alt), _woerter(neu)
    sm = difflib.SequenceMatcher(None, [w.strip() for w in a], [w.strip() for w in b], autojunk=False)
    out = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            out.append(html.escape("".join(b[j1:j2])))
            continue
        if i2 > i1:
            out.append(f'<font color="{rot}"><strike>{html.escape("".join(a[i1:i2]).rstrip())}</strike></font> ')
        if j2 > j1:
            out.append(f'<font color="{gruen}"><u>{html.escape("".join(b[j1:j2]).rstrip())}</u></font> ')
    return "".join(out)


def _paare(alt, neu):
    """Bei «replace»: ähnliche Absätze einander zuordnen. [(i|None, j|None)]"""
    paare, j0 = [], 0
    for i, a in enumerate(alt):
        best, bj = 0.0, None
        for j in range(j0, len(neu)):
            r = difflib.SequenceMatcher(None, a[0], neu[j][0], autojunk=False).quick_ratio()
            if r > best:
                best, bj = r, j
        if bj is not None and best >= 0.5 and difflib.SequenceMatcher(None, a[0], neu[bj][0], autojunk=False).ratio() >= 0.5:
            paare += [(None, j) for j in range(j0, bj)] + [(i, bj)]
            j0 = bj + 1
        else:
            paare.append((i, None))
    paare += [(None, j) for j in range(j0, len(neu))]
    return paare


def vergleiche(alt, neu):
    """[(art, ort, fassung, alt_text, neu_text)] mit art = geaendert | neu | gestrichen."""
    sm = difflib.SequenceMatcher(None, [x[0] for x in alt], [x[0] for x in neu], autojunk=False)
    out = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            continue
        a, b = alt[i1:i2], neu[j1:j2]
        for i, j in (_paare(a, b) if op == "replace" else [(i, None) for i in range(len(a))] + [(None, j) for j in range(len(b))]):
            if i is not None and j is not None:
                out.append(("geaendert", b[j][1], b[j][2] or a[i][2], a[i][0], b[j][0]))
            elif i is not None:
                out.append(("gestrichen", a[i][1], a[i][2], a[i][0], ""))
            else:
                out.append(("neu", b[j][1], b[j][2], "", b[j][0]))
    return out


def werte_vergleich(alt, neu, datei):
    if not alt.strip() or not neu.strip():        # Datei fehlt in einem Stand: nicht vergleichen
        return []
    a, b = _werte(alt), _werte(neu)
    out = []
    for k in list(a) + [k for k in b if k not in a]:
        if a.get(k) != b.get(k):
            out.append((datei, k[0], k[1], a.get(k), b.get(k)))
    return out


# --- PDF ------------------------------------------------------------------------
def _zeige(s, fett=False):
    """Für die Anzeige: Überschrift ohne #, Teil «Teil 1|Titel|Untertitel» lesbar, Listenpunkt mit •.
    fett=False: ohne ** (Text) · fett=True: Markup mit <b> (schon maskiert)."""
    s = s.strip()
    m = re.match(r"^(#{1,6})\s+(.*)$", s)
    if m:
        s = " · ".join(x.strip() for x in m.group(2).split("|") if x.strip()) if len(m.group(1)) == 1 else m.group(2)
    s = re.sub(r"^[-*]\s+", "• ", s)
    if not fett:
        return s.replace("**", "")
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", html.escape(s)).replace("**", "")


def pdf(ziel, kopf, aenderungen, werte, schrift, schrift_fett, akzent="#1F3A68"):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether
    GRUEN, ROT, GRAU = "#1A7F37", "#B42318", "#6B6B6B"
    st = lambda n, **k: ParagraphStyle(n, fontName=k.pop("fn", schrift), **k)
    text = st("t", fontSize=10, leading=14.5)
    punkt = st("p", fontSize=10, leading=14.5, leftIndent=5 * mm, firstLineIndent=-3.5 * mm)
    klein = st("k", fontSize=8, leading=11, textColor=colors.HexColor(GRAU))
    h1 = st("h1", fn=schrift_fett, fontSize=16, leading=20, textColor=colors.HexColor(akzent), spaceAfter=4)
    h2 = st("h2", fn=schrift_fett, fontSize=11.5, leading=15, textColor=colors.HexColor(akzent), spaceBefore=12, spaceAfter=4)
    e = html.escape
    fl = []
    fl += [Paragraph(e(kopf["titel"]), h1), Paragraph(e(kopf["vergleich"]), text), Spacer(1, 3 * mm)]
    z = {k: sum(1 for x in aenderungen if x[0] == k) for k in ("geaendert", "neu", "gestrichen")}
    zus = (f"{z['geaendert']} Absätze geändert · {z['neu']} neu · {z['gestrichen']} gestrichen"
           + (f" · {len(werte)} Werte (Variablen, Umschlag, Stichwörter)" if werte else ""))
    fl += [Paragraph(e(zus), text),
           Paragraph(f'Legende: <font color="{GRUEN}"><u>neu</u></font> · '
                     f'<font color="{ROT}"><strike>gestrichen</strike></font> · unveränderte Absätze fehlen.', klein),
           Spacer(1, 2 * mm)]
    orte = []
    for x in aenderungen:
        if x[1] not in orte:
            orte.append(x[1])
    if len(orte) > 1:
        fl.append(Paragraph("Betroffen: " + " · ".join(
            e(o or "Anfang") + f" ({sum(1 for x in aenderungen if x[1] == o)})" for o in orte), klein))
    letzter, vorher = None, None
    for art, ort, fassung, alt, neu in aenderungen:
        if ort != letzter:
            fl.append(Paragraph(e(ort or "Anfang (Titelei)"), h2))
            letzter = ort
        marke = {"geaendert": "geändert", "neu": "neu", "gestrichen": "gestrichen"}[art]
        info = marke + (f" · {fassung}" if fassung else "")
        if (neu or alt).lstrip().startswith("#"):
            info = "Überschrift " + info
        if art == "geaendert":
            inhalt = _markiert(_zeige(alt), _zeige(neu), GRUEN, ROT)
        elif art == "neu":
            inhalt = f'<font color="{GRUEN}"><u>{_zeige(neu, True)}</u></font>'
        else:
            inhalt = f'<font color="{ROT}"><strike>{_zeige(alt, True)}</strike></font>'
        ist_punkt = _zeige(neu or alt).startswith("• ")
        if ist_punkt and vorher == (info, ort):
            fl.append(Paragraph(inhalt, punkt))          # weitere Listenpunkte derselben Art: ohne neue Marke
            fl.append(Spacer(1, 1.2 * mm))
        else:
            fl.append(KeepTogether([Paragraph(e(info), klein), Paragraph(inhalt, punkt if ist_punkt else text),
                                    Spacer(1, 1.2 * mm if ist_punkt else 2.5 * mm)]))
        vorher = (info, ort) if ist_punkt else None
    if werte:
        fl.append(Paragraph("Werte", h2))
        for datei, abschnitt, name, a, b in werte:
            wo = datei if datei == "Stichwörter" else (f"{datei} · {abschnitt} · {{{name}}}" if abschnitt else f"{datei} · {{{name}}}")
            a_ = f'<font color="{ROT}"><strike>{e(a)}</strike></font>' if a not in (None, "") else "<i>(leer)</i>"
            b_ = f'<font color="{GRUEN}"><u>{e(b)}</u></font>' if b not in (None, "") else "<i>(leer)</i>"
            if a is None:
                a_ = "<i>(neu)</i>"
            if b is None:
                b_ = "<i>(entfernt)</i>"
            fl.append(KeepTogether([Paragraph(e(wo), klein), Paragraph(f"{a_}  ›  {b_}", text), Spacer(1, 2 * mm)]))

    def fuss(c, d):
        c.saveState(); c.setFont(schrift, 7.5); c.setFillColor(colors.HexColor(GRAU))
        c.drawString(18 * mm, 10 * mm, kopf["fuss"]); c.drawRightString(A4[0] - 18 * mm, 10 * mm, f"Seite {d.page}")
        c.restoreState()
    os.makedirs(os.path.dirname(ziel), exist_ok=True)
    SimpleDocTemplate(ziel, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm,
                      bottomMargin=18 * mm, title=kopf["titel"]).build(fl, onFirstPage=fuss, onLaterPages=fuss)
    return z


# --- Einstieg aus bauen.py -------------------------------------------------------
def _lies(p):
    try:
        return open(p, encoding="utf-8").read()
    except OSError:
        return ""


def _texte(wurzel, bk, geschichten_pfade):
    import geschichten as G
    g = {}
    for n, p in geschichten_pfade.items():
        _, _, zeilen = G.lies(p)
        g[n] = "\n".join(z for _, z in zeilen)
    return {"buch": _lies(os.path.join(wurzel, bk.TEXT)), "geschichten": g,
            "variablen": _lies(os.path.join(wurzel, bk.VARIABLEN)) if bk.VARIABLEN else "",
            "umschlag": _lies(os.path.join(wurzel, bk.UMSCHLAG)) if bk.UMSCHLAG else "",
            "stichworte": _lies(os.path.join(wurzel, bk.stichwort_datei())) if bk.stichwort_datei() else ""}


def _stand_geschichten(pfad):
    o = os.path.join(pfad, "geschichten")
    return {f[:-3]: os.path.join(o, f) for f in sorted(os.listdir(o)) if f.endswith(".md")} if os.path.isdir(o) else {}


def befehl(base, bk, argumente):
    """argumente: [art, name1?, name2?] wie auf der Kommandozeile (Gross/klein erhalten)."""
    import geschichten as G
    art = argumente[0].lower()
    namen = argumente[1:]
    if art == "stand":
        if not namen:
            zeigen(base); return
        namen, bis = zeit_aus(namen)
        if not namen:
            raise SystemExit('Bitte einen Namen angeben, z. B.:  sh build.sh stand "Probedruck 1" 23.10.2026 15:00')
        name = " ".join(namen)
        dateien = [bk.TEXT, bk.VARIABLEN, bk.UMSCHLAG, bk.stichwort_datei()]
        if bis:                                   # nachträglich: Fassung aus md-history/
            quellen, gesch, zeit = aus_history(base, dateien, bis)
            ziel = speichern(base, name, quellen, gesch, bk.MOTOR_VERSION, zeit,
                             f"nachträglich aus md-history/ (neueste Fassung bis {bis:%d.%m.%Y %H:%M})")
            print(f"Stand «{name}» aus md-history/ festgehalten: Fassung vom {zeit:%d.%m.%Y %H:%M}")
            for d, q in quellen.items():
                print(f"  {d}  ←  md-history/{os.path.basename(q)}")
            if gesch:
                print(f"  dazu {len(gesch)} Geschichten")
        else:
            ziel = speichern(base, name, dateien, G.alle(base), bk.MOTOR_VERSION)
            print(f"Stand «{name}» festgehalten: {os.path.relpath(ziel, base)}/")
        print("$ sh build.sh aenderungen   (später: was sich seither geändert hat)")
        return
    # aenderungen
    p1, i1 = finde(base, namen[0] if namen else None)
    alt = _texte(p1, bk, _stand_geschichten(p1))
    if len(namen) > 1:
        p2, i2 = finde(base, namen[1])
        neu = _texte(p2, bk, _stand_geschichten(p2))
        jetzt = f"Stand «{i2['name']}» ({i2['datum']})"
    else:
        neu = _texte(base, bk, G.alle(base))
        jetzt = f"heute ({datetime.now():%d.%m.%Y %H:%M})"
    aend = vergleiche(absaetze(alt["buch"], alt["geschichten"]), absaetze(neu["buch"], neu["geschichten"]))
    werte = (werte_vergleich(alt["variablen"], neu["variablen"], "Variablen")
             + werte_vergleich(alt["umschlag"], neu["umschlag"], "Umschlag"))
    sa = {z.strip() for z in alt["stichworte"].split("\n") if z.strip() and not z.startswith("#")}
    sn = {z.strip() for z in neu["stichworte"].split("\n") if z.strip() and not z.startswith("#")}
    if sa and sn:                                 # Stichwort-Datei fehlt in einem Stand: nicht vergleichen
        werte += [("Stichwörter", "", "Stichwort", None, s) for s in sorted(sn - sa)]
        werte += [("Stichwörter", "", "Stichwort", s, None) for s in sorted(sa - sn)]
    vergleich = f"Seit Stand «{i1['name']}» ({i1['datum']}) bis {jetzt}"
    if not aend and not werte:
        print(f"Keine Änderungen. {vergleich}.")
        return
    g = bk.AUSGABEN["A"]
    ziel = os.path.join(base, g["ordner"], f"{g['datei']}_Aenderungen.pdf")
    z = pdf(ziel, {"titel": f"Änderungen – {bk.V('titel')}", "vergleich": vergleich,
                   "fuss": f"{bk.V('titel')} · Änderungen seit «{i1['name']}» · pureSATZ {bk.MOTOR_VERSION}"},
            aend, werte, bk.schrift("text"), bk.schrift("text_fett"), bk.hexfarbe("haupt"))
    print(vergleich)
    print(f"  {z['geaendert']} geändert · {z['neu']} neu · {z['gestrichen']} gestrichen"
          + (f" · {len(werte)} Werte" if werte else ""))
    orte = []
    for x in aend:
        if x[1] not in orte:
            orte.append(x[1])
    for o in orte:
        print(f"    {o or 'Anfang'}: {sum(1 for x in aend if x[1] == o)}")
    oeffnen = {"darwin": "open", "win32": 'start ""'}.get(sys.platform, "xdg-open")    # wie in bauen.py
    print(f'PDF: {oeffnen} "{os.path.relpath(ziel, base)}"')
