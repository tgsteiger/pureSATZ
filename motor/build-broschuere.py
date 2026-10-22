"""
Druckdateien für epubli oder BoD erstellen: Buchblock (Innenteil) und Umschlag.
Aufruf (im Buchordner):  python3 motor/build-broschuere.py      (normale Ausgabe)
                         python3 motor/build-broschuere.py uz   (zweite Ausgabe)
Ergebnis: im Ordner der Ausgabe: <kurz>_Buchblock.pdf, Umschlag und Cover (PDF und JPG).
Alle Angaben stehen in der Variablen-Datei (format, bindung, ruecken, projekt, isbn-buch …) oder –
ab pureSATZ 2.19 – in einer Druckdatei pro Fassung (druck/…md, Variable «druck-normal» / «druck-uz»).
Die Werte der Druckdatei haben Vorrang. Test mit einer anderen Datei: sh build.sh final druck=<datei>
Benötigt: reportlab, Pillow, pypdfium2 für die JPG-Dateien (sonst poppler)
"""
import os
import sys
import shutil
import subprocess
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
os.environ["BUCH_DRUCKMODUS"] = "1"              # Druckangaben (druck/…md) gelten nur in diesem Prozess
import build as bk
import manuskript as M
try:                                            # Windows: «sh build.sh» in Meldungen als «.\build.bat»
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "."))
    import plattform
    plattform.windows_befehle()
except ImportError:
    pass
E = bk.E
bk.waehle(sys.argv[1] if len(sys.argv) > 1 else None)
bk.DRUCK = True
A = bk.AUSGABE
KUERZEL = bk.ausgabe().get("kuerzel", A)

PLATTFORM = bk.V("plattform", "epubli").strip().lower()   # "epubli" oder "bod"
# "veroeffentlichen" = Buch veröffentlichen (mit ISBN) / "privatdruck" = ohne ISBN
PROJEKT = bk.ausgabe()["epubli"]
ISBN = bk.V("isbn-buch")
EXTRA_SEITEN = bk.ausgabe()["extra_seiten"]       # zusätzliche Notizseiten
BINDUNG = bk.V("bindung", "hardcover").lower()     # hardcover, softcover oder beide
if BINDUNG not in ("hardcover", "softcover", "beide"):
    raise SystemExit(f"Unbekannte Bindung «{BINDUNG}». Möglich: hardcover, softcover, beide")
RUECKEN_SOFT = float(bk.V("ruecken-softcover") or (bk.V("ruecken") if BINDUNG == "softcover" else "") or 3)
RUECKEN_HART = float(bk.V("ruecken-hardcover") or (bk.V("ruecken") if BINDUNG != "softcover" else "") or 6)
RUECKEN_MM = RUECKEN_SOFT


def mm_wert(name, standard):
    """Zahl in mm aus der Variablen-Datei (Komma oder Punkt), sonst der Standard."""
    w = bk.V(name).replace(",", ".").replace("mm", "").strip()
    try:
        return float(w) if w else float(standard)
    except ValueError:
        raise SystemExit(f"Variable «{name}»: «{bk.V(name)}» ist keine Zahl (mm).")


def deckel():
    """Hardcover-Deckel in mm: Variable «deckel-hardcover: 157x228», sonst laut Format."""
    w = bk.V("deckel-hardcover").lower().replace("×", "x").replace(" ", "").replace("mm", "")
    if not w:
        return bk.FMT["deckel"]
    try:
        b, h = (float(x.replace(",", ".")) for x in w.split("x"))
        return (b, h)
    except ValueError:
        raise SystemExit(f"Variable «deckel-hardcover»: «{bk.V('deckel-hardcover')}» – Form: 157x228")


COVER_RAND_MM = mm_wert("beschnitt-softcover", 3)        # Beschnitt rund um den Softcover-Umschlag
HARDCOVER = dict(deckel=deckel(), ruecken=RUECKEN_HART, einschlag=mm_wert("beschnitt-hardcover", bk.EINSCHLAG_MM))
PAPIER = bk.V("papier")

PROFILE = {
    # Der Impressumstext (Verlag, Herstellung) steht in der Buch-MD unter @IMPRESSUM (::: nur-buch)
    "epubli": dict(beschnitt_mm=3, min_seiten=36, eigener_barcode=False),
    "bod":    dict(beschnitt_mm=5, min_seiten=0, eigener_barcode=True),
}
# ===========================================================================

if PLATTFORM not in PROFILE:
    raise SystemExit(f"Unbekannte Plattform «{PLATTFORM}». Möglich: " + ", ".join(PROFILE))
P = dict(PROFILE[PLATTFORM])
P["beschnitt_mm"] = mm_wert("beschnitt-buchblock", P["beschnitt_mm"])
bk.B = P["beschnitt_mm"] * mm
bk.EIGENER_BARCODE = P["eigener_barcode"]
bk.PRIVATDRUCK = PROJEKT == "privatdruck"
bk.ISBN = "" if bk.PRIVATDRUCK else ISBN  # leer = Platzhalter «ISBN folgt»

DRUCKDATEI = bk.druck_datei()
TEST = bool(os.environ.get("BUCH_DRUCK_DATEI"))      # «sh build.sh final druck=<datei>» = Testlauf
# Ausgabeordner: immer der Ordner der Fassung (egal welche Plattform); ein Testlauf nach ausgabe-test/<datei>/
OUT = os.path.join(bk.BASE, "ausgabe-test", os.path.splitext(os.path.basename(DRUCKDATEI))[0]) if TEST \
    else os.path.join(bk.BASE, bk.ausgabe()["ordner"])
os.makedirs(OUT, exist_ok=True)
if DRUCKDATEI:
    print(f"Druckangaben: {DRUCKDATEI}" + (f" (Test, Ordner {os.path.relpath(OUT, bk.BASE)}/)" if TEST else ""))
    shutil.copy(os.path.join(bk.BASE, DRUCKDATEI), os.path.join(OUT, os.path.basename(DRUCKDATEI)))
if tuple(bk.FMT["seite"]) != tuple(bk.GRUNDFORMAT["seite"]):
    print(f"Hinweis: Druckformat {bk.FMT['name']}" + ("" if " mm" in bk.FMT["name"] else
          f" ({bk.FMT['seite'][0]:g} x {bk.FMT['seite'][1]:g} mm)") + " weicht vom "
          f"Grundformat {bk.GRUNDFORMAT['name']} ab – Seitenzahlen im Druck anders als im Lese-PDF.")
BLOCK = os.path.join(OUT, KUERZEL + "_Buchblock.pdf")

# --- 1) Buchblock -----------------------------------------------------------
bk.build.auffuellen = 0
n = bk.build(BLOCK)
INHALT = n                      # Seiten mit Inhalt (vor dem Auffüllen)
# epubli druckt Strichcode/ISBN auf die letzte Inhaltsseite -> diese immer frei halten (Lotus-Seite)
ziel = max(n + (1 if not P["eigener_barcode"] else 0), P["min_seiten"])
ziel += EXTRA_SEITEN
if ziel % 2:
    ziel += 1
if ziel != n:
    bk.build.auffuellen = ziel - n
    n = bk.build(BLOCK)
print(f"Buchblock: {n} Seiten, {(bk.W + 2 * bk.B) / mm:.1f} x {(bk.H + 2 * bk.B) / mm:.1f} mm "
      f"(Seite + {P['beschnitt_mm']:g} mm Beschnitt rundum, nur Innenseiten)")

# Versatz (pureSATZ 2.22): ganzen Seiteninhalt verschieben, z. B. nach Messung am Probeexemplar.
# versatz-vertikal: + = nach oben · versatz-horizontal: + = nach aussen (rechte Seiten nach rechts, linke nach links)
VERSATZ_V, VERSATZ_H = mm_wert("versatz-vertikal", 0), mm_wert("versatz-horizontal", 0)
if VERSATZ_V or VERSATZ_H:
    from pypdf import PdfReader, PdfWriter, Transformation
    _r = PdfReader(BLOCK); _w = PdfWriter()
    for _nr, _s in enumerate(_r.pages, 1):
        _dx = VERSATZ_H * mm * (1 if _nr % 2 else -1)      # Seite 1 = rechte Seite, aussen = rechts
        _w.add_page(_s).add_transformation(Transformation().translate(_dx, VERSATZ_V * mm))   # erst kopieren, dann verschieben
    _w.add_metadata(_r.metadata or {})
    with open(BLOCK + ".tmp", "wb") as _f:
        _w.write(_f)
    os.replace(BLOCK + ".tmp", BLOCK)
    print(f"Versatz: Inhalt {VERSATZ_V:+g} mm vertikal (+ = nach oben), {VERSATZ_H:+g} mm horizontal (+ = nach aussen)"
          + (" – WARNUNG: mehr als der Beschnitt minus 2 mm, Hintergründe können Blitzer zeigen"
             if max(abs(VERSATZ_V), abs(VERSATZ_H)) > max(P["beschnitt_mm"] - 2, 0) else ""))

# --- 2) Umschlag --------------------------------------------------------------
W, H = bk.W, bk.H
R = COVER_RAND_MM * mm
bk.B = R                        # Hintergrund der Cover-Seiten bis an den Rand ziehen
doc = bk.Doc(os.path.join(OUT, "_tmp.pdf"))


def seite(pfad, zeichne):
    """Einzelne Cover-Seite (Vorder- oder Rückseite) mit Rand R als PDF."""
    c = canvas.Canvas(pfad, pagesize=(W + 2 * R, H + 2 * R))
    c.setFillColor(bk.CREAM); c.rect(0, 0, W + 2 * R, H + 2 * R, fill=1, stroke=0)
    c.saveState(); c.translate(R, R); zeichne(c, None); c.restoreState()
    c.showPage(); c.save()


def gesamt(pfad):
    """Ganzer Umschlag: Rand | Rückseite | Rücken | Vorderseite | Rand."""
    Rk = RUECKEN_MM * mm
    br, ho = 2 * W + Rk + 2 * R, H + 2 * R
    c = canvas.Canvas(pfad, pagesize=(br, ho))
    c.setFillColor(bk.CREAM); c.rect(0, 0, br, ho, fill=1, stroke=0)
    c.saveState(); c.translate(R, R); doc.backpage(c, None); c.restoreState()
    c.saveState(); c.translate(R + W + Rk, R); doc.cover(c, None); c.restoreState()
    if RUECKEN_MM >= 8:
        c.saveState(); c.translate(R + W + Rk / 2, R + H / 2); c.rotate(90)
        c.setFillColor(bk.BLAU); c.setFont(bk.schrift("titel"), 8)
        c.drawCentredString(0, -3, f"{VORNE('autor', E.AUTOR)} · {VORNE('titel', E.TITEL)}"); c.restoreState()
    c.showPage(); c.save()


FETT, KURSIV = bk.schrift("titel_fett"), bk.schrift("text_kursiv")


def VORNE(k, standard=""):
    """Angabe der Vorderseite aus der Umschlag-MD (Titel, Untertitel, Autor, Stempel)."""
    return M.eins(bk.umschlag().get("vorderseite", []), k, standard)


def buchruecken(c, cx, cy, ruecken_mm, laenge):
    """Buchrücken, von unten nach oben lesbar: [UNZENSIERT ·] Titel · Untertitel · Name.
    Schriftgrösse passend zur Rückenbreite; Teile, die keinen Platz haben, fallen weg."""
    gr = min(11, ruecken_mm * 1.5)            # 6 mm Rücken -> 9 pt
    teile = []
    if VORNE("stempel"):
        teile.append((VORNE("stempel"), FETT, bk.farbe("stempel"), gr * 0.85))
    teile.append((VORNE("titel", E.TITEL), FETT, bk.DEEP, gr))
    if VORNE("untertitel"):
        teile.append((VORNE("untertitel"), KURSIV, bk.SOFT, gr * 0.95))
    teile.append((VORNE("autor", E.AUTOR), bk.schrift("titel"), bk.INK, gr))
    luecke = 5 * mm
    def breite(tt):
        return sum(c.stringWidth(t, f, g) for t, f, _, g in tt) + luecke * (len(tt) - 1)
    while breite(teile) > laenge - 24 * mm and len(teile) > 2:
        teile = [t for t in teile if t[1] != KURSIV] if any(t[1] == KURSIV for t in teile) else teile[1:]
    c.saveState(); c.translate(cx, cy); c.rotate(90)
    x = -breite(teile) / 2; yb = -gr * 0.36
    for k, (t, f, farbe, g) in enumerate(teile):
        if k:
            c.setFillColor(bk.GOLD); c.circle(x - luecke / 2, yb + gr * 0.36, 0.7, fill=1, stroke=0)
        c.setFillColor(farbe); c.setFont(f, g); c.drawString(x, yb, t)
        x += c.stringWidth(t, f, g) + luecke
    c.restoreState()


def hardcover(pfad, m):
    """Hardcover-Umschlag nach epubli-Vorlage: Einschlag | Rückseite | Rücken | Vorderseite | Einschlag.
    Das A5-Motiv wird gleichmässig auf die etwas grösseren Buchdeckel vergrössert und mittig gesetzt."""
    dw, dh = m["deckel"][0] * mm, m["deckel"][1] * mm
    rk, e = m["ruecken"] * mm, m["einschlag"] * mm
    br, ho = 2 * dw + rk + 2 * e, dh + 2 * e
    s = min(dw / W, dh / H)
    c = canvas.Canvas(pfad, pagesize=(br, ho))
    c.setFillColor(bk.CREAM); c.rect(0, 0, br, ho, fill=1, stroke=0)
    for x0, zeichne in ((e, doc.backpage), (e + dw + rk, doc.cover)):
        c.saveState()
        c.translate(x0 + (dw - W * s) / 2, e + (dh - H * s) / 2); c.scale(s, s)
        zeichne(c, None)
        c.restoreState()
    if m["ruecken"] >= 5:
        buchruecken(c, e + dw + rk / 2, e + dh / 2, m["ruecken"], dh)
    c.showPage(); c.save()
    print(f"Hardcover-Umschlag: {round(br / mm, 1):g} x {round(ho / mm, 1):g} mm (Deckel {m['deckel'][0]:g} x {m['deckel'][1]:g}, "
          f"Rücken {m['ruecken']:g}, Beschnitt/Einschlag {m['einschlag']:g} mm)")


vorne = os.path.join(OUT, KUERZEL + "_Cover_Vorderseite.pdf")
hinten = os.path.join(OUT, KUERZEL + "_Cover_Rueckseite.pdf")
ganz = os.path.join(OUT, KUERZEL + "_Umschlag_gesamt.pdf")
seite(vorne, doc.cover)
seite(hinten, doc.backpage)
ganz = hc = None
if BINDUNG in ("softcover", "beide"):
    ganz = os.path.join(OUT, KUERZEL + "_Umschlag_Softcover.pdf")
    gesamt(ganz)
    print(f"Softcover-Umschlag: {(2 * W + RUECKEN_MM * mm + 2 * R) / mm:.1f} x {(H + 2 * R) / mm:.1f} mm "
          f"(Rücken {RUECKEN_MM:g} mm, Beschnitt {COVER_RAND_MM:g} mm)")
if BINDUNG in ("hardcover", "beide"):
    hc = os.path.join(OUT, KUERZEL + "_Umschlag_Hardcover.pdf")
    bk.B = 20 * mm   # Hintergrund grosszügig, damit er auch nach dem Vergrössern bis an den Rand reicht
    hardcover(hc, HARDCOVER)

print()
print(f"*** {KUERZEL}: {bk.FMT['name']}, {BINDUNG}" + (f", {PAPIER}" if PAPIER else "") + f", Buchblock {n} Seiten. Rücken "
      + ", ".join(x for x in (f"Softcover {RUECKEN_SOFT:g} mm" if ganz else "",
                              f"Hardcover {RUECKEN_HART:g} mm" if hc else "") if x) + ".")
print(f"*** Stimmt das mit dem {'BoD' if PLATTFORM == 'bod' else 'epubli'}-Coverrechner überein (Seitenzahl, Papier, Gesamtbreite, Gesamthöhe)? "
      f"Sonst in {DRUCKDATEI or 'der Variablen-Datei'} anpassen (ruecken-…, beschnitt-…, deckel-hardcover).")
print()

# epubli möchte das Cover als JPG (mind. 300 dpi)
import pdfwerkzeug
if pdfwerkzeug.verfuegbar():
    for pdf in [p for p in (vorne, hinten, ganz, hc) if p]:
        pdfwerkzeug.als_jpg(pdf, pdf[:-4] + ".jpg", dpi=400)
    print("Cover als JPG (400 dpi) erstellt (Vorderseite, Rückseite, Umschlag gesamt)")
else:
    print("Hinweis: " + pdfwerkzeug.HINWEIS)

def leere_seiten(pdf, bis):
    """Seiten ohne Text und ohne Bild innerhalb des Inhalts (z. B. durch @UMBRUCH-RECHTS oder Teil-Rückseiten)."""
    try:
        from pypdf import PdfReader
    except ImportError:
        return None
    leer = []
    for i, seite in enumerate(PdfReader(pdf).pages[:bis], 1):
        res = seite.get("/Resources") or {}
        hat_bild = bool(res.get("/XObject")) if hasattr(res, "get") else False
        zeilen = [z for z in (seite.extract_text() or "").split("\n") if z.strip()]
        # leer = kein Bild und höchstens Kopfzeile und Seitenzahl
        if not hat_bild and len(zeilen) <= 2 and sum(len(z) for z in zeilen) < 120:
            leer.append(i)
    return leer


# Seitenbilanz: Wie viele Seiten sind leer? (Hilfe zum Kürzen vor der Bestellung)
fuell = n - INHALT
innen = leere_seiten(BLOCK, INHALT)
print(f"*** Seitenbilanz {KUERZEL}: {INHALT} Seiten Inhalt + {fuell} Füllseite(n) = {n} Seiten Buchblock")
if fuell:
    teile = []
    if not P["eigener_barcode"]:
        teile.append("letzte Seite frei für den epubli-Strichcode")
    if EXTRA_SEITEN:
        teile.append(f"{EXTRA_SEITEN} Notizseite(n) laut «extra-seiten»")
    if INHALT + (0 if P["eigener_barcode"] else 1) < P["min_seiten"]:
        teile.append(f"Mindestumfang {P['min_seiten']} Seiten")
    teile.append("gerade Seitenzahl")
    print("    Füllseiten wegen: " + ", ".join(teile))
if innen:
    print(f"    Leere Seiten im Inhalt: {', '.join(map(str, innen))} (z. B. vor einer rechten Seite)")
ohne = INHALT + (0 if P["eigener_barcode"] else 1)
if ohne % 2 and ohne >= P["min_seiten"]:
    print(f"    Tipp: Mit einer Seite weniger Inhalt ({INHALT - 1}) fiele eine leere Füllseite weg.")

# Probedruck-Booklet (bauen.py final): Vorderseite + Buchblock + Rückseite, ohne Beschnitt, wie das Buch
if os.environ.get("BUCH_BOOKLET") == "druck":
    try:
        import booklet
        probe = os.path.join(OUT, KUERZEL + "_Probedruck_booklet.pdf")
        blaetter = booklet.erstelle([(vorne, COVER_RAND_MM), (BLOCK, P["beschnitt_mm"]), (hinten, COVER_RAND_MM)],
                                    probe, leise=True)
        alt = os.path.join(OUT, bk.ausgabe()["datei"] + "_booklet.pdf")     # Booklet aus dem Entwurf
        if os.path.exists(alt):
            os.remove(alt)
        extra = 4 * blaetter - (n + 2)
        print(f"Probedruck-Booklet: {os.path.relpath(probe, bk.BASE)} ({blaetter} Blätter A4, kurze Kante wenden"
              + (f"; {extra} Leerseite(n) nur im Booklet, damit es aufgeht)" if extra else ")"))
    except SystemExit as e:
        print(f"Hinweis: kein Probedruck-Booklet – {e}")

if not ISBN and not bk.PRIVATDRUCK:
    print("Hinweis: Noch keine ISBN eingetragen – im Impressum steht ein Platzhalter.")

if bk.ENTWURF:
    offen = sum(1 for z in bk.text_zeilen() if isinstance(z, tuple) and z[0] in ("PH", "OFFEN"))
    print(f"ENTWURF: {offen} offene Stellen und Notizen sichtbar. Für den Druck: sh build.sh final")
