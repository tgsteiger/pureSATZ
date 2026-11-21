#!/usr/bin/env python3
"""
umbenennen.py – Buch-MD auf die Schreibweise von pureSATZ 3.0 umstellen (alte Namen -> neue).

    python3 motor/umbenennen.py              zeigt, was sich ändern würde (Buch, Umschlag, Geschichten)
    python3 motor/umbenennen.py ja           schreibt es (vorher Sicherung nach md-history/)

Code-Blöcke (```) und `Code` bleiben unverändert. Das Buch sieht danach genau gleich aus.
"""
import datetime
import glob
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import manuskript as M                                          # noqa: E402

ALT = {"v2": "normal", "offiziell": "normal", "dc": "uz"}   # ganz alte Fassungsnamen (::: nur-dc, ::: dc …)
TAG = {"uz": "UC", "dc": "UC", "normal": "NORMAL", "v2": "NORMAL", "offiziell": "NORMAL", "ebook": "EBOOK",
       "druck": "PRINT", "bildschirm": "SCREEN"}
BEREICH = {"offen": "DRAFT", "offen-notiz": "NOTE", "platzhalter": "NOTE", "zusammen": "KEEP-TOGETHER",
           "zeitstrahl": "TIMELINE"}
TITELEI = {"TITEL": "TITLE", "IMPRESSUM": "IMPRINT", "HINWEIS": "NOTICE", "WIDMUNG": "DEDICATION",
           "INHALTSVERZEICHNIS": "CONTENTS", "STICHWORTE": "INDEX", "BILDERVERZEICHNIS": "LIST-PICTURES",
           "TABELLENVERZEICHNIS": "LIST-TABLES", "BILDNACHWEIS": "PICTURE-CREDITS", "RUECKSEITE": "BACK-COVER"}
VAR_NEU = {"logo-light": "zier-hell", "logo": "zier", "decorate-stil": "mitte-stil", "block-kopf": "kasten-kopf",
           "block-hinweis": "kasten-hinweis"}                     # neuer Name: alter Name
# Die alte Schreibweise (vor 3.0) kennt nur noch diese Datei: Blöcke «::: art[-fassung] Titel» … «:::»
TAGS = ("normal", "uz", "bildschirm", "druck", "ebook", "buch", "privatdruck")
ARTEN = ("nur", "mitte", "foto", "platzhalter", "offen-notiz", "offen", "zusammen", "widmung", "zeitstrahl", "uz")
FOTO_KOPF = re.compile(r"^#{1,6}\s+@FOTO(-[A-Za-z]+)?(?:\s+(.*))?$")   # «#### @FOTO Titel»
STIL = {"aufrecht": "UPRIGHT", "blau": "UPRIGHT-MAIN", "zitat": "ITALIC"}


def zahl(w, i):
    return w[i] if len(w) > i and re.fullmatch(r"\d+(?:[.,]\d+)?", w[i]) else None


def zeile(s, buch=True):
    """Eine Zeile (ohne Blöcke) alt -> neu. None = bleibt. Im Umschlag (buch=False) nur die Blöcke."""
    if not buch:
        return None
    m = re.match(r"^(\s*)(.*)$", s)
    ein, t = m.group(1), m.group(2).rstrip()
    k = re.match(r"^(#{1,6}\s+)?@([A-Z][A-Z-]*)(?:\s+(.*))?$", t)
    if t == "---":
        return ein + "@NEWPAGE"
    if t.startswith("> "):
        return ein + "@DECORATE " + t[2:]
    if t.startswith("~ "):
        return ein + "@ASIDE " + t[2:]
    if not k:
        return None
    kopf, name, rest = k.group(1) or "", k.group(2), (k.group(3) or "").strip()
    w = rest.split()
    mit = lambda n: ein + kopf + "@" + n + ((" " + rest) if rest else "")
    if name in TITELEI:
        return mit(TITELEI[name])
    if name == "KERNSATZ":
        return mit("DECORATE-PAGE")
    einfach = {"ZITAT-ZIER": "DECORATE", "ZITAT": "DECORATE-TEXT", "UNTEN": "DECORATE-TEXT-BOTTOM",
               "MOTTO": "DECORATE-PAGE", "KOPF": "HEADER", "QR-PAAR": "QR", "QR-FLUSS": "QR-RIGHT",
               "ZIER-LINIE": "DECORATE-LOGO", "UMBRUCH": "NEWPAGE", "UMBRUCH-RECHTS": "NEWPAGE-RIGHT",
               "SEITENMITTE": "PAGE-CENTER"}
    if name in einfach and not (name in ("ZIER-LINIE", "UMBRUCH", "UMBRUCH-RECHTS", "SEITENMITTE") and rest):
        return mit(einfach[name])
    if name in ("ABSTAND", "PLATZ") and (not w or zahl(w, 0)) and len(w) <= 1:
        return ein + ("@SPACER" if name == "ABSTAND" else "@NEWPAGE") + ("-" + w[0] if w else "")
    if name in ("ZIER", "LOTUS", "ZIER-UNTEN", "LOTUS-UNTEN", "ZIER-TRENNER", "LOTUS-TRENNER"):
        n = zahl(w, 0)
        uebrig = w[1:] if n else w
        art = name.split("-")[1] if "-" in name else ""
        if art == "UNTEN" and uebrig == ["mitte"]:
            ort, uebrig = "-REST", []
        else:
            ort = {"": "", "UNTEN": "-BOTTOM", "TRENNER": "-GAP"}[art]
        if uebrig:
            return None
        return ein + "@LOGO" + ("-" + n if n else "") + ort
    return None


def bloecke(zeilen, buch=True):
    """Ganze Datei: Blöcke «::: …» und Fotos umstellen, danach Zeilen; kurze Blöcke werden eine Zeile."""
    code = M.im_code(zeilen)
    out, i = [], 0
    while i < len(zeilen):
        s = zeilen[i]
        t = s.strip()
        if i in code:
            out.append(s); i += 1; continue
        fk = FOTO_KOPF.match(t)
        if fk:                                             # Foto: breite/fluss in den Namen
            ende = i + 1
            while ende < len(zeilen) and zeilen[ende].strip() and not zeilen[ende].lstrip().startswith(("#", ":::")):
                ende += 1
            teil, groesse, seite = [], "", ""
            for z in zeilen[i + 1:ende]:
                zz = z.strip()
                zz = zz[2:].strip() if zz[:2] in ("- ", "* ") else zz
                if re.match(r"^breite:\s*\d+(?:[.,]\d+)?\s*$", zz, re.I):
                    groesse = "-" + zz.split(":", 1)[1].strip()
                elif re.match(r"^fluss:\s*(rechts|links)\s*$", zz, re.I):
                    seite = "-RIGHT" if "rechts" in zz.lower() else "-LEFT"
                else:
                    teil.append(z)
            name = groesse + seite                         # Bauplan: Grösse vor dem Ort
            tag = (fk.group(1) or "")[1:].lower()
            if tag and tag not in TAG:
                out.append(s); i += 1; continue
            vor = (TAG[tag] + "-") if tag else ""
            kopf = t[:t.index("@")]
            out.append(kopf + "@" + vor + "PICTURE" + name + ((" " + fk.group(2)) if fk.group(2) else ""))
            out += teil
            i = ende
            continue
        if t.startswith(":::") and t != ":::":
            art, tag, titel = _art(t[3:])
            ende = next((j for j in range(i + 1, len(zeilen)) if zeilen[j].strip() == ":::"), None)
            neu_kopf = kopf_neu(art, tag, titel)
            if neu_kopf is None or ende is None:
                out.append(s); i += 1; continue
            inhalt = zeilen[i + 1:ende]
            kurz = kurzform(art, neu_kopf, inhalt) if buch else None
            if kurz:
                out += kurz
            else:
                out.append(neu_kopf)
                out += [zeile(z, buch) or z for z in inhalt]
                out.append("@END")
            i = ende + 1
            continue
        out.append(zeile(s, buch) or s)
        i += 1
    return out


def _art(kopf):
    """'foto-uz Titel' -> ('foto', 'uz', 'Titel'); versteht auch die ganz alten Fassungsnamen (dc, v2, offiziell)."""
    art, _, titel = kopf.strip().partition(" ")
    art = art.lower()
    b, _, t = art.rpartition("-")
    art = (b + "-" + ALT[t]) if b and t in ALT else ALT.get(art, art)
    tag = None
    if "-" in art:
        basis, _, t = art.rpartition("-")
        if t in TAGS and basis in ARTEN:
            art, tag = basis, t
    if art not in ARTEN:
        return None, None, titel
    return art, tag, titel.strip()


def kopf_neu(art, tag, titel):
    vor = (TAG[tag] + "-") if tag in TAG else ""
    if tag and tag not in TAG:
        return None
    w = titel.lower().split()
    if art == "nur" and tag in TAG and not titel:
        return "@" + TAG[tag]
    if art == "uz":
        return "@UC-BLOCK" + ((" " + titel) if titel else "")
    if art in BEREICH:
        return "@" + vor + BEREICH[art] + ((" " + titel) if titel else "")
    if art == "mitte":
        name = "DECORATE" + ("-ABOVE" if "oben" in w else "")
        if "fest" in w:
            n = zahl(w, w.index("fest") + 1)
            name += "-BOTTOM" + ("-" + n if n else "")
        else:
            name += "-REST"
        stil = next((STIL[x] for x in w if x in STIL), "")
        if any(x not in ("oben", "fest", "aufrecht", "blau", "zitat") and not re.fullmatch(r"\d+", x) for x in w):
            return None
        return "@" + vor + name + (("-" + stil) if stil and stil != "ITALIC" else "")
    return None


def kurzform(art, kopf, inhalt):
    """Ein Absatz in einem mitte-Block -> eine Zeile; eine einzelne Befehlszeile in «nur-…» -> @UC-BEFEHL."""
    z = [x for x in inhalt]
    while z and not z[-1].strip():
        z.pop()
    while z and not z[0].strip():
        z.pop(0)
    if not z or any(not x.strip() for x in z):
        return None
    if art == "mitte":
        if all(x.rstrip().endswith("\\") for x in z[:-1]) and not any(x.lstrip().startswith(("@", "#", ">", "~", "- ")) for x in z):
            return [kopf + " " + z[0].strip()] + [x.strip() for x in z[1:]]
        return None
    if art == "nur" and len(z) == 1:
        n = zeile(z[0]) or z[0]
        n = n.strip()
        if n.startswith("@") and not n.startswith(("@@", "@#")) and _neu(n):
            return [kopf + "-" + n[1:]]
    return None


def _neu(zeile):
    """Ist die Zeile ein gültiger Befehl der neuen Schreibweise?"""
    try:
        return M.befehl(zeile) is not None
    except M.Fehler:
        return False


def umstellen(text, buch=True):
    zeilen = text.split("\n")
    start = next((i + 1 for i, z in enumerate(zeilen) if M.ist_buchstart(z)), 0)
    return "\n".join(zeilen[:start] + bloecke(zeilen[start:], buch))


def variablen(text):
    """Variablen-Datei: alte Namen {zier} usw. -> neue (auch in den Erklärungen «> {zier}: …»), {name-dc} -> {name-uz}."""
    text = re.sub(r"\{([a-z][a-z0-9-]*)-dc\}", r"{\1-uz}", text)
    for neu, alt in sorted(VAR_NEU.items(), key=lambda x: -len(x[1])):
        text = re.sub(r"\{" + re.escape(alt) + r"(-[a-z-]+)?\}",
                      lambda m: "{" + neu + (m.group(1) or "") + "}" if not (m.group(1) or "").startswith("-hell")
                      or alt == "zier-hell" else m.group(0), text)
    return text


def dateien(basis):
    d = [p for p in glob.glob(os.path.join(basis, "*-buch.md")) + glob.glob(os.path.join(basis, "*-umschlag.md"))]
    d += sorted(glob.glob(os.path.join(basis, "geschichten", "*.md")))
    d += glob.glob(os.path.join(basis, "*-variablen.md"))
    return [p for p in d if os.path.basename(p) != "UEBERSICHT.md"]


def aenderungen(basis):
    """[(pfad, alt, neu, [diff-zeilen])] – nur Dateien, die sich ändern würden (für Menü und Befehl)."""
    import difflib
    out = []
    for p in dateien(basis):
        try:
            alt = open(p, encoding="utf-8").read()
        except OSError:
            continue
        neu = variablen(alt) if p.endswith("-variablen.md") else umstellen(alt, not p.endswith("-umschlag.md"))
        if neu != alt:
            diff = [d for d in difflib.unified_diff(alt.split("\n"), neu.split("\n"), lineterm="", n=0)
                    if d[:1] in "+-" and not d.startswith(("+++", "---"))]
            out.append((p, alt, neu, diff))
    return out


def schreiben(basis, liste):
    """Sicherung nach md-history/, dann die neue Fassung schreiben. Gibt die Anzahl geänderter Zeilen zurück."""
    zeit = datetime.datetime.now().strftime("%Y%m%d-%H-%M-%S")
    n = 0
    for p, alt, neu, diff in liste:
        ziel = os.path.join(basis, "md-history", os.path.splitext(os.path.relpath(p, basis))[0] + "_" + zeit + ".md")
        os.makedirs(os.path.dirname(ziel), exist_ok=True)
        shutil.copy2(p, ziel)
        open(p, "w", encoding="utf-8").write(neu)
        n += sum(1 for d in diff if d.startswith("-"))
    return n


def zeigen(basis, liste):
    try:
        for p, _, _, diff in liste:
            print(f"{os.path.relpath(p, basis)}: {sum(1 for d in diff if d.startswith('-'))} Zeilen")
            for d in diff:
                print("   " + d)
    except BrokenPipeError:
        pass


def main():
    basis = os.getcwd()
    liste = aenderungen(basis)
    if not liste:
        return print("Schon alles in der Schreibweise 3.0.")
    if len(sys.argv) > 1 and sys.argv[1] in ("ja", "j"):
        print(f"Umgestellt ({schreiben(basis, liste)} Zeilen). Sicherung in md-history/.")
    else:
        zeigen(basis, liste)
        print("Nichts geschrieben. Umstellen:  python3 motor/umbenennen.py ja  (oder im Menü: um)")


if __name__ == "__main__":
    main()
