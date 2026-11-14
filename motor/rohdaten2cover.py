#!/usr/bin/env python3
"""
rohdaten2cover.py – Coverrechner-Text der Druckerei lesen und die Umschlagwerte oben in die Druckdatei schreiben (ab 2.82).

Unter «## Coverrechner (Rohdaten)» in druck/<datei>.md steht der Text aus dem Coverrechner (kopiert, wie er kommt).
Gesucht werden Rücken, Beschnitt/Einschlag, Gesamtbreite/-höhe, Vorderseite, Seitenzahl und Papier – egal, wie die
Druckerei sie nennt (tredition, epubli, BoD, KDP …) und ob in cm, mm oder Zoll. Daraus rechnet es den Deckel.

Läuft bei jedem Bau der Druckdateien von selbst (final, komplett, Menü w → co, sh build.sh covers):
  neue Rohdaten (anderer Text als beim letzten Mal) → Werte oben eintragen, für die Seitenzahl des Buchblocks
  gleicher Text, gleiche Seitenzahl                 → passt ({neu-berechnet}: ja)
  gleicher Text, andere Seitenzahl, keine/unlesbare Rohdaten → Werte bleiben, {neu-berechnet}: nein, ⚠ im Menü
Kopfzeilen, die es selbst setzt: {neu-berechnet}, {berechnet-fuer-seiten}, {berechnet-am} (mit Prüfsumme des Textes).
Alte Dateien mit {neu-berechnen} werden dabei umgestellt.

Von Hand:  python3 motor/rohdaten2cover.py druck/<datei>.md [Seiten]   (ohne Seiten: letzter Buchblock)
"""
import datetime
import glob
import hashlib
import os
import re
import shutil
import sys
import time

ROHKOPF = re.compile(r"^#+\s*.*(coverrechner|rohdaten)", re.I)
ZAHL = r"(\d+(?:[.,]\d+)?)"
EINHEIT = r"(mm|cm|in(?:ch(?:es)?)?\b|zoll|\")?"
# Was die Druckereien schreiben → Name hier (erster Fund zählt)
WOERTER = [
    ("format",  r"gesamtformat|gesamtgr(?:ö|oe)(?:ss|ß)e|umschlag\s*gesamt|umschlaggr(?:ö|oe)(?:ss|ß)e|cover\s*size|full\s*cover(?:\s*size)?|gesamtma(?:ss|ß)e?"),
    ("breite",  r"gesamtbreite|umschlagbreite|cover\s*breite|total\s*width|full\s*cover\s*width|cover\s*width|breite\s*gesamt"),
    ("hoehe",   r"gesamth(?:ö|oe)he|umschlagh(?:ö|oe)he|cover\s*h(?:ö|oe)he|total\s*height|full\s*cover\s*height|cover\s*height|h(?:ö|oe)he\s*gesamt"),
    ("ruecken", r"buchr(?:ü|ue)cken(?:breite|st(?:ä|ae)rke)?|r(?:ü|ue)ckenbreite|r(?:ü|ue)ckenst(?:ä|ae)rke|r(?:ü|ue)cken|spine(?:\s*width)?"),
    ("beschnitt", r"beschnittrand|beschnitt|einschlag|bleed|wrap(?:\s*around)?|umschlag\s*rand"),
    ("vorne",   r"vorderseite|front\s*cover|front|buchdeckel|deckel"),
    ("seiten",  r"seitenzahl|seitenanzahl|anzahl\s*seiten|seiten|page\s*count|pages|umfang"),
]
STATUS, ALT = "neu-berechnet", "neu-berechnen"          # bis 2.81: {neu-berechnen} (wird umgestellt)
KOPF = (STATUS, "berechnet-fuer-seiten", "berechnet-am")
ERKL_STATUS = ("> {neu-berechnet}, {berechnet-fuer-seiten}, {berechnet-am}: setzt der Motor beim Bau der Druckdateien. "
               "nein = Seitenzahl geändert oder Rohdaten fehlen → Coverrechner rechnen, Text unten ersetzen.")
ERKL_ROH = "> Text aus dem Coverrechner der Druckerei hier einfügen (wie er kommt). Der Motor liest ihn beim Bau selbst."


def _mm(zahl, einheit, standard):
    z = float(zahl.replace(",", "."))
    e = (einheit or standard or "mm").lower()
    return z * 10 if e == "cm" else z * 25.4 if e.startswith(("in", "zoll", '"')) else z


def rohtext(text):
    """Zeilen des Abschnitts «## Coverrechner (Rohdaten)», ohne «>»-Zeilen."""
    zeilen, drin = [], False
    for z in text.split("\n"):
        if z.lstrip().startswith("#"):
            drin = bool(ROHKOPF.match(z.strip()))
            continue
        if drin and not z.lstrip().startswith(">"):
            zeilen.append(z)
    return zeilen


def lesen(zeilen):
    """Werte in mm (seiten als Zahl, papier als Text) aus den Rohdaten-Zeilen."""
    einheiten = re.findall(r"\d\s*(mm|cm)\b", " ".join(zeilen), re.I)
    standard = max(set(einheiten), key=einheiten.count).lower() if einheiten else "mm"
    w = {}
    teile = [s.strip() for z in zeilen for s in z.split("|")]
    for i, t in enumerate(teile):
        m = re.match(r"\s*(papier|paper)\s*[:=]\s*(.+)$", t, re.I)
        if m and "papier" not in w:
            w["papier"] = m.group(2).strip()
        for name, muster in WOERTER:
            if name in w:
                continue
            m = re.search(rf"(?<![a-zäöü])(?:{muster})(?![a-zäöü])", t, re.I)
            if not m:
                continue
            nach, vor = t[m.end():], t[:m.start()]
            if name == "seiten":
                s = re.match(r"\s*[:=]?\s*(\d+)\b", nach) or re.search(r"(\d+)\s*$", vor)
                if s and 4 <= int(s.group(1)) <= 2000:
                    w[name] = int(s.group(1))
                continue
            if name == "format":
                f = re.search(rf"{ZAHL}\s*{EINHEIT}\s*[x×]\s*{ZAHL}\s*{EINHEIT}", nach, re.I)
                if f:
                    e = f.group(4) or f.group(2)
                    w["format"] = (_mm(f.group(1), f.group(2) or e, standard), _mm(f.group(3), e, standard))
                continue
            v = (re.match(rf"\s*(?:[:=]|ist|is|beträgt|betraegt)?\s*{ZAHL}\s*{EINHEIT}(?![\d])", nach, re.I)
                 or re.search(rf"{ZAHL}\s*{EINHEIT}\s*$", vor, re.I))
            if not v and not nach.strip(" :") and i + 1 < len(teile):       # Wert auf der nächsten Zeile (tredition)
                v = re.fullmatch(rf"\s*{ZAHL}\s*{EINHEIT}\s*", teile[i + 1], re.I)
            if v:
                w[name] = _mm(v.group(1), v.group(2), standard)
    if "format" in w:
        w.setdefault("breite", w["format"][0])
        w.setdefault("hoehe", w["format"][1])
    return w


def rechnen(w, bindung="hardcover", seite=None):
    """Aus den gefundenen Werten: ruecken, beschnitt, deckel (b, h) … oder (None, Grund)."""
    R, B, GB, GH, V = (w.get(k) for k in ("ruecken", "beschnitt", "breite", "hoehe", "vorne"))
    if R is None:
        return None, "kein Rücken gefunden"
    if B is None and GB and V:
        B = (GB - R - 2 * V) / 2
    if B is None:
        return None, "kein Beschnitt/Einschlag gefunden"
    if not (GB and GH):
        return None, "keine Gesamtbreite/-höhe gefunden"
    db, dh = (GB - 2 * B - R) / 2, GH - 2 * B
    if not (50 < db < 400 and 50 < dh < 500 and 0 < R < 120 and 0 <= B < 40):
        return None, f"Werte unplausibel (Deckel {db:.1f} x {dh:.1f}, Rücken {R:.1f}, Beschnitt {B:.1f} mm)"
    if V and abs(V - db) > 0.6:
        return None, f"Vorderseite {V:g} mm passt nicht zu Gesamtbreite − Rücken − Beschnitt ({db:.1f} mm)"
    if seite:                                   # passt der Umschlag zum Buchformat (Seite b x h in mm)?
        sb, sh = seite
        if (bindung == "softcover" and (abs(db - sb) > 1.5 or abs(dh - sh) > 1.5)) or \
           (bindung != "softcover" and not (sb - 0.5 <= db <= sb + 15 and sh - 0.5 <= dh <= sh + 25)):
            return None, f"Deckel {db:.1f} x {dh:.1f} mm passt nicht zum Buchformat {sb:g} x {sh:g} mm (anderes Format gerechnet?)"
    return dict(ruecken=R, beschnitt=B, deckel=(db, dh), breite=GB, hoehe=GH, seiten=w.get("seiten"),
                papier=w.get("papier")), None


def zahl(x):
    return f"{round(x, 1):g}"


def kopf(text):
    """{name: wert} der Zeilen oben (vor den Rohdaten); {neu-berechnen} gilt als {neu-berechnet}."""
    w, roh = {}, False
    for z in text.split("\n"):
        if z.lstrip().startswith("#"):
            roh = bool(ROHKOPF.match(z.strip()))
        m = None if roh else re.match(r"^\{([a-z-]+)\}:[ \t]*(.*)$", z)
        if m:
            w.setdefault(STATUS if m.group(1) == ALT else m.group(1), m.group(2).strip())
    return w


def eintragen(text, neu):
    """«{name}:»-Zeilen oben ersetzen ({neu-berechnen} → {neu-berechnet}), Erklärungen von früher erneuern,
    fehlende Kopfzeilen unter {berechnet-fuer-seiten} bzw. unter dem Titel einfügen."""
    aus, roh, gesetzt = [], False, set()
    for z in text.split("\n"):
        if z.lstrip().startswith("#"):
            roh = bool(ROHKOPF.match(z.strip()))
        m = None if roh else re.match(r"^\{([a-z-]+)\}:", z)
        name = m and (STATUS if m.group(1) == ALT else m.group(1))
        if name in neu and name not in gesetzt:
            z = f"{{{name}}}: {neu[name]}"
            gesetzt.add(name)
        elif z.startswith(f"> {{{ALT}}}:"):
            z = ERKL_STATUS
        elif z.startswith("> {berechnet-fuer-seiten}:"):     # steht jetzt in ERKL_STATUS
            continue
        elif z.startswith(">") and ("«Coverwerte übernehmen»" in z or "Der Motor liest diesen Abschnitt nicht" in z):
            z = ERKL_ROH if roh else "> Neue Werte: Text des Coverrechners unten unter «## Coverrechner (Rohdaten)» einfügen."
        aus.append(z)
    fehlt = [f"{{{k}}}: {neu[k]}" for k in KOPF if k in neu and k not in gesetzt]
    if fehlt:
        i = next((k for n in ("berechnet-fuer-seiten", STATUS) for k, z in enumerate(aus) if z.startswith(f"{{{n}}}:")), None)
        if i is None:
            i = next((k for k, z in enumerate(aus) if z.startswith("# ")), -1)
            fehlt = ([""] if i >= 0 else []) + fehlt
        aus[i + 1:i + 1] = fehlt
    return "\n".join(aus)


def bindung_aus(text):
    m = re.search(r"^\{bindung\}:\s*(\w+)", text, re.M)
    return (m.group(1).lower() if m else "hardcover").replace("beide", "hardcover")


def pruefsumme(zeilen):
    return hashlib.sha1(" ".join(" ".join(zeilen).split()).encode()).hexdigest()[:6]


def sichern(pfad, zeit):
    """Druckdatei nach md-history/druck/<name>_JJJJMMTT-HH-MM-SS.md kopieren (wie die anderen MD)."""
    basis = os.path.dirname(os.path.dirname(os.path.abspath(pfad)))
    ziel = os.path.join(basis, "md-history", "druck")
    try:
        os.makedirs(ziel, exist_ok=True)
        stamm, endung = os.path.splitext(os.path.basename(pfad))
        shutil.copy2(pfad, os.path.join(ziel, f"{stamm}_{zeit:%Y%m%d-%H-%M-%S}{endung}"))
    except OSError:
        pass


def auto(pfad, seiten, seite=None, schreiben=True, jetzt=None):
    """Beim Bau der Druckdateien (seiten = Buchblock). Gibt (stufe, meldung):
    «neu» = Rohdaten übernommen · «passt» · «warnung» = Werte oben bleiben, Coverrechner nötig."""
    jetzt = jetzt or datetime.datetime.now()
    text = open(pfad, encoding="utf-8").read()
    oben = kopf(text)
    B = oben.get("berechnet-fuer-seiten", "")
    am = oben.get("berechnet-am", "")
    alt = am.split("#")[1].strip() if "#" in am else ""
    zeilen = rohtext(text)
    neu, werte = {}, None
    if not "".join(zeilen).strip():
        stufe, msg = (("passt", f"Coverwerte von Hand, für {B} Seiten") if B == str(seiten) else
                      ("warnung", f"Buchblock {seiten} Seiten, Umschlag für {B} – Coverrechner rechnen, Text unter "
                                  "«## Coverrechner (Rohdaten)» einfügen." if B else
                                  "keine Rohdaten – Coverrechner rechnen, Text unter «## Coverrechner (Rohdaten)» einfügen."))
    else:
        bindung = bindung_aus(text)
        werte, grund = rechnen(lesen(zeilen), bindung, seite)
        summe = pruefsumme(zeilen)
        if not werte:
            stufe, msg = "warnung", (f"Rohdaten {'nicht lesbar' if grund.startswith('kein') else 'passen nicht'} ({grund}). "
                                     "Werte oben bleiben. Den Rohdaten-Block einer KI geben («Rücken, Beschnitt/Einschlag "
                                     "und Deckel in mm») oder die Werte von Hand eintragen.")
        elif werte["seiten"] and werte["seiten"] != seiten:
            stufe, msg = "warnung", f"Rohdaten sind für {werte['seiten']} Seiten, der Buchblock hat {seiten} – Coverrechner neu rechnen."
        elif summe == alt:
            stufe, msg = (("passt", f"Coverwerte passen ({B} Seiten, berechnet {am.split('#')[0].strip()})") if B == str(seiten) else
                          ("warnung", f"Buchblock jetzt {seiten} Seiten, Rohdaten für {B} – Coverrechner neu rechnen und Text "
                                      "ersetzen (gleicher Text wie vorher? dann {berechnet-fuer-seiten} von Hand anpassen)."))
        else:
            fuer = B if (not alt and B and B != str(seiten) and not werte["seiten"]) else str(seiten)   # alte Datei: Rohdaten gehören zu B
            art = "softcover" if bindung == "softcover" else "hardcover"
            neu = {f"ruecken-{art}": zahl(werte["ruecken"]), f"beschnitt-{art}": zahl(werte["beschnitt"]),
                   "berechnet-fuer-seiten": fuer, "berechnet-am": f"{jetzt:%d.%m.%Y %H:%M} #{summe}"}
            if art == "hardcover":
                neu["deckel-hardcover"] = f"{zahl(werte['deckel'][0])}x{zahl(werte['deckel'][1])}"
            if werte["papier"] and "papier" in oben:
                neu["papier"] = werte["papier"]
            zeile = (f"Rücken {zahl(werte['ruecken'])} mm · Beschnitt {zahl(werte['beschnitt'])} mm"
                     + (f" · Deckel {neu['deckel-hardcover']} mm" if art == "hardcover" else "")
                     + f" · Umschlag {zahl(werte['breite'])} x {zahl(werte['hoehe'])} mm")
            wechsel = ", ".join(f"{k.split('-')[0]} {oben.get(k) or '–'} → {v}" for k, v in neu.items()
                                if k.startswith(("ruecken", "beschnitt", "deckel")) and oben.get(k, "") != v)
            if fuer != str(seiten):
                stufe, msg = "warnung", (f"Rohdaten gemerkt (für {fuer} Seiten): {zeile}. Buchblock jetzt {seiten} – "
                                         "Coverrechner neu rechnen und Text ersetzen.")
            else:
                stufe, msg = "neu", f"Rohdaten übernommen für {seiten} Seiten: {zeile}" + (f" ({wechsel})" if wechsel else "")
    neu[STATUS] = "nein" if stufe == "warnung" else "ja"
    neutext = eintragen(text, neu)
    if schreiben and neutext != text:
        sichern(pfad, jetzt)
        tmp = f"{pfad}.{os.getpid()}.tmp"           # ganz oder gar nicht: beide Fassungen bauen gleichzeitig
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(neutext)
        for versuch in range(5):                     # Windows: liest die andere Fassung gerade, kurz warten
            try:
                os.replace(tmp, pfad)
                break
            except PermissionError:
                time.sleep(0.3)
        else:
            os.remove(tmp)
            return "warnung", msg + " (Druckdatei gesperrt – nichts eingetragen, nochmals bauen)"
    return stufe, msg


def buchblock_seiten(pfad_druckdatei):
    """Für den Aufruf von Hand: Seiten des neuesten Buchblocks im Buchordner (sonst None)."""
    try:
        from pypdf import PdfReader
        basis = os.path.dirname(os.path.dirname(os.path.abspath(pfad_druckdatei)))
        pdfs = sorted(glob.glob(os.path.join(basis, "ausgabe-*", "*_Buchblock.pdf")), key=os.path.getmtime)
        return len(PdfReader(pdfs[-1]).pages) if pdfs else None
    except Exception:
        return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    p = sys.argv[1]
    s = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else buchblock_seiten(p)
    if not s:
        print("Seitenzahl des Buchblocks unbekannt – zuerst bauen (Menü w → co) oder Zahl angeben.")
        sys.exit(1)
    stufe, txt = auto(p, s)
    print(txt)
    sys.exit(2 if stufe == "warnung" else 0)
