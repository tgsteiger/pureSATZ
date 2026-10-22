"""
build.py – Bildschirm-PDF eines Buchs (pureSATZ).
Aufruf (im Buchordner):  python3 motor/build.py      -> normale Ausgabe
                         python3 motor/build.py uz   -> zweite Ausgabe (Unzensiert / Director's Cut)
Alles zum Buch steht in der Buch-MD (Variablen oben, dann der Text) und in <buch>-umschlag.md.
Das Aussehen (Schriften, Farben) steht in layout.py.
"""
import os
import re
import sys
try:                                            # Windows: «sh build.sh» in Meldungen als «.\build.bat»
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "."))
    import plattform
    plattform.windows_befehle()
except ImportError:
    pass
sys.dont_write_bytecode = True                # keine __pycache__-Ordner im Buchordner

MOTOR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(MOTOR)                 # Buchordner
sys.path.insert(0, MOTOR)                     # Motor-Module haben Vorrang (alte Skripte im Buchordner stören nicht)
import manuskript as M      # liest Variablen, Blöcke und Text aus der MD


def _layout():
    """layout.py aus dem Buchordner, sonst die Vorgabe aus motor/layout.py."""
    import importlib.util
    pfad = os.path.join(BASE, "layout.py")
    if not os.path.exists(pfad):
        pfad = os.path.join(MOTOR, "layout.py")
    spec = importlib.util.spec_from_file_location("layout", pfad)
    modul = importlib.util.module_from_spec(spec); spec.loader.exec_module(modul)
    sys.modules["layout"] = modul
    return modul


L = _layout()               # Aussehen
from reportlab.lib.pagesizes import A5, A4, B5
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
                                PageBreak, NextPageTemplate, Table, TableStyle, KeepTogether,
                                CondPageBreak, Flowable, ImageAndFlowables)
from reportlab.platypus.doctemplate import ActionFlowable
from reportlab.platypus.tableofcontents import TableOfContents, SimpleIndex
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing


# --- Buchdateien ---------------------------------------------------------------
#   Drei Dateien:  <name>-variablen.md, <name>-buch.md, <name>-umschlag.md
#   (früher: eine Buch-MD mit «# BUCHSTART» oder «---»-Block oben – geht weiterhin)
def _buchdateien():
    if os.environ.get("BUCH_MD"):
        t = os.environ["BUCH_MD"]
        return t, None, t[:-3] + "-umschlag.md"
    mds = sorted(f for f in os.listdir(BASE) if f.endswith(".md") and f.lower() != "readme.md")
    buch = [f for f in mds if f.endswith("-buch.md")]
    if len(buch) == 1:
        stamm = buch[0][:-8]
        var = stamm + "-variablen.md"
        if not os.path.exists(os.path.join(BASE, var)):
            raise SystemExit(f"Zu {buch[0]} fehlt die Datei {var}.")
        return buch[0], var, stamm + "-umschlag.md"
    if len(buch) > 1:
        raise SystemExit("Mehr als eine *-buch.md im Buchordner: " + ", ".join(buch))
    kand = []
    for f in mds:
        if f.endswith(("-umschlag.md", "-variablen.md")):
            continue
        with open(os.path.join(BASE, f), encoding="utf-8") as d:
            zeilen = d.read().split("\n")
        if (zeilen and zeilen[0].strip() == "---") or any(M.ist_buchstart(z) for z in zeilen):
            kand.append(f)
    if len(kand) != 1:
        raise SystemExit("Keine Buchdateien gefunden. Erwartet: <name>-variablen.md, <name>-buch.md, "
                         "<name>-umschlag.md. Gefunden: " + (", ".join(mds) or "keine"))
    return kand[0], None, kand[0][:-3] + "-umschlag.md"


TEXT, VARIABLEN, UMSCHLAG = _buchdateien()           # z. B. Mein-Buch-buch.md, …-variablen.md, …-umschlag.md
NAME = TEXT[:-8] if TEXT.endswith("-buch.md") else TEXT[:-3]   # technischer Buchname
if os.environ.get("BUCH_TEXT"):                      # Sammel-PDF der Geschichten (bauen.py geschichten)
    TEXT = os.environ["BUCH_TEXT"]


def _grundvariablen():
    """Variablen aus <name>-variablen.md, sonst aus dem Kopf der Buch-MD."""
    if VARIABLEN:
        return M.lies_variablen(os.path.join(BASE, VARIABLEN))[0]
    return M.lies(os.path.join(BASE, TEXT))[0]


# --- Druckangaben (pureSATZ 2.19) ----------------------------------------------
#   Pro Fassung eine Datei in druck/ (Variable «druck-normal: epubli-a5-normal», «druck-uz: …»).
#   Ihre Werte gelten nur für die Druckdateien (build-broschuere.py) und haben dort Vorrang vor der
#   Variablen-Datei. Ohne «druck»-Zeile bleibt alles wie bisher. Test: sh build.sh final druck=<datei>
DRUCK_NAMEN = ("plattform", "format", "seite", "bindung", "projekt", "ruecken", "ruecken-hardcover",
               "ruecken-softcover", "beschnitt-hardcover", "beschnitt-softcover", "beschnitt-buchblock",
               "deckel-hardcover", "papier", "extra-seiten", "isbn-buch", "barcode-position",
               "barcode-groesse", "barcode-bild", "versatz-vertikal", "versatz-horizontal")


def druckmodus():
    """True im Prozess, der die Druckdateien baut (build-broschuere.py setzt BUCH_DRUCKMODUS=1)."""
    return os.environ.get("BUCH_DRUCKMODUS") == "1"


def druck_datei(fassung=None):
    """Druckdatei der Fassung als Pfad relativ zum Buchordner (z. B. druck/epubli-a5-normal.md), sonst None.
    Vorrang hat «druck=<datei>» beim Aufruf (Umgebungsvariable BUCH_DRUCK_DATEI)."""
    w = os.environ.get("BUCH_DRUCK_DATEI", "").strip() or \
        M.Ausgabe(_grundvariablen(), fassung or FASSUNG)("druck").strip()
    if not w:
        return None
    w = w.replace("\\", "/")
    if not w.lower().endswith(".md"):
        w += ".md"
    return w if w.startswith("druck/") else "druck/" + w


def druck_variablen(fassung=None):
    """Variablen aus der Druckdatei der Fassung ({} ohne Druckdatei)."""
    d = druck_datei(fassung)
    if not d:
        return {}
    pfad = os.path.join(BASE, d)
    if not os.path.exists(pfad):
        raise SystemExit(f"Druckangaben: {d} fehlt. Name prüfen (Variable «druck-…» bzw. druck=…); "
                         "Musterdateien liegen in pureSATZ/vorlage/druck/.")
    return M.lies_variablen(pfad)[0]


def mit_druckangaben(v, fassung=None):
    """Variablen v, überlagert mit der Druckdatei der Fassung (deren Werte haben Vorrang)."""
    dv = druck_variablen(fassung)
    if not dv:
        return v
    f = fassung or FASSUNG
    v = dict(v)

    def zerlege(k):
        for t in ("normal", "uz", "dc"):
            if k.endswith("-" + t):
                return k[:-len(t) - 1], t
        return k, None
    for k in sorted(dv, key=lambda k: zerlege(k)[1] is not None):     # erst allgemein, dann «-normal»/«-uz»
        basis, tag = zerlege(k)
        if tag and (tag == "normal") != (f == "normal"):
            continue                                                  # gilt für die andere Fassung
        for x in (basis, basis + "-normal", basis + "-uz", basis + "-dc"):
            v.pop(x, None)
        v[basis] = dv[k]
    return v


def alle_variablen(fassung=None, druck=None):
    """Alle Variablen: aus <name>-variablen.md, sonst aus dem Kopf der Buch-MD.
    Beim Bau der Druckdateien (oder druck=True) mit den Druckangaben der Fassung überlagert."""
    v = _grundvariablen()
    if druck is None:
        druck = druckmodus()
    return mit_druckangaben(v, fassung) if druck else v


def stichwort_datei():
    """stichworte-<name>.txt (z. B. stichworte-MeinBuch.txt), sonst stichworte.txt. None = keine."""
    for f in (f"stichworte-{NAME}.txt", "stichworte.txt"):
        if os.path.exists(os.path.join(BASE, f)):
            return f
    return None


def stichwort_zeilen():
    """Stichwörter: stichworte-<name>.txt im Buchordner (eine Zeile pro Stichwort, # = Kommentar);
    sonst der Abschnitt «# STICHWORTE» der Variablen-Datei. Dazu «stichworte:» aus den Geschichten."""
    if stichwort_datei():
        z = open(os.path.join(BASE, stichwort_datei()), encoding="utf-8").read().split("\n")
    elif VARIABLEN:
        z = list(M.lies_variablen(os.path.join(BASE, VARIABLEN))[1])
    else:
        z = []
    try:
        import geschichten
        schon = {x.split("|")[0].strip().lower() for x in z if x.strip() and not x.strip().startswith("#")}
        z += [w for w in geschichten.stichworte(BASE) if w.lower() not in schon]
    except SystemExit:
        pass
    return z


def _fassung_aus_aufruf():
    a = [x.lower() for x in sys.argv[1:]]
    return "uz" if any(x in ("b", "dc", "uz", "unzensiert", "directors-cut", "v3uz") for x in a) else "normal"


FASSUNG = _fassung_aus_aufruf()      # "normal" oder "uz" (zweite Ausgabe)
AUSGABE = "B" if FASSUNG == "uz" else "A"
MEDIUM = None                        # None = bildschirm/druck automatisch, "ebook" setzt build-epub.py
DRUCK = False                        # True = Buchblock (wird von build-broschuere.py gesetzt)
PRIVATDRUCK = False


def medium():
    return MEDIUM or ("druck" if DRUCK else "bildschirm")


def var(fassung=None):
    """Variablen der MD für eine Ausgabe:  var()("titel")"""
    return M.Ausgabe(alle_variablen(fassung or FASSUNG), fassung or FASSUNG, medium(), PRIVATDRUCK)


def druck_V(name, standard="", fassung=None):
    """Wert für den Druck (mit Druckangaben), auch ausserhalb von build-broschuere.py (z. B. shop-angaben.txt)."""
    f = fassung or FASSUNG
    return M.Ausgabe(alle_variablen(f, druck=True), f, "druck", PRIVATDRUCK)(name, standard)


def V(name, standard="", fassung=None):
    return var(fassung)(name, standard)


def ja(name, standard="ja"):
    return V(name, standard).strip().lower() in ("ja", "true", "1", "yes")


def umschlag():
    """Abschnitte der Umschlag-MD (vorderseite, ruecken, rueckseite) für die aktuelle Ausgabe."""
    pfad = os.path.join(BASE, UMSCHLAG)
    return M.umschlag(pfad, var()) if os.path.exists(pfad) else {}


def zweite_ausgabe():
    w = V("zweite-ausgabe")
    if w:
        return w.lower() in ("ja", "true", "1")
    return any(k.endswith(("-uz", "-dc")) for k in alle_variablen())


class _Einstellungen:
    """Alte Namen (E.TITEL, E.JAHR …) lesen jetzt die Variablen der MD (titel, jahr …)."""
    STANDARD = {"SPRACHE": "de", "PLATTFORM": "epubli", "KASTEN_HINWEIS": "darf übersprungen werden",
                "WORT_INHALT": "Inhalt", "WORT_ZEITSTRAHL": "Zeitstrahl", "WORT_NOTIZEN": "Notizen",
                "WORT_STICHWORTE": "Stichwortverzeichnis", "WORT_BILDNACHWEIS": "Bildnachweis", "TRENNUNG": "de_CH", "STEMPEL": True,
                "STICHWORTE_DATEI": "stichworte.txt", "STICHWORTE_IM_ANHANG": False}

    def __getattr__(self, n):
        if n == "MANUSKRIPT": return TEXT
        if n == "ZWEITE_AUSGABE": return zweite_ausgabe()
        if n == "STICHWORTVERZEICHNIS": return ja("stichworte")
        if n == "KASTEN_KOPF": return V("kasten-kopf") or V("stempel", fassung="uz") or "UNZENSIERT"
        w = var().wert(n.lower().replace("_", "-"))
        if w not in (None, ""):
            return w
        if n in self.STANDARD:
            return self.STANDARD[n]
        return ""          # nicht gesetzt = leer


E = _Einstellungen()

MOTOR_VERSION = open(os.path.join(MOTOR, "VERSION")).read().strip() if os.path.exists(os.path.join(MOTOR, "VERSION")) else "?"


def finde(name, ordner=("bilder", "fotos", "")):
    """Datei im Buchordner suchen (bilder/, fotos/, Buchordner), sonst im Motor."""
    if not name:
        return None
    if os.path.isabs(name) and os.path.exists(name):
        return name
    for o in ordner:
        p = os.path.join(BASE, o, name)
        if os.path.exists(p):
            return p
    for o in ("bilder", "fonts", ""):
        p = os.path.join(MOTOR, o, name)
        if os.path.exists(p):
            return p
    return None


def je(wert, ausgabe=None):
    """Einstellung, die je Ausgabe verschieden sein kann: {"A": ..., "B": ...}."""
    if isinstance(wert, dict) and set(wert) <= {"A", "B"} and wert:
        return wert.get(ausgabe or AUSGABE, wert.get("A"))
    return wert


# --- Schriften (layout.py) ---------------------------------------------------
def _layout_aus_variablen():
    """Abschnitt «# LAYOUT» der Variablen: farbe-…, schrift-text, schrift-titel, schriftgroesse,
    zeilenabstand, blocksatz. Gesetzte Werte haben Vorrang vor layout.py."""
    v = alle_variablen()
    for k, w in v.items():
        if k.startswith("farbe-") and w:
            L.FARBEN[k[6:].replace("-", "_")] = w

    def familie(name, rollen):
        for rolle, (endung, ersatz) in rollen.items():
            datei = next((f"{name}-{e}.ttf" for e in (endung, ersatz, "Regular") if finde(f"{name}-{e}.ttf", ("fonts",))), None)
            if not datei:
                raise SystemExit(f"Schrift «{name}» nicht gefunden (Ordner fonts/ oder motor/fonts/, z. B. {name}-Regular.ttf)")
            L.SCHRIFTDATEIEN[f"{name}-{endung}"] = datei
            L.SCHRIFT[rolle] = f"{name}-{endung}"
    if v.get("schrift-text"):
        familie(v["schrift-text"], {"text": ("Regular", "Regular"), "text_fett": ("Bold", "Regular"),
                                    "text_kursiv": ("Italic", "Regular"), "text_fettkursiv": ("BoldItalic", "Bold")})
    if v.get("schrift-titel"):
        familie(v["schrift-titel"], {"titel": ("Medium", "Regular"), "titel_fett": ("Bold", "Regular"),
                                     "titel_leicht": ("Light", "Regular"), "titel_normal": ("Regular", "Regular")})
    for k, ziel in (("schriftgroesse", "groesse"), ("zeilenabstand", "zeilenabstand")):
        if v.get(k):
            L.TEXT[ziel] = float(v[k])
    if v.get("blocksatz"):
        L.TEXT["blocksatz"] = v["blocksatz"].lower() in ("ja", "true", "1")


_layout_aus_variablen()
for _name, _datei in L.SCHRIFTDATEIEN.items():
    _pfad = finde(_datei, ("fonts",))
    if not _pfad:
        raise SystemExit(f"Schrift nicht gefunden: {_datei} (Ordner fonts/ oder motor/fonts/)")
    pdfmetrics.registerFont(TTFont(_name, _pfad))
FT = dict(L.SCHRIFT)
pdfmetrics.registerFontFamily(FT["text"], normal=FT["text"], bold=FT["text_fett"],
                              italic=FT["text_kursiv"], boldItalic=FT["text_fettkursiv"])
# Nur eingebettete Schriften im PDF (2.21.1): Seiten und Grafiken (QR-Codes) starten mit der Buchschrift
# statt mit Helvetica/Times-Roman – sonst melden Druckereien «nicht eingebettete Schriften».
from reportlab import rl_config as _rl
from reportlab.graphics import shapes as _shapes
if FT.get("text") in pdfmetrics.getRegisteredFontNames():
    from reportlab.lib import styles as _st
    from reportlab.platypus import tables as _tb
    _rl.canvas_basefontname = FT["text"]
    _shapes.STATE_DEFAULTS["fontName"] = FT["text"]
    for _cls in (_st.ParagraphStyle, _st.ListStyle):          # Vorgaben für Absätze, Tabellen, Aufzählungszeichen
        for _k in ("fontName", "bulletFontName"):
            if _k in _cls.defaults:
                _cls.defaults[_k] = FT["text"]
    _tb.CellStyle.fontname = FT["text"]


def schrift(rolle):
    return FT.get(rolle, rolle)


# --- Farben (layout.py) --------------------------------------------------------
STANDARD_FARBEN = {"offen": "#FFF4C2", "offen_linie": "#D9A800", "kasten": "#EEF2F9", "linie": "#E3D8C4",
                   "platzhalter": "#C0392B", "stempel": "#A8322A"}


def farbe(n):
    if n is None:
        return None
    return colors.HexColor(L.FARBEN.get(n, STANDARD_FARBEN.get(n, n)))


def hexfarbe(n):
    return L.FARBEN.get(n, STANDARD_FARBEN.get(n, n))


def _luminanz(h):
    h = h.lstrip("#")
    k = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    k = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in k]
    return 0.2126 * k[0] + 0.7152 * k[1] + 0.0722 * k[2]


def kontrast(a, b):
    """Kontrastverhältnis zweier Farben (#RRGGBB) nach WCAG, z. B. 4.5 = 4,5:1."""
    la, lb = _luminanz(a), _luminanz(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def lesbare_farbe(farbe_, hintergruende, ziel=4.5):
    """Farbe abdunkeln (gleicher Farbton), bis Text auf allen Hintergründen den Kontrast «ziel» erreicht."""
    h = farbe_.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    for schritt in range(101):
        f = 1 - schritt / 100
        neu = "#{:02X}{:02X}{:02X}".format(round(r * f), round(g * f), round(b * f))
        if all(kontrast(neu, x) >= ziel for x in hintergruende):
            return neu
    return "#000000"


if __name__ == "__main__" and ja("bildschirm-dunkler", "nein"):   # nur Bildschirm-PDF: für Schwarz-weiss-Ausdrucke
    def _dunkler(hx, f):
        h = hexfarbe(hx).lstrip("#")
        return "#" + "".join(f"{int(int(h[i:i + 2], 16) * f):02X}" for i in (0, 2, 4))
    L.FARBEN = dict(L.FARBEN, leise=_dunkler("leise", 0.8), akzent=_dunkler("akzent", 0.86))
INK = farbe("text")
SOFT = farbe("leise")
GOLD = farbe("akzent")
CREAM = farbe("papier")
BLAU = farbe("haupt")
DEEP = BLAU
STEMPEL = "stempel" if getattr(E, "STEMPEL", True) else None
STEMPEL_FARBEN = {"stempel": farbe("stempel")}
# Verzierung (z. B. Lotusblüte) aus layout.py
# Verzierung («Zier»): Bild aus der Variable «zier» der MD, sonst aus layout.py
LOTUS = finde(V("zier") or L.VERZIERUNG["bild"])
LOTUS_HELL = finde(V("zier-hell") or V("zier") or L.VERZIERUNG.get("hell") or L.VERZIERUNG["bild"])
if not LOTUS or not LOTUS_HELL:
    raise SystemExit(f"Bild für die Verzierung nicht gefunden: {V('zier') or L.VERZIERUNG['bild']}")


def standardbild(name, hell=False):
    """Bild aus layout.py; das Standard-Verzierungsbild wird durch die Variable «zier» ersetzt."""
    if name in (L.VERZIERUNG.get("bild"), L.VERZIERUNG.get("hell"), "verzierung.png", "verzierung-hell.png"):
        return LOTUS_HELL if (hell or "hell" in name) else LOTUS
    return finde(name)


def _bild_laden(pfad, umwandeln=None):
    """Bild öffnen und die Datei SOFORT wieder schliessen (Windows sperrt offene Dateien).
    Ein paralleler Lauf kann eine Cache-Datei gerade ersetzen: dann kurz warten und nochmals versuchen."""
    import time
    from PIL import Image as _I
    for versuch in range(10):
        try:
            with _I.open(pfad) as im:
                if umwandeln:
                    return im.convert(umwandeln)        # convert() liest alles ein, Datei danach frei
                return im.size, im.mode
        except PermissionError:
            if versuch == 9:
                raise
            time.sleep(0.2 * (versuch + 1))


def bildgroesse(pfad):
    return _bild_laden(pfad)[0]


def seitenverhaeltnis(pfad):
    w, h = bildgroesse(pfad)
    return h / w


LOTUS_RATIO = seitenverhaeltnis(LOTUS)                       # Höhe / Breite


def _ersetzen(tmp, ziel):
    """Fertige Zwischendatei an ihren Platz. Unter Windows kann ein paralleler Lauf die Datei gerade lesen:
    dann gilt dessen (gleiche) Datei, die eigene Kopie wird verworfen."""
    try:
        os.replace(tmp, ziel)
    except PermissionError:
        if not os.path.exists(ziel):
            raise
        try:
            os.remove(tmp)
        except OSError:
            pass


def bild(pfad, hintergrund="weiss"):
    """Im Druck keine Transparenzen (epubli-Vorgabe): Bild auf seine Hintergrundfarbe setzen.
    Im Bildschirm-PDF wird das Original mit Transparenz verwendet."""
    if not DRUCK:
        return pfad
    from PIL import Image
    if _bild_laden(pfad)[1] not in ("RGBA", "LA", "P"):   # ohne Transparenz: Original nehmen
        return pfad
    if hintergrund == "weiss":
        farbe = (255, 255, 255)
    else:
        hx = hexfarbe("papier" if hintergrund == "creme" else hintergrund).lstrip("#")
        farbe = tuple(int(hx[i:i + 2], 16) for i in (0, 2, 4))
    ordner = os.path.join(BASE, "_druckbilder")
    os.makedirs(ordner, exist_ok=True)
    ziel = os.path.join(ordner, os.path.splitext(os.path.basename(pfad))[0] + "_" + hintergrund + ".png")
    if not os.path.exists(ziel) or os.path.getmtime(ziel) < os.path.getmtime(pfad):
        im = _bild_laden(pfad, "RGBA")
        flach = Image.new("RGB", im.size, farbe)
        flach.paste(im, mask=im.getchannel("A"))
        tmp = f"{ziel}.{os.getpid()}.tmp"     # erst fertig schreiben, dann umbenennen (parallele Läufe)
        flach.save(tmp, "PNG"); _ersetzen(tmp, ziel)
    return ziel


# --- Formate (Masse laut epubli, Hardcover-Deckel laut epubli-Coverrechner) -----------
#   seite = Buchseite (mm), deckel = Hardcover-Deckel (mm, Einschlag rundum 11 mm),
#   rand = innen, aussen, oben, unten (mm), text = Schriftgrösse, Zeilenabstand (pt)
FORMATE = {
    "a5":          dict(name="DIN A5 hoch", seite=(148, 210), deckel=(157, 228), rand=(18, 15, 18, 20), text=(10.2, 15.2)),
    "taschenbuch": dict(name="Taschenbuch", seite=(125, 190), deckel=(134, 208), rand=(16, 13, 16, 18), text=(9.8, 14.6)),
    "sachbuch":    dict(name="Sachbuch",    seite=(135, 205), deckel=(144, 223), rand=(17, 14, 17, 19), text=(10.0, 15.0)),
    "a4":          dict(name="DIN A4 hoch", seite=(210, 297), deckel=(219, 315), rand=(28, 22, 25, 25), text=(11.5, 17.0)),
    "quadrat":     dict(name="Quadrat",     seite=(205, 205), deckel=(214, 223), rand=(22, 18, 20, 22), text=(10.8, 16.0)),
}
EINSCHLAG_MM = 11


def _format(wert=None):
    f = ((wert if wert is not None else V("format")) or str(L.SEITE.get("format", "a5"))).strip().lower().replace(" ", "")
    f = {"a5hoch": "a5", "dina5": "a5", "a4hoch": "a4", "dina4": "a4", "tb": "taschenbuch"}.get(f, f)
    if f not in FORMATE:
        raise SystemExit(f"Unbekanntes Format «{f}». Möglich: " + ", ".join(FORMATE))
    return f


def masse_mm(wert, name="seite"):
    """«148 x 210» (mm, Komma oder Punkt, × oder x) -> (148.0, 210.0); leer -> None."""
    w = (wert or "").lower().replace("×", "x").replace("mm", "").replace(" ", "")
    if not w:
        return None
    try:
        b, h = (float(x.replace(",", ".")) for x in w.split("x"))
        return (b, h)
    except ValueError:
        raise SystemExit(f"Variable «{name}»: «{wert}» – Form: 148 x 210 (Breite x Höhe in mm)")


def format_angaben(wert_format, wert_seite=""):
    """(Formatname, Angaben) aus «format» und «seite». Mit «seite: 148 x 210» ein freies Format: Ränder und
    Schrift vom nächstliegenden Format, Deckel = Seite + 9 x 18 mm (wie bei epubli)."""
    seite = masse_mm(wert_seite)
    if not seite:
        f = _format(wert_format)
        return f, FORMATE[f]
    f = min(FORMATE, key=lambda k: abs(FORMATE[k]["seite"][0] - seite[0]) + abs(FORMATE[k]["seite"][1] - seite[1]))
    if tuple(FORMATE[f]["seite"]) == seite:
        return f, FORMATE[f]
    return f, dict(FORMATE[f], name=f"Eigenes Format {seite[0]:g} x {seite[1]:g} mm", seite=seite,
                   deckel=(seite[0] + 9, seite[1] + 18))


FORMAT, FMT = format_angaben(V("format"), V("seite"))
GRUNDFORMAT = format_angaben(M.Ausgabe(_grundvariablen(), FASSUNG)("format"))[1]   # ohne Druckangaben (Lese-PDF)
W, H = FMT["seite"][0] * mm, FMT["seite"][1] * mm
S = ((W * H) / (148 * mm * 210 * mm)) ** 0.5     # Grössenfaktor für Umschlag und Teil-Seiten (A5 = 1)
# ENTWURF = True : offene Stellen und Foto-Vorschläge werden als Kästen gezeigt.
# ENTWURF = False: sie verschwinden (für den Druck!). Fotos mit vorhandener Datei erscheinen immer.
ENTWURF = not (os.environ.get("BUCH_FINAL") == "1" or os.environ.get("LR_FINAL") == "1")


def waehle(arg=None):
    """Ausgabe wählen: normal (Standard) oder zweite Ausgabe («uz», «dc», «b», «unzensiert»)."""
    global AUSGABE, FASSUNG
    a = (arg or "A").lower()
    FASSUNG = "uz" if a in ("b", "dc", "uz", "unzensiert", "directors-cut", "v3uz") else "normal"
    AUSGABE = "B" if FASSUNG == "uz" else "A"
    if AUSGABE == "B" and not zweite_ausgabe():
        raise SystemExit("Es gibt keine zweite Ausgabe (Variable «zweite-ausgabe: nein» in der MD).")
    return AUSGABE


def unzensiert():
    return AUSGABE == "B"


class _Ausgaben(dict):
    """AUSGABEN["A"] / ["B"]: Angaben der normalen bzw. zweiten Ausgabe aus den Variablen der MD."""
    def __getitem__(self, k):
        f = "uz" if k == "B" else "normal"
        return dict(name=V("ausgabe-name", "Zweite Ausgabe" if f == "uz" else "Normale Ausgabe", f),
                    kuerzel=V("kurz", NAME + ("-UZ" if f == "uz" else ""), f),
                    ordner=V("ordner", "ausgabe-" + f, f),
                    untertitel=V("untertitel", "", f),
                    label=V("stempel", "", f),
                    datei=V("datei", NAME + ("_" + V("stempel", "zweite", f).replace(" ", "-") if f == "uz" else ""), f),
                    epubli=V("projekt", "privatdruck" if f == "uz" else "veroeffentlichen", f),
                    extra_seiten=int(V("extra-seiten", "0", f) or 0))


AUSGABEN = _Ausgaben()


def text_zeilen():
    """Zeilen der gewählten Ausgabe; Blöcke (Kasten, Foto, Mitte …) als Tupel (ART, titel, zeilen)."""
    return M.zeilen(os.path.join(BASE, TEXT), var(), entwurf=ENTWURF)


def foto_optionen(inhalt):
    """Zusatzoptionen eines Foto-Blocks: 'breite: 60' (mm) und 'fluss: rechts|links' (Text umfliesst)."""
    opt = {}
    for z in inhalt:
        t = z.strip()
        for k in ("breite", "fluss", "ausschnitt"):
            if t.lower().startswith(k + ":"):
                opt[k] = t[len(k) + 1:].strip().lower()
    return opt


def foto_info(inhalt):
    """Liest 'datei:' und 'text:' aus einem Foto-Block. Gibt (pfad oder None, bildtext, vorschlag)."""
    datei, text, vorschlag = "", "", []
    for z in inhalt:
        t = z.strip()
        if t.lower().startswith("datei:"):
            datei = t[6:].strip()
        elif t.lower().startswith("text:"):
            text = t[5:].strip()
        elif t.lower().startswith(("breite:", "fluss:", "quelle:", "alt:", "ausschnitt:")):
            pass
        elif t:
            vorschlag.append(t)
    pfad = finde(datei, ("fotos", "bilder")) or "" if datei else ""
    klein = verkleinert(pfad) if pfad and os.path.exists(pfad) else None
    if klein:
        r, opt = foto_format(), foto_optionen(inhalt)
        if r and opt.get("fluss") not in ("rechts", "links"):
            klein = zugeschnitten(klein, r, opt.get("ausschnitt", "mitte"))
    return klein, text, " ".join(vorschlag), datei


def foto_format():
    """Variable «foto-format»: 3:2, 4:3, 16:9, 1:1 (oder quadrat) → Breite/Höhe; leer = Fotos wie sie sind."""
    w = V("foto-format", "").strip().lower()
    if w in ("quadrat", "quadratisch"):
        return 1.0
    m = re.match(r"^(\d+(?:[.,]\d+)?)\s*[:/x]\s*(\d+(?:[.,]\d+)?)$", w)
    if not m:
        return None
    a, b = (float(x.replace(",", ".")) for x in m.groups())
    return a / b if a > 0 and b > 0 else None


def zugeschnitten(pfad, ratio, ausschnitt="mitte"):
    """Foto auf ein Seitenverhältnis zuschneiden (Zwischenspeicher _bildcache/). ausschnitt: mitte (Standard),
    oben/unten (bei Hochformat: was bleibt), links/rechts (bei Querformat)."""
    from PIL import Image as PImg
    a = (ausschnitt or "mitte").strip().lower()
    ziel = os.path.join(BASE, "_bildcache", f"{os.path.splitext(os.path.basename(pfad))[0]}_{ratio:.3f}_{a}.jpg")
    if not os.path.exists(ziel) or os.path.getmtime(ziel) < os.path.getmtime(pfad):
        im = _bild_laden(pfad, "RGB")
        w, h = im.size
        if w / h > ratio:                                   # zu breit: links/rechts wegschneiden
            nw = round(h * ratio); x = {"links": 0, "rechts": w - nw}.get(a, (w - nw) // 2)
            im = im.crop((x, 0, x + nw, h))
        elif w / h < ratio:                                 # zu hoch: oben/unten wegschneiden
            nh = round(w / ratio); y = {"oben": 0, "unten": h - nh}.get(a, (h - nh) // 2)
            im = im.crop((0, y, w, y + nh))
        tmp = f"{ziel}.{os.getpid()}.tmp"
        im.save(tmp, "JPEG", quality=90); _ersetzen(tmp, ziel)
    return ziel


def foto_hinweise():
    """Hinweise auf Fotos, die für ihre gedruckte Grösse zu wenig Pixel haben (300 dpi = Breite in mm × 12)."""
    try:
        from PIL import Image as PImg
    except ImportError:
        return
    gesehen, textbreite = set(), (W - IN - OUT) / mm
    fb = V("foto-breite", "").strip()
    for fassung in ("normal", "uz"):
        for z in M.zeilen(os.path.join(BASE, TEXT), var(fassung), entwurf=True):
            if not (isinstance(z, tuple) and z[0] == "FOTO"):
                continue
            datei = next((t.strip()[6:].strip() for t in z[2] if t.strip().lower().startswith("datei:")), "")
            pfad = finde(datei, ("fotos", "bilder")) if datei else None
            if not pfad or not os.path.exists(pfad) or datei in gesehen:
                continue
            gesehen.add(datei)
            opt = foto_optionen(z[2])
            try:
                px, py = bildgroesse(pfad)
            except Exception:
                continue
            b = opt.get("breite") or (fb if opt.get("fluss") not in ("rechts", "links") else "") or ""
            try:
                mmb = float(b.replace(",", ".")) if b else (45 if opt.get("fluss") in ("rechts", "links") else textbreite)
            except ValueError:
                mmb = textbreite
            r = foto_format() if opt.get("fluss") not in ("rechts", "links") else None
            if not opt.get("fluss") in ("rechts", "links"):
                mmb = min(mmb, textbreite, 75 * (r or px / py))      # höchstens 75 mm hoch
            if r:
                px = min(px, round(py * r))
            noetig = round(mmb * 12)
            if px < noetig * 0.66:
                print(f"Hinweis: fotos/{datei} hat {px} Pixel Breite, für {mmb:.0f} mm im Druck sind etwa "
                      f"{noetig} gut (darunter wird es unscharf).")


def foto_quelle(inhalt):
    """«quelle: Foto: Max Muster» aus einem Foto-Block (für den Bildnachweis)."""
    for z in inhalt:
        if z.strip().lower().startswith("quelle:"):
            return z.strip()[7:].strip()
    return ""


def foto_alt(inhalt):
    """«alt: Beschreibung» aus einem Foto-Block (für Vorlesegeräte im E-Book, Barrierefreiheit)."""
    for z in inhalt:
        if z.strip().lower().startswith("alt:"):
            return z.strip()[4:].strip()
    return ""


# --- Bildnachweis ---------------------------------------------------------------
# Fotos mit «quelle:» werden gesammelt; im Anhang entsteht die Seite «Bildnachweis»
# (an der Stelle von @BILDNACHWEIS, sonst automatisch vor dem Stichwortverzeichnis).
QUELLEN = []              # [(nr, bildtext, quelle)] des laufenden Durchlaufs
QUELLEN_SEITE = {}        # nr -> Seite (aus dem vorherigen Durchlauf)


class QuellenMarke(Flowable):
    """Unsichtbar: merkt sich, auf welcher Seite ein Foto mit Quelle steht."""
    def __init__(self, nr):
        super().__init__(); self.nr = nr
    def wrap(self, aw, ah):
        return 0, 0
    def draw(self):
        QUELLEN_SEITE[self.nr] = self.canv.getPageNumber()


def bildnachweis():
    if not QUELLEN:
        return []
    titel = E.WORT_BILDNACHWEIS or "Bildnachweis"
    p = Paragraph(titel, ZEIT_STIL); p._toc = (0, titel)
    st = ParagraphStyle("bn", parent=small, fontSize=8.8, leading=12.5, spaceAfter=4, leftIndent=12 * mm,
                        firstLineIndent=-12 * mm)
    zeilen = []
    for nr, text, quelle in QUELLEN:
        seite = QUELLEN_SEITE.get(nr)
        zeilen.append(Paragraph(f"S. {seite if seite else '–'}&nbsp;&nbsp;&nbsp;"
                                + (inline_einfach(text) + " – " if text else "") + inline_einfach(quelle), st))
    return [NextPageTemplate("body"), PageBreak(), p, Spacer(1, 4)] + zeilen


def verkleinert(pfad, maxpx=1800):
    """Grosse Fotos für das Buch auf max. 1800 px verkleinern (reicht für 300 dpi bei voller
    Satzbreite) und als JPG zwischenspeichern. Das hält PDFs klein und den Bau schnell."""
    from PIL import Image as PImg
    ordner = os.path.join(BASE, "_bildcache"); os.makedirs(ordner, exist_ok=True)
    ziel = os.path.join(ordner, os.path.splitext(os.path.basename(pfad))[0] + ".jpg")
    if not os.path.exists(ziel) or os.path.getmtime(ziel) < os.path.getmtime(pfad):
        im = _bild_laden(pfad, "RGB")
        im.thumbnail((maxpx, maxpx), PImg.LANCZOS)
        tmp = f"{ziel}.{os.getpid()}.tmp"
        im.save(tmp, "JPEG", quality=90); _ersetzen(tmp, ziel)
    return ziel


def ausgabe():
    return AUSGABEN[AUSGABE]


# --- Druckmodus (wird von build-broschuere.py gesetzt) -----------------------
B = 0                  # Beschnitt rundum in Punkten (BoD: 5 mm)
ISBN = ""              # z. B. "978-3-7597-0000-0"
IMPRESSUM_VERLAG = ""  # Verlags-/Druckangaben der Plattform
EIGENER_BARCODE = True # False bei epubli: epubli druckt den Strichcode selbst
# Ränder: aus layout.py, sonst passend zum Format
IN, OUT, TOP, BOT = (((L.SEITE.get(k) if L.SEITE.get(k) is not None else d) * mm)
                     for k, d in zip(("rand_innen", "rand_aussen", "rand_oben", "rand_unten"), FMT["rand"]))
TEXT_GROESSE = L.TEXT.get("groesse") or FMT["text"][0]
TEXT_ZEILE = L.TEXT.get("zeilenabstand") or FMT["text"][1]

try:                       # Silbentrennung, falls python3-pyphen installiert ist
    import pyphen  # noqa: F401
    TRENNUNG = getattr(E, "TRENNUNG", "de_CH")
except ImportError:
    TRENNUNG = None
def _stil(name, d, **k):
    """ParagraphStyle aus einem layout.py-Eintrag (schrift, groesse, zeilenabstand, farbe, abstand_*)."""
    a = dict(k)
    if "schrift" in d: a["fontName"] = schrift(d["schrift"])
    if "groesse" in d: a["fontSize"] = d["groesse"]
    if "zeilenabstand" in d: a["leading"] = d["zeilenabstand"]
    if "farbe" in d: a["textColor"] = farbe(d["farbe"])
    if "abstand_vor" in d: a["spaceBefore"] = d["abstand_vor"]
    if "abstand_nach" in d: a["spaceAfter"] = d["abstand_nach"]
    return ParagraphStyle(name, **a)


body = ParagraphStyle("body", fontName=schrift("text"), fontSize=TEXT_GROESSE, leading=TEXT_ZEILE,
                      textColor=farbe(L.TEXT["farbe"]),
                      alignment=TA_JUSTIFY if L.TEXT.get("blocksatz", True) else TA_LEFT,
                      spaceAfter=L.TEXT["abstand_nach"], hyphenationLang=TRENNUNG,
                      allowWidows=0, allowOrphans=0)
h2 = _stil("h2", L.KAPITEL, keepWithNext=1)
h3 = _stil("h3", L.ZWISCHENTITEL, keepWithNext=1)
quote = _stil("quote", L.ZITAT, alignment=TA_CENTER, spaceBefore=10, spaceAfter=12, leftIndent=8 * mm,
              rightIndent=8 * mm)
note = _stil("note", L.NOTIZ, parent=body, leftIndent=6 * mm, rightIndent=6 * mm, alignment=TA_LEFT)
bullet = ParagraphStyle("bullet", parent=body, leftIndent=5 * mm, bulletIndent=0,
                        alignment=TA_LEFT, spaceAfter=5)
bullet2 = ParagraphStyle("bullet2", parent=bullet, leftIndent=11 * mm, bulletIndent=6.5 * mm)
nummer = ParagraphStyle("nummer", parent=bullet, leftIndent=7 * mm, bulletIndent=5 * mm, bulletAnchor="end",
                        bulletFontName=schrift("text"), bulletFontSize=TEXT_GROESSE)
nummer2 = ParagraphStyle("nummer2", parent=nummer, leftIndent=13 * mm, bulletIndent=11 * mm)


# --- Listen: «- Punkt» und nummerierte Aufzählung «1. Punkt» (ab 2.16), Unterpunkte eingerückt ----------
LISTE = re.compile(r"^( *)(-|\d{1,3}\.)\s+(.*)$")


class Nummerierung:
    """Zählt «1.»-Punkte: die erste Zahl bestimmt den Start, danach wird hochgezählt (pro Ebene)."""
    def __init__(self):
        self.z = [None, None]

    def punkt(self, m):
        """m = LISTE-Treffer → (ebene 0/1, '-' oder Nummer, text)."""
        ebene = 1 if len(m.group(1)) >= 2 else 0
        if ebene == 0:
            self.z[1] = None
        if m.group(2) == "-":
            return ebene, "-", m.group(3)
        n = int(m.group(2)[:-1]) if self.z[ebene] is None else self.z[ebene] + 1
        self.z[ebene] = n
        return ebene, n, m.group(3)


class Liste:
    """Sammelt Listenpunkte; kurze nummerierte Aufzählungen (bis 6) werden nicht getrennt."""
    def __init__(self, stil=None):
        self.punkte, self.num, self.nummeriert, self.stil = [], Nummerierung(), False, stil or {}

    def punkt(self, m):
        ebene, art, text = self.num.punkt(m)
        if art == "-":
            st = self.stil.get("-", bullet) if ebene == 0 else bullet2
            self.punkte.append(Paragraph(inline(text), st, bulletText="•"))
        else:
            st = self.stil.get("1", nummer) if ebene == 0 else nummer2
            self.punkte.append(Paragraph(inline(text), st, bulletText=f"{art}."))
            self.nummeriert = True

    def ende(self):
        out = self.punkte
        if self.nummeriert and 1 < len(out) <= 6:
            out = [KeepTogether(out)]
        self.punkte, self.num, self.nummeriert = [], Nummerierung(), False
        return out


small = ParagraphStyle("small", parent=body, fontSize=8.8, leading=12.5, textColor=SOFT,
                       alignment=TA_LEFT)
toc1 = ParagraphStyle("toc1", fontName=schrift("titel"), fontSize=10, leading=14, textColor=DEEP,
                      spaceBefore=8)
toc2 = ParagraphStyle("toc2", fontName=schrift("text"), fontSize=9.3, leading=12.6, textColor=INK,
                      leftIndent=5 * mm)


# Trennstellen für lange Wörter, die sonst im Blocksatz grosse Lücken reissen.
# Nur im PDF wirksam (weiches Trennzeichen), die md bleibt unverändert.
def _trennstellen():
    """trennstellen.txt: pro Zeile ein Wort mit Trennstrichen, z. B. Welt-anschauung."""
    d = {}
    p = os.path.join(BASE, "trennstellen.txt")
    if os.path.exists(p):
        for z in open(p, encoding="utf-8"):
            z = z.split("#", 1)[0].strip()
            if "=" in z:            # Wort mit echtem Bindestrich: Emotionscode-Anwender = Emotions|code-Anwender
                a, b = (v.strip() for v in z.split("=", 1))
                d[a] = b.replace("|", "\xad")
            elif "-" in z:
                d[z.replace("-", "")] = z.replace("-", "\xad")
    for w in V("trennstellen").split(","):     # Variable in der MD: Welt|anschauung, Gerichts|verhandlung
        w = w.strip()
        if "|" in w:
            d[w.replace("|", "")] = w.replace("|", "\xad")
    return d


TRENNSTELLEN = _trennstellen()


# --- Stichwortverzeichnis -------------------------------------------------------
# stichworte.txt: eine Zeile pro Stichwort, Varianten mit | getrennt, # = Kommentar.
#   Trance Healing | Intuitives Trance Healing   erste Schreibweise erscheint, alle werden gesucht
#   Quelle = göttlichen Quelle | Urquelle        links vom = steht der Eintrag, gesucht wird nur rechts
#   Gott -> Quelle                               Verweis «Gott, siehe Quelle» (ohne Seitenzahl)
REGISTER = None          # SimpleIndex des laufenden Durchlaufs (None = kein Verzeichnis)
_STICHWORTE = None       # [(Eintrag, [kompilierte Muster]), ...]
_VERWEISE = []           # [(Wort, Ziel), ...]  -> «Wort, siehe Ziel»


class Register(SimpleIndex):
    """Stichwortverzeichnis mit zusätzlichen Verweisen («Gott, siehe Quelle»)."""
    def _getlastEntries(self, *a):
        eintraege = list((self._lastEntries or self._entries).items())
        eintraege += [(("%s, siehe %s" % (w, z),), set()) for w, z in _VERWEISE]
        return sorted(eintraege) or super()._getlastEntries()

    def _build(self, availWidth, availHeight):
        """Buchstaben-Überschrift fest mit dem ersten Eintrag verbinden (nie allein am Seitenende)."""
        super()._build(availWidth, availHeight)
        kopf = ParagraphStyle("regkopf", parent=body, fontName=schrift("titel"), fontSize=10,
                              leading=13, textColor=DEEP, spaceBefore=0, spaceAfter=0)
        zellen = [r[0] for r in self._flowable._cellvalues]
        neu, i = [], 0
        while i < len(zellen):
            if (i + 2 < len(zellen) and isinstance(zellen[i], Spacer)
                    and isinstance(zellen[i + 1], Paragraph) and isinstance(zellen[i + 2], Spacer)):
                gruppe = [Spacer(1, 7 if neu else 0), Paragraph(zellen[i + 1].text, kopf), Spacer(1, 2)]
                i += 3
                while i < len(zellen) and isinstance(zellen[i], Spacer):
                    i += 1
                if i < len(zellen):
                    gruppe.append(zellen[i]); i += 1
                neu.append([gruppe])
            else:
                neu.append([zellen[i]]); i += 1
        self._flowable = Table(neu, colWidths=[availWidth], style=self.tableStyle)


import reportlab.platypus.tableofcontents as _toc_modul
_seitenzahlen_orig = _toc_modul.drawPageNumbers


def _seitenzahlen(canvas, style, pages, *a, **k):
    if pages:                      # Verweise haben keine Seitenzahlen: keine Punkte zeichnen
        return _seitenzahlen_orig(canvas, style, pages, *a, **k)


_toc_modul.drawPageNumbers = _seitenzahlen


def stichworte():
    global _STICHWORTE
    if _STICHWORTE is None:
        _STICHWORTE = []
        _VERWEISE.clear()
        if getattr(E, "STICHWORTVERZEICHNIS", False):
            for z in stichwort_zeilen():
                z = z.split("#", 1)[0].strip()
                if not z:
                    continue
                if "->" in z:                                   # Verweis
                    wort, ziel = (v.strip() for v in z.split("->", 1))
                    if wort and ziel:
                        _VERWEISE.append((wort, ziel))
                    continue
                if "=" in z:                                    # Eintrag = Suchwörter
                    name, z = (v.strip() for v in z.split("=", 1))
                else:
                    name = None
                teile = [v.strip() for v in z.split("|") if v.strip()]
                if not teile:
                    continue
                muster = [re.compile(r"(?<![\wÄÖÜäöüß])" + re.escape(v) + r"(?![\wÄÖÜäöüß])")
                          for v in sorted(teile, key=len, reverse=True)]
                _STICHWORTE.append(((name or teile[0]).replace(",", " "), muster))
    return _STICHWORTE


IM_ANHANG = False        # Zeitstrahl und «::: seite»-Seiten: nicht ins Stichwortverzeichnis


def stichwort_marken(t):
    """Setzt vor die erste Fundstelle jedes Stichworts eine unsichtbare Registermarke."""
    if REGISTER is None or not stichworte() or (IM_ANHANG and not getattr(E, "STICHWORTE_IM_ANHANG", False)):
        return t
    teile = re.split(r"(<[^>]+>)", t)          # nur im Text suchen, nicht in Tags
    for eintrag, muster in stichworte():
        for i in range(0, len(teile), 2):
            treffer = None
            for m in muster:
                treffer = m.search(teile[i])
                if treffer:
                    break
            if treffer:
                marke = '<index item="%s"/>' % eintrag.replace('"', "")
                teile[i] = teile[i][:treffer.start()] + marke + teile[i][treffer.start():]
                # die Marke selbst nicht nochmals durchsuchen: Text in Tag + Rest aufteilen
                teile = re.split(r"(<[^>]+>)", "".join(teile))
                break
    return "".join(teile)


def stichwortverzeichnis():
    if REGISTER is None:
        return []
    wort = getattr(E, "WORT_STICHWORTE", "Stichwortverzeichnis")
    p = Paragraph(wort, ParagraphStyle("sv", parent=h2, spaceBefore=0))
    p._toc = (0, wort)
    return [PageBreak(), p, Spacer(1, 4), REGISTER]


def links(t):
    """Markdown-Link [Text](https://…) -> farbiger Link im PDF."""
    return re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)",
                  lambda m: f'<a href="{m.group(2)}" color="{hexfarbe("akzent")}">{m.group(1)}</a>', t)


def inline(t):
    t = re.sub(r"^(\d{1,3})\\\.", r"\1.", t)          # «3\. Mai» = keine Aufzählung, gedruckt «3. Mai»
    t = stichwort_marken(links(t))
    for wort, getrennt in TRENNSTELLEN.items():
        t = t.replace(wort, getrennt)
    t = re.sub(r"&(?!amp;|lt;|gt;|quot;|#)", "&amp;", t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    return t


class Ornament(Flowable):
    def __init__(self, width=40 * mm):
        super().__init__(); self.w = width
    def wrap(self, aw, ah):
        self.aw = aw; return aw, 14
    def draw(self):
        # goldene Linien links und rechts, kleine blaue Lotusblüte in der Mitte
        c = self.canv; x0 = (self.aw - self.w) / 2; cx = x0 + self.w / 2
        lw = 13; lh = lw * LOTUS_RATIO
        c.setStrokeColor(farbe(L.VERZIERUNG.get("linie", "akzent"))); c.setLineWidth(0.6)
        c.line(x0, 7, cx - lw / 2 - 4, 7); c.line(cx + lw / 2 + 4, 7, x0 + self.w, 7)
        c.drawImage(bild(LOTUS), cx - lw / 2, 7 - lh / 2, lw, lh, mask="auto")


class PartMarker(Flowable):
    """Steht oben auf der Teil-Seite und zeichnet Bild und Titel (Teil, Titel, Untertitel).
    Die Seitenvorlage «part» zeichnet nur den Hintergrund."""
    def __init__(self, num, title, sub, bild_=None):
        super().__init__(); self.num, self.title, self.sub, self.bild = num, title, sub, bild_
    def wrap(self, aw, ah): return aw, 1
    def draw(self):
        c = self.canv
        T = L.TEIL
        def pos(yp):   # Seitenkoordinate -> Koordinate dieses Flowables (steht ganz oben im Rahmen)
            return yp - (H - TOP - 1)
        x = W / 2 - IN
        c.saveState()
        pfad = finde(self.bild) if self.bild else (standardbild(T.get("bild"), hell=True) if T.get("bild") else None)
        if pfad:
            lw = T.get("bild_breite", 72) * mm * S; lh = lw * seitenverhaeltnis(pfad)
            c.drawImage(bild(pfad, "creme"), x - lw / 2, pos(H * 0.50), lw, lh, mask="auto")
        c.setFillColor(farbe(T["nummer_farbe"])); c.setFont(schrift(T["nummer_schrift"]), T["nummer_groesse"] * S)
        c.drawCentredString(x, pos(H * 0.44), self.num.upper())
        c.setFillColor(farbe(T["titel_farbe"])); c.setFont(schrift(T["titel_schrift"]), T["titel_groesse"] * S)
        c.drawCentredString(x, pos(H * 0.44 - 38 * S), self.title)
        c.setStrokeColor(GOLD); c.setLineWidth(0.6)
        c.line(x - 12 * mm * S, pos(H * 0.44 - 54 * S), x + 12 * mm * S, pos(H * 0.44 - 54 * S))
        c.setFillColor(farbe(T["untertitel_farbe"])); c.setFont(schrift(T["untertitel_schrift"]), T["untertitel_groesse"] * S)
        c.drawCentredString(x, pos(H * 0.44 - 76 * S), self.sub)
        c.restoreState()


INHALT_STIL = ParagraphStyle("ih", parent=h2, fontSize=16, spaceBefore=0, spaceAfter=10)
ZEIT_STIL = ParagraphStyle("zh", parent=h2, spaceBefore=0)


def stempel(c, cx, cy, text, farbe, gr=15, winkel=14):
    """Schrägstehender Stempel mit doppeltem Rahmen und leicht unregelmässiger «Tinte»."""
    import random
    rnd = random.Random(7)
    c.saveState(); c.translate(cx, cy); c.rotate(winkel)
    tb = c.stringWidth(text, schrift("titel_fett"), gr) + 3 * len(text)
    bw, bh = tb + 9 * mm, gr + 7 * mm
    # Keine Transparenz (epubli-Vorgabe): Farbe mit 85 % Deckkraft auf dem Papier vorgemischt, deckend gezeichnet
    tinte = colors.Color(*[p + 0.85 * (f - p) for p, f in zip(CREAM.rgb(), farbe.rgb())])
    c.setStrokeColor(tinte); c.setFillColor(tinte)
    c.setLineWidth(1.6); c.roundRect(-bw / 2, -bh / 2, bw, bh, 2.5, stroke=1, fill=0)
    c.setLineWidth(0.6); c.roundRect(-bw / 2 + 1.6 * mm, -bh / 2 + 1.6 * mm, bw - 3.2 * mm, bh - 3.2 * mm, 1.5, stroke=1, fill=0)
    t = c.beginText(); t.setFont(schrift("titel_fett"), gr); t.setCharSpace(3)
    t.setTextOrigin(-tb / 2 + 1.5, -gr * 0.36); t.textOut(text); c.drawText(t)
    # Tinte nicht ganz deckend: kleine helle Sprenkel
    # deckend in Papierfarbe, etwas kleiner (wirkt wie früher 55 % Deckkraft, auf dem Papier unsichtbar)
    c.setFillColor(CREAM)
    for _ in range(140):
        x = rnd.uniform(-bw / 2, bw / 2); y = rnd.uniform(-bh / 2, bh / 2); r = rnd.uniform(0.15, 0.55) * 0.74
        c.circle(x, y, r, stroke=0, fill=1)
    c.restoreState()


class Doc(BaseDocTemplate):
    def __init__(self, fn):
        super().__init__(fn, pagesize=(W + 2 * B, H + 2 * B), title=E.TITEL + " – " + je(ausgabe()["untertitel"]),
                         author=E.AUTOR, subject=getattr(E, "PDF_THEMA", ""),
                         creator=f"{E.WEBSITE} · pureSATZ {MOTOR_VERSION}")
        self.part = None
        def frame_for(odd):
            l = IN if odd else OUT
            return Frame(l + B, BOT + B, W - IN - OUT, H - TOP - BOT, id="f", leftPadding=0,
                         rightPadding=0, topPadding=0, bottomPadding=0)
        full = Frame(B, B, W, H, id="full", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        # Folgeseiten des Inhaltsverzeichnisses beginnen auf derselben Höhe wie die Einträge auf Seite 1
        ih = Paragraph(getattr(E, "WORT_INHALT", "Inhalt"), INHALT_STIL).wrap(W - IN - OUT, H)[1] + INHALT_STIL.spaceAfter
        tocfolge = Frame(IN + B, BOT + B, W - IN - OUT, H - TOP - BOT - ih, id="f", leftPadding=0,
                         rightPadding=0, topPadding=0, bottomPadding=0)
        zh = Paragraph(getattr(E, "WORT_ZEITSTRAHL", "Zeitstrahl"), ZEIT_STIL).wrap(W - IN - OUT, H)[1] + ZEIT_STIL.spaceAfter
        zeitfolge = Frame(IN + B, BOT + B, W - IN - OUT, H - TOP - BOT - zh, id="f", leftPadding=0,
                          rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates([
            PageTemplate("cover", [full], onPage=self._b(self.cover)),
            PageTemplate("plain", [frame_for(True)], onPage=self._b(self.plain)),
            PageTemplate("part", [frame_for(True)], onPage=self._b(self.partpage)),
            PageTemplate("body", [frame_for(True)], onPage=self._b(self.bodypage),
                         onPageEnd=self._b(self.kopfzeile)),
            PageTemplate("back", [full], onPage=self._b(self.backpage)),
            PageTemplate("leer", [frame_for(True)], onPage=self._b(self.leerseite)),
            PageTemplate("notizen", [frame_for(True)], onPage=self._b(self.notizen)),
            PageTemplate("tocfolge", [tocfolge], onPage=self._b(self.bodypage)),
            PageTemplate("zeitfolge", [zeitfolge], onPage=self._b(self.bodypage),
                         onPageEnd=self._b(self.kopfzeile)),
        ])
        if DRUCK:  # im Buchblock beginnt das Buch mit der Titelei, nicht mit dem Umschlag
            self.pageTemplates.insert(0, self.pageTemplates.pop(1))

    def _b(self, fn):
        """Verschiebt alle Zeichnungen um den Beschnitt (im Bildschirm-PDF ist B = 0)."""
        def wrapped(c, d):
            c.saveState(); c.translate(B, B); fn(c, d); c.restoreState()
        return wrapped

    def notizen(self, c, d):
        """Notizseite mit feinen Linien (füllt den Druck auf die Mindestseitenzahl auf)."""
        c.saveState()
        c.setFillColor(DEEP); c.setFont(schrift("titel"), 13.5)
        c.drawString(IN, H - TOP - 14, getattr(E, "WORT_NOTIZEN", "Notizen"))
        c.setStrokeColor(farbe("linie")); c.setLineWidth(0.4)
        y = H - TOP - 40
        while y > BOT + 10:
            c.line(IN, y, W - OUT, y); y -= 9 * mm
        c.restoreState()
        self.footer(c, d, show_title=True)

    def leerseite(self, c, d):
        lw = 14 * mm; lh = lw * LOTUS_RATIO
        c.drawImage(bild(LOTUS_HELL), W / 2 - lw / 2, H / 2 - lh / 2, lw, lh, mask="auto")

    def afterFlowable(self, f):
        # Seitenausgleich: merken, auf welcher Seite und wie weit unten jedes Element landet
        i = getattr(f, "_lr", None)
        if i is not None and hasattr(self, "lr_info"):
            e = self.lr_info.setdefault(i, [self.page, self.page, 0, 0])
            e[1] = self.page; e[2] = self.frame._y; e[3] = self.frame._y1
            if e[0] > self.page: e[0] = self.page
        # Jeder Eintrag bekommt ein Sprungziel (key). Damit wird der Eintrag im
        # Inhaltsverzeichnis klickbar, und er erscheint als Lesezeichen in der PDF-Seitenleiste.
        if isinstance(f, Paragraph) and getattr(f, "_toc", None):
            lvl, text = f._toc
            self.link_entry(lvl, text)
        if isinstance(f, PartMarker):
            self.link_entry(0, f"{f.num} · {f.title}: {f.sub}")
            self.kopf = f.title; self.kap = None; self.zusatz = None
        if isinstance(f, Paragraph) and getattr(f, "_toc", None) and f._toc[0] == 0:
            self.kopf = f._toc[1]     # Vorwort, Zeitstrahl, Über den Autor …
            self.kap = None; self.zusatz = None
            self._kap_start = self._kap_seite = self._zusatz_start = None
        if isinstance(f, Paragraph) and getattr(f, "_toc", None) and f._toc[0] == 1:
            self.kap = f._toc[1]      # Kapitel für die Kopfzeile
            if self._kap_seite is None: self._kap_seite = self.kap
        if isinstance(f, KopfZusatz):
            self.zusatz = f.text or None

    def link_entry(self, lvl, text):
        self._n = getattr(self, "_n", 0) + 1
        key = f"ziel{self._n}"
        self.canv.bookmarkPage(key)
        # Lesezeichen-Ebene: Kapitel ohne übergeordneten Teil kommen auf Ebene 0
        olvl = lvl if (lvl == 0 or self._has_parent) else 0
        if lvl == 0:
            self._has_parent = True
        self.canv.addOutlineEntry(text, key, level=olvl, closed=False)
        self.notify("TOCEntry", (lvl, text, self.page, key))

    def handle_documentBegin(self):
        # wird bei jedem Durchlauf von multiBuild neu gesetzt
        if hasattr(self, "lr_info"): self.lr_info.clear()
        self.kopf = self.KOPF_STANDARD
        self.kap = self.zusatz = self._kap_start = self._kap_seite = self._zusatz_start = None
        self._n = 0
        self._has_parent = False
        super().handle_documentBegin()

    def cover(self, c, d):
        """Vorderseite: Texte aus der Umschlag-MD (# Vorderseite), Aussehen aus layout.py (UMSCHLAG)."""
        U = L.UMSCHLAG
        u = umschlag().get("vorderseite", [])
        c.saveState()
        if U.get("hintergrund"):
            c.setFillColor(farbe(U["hintergrund"])); c.rect(-B, -B, W + 2 * B, H + 2 * B, fill=1, stroke=0)
        pfad = finde(M.eins(u, "bild")) if M.eins(u, "bild") else (standardbild(U["bild"]) if U.get("bild") else None)
        if pfad:                    # grosses Bild oben (z. B. die Verzierung)
            lw = U.get("bild_breite", 52) * mm * S; lh = lw * seitenverhaeltnis(pfad)
            c.drawImage(bild(pfad, "creme"), W / 2 - lw / 2, H * 0.64 - lh / 2, lw, lh, mask="auto")
        y = H * 0.40
        c.setFillColor(farbe(U.get("titel_farbe", "haupt"))); c.setFont(schrift("titel"), U.get("titel_groesse", 24) * S)
        c.drawCentredString(W / 2, y, M.eins(u, "titel", E.TITEL))
        c.setFillColor(farbe(U.get("untertitel_farbe", "leise"))); c.setFont(schrift("text_kursiv"), U.get("untertitel_groesse", 12) * S)
        c.drawCentredString(W / 2, y - 22 * S, M.eins(u, "untertitel"))
        stempel_text = M.eins(u, "stempel")
        stempel_art = M.eins(u, "stempel-farbe", "rot").lower()
        if stempel_text and stempel_art in ("keine", "zeile", "gold"):   # feine Zeile über dem Titel
            c.setFillColor(GOLD); c.setFont(schrift("titel_leicht"), 10 * S)
            c.drawCentredString(W / 2, y + 26 * S, " ".join(stempel_text))
        c.setStrokeColor(GOLD); c.setLineWidth(0.6)
        c.line(W / 2 - 15 * mm * S, y - 38 * S, W / 2 + 15 * mm * S, y - 38 * S)
        c.setFillColor(farbe(U.get("autor_farbe", "text"))); c.setFont(schrift("titel_normal"), U.get("autor_groesse", 12) * S)
        c.drawCentredString(W / 2, y - 60 * S, M.eins(u, "autor", E.AUTOR))
        c.setFillColor(SOFT); c.setFont(schrift("titel_leicht"), 8.5 * S)
        fuss = M.alle(u, "fuss")
        for k, z in enumerate(fuss[:2]):
            c.drawCentredString(W / 2, ((16 - 5 * k) if len(fuss) > 1 else 11) * mm * S, z)
        if stempel_text and stempel_art not in ("keine", "zeile", "gold"):
            stempel(c, W / 2, y - 60 * S - 20 * mm * S, stempel_text, farbe("stempel"), gr=15 * S, winkel=8)
        c.restoreState()

    def backpage(self, c, d):
        """Rückseite: Texte aus der Umschlag-MD (# Rückseite): Slogan, rundes Foto, Texte, Auszüge, Fuss."""
        u = umschlag().get("rueckseite", [])
        c.saveState()
        if L.UMSCHLAG.get("hintergrund"):
            c.setFillColor(farbe(L.UMSCHLAG["hintergrund"])); c.rect(-B, -B, W + 2 * B, H + 2 * B, fill=1, stroke=0)
        x0 = 16 * mm * S; bw = W - 2 * x0
        def para(text, style, y):
            p = Paragraph(text, style); _, h = p.wrap(bw, H); p.drawOn(c, x0, y - h); return y - h
        slogan = ParagraphStyle("slo", fontName=schrift("titel"), fontSize=15 * S, leading=20 * S, textColor=BLAU, alignment=TA_CENTER)
        blurb = ParagraphStyle("blu", fontName=schrift("text"), fontSize=9.6 * S, leading=14 * S, textColor=INK, alignment=TA_CENTER)
        zitat = ParagraphStyle("zit", fontName=schrift("text_kursiv"), fontSize=9.6 * S, leading=13.5 * S, textColor=BLAU, alignment=TA_CENTER)
        y = H - 22 * mm * S
        for z in M.alle(u, "slogan"):
            y = para(z, slogan, y)
        foto_ = finde(M.eins(u, "foto")) if M.eins(u, "foto") else None
        if foto_:
            fs = 42 * mm * S; y -= 11 * mm * S + fs
            c.drawImage(bild(foto_, "creme"), W / 2 - fs / 2, y, fs, fs, mask="auto")
            c.setStrokeColor(BLAU); c.setLineWidth(1.1); c.circle(W / 2, y + fs / 2, fs / 2 + 2.5, stroke=1, fill=0)
        y -= 10 * mm * S
        for k, txt in enumerate(M.alle(u, "text")):
            if k: y -= 3 * S
            y = para(txt, blurb, y)
        zitate = M.alle(u, "auszug")
        if zitate:   # Auszüge zwischen zwei feinen Linien
            y -= 9 * mm * S
            c.setStrokeColor(GOLD); c.setLineWidth(0.6); c.line(W / 2 - 18 * mm * S, y, W / 2 + 18 * mm * S, y)
            y -= 4 * mm * S
            for z in zitate:
                y = para(z, zitat, y) - 3 * S
            y -= 2 * mm * S
            c.line(W / 2 - 18 * mm * S, y, W / 2 + 18 * mm * S, y)
        # Fuss: Verzierung + Name + Website
        fuss = M.alle(u, "fuss")
        lw = 13 * mm * S; lh = lw * LOTUS_RATIO
        if y < 19 * mm * S + lh + 4 * mm:
            print(f"WARNUNG: Text der Rückseite ist zu lang, bitte in {UMSCHLAG} kürzen.")
        feld = barcode_feld() if DRUCK else None
        if feld:   # Barcode-Feld aus den Druckangaben (barcode-position, -groesse, -bild; pureSATZ 2.19)
            fx, fy, fw, fh = feld["x"], feld["y"], feld["b"], feld["h"]
            if y < fy + fh + 3 * mm:
                print(f"WARNUNG: Text der Rückseite reicht ins Barcode-Feld ({feld['position']}, "
                      f"{fw / mm:g} x {fh / mm:g} mm), bitte in {UMSCHLAG} kürzen.")
            if feld["position"] == "links":      # Fuss rechtsbündig, Verzierung in der Mitte (wie epubli)
                xr = W - x0
                mitte = (13 * mm * S + 8.5 * mm * S + 0.7 * 9 * S) / 2
                c.drawImage(bild(LOTUS, "creme"), W / 2 - lw / 2, mitte - lh * leerer_rand_unten(LOTUS), lw, lh, mask="auto")
                c.setFillColor(SOFT); c.setFont(schrift("titel_leicht"), 8.5 * S)
                if fuss: c.drawRightString(xr, 13 * mm * S, fuss[0])
                c.setFillColor(BLAU); c.setFont(schrift("titel"), 9 * S)
                if len(fuss) > 1: c.drawRightString(xr, 8.5 * mm * S, fuss[1])
            else:                                # mitte oder rechts: Fuss und Verzierung links (wie BoD)
                c.drawImage(bild(LOTUS, "creme"), x0, 19 * mm * S, lw, lh, mask="auto")
                c.setFillColor(SOFT); c.setFont(schrift("titel_leicht"), 8.5 * S)
                if fuss: c.drawString(x0, 13 * mm * S, fuss[0])
                c.setFillColor(BLAU); c.setFont(schrift("titel"), 9 * S)
                if len(fuss) > 1: c.drawString(x0, 8.5 * mm * S, fuss[1])
            if feld["bild"]:                     # weisses Feld + Bild (z. B. Strichcode der Plattform als PNG)
                c.setFillColor(colors.white); c.rect(fx, fy, fw, fh, fill=1, stroke=0)
                c.drawImage(feld["bild"], fx, fy, fw, fh, mask="auto", preserveAspectRatio=True, anchor="c")
            elif EIGENER_BARCODE:                # Strichcode aus der ISBN (bzw. Platzhalter), in Feldgrösse
                c.saveState(); c.translate(fx, fy); c.scale(fw / (40 * mm), fh / (24 * mm))
                barcode(c, 0, 0); c.restoreState()
            c.restoreState(); return
        if DRUCK and EIGENER_BARCODE:  # BoD: Fuss links, rechts eigener ISBN-Strichcode
            c.drawImage(bild(LOTUS, "creme"), x0, 19 * mm * S, lw, lh, mask="auto")
            c.setFillColor(SOFT); c.setFont(schrift("titel_leicht"), 8.5 * S)
            if fuss: c.drawString(x0, 13 * mm * S, fuss[0])
            c.setFillColor(BLAU); c.setFont(schrift("titel"), 9 * S)
            if len(fuss) > 1: c.drawString(x0, 8.5 * mm * S, fuss[1])
            barcode(c, W - x0 - 40 * mm, 8 * mm)
            c.restoreState(); return
        if DRUCK:  # epubli setzt den Strichcode unten links -> Fuss rechtsbündig, links 60 x 35 mm frei
            xr = W - x0
            if y < 38 * mm:
                print(f"WARNUNG: Text der Rückseite reicht in den Platz für den epubli-Strichcode (unten links), "
                      f"bitte in {UMSCHLAG} kürzen.")
            # Lotus in der Seitenmitte: sichtbarer unterer Rand mittig zwischen grauer Zeile (Grundlinie)
            # und blauer Zeile (Oberkante Grossbuchstaben); leerer Rand im Bild wird herausgerechnet
            mitte = (13 * mm * S + 8.5 * mm * S + 0.7 * 9 * S) / 2
            c.drawImage(bild(LOTUS, "creme"), W / 2 - lw / 2, mitte - lh * leerer_rand_unten(LOTUS), lw, lh, mask="auto")
            c.setFillColor(SOFT); c.setFont(schrift("titel_leicht"), 8.5 * S)
            if fuss: c.drawRightString(xr, 13 * mm * S, fuss[0])
            c.setFillColor(BLAU); c.setFont(schrift("titel"), 9 * S)
            if len(fuss) > 1: c.drawRightString(xr, 8.5 * mm * S, fuss[1])
            c.restoreState(); return
        c.drawImage(bild(LOTUS, "creme"), W / 2 - lw / 2, 19 * mm * S, lw, lh, mask="auto")
        c.setFillColor(SOFT); c.setFont(schrift("titel_leicht"), 8.5 * S)
        if fuss: c.drawCentredString(W / 2, 13 * mm * S, fuss[0])
        c.setFillColor(BLAU); c.setFont(schrift("titel"), 9 * S)
        if len(fuss) > 1: c.drawCentredString(W / 2, 8.5 * mm * S, fuss[1])
        c.restoreState()

    def hintergrund(self, c):
        if L.SEITE.get("hintergrund"):
            c.saveState(); c.setFillColor(farbe(L.SEITE["hintergrund"]))
            c.rect(-B, -B, W + 2 * B, H + 2 * B, fill=1, stroke=0); c.restoreState()

    def plain(self, c, d):
        self.hintergrund(c)
        self.footer(c, d, show_title=False)

    def bodypage(self, c, d):
        self.hintergrund(c)
        self._kap_start, self._kap_seite, self._zusatz_start = self.kap, None, self.zusatz
        self.footer(c, d, show_title=False)

    KOPF_STANDARD = E.TITEL

    def kopfzeile(self, c, d):
        """Kopfzeile: «Autor · Teil · Kapitel» (Variable «kopfzeile»: ohne-autor, autor, wechselnd).
        Kapitel = das erste Kapitel, das auf der Seite beginnt, sonst das laufende.
        Ein @KOPF-Zusatz (z. B. «Ecuador») ersetzt das Kapitel, solange er die ganze Seite gilt."""
        teil = getattr(self, "kopf", self.KOPF_STANDARD)
        kap = self._kap_seite or self._kap_start
        if self._zusatz_start:
            kap = self._zusatz_start
        art = V("kopfzeile", "ohne-autor").strip().lower()   # ohne-autor (Standard) · autor · wechselnd
        if art == "wechselnd":   # links (gerade Seite) der Teil, rechts (ungerade) das Kapitel
            teile = [teil] if d.page % 2 == 0 else [kap or teil]
        else:
            teile = ([] if art == "ohne-autor" else [E.AUTOR]) + \
                    ([] if teil == self.KOPF_STANDARD and kap else [teil]) + ([kap] if kap else [])
        c.saveState()
        K = L.KOPFZEILE
        c.setFillColor(farbe(K["farbe"])); c.setFont(schrift(K["schrift"]), K["groesse"])
        c.drawCentredString(W / 2, H - 10 * mm, " · ".join(teile).replace("«", "").replace("»", ""))
        c.restoreState()

    def partpage(self, c, d):
        c.saveState()
        if L.TEIL.get("hintergrund"):
            c.setFillColor(farbe(L.TEIL["hintergrund"])); c.rect(-B, -B, W + 2 * B, H + 2 * B, fill=1, stroke=0)
        c.restoreState()

    def footer(self, c, d, show_title):
        c.saveState()
        K = L.KOPFZEILE
        c.setFillColor(farbe(K["farbe"])); c.setFont(schrift(K["schrift"]), K["groesse"])
        c.drawCentredString(W / 2, 10 * mm, str(d.page))
        if show_title:
            c.drawCentredString(W / 2, H - 10 * mm, f"{E.AUTOR} · {E.TITEL}")
        c.restoreState()


def leerer_rand_unten(pfad):
    """Anteil (0..1) der Bildhöhe, der unten durchsichtig oder weiss ist (für genaues Ausrichten)."""
    from PIL import Image
    with Image.open(pfad) as _f:
        im = _f.copy()                                     # Datei gleich wieder schliessen (Windows)
    if im.mode in ("RGBA", "LA", "P"):
        maske = im.convert("RGBA").getchannel("A").point(lambda v: 255 if v > 40 else 0)
    else:
        maske = im.convert("L").point(lambda v: 255 if v < 235 else 0)
    box = maske.getbbox()
    return (im.size[1] - box[3]) / im.size[1] if box else 0


def barcode_feld():
    """Barcode-Feld der Rückseite aus den Druckangaben, None = wie bisher (epubli links frei, BoD rechts).
    barcode-position: links | mitte | rechts · barcode-groesse: 40x20 (mm; leer = 60 x 35 frei ab der Ecke)
    barcode-bild: Datei aus bilder/ (leer = nichts zeichnen, Platz bleibt frei; BoD: Strichcode aus der ISBN)"""
    pos, gr, bd = (V(n).strip() for n in ("barcode-position", "barcode-groesse", "barcode-bild"))
    if not (pos or gr or bd):
        return None
    pos = (pos or "links").lower()
    if pos not in ("links", "mitte", "rechts"):
        raise SystemExit(f"Variable «barcode-position»: «{pos}» – möglich: links, mitte, rechts")
    masse = masse_mm(gr, "barcode-groesse")
    if masse:            # Feld mit Abstand zum Rand: seitlich wie der Text, unten 8 mm
        b, h, rand, unten = masse[0] * mm, masse[1] * mm, 16 * mm * S, 8 * mm
    else:                # wie bisher bei epubli: 60 x 35 mm ab der Ecke frei
        b, h, rand, unten = 60 * mm, 35 * mm, 0, 0
    x = {"links": rand, "mitte": (W - b) / 2, "rechts": W - rand - b}[pos]
    pfad = None
    if bd:
        pfad = finde(bd, ("bilder",))
        if not pfad or not os.path.exists(pfad):
            raise SystemExit(f"Variable «barcode-bild»: {bd} fehlt im Ordner bilder/.")
    return dict(position=pos, x=x, y=unten, b=b, h=h, bild=pfad)


def barcode(c, x, y):
    """ISBN als EAN-13-Strichcode auf weissem Feld (40 x 24 mm)."""
    from reportlab.graphics.barcode.eanbc import Ean13BarcodeWidget
    c.saveState()
    c.setFillColor(colors.white); c.rect(x, y, 40 * mm, 24 * mm, fill=1, stroke=0)
    digits = ISBN.replace("-", "").replace(" ", "")
    if len(digits) == 13:
        bc = Ean13BarcodeWidget(digits[:12]); bc.barHeight = 14 * mm; bc.fontName = schrift("titel"); bc.fontSize = 7
        b = bc.getBounds(); bw = b[2] - b[0]; sc = (34 * mm) / bw
        dr = Drawing(bw * sc, (b[3] - b[1]) * sc, transform=[sc, 0, 0, sc, 0, 0]); dr.add(bc)
        dr.drawOn(c, x + 3 * mm, y + 2 * mm)
        c.setFillColor(INK); c.setFont(schrift("titel"), 7)
        c.drawCentredString(x + 20 * mm, y + 20.5 * mm, "ISBN " + ISBN)
    else:
        c.setStrokeColor(SOFT); c.setDash(2, 2); c.rect(x, y, 40 * mm, 24 * mm, fill=0, stroke=1)
        c.setFillColor(SOFT); c.setFont(schrift("titel_leicht"), 7)
        c.drawCentredString(x + 20 * mm, y + 11 * mm, "Platz für ISBN-Strichcode")
    c.restoreState()


class SetPart(Flowable):
    def __init__(self, doc, p): super().__init__(); self.d, self.p = doc, p
    def wrap(self, aw, ah): return 0, 0
    def draw(self): self.d.part = self.p


# --- Unzensiert-Kasten ------------------------------------------------------
UZ_HG = farbe("kasten")
uz_kopf = ParagraphStyle("uzk", fontName=schrift("titel"), fontSize=7.2, leading=10, textColor=GOLD,
                         spaceAfter=3)
uz_titel = ParagraphStyle("uzt", fontName=schrift("titel"), fontSize=11, leading=15, textColor=DEEP)
uz_body = ParagraphStyle("uzb", parent=body, fontSize=9.6, leading=14.2, spaceAfter=0)
uz_note = ParagraphStyle("uzn", parent=uz_body, fontName=schrift("text_kursiv"), textColor=SOFT)
uz_bullet = ParagraphStyle("uzbl", parent=uz_body, leftIndent=5 * mm, alignment=TA_LEFT)
uz_nummer = ParagraphStyle("uznr", parent=uz_bullet, leftIndent=7 * mm, bulletIndent=5 * mm, bulletAnchor="end",
                           bulletFontName=uz_bullet.fontName, bulletFontSize=uz_bullet.fontSize)


def offen_kasten(zusatz, inhalt):
    """«::: offen»: Buchtext, über den noch nicht entschieden ist. Nur im Entwurf als gelber Kasten."""
    return uz_kasten("", inhalt, kopf_text="OFFEN", hinweis="noch nicht entschieden " + zusatz,
                     hg=farbe("offen"), linie=farbe("offen_linie"), stil=ParagraphStyle("ofb", parent=body, spaceAfter=0))


def uz_kasten(titel, inhalt, kopf_text=None, hinweis=None, hg=None, linie=None, stil=None):
    """Heller Kasten mit farbigem Rand links. Jede Zeile eine Tabellenzeile,
    damit der Kasten über Seitenumbrüche laufen kann."""
    # Kopfzeile (und Titel) werden Teil des ersten Absatzes: so kann der Kasten über
    # Seiten laufen, ohne dass der Kopf allein unten auf einer Seite stehen bleibt.
    uz_body_ = stil or uz_body
    if hinweis is None:
        hinweis = getattr(E, "KASTEN_HINWEIS", "")
    kopf_farbe = hexfarbe("offen_linie") if kopf_text == "OFFEN" else hexfarbe("akzent")
    kopf = (f"<font name='{schrift('titel')}' size='7.2' color='{kopf_farbe}'>{kopf_text or getattr(E, 'KASTEN_KOPF', 'UNZENSIERT')}</font> "
            + (f"<font name='{schrift('text_kursiv')}' size='7.2' color='{hexfarbe('leise')}'>· {hinweis.strip()}</font>" if hinweis.strip() else "")
            + "<br/>")
    if titel:
        kopf += f"<font name='{schrift('titel')}' size='11' color='{hexfarbe('haupt')}'>{inline(titel)}</font><br/>"
    rows = []
    para = []

    def fl():
        nonlocal kopf
        if para:
            rows.append([Paragraph(kopf + inline(" ".join(para)), uz_body_)]); para.clear()
            kopf = ""
    zahl = Nummerierung()
    for z in inhalt + [""]:
        t = z.strip()
        m = LISTE.match(t) if t else None
        if not t:
            fl()
        elif m:
            fl()
            if kopf:
                rows.append([Paragraph(kopf.rstrip("<br/>"), uz_body_)]); kopf = ""
            _, art, text = zahl.punkt(m)
            rows.append([Paragraph(inline(text), uz_bullet, bulletText="•") if art == "-" else
                         Paragraph(inline(text), uz_nummer, bulletText=f"{art}.")])
        elif t.startswith("~ "):
            fl()
            if kopf:
                rows.append([Paragraph(kopf.rstrip("<br/>"), uz_body_)]); kopf = ""
            rows.append([Paragraph(inline(t[2:]), uz_note)])
        else:
            para.append(t)
    try:                    # splitInRow gibt es erst ab reportlab 3.6.10
        tb = Table(rows, colWidths=[W - IN - OUT - 2], splitInRow=1)
    except TypeError:
        tb = Table(rows, colWidths=[W - IN - OUT - 2])
    tb.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), hg or UZ_HG),
        ("LINEBEFORE", (0, 0), (0, -1), 2, linie or GOLD),
        ("LEFTPADDING", (0, 0), (-1, -1), 4 * mm), ("RIGHTPADDING", (0, 0), (-1, -1), 4 * mm),
        ("TOPPADDING", (0, 0), (-1, -1), 2.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, 0), 3 * mm), ("BOTTOMPADDING", (0, -1), (-1, -1), 3 * mm),
    ]))
    return [CondPageBreak(28 * mm), Spacer(1, 4), tb, Spacer(1, 8)]


# --- Platzhalter und Fotos --------------------------------------------------
PH_FARBE = farbe("platzhalter")
ph_kopf = ParagraphStyle("phk", parent=uz_kopf, textColor=PH_FARBE)
ph_body = ParagraphStyle("phb", parent=uz_body, fontName=schrift("text_kursiv"), textColor=SOFT, alignment=TA_LEFT)
bildtext = ParagraphStyle("bt", parent=small, fontName=schrift("text_kursiv"), alignment=TA_CENTER, spaceBefore=3)


def gestrichelt(kopf, titel, text, hoehe=None):
    rows = [[[Paragraph(kopf, ph_kopf)] + ([Paragraph(inline(titel), uz_titel)] if titel else [])
             + [Paragraph(inline(text), ph_body)]]]
    tb = Table(rows, colWidths=[W - IN - OUT - 2], rowHeights=[hoehe] if hoehe else None)
    tb.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.8, PH_FARBE, None, (3, 2)),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE" if hoehe else "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4 * mm), ("RIGHTPADDING", (0, 0), (-1, -1), 4 * mm),
        ("TOPPADDING", (0, 0), (-1, -1), 3 * mm), ("BOTTOMPADDING", (0, 0), (-1, -1), 3 * mm),
    ]))
    return [Spacer(1, 4), KeepTogether([tb]), Spacer(1, 8)]


def platzhalter(titel, inhalt):
    text = " ".join(z.strip() for z in inhalt if z.strip())
    return gestrichelt(f"NOTIZ <font name='{schrift('text_kursiv')}' color='{hexfarbe('leise')}'>· wird nicht gedruckt</font>",
                       titel, text)


class MottoSeite(Flowable):
    """Ein Satz allein auf einer Seite, waagrecht und senkrecht zentriert, mit Lotus-Verzierung."""
    def __init__(self, text):
        super().__init__(); self.text = text

    def wrap(self, aw, ah):
        self.aw, self.ah = aw, ah
        self.p = Paragraph(self.text, ParagraphStyle("motto", parent=quote, fontSize=14, leading=20,
                                                      spaceBefore=0, spaceAfter=0))
        self.ph = self.p.wrap(aw, ah)[1]
        return aw, ah - 1

    def draw(self):
        o1, o2 = Ornament(), Ornament()
        oh = o1.wrap(self.aw, 30)[1]; o2.wrap(self.aw, 30)
        gap = 10
        gesamt = oh + gap + self.ph + gap + oh
        y = (self.ah - gesamt) / 2 + 12 * mm      # optisch etwas über der Mitte
        o2.drawOn(self.canv, 0, y)
        self.p.drawOn(self.canv, 0, y + oh + gap)
        o1.drawOn(self.canv, 0, y + oh + gap + self.ph + gap)


def mitte(titel, inhalt):
    """Zentrierter Block zwischen zwei kleinen Lotusblüten (z. B. der Dank am Schluss)."""
    st = ParagraphStyle("mitte", parent=body, alignment=TA_CENTER, spaceAfter=7)
    teile, para = [Spacer(1, 10), Ornament(), Spacer(1, 8)], []
    for z in inhalt + [""]:
        if z.strip():
            para.append(z.strip())
        elif para:
            teile.append(Paragraph(inline(" ".join(para)), st)); para = []
    teile += [Spacer(1, 4), Ornament(), Spacer(1, 6)]
    return [MitteBlock(teile)]


class MitteBlock(Flowable):
    """Hält den Block zusammen und setzt ihn senkrecht in die Mitte des restlichen Platzes der Seite."""
    def __init__(self, teile):
        super().__init__(); self.teile = teile

    def wrap(self, aw, ah):
        self.aw = aw
        self.hs = [t.wrap(aw, ah)[1] + t.getSpaceAfter() for t in self.teile]
        self.h = sum(self.hs)
        if self.h > ah and isinstance(self.teile[0], Spacer) and isinstance(self.teile[-1], Spacer) \
                and self.h - self.hs[0] - self.hs[-1] <= ah:
            # knapp zu gross: äussere Abstände weglassen, damit der Block noch auf die Seite passt
            self.teile = self.teile[1:-1]; self.hs = self.hs[1:-1]; self.h = sum(self.hs)
        self.platz = ah if self.h <= ah else self.h
        return aw, self.platz - 0.5

    def split(self, aw, ah):
        self.wrap(aw, ah)
        if self.h > ah:
            return []          # passt nicht: ganzer Block auf die nächste Seite
        return [self]

    def draw(self):
        y = self.platz - 0.5 - (self.platz - self.h) / 2 + 8 * mm   # optisch leicht über der Mitte
        y = min(y, self.platz - 0.5)
        for t, h in zip(self.teile, self.hs):
            y -= h
            t.drawOn(self.canv, 0, y + t.getSpaceAfter())


class LotusUnten(Flowable):
    """@LOTUS-UNTEN: füllt den Rest der Seite und setzt eine Lotusblüte zentriert an den unteren Rand."""
    def __init__(self, breite):
        super().__init__(); self.b = breite
    def wrap(self, aw, ah):
        self.aw, self.ah = aw, ah
        return aw, ah - 0.5
    def split(self, aw, ah):
        return []
    def draw(self):
        h = self.b * LOTUS_RATIO
        if self.ah > h + 6 * mm:
            self.canv.drawImage(bild(LOTUS), (self.aw - self.b) / 2, 2 * mm, self.b, h, mask="auto")


class LotusTrenner(Flowable):
    """@LOTUS-TRENNER: Lotusblüte ohne Höhe; sie wird in den Abstand vor der folgenden Überschrift gezeichnet."""
    def __init__(self, breite):
        super().__init__(); self.b = breite
    def wrap(self, aw, ah):
        self.aw = aw; return aw, 0
    def draw(self):
        h = self.b * LOTUS_RATIO
        self.canv.drawImage(bild(LOTUS), (self.aw - self.b) / 2, -h / 2 - 2, self.b, h, mask="auto")


class BildMitText(Flowable):
    """Bild + Bildtext als ein Block, der von Text umflossen werden kann (für ImageAndFlowables)."""
    def __init__(self, teile, bw):
        super().__init__(); self.teile, self.bw = teile, bw

    def wrap(self, aw, ah):
        self.hs = [t.wrap(self.bw, ah)[1] for t in self.teile]
        return self.bw, sum(self.hs) + 2 * (len(self.teile) - 1)

    def _restrictSize(self, aw, ah):
        return self.wrap(aw, ah)

    def _unRestrictSize(self):      # von ImageAndFlowables beim erneuten Umbruch aufgerufen
        pass

    def draw(self):
        y = sum(self.hs) + 2 * (len(self.teile) - 1)
        for t, h in zip(self.teile, self.hs):
            y -= h
            t.drawOn(self.canv, 0, y)
            y -= 2


class FlexBild(Flowable):
    """Foto, das sich dem Platz auf der Seite anpasst: Ist unten noch Platz für mindestens
    45 mm Bildhöhe, wird es so weit verkleinert, dass es noch auf die Seite passt.
    So beginnt eine Seite seltener mit einem Foto und es entstehen keine grossen Lücken."""
    MAXH, MINH = 75 * mm, 38 * mm

    def __init__(self, pfad, ratio, text, maxw=None, anpassen=True):
        super().__init__(); self.pfad, self.ratio, self.text, self.maxw, self.anpassen = pfad, ratio, text, maxw, anpassen

    def wrap(self, aw, ah):
        self.cap = Paragraph(inline(self.text), bildtext) if self.text else None
        ch = self.cap.wrap(aw, ah)[1] + 3 if self.cap else 0
        h = min(self.MAXH, min(aw, self.maxw or aw) / self.ratio)
        if self.anpassen and ah - ch < h and ah - ch >= self.MINH:
            h = ah - ch - 1
        self.ih, self.iw, self.ch, self.aw = h, h * self.ratio, ch, aw
        return aw, h + ch

    def draw(self):
        x = (self.aw - self.iw) / 2
        self.canv.drawImage(self.pfad, x, self.ch, self.iw, self.ih)
        if self.cap:
            self.cap.drawOn(self.canv, 0, 0)


def foto(titel, inhalt):
    from reportlab.platypus import Image as Image_
    pfad, text, vorschlag, datei = foto_info(inhalt)
    if pfad:
        from PIL import Image as PImg
        w, h = bildgroesse(pfad)
        maxw, maxh = W - IN - OUT, 75 * mm
        opt = foto_optionen(inhalt)
        breite = float(opt["breite"]) * mm if opt.get("breite") else None
        if opt.get("fluss") in ("rechts", "links"):
            # Bild mit Bildtext als kleiner Block; die folgenden Absätze umfliessen es
            bw = breite or 45 * mm
            teile = [Image_(bild(pfad), bw, bw * h / w)]
            if text:
                teile.append(Paragraph(inline(text), ParagraphStyle("btf", parent=bildtext, fontSize=7.8, leading=10)))
            return [("FLOAT", teile, "right" if opt["fluss"] == "rechts" else "left", bw)]
        if breite is None and V("foto-breite", "").strip():
            try:
                breite = float(V("foto-breite").replace(",", ".")) * mm
            except ValueError:
                pass
        fb = FlexBild(bild(pfad), w / h, text, breite, anpassen=ja("foto-anpassen", "ja"))
        fb.spaceAfter = 10    # Abstand nach dem Bild fällt am Seitenende weg (kein leeres Blatt)
        return [Spacer(1, 6), fb]
    if not ENTWURF:
        return []
    return gestrichelt(f"FOTO-VORSCHLAG <font name='{schrift('text_kursiv')}' color='{hexfarbe('leise')}'>· Datei: fotos/"
                       + (datei or "…") + "</font>", titel, vorschlag, hoehe=38 * mm)


def _build(out, ausgleich=None):
    global REGISTER, IM_ANHANG
    IM_ANHANG = False
    doc = Doc(out)
    REGISTER = None
    if stichworte():
        REGISTER = Register(dot=" . ", headers=True,
                               style=ParagraphStyle("reg", parent=body, fontSize=9, leading=12.5, spaceBefore=0, spaceAfter=0),
                               tableStyle=TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                                                      ("LEFTPADDING", (0, 0), (-1, -1), 0),
                                                      ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                                                      ("TOPPADDING", (0, 0), (-1, -1), 0),
                                                      ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    mache = REGISTER.getCanvasMaker() if REGISTER else None
    story = [] if DRUCK else [NextPageTemplate("plain"), PageBreak()]
    vorspann = {"kernsatz": False}
    lines = text_zeilen()
    para = []
    first = True
    teil_gesehen = False
    schwebe = {}   # Foto, das von den folgenden Absätzen umflossen wird

    def ausgeben():
        if schwebe:
            bildblock = BildMitText(schwebe["teile"], schwebe["bw"])
            story.append(ImageAndFlowables(bildblock, schwebe["paras"], imageSide=schwebe["seite"],
                                           imageLeftPadding=5 * mm if schwebe["seite"] == "right" else 0,
                                           imageRightPadding=0 if schwebe["seite"] == "right" else 5 * mm,
                                           imageTopPadding=2, imageBottomPadding=4))
            schwebe.clear()

    def flush():
        if para:
            p = Paragraph(inline(" ".join(para)), body); para.clear()
            if schwebe:
                schwebe["paras"].append(p)
                if len(schwebe["paras"]) >= 5:
                    ausgeben()
            else:
                story.append(p)

    sammle = None          # @TITEL / @IMPRESSUM: die folgenden Zeilen gehören dazu
    QUELLEN.clear()
    bn_gesetzt = False     # Bildnachweis schon gesetzt?

    def vorspann_fertig():
        """@TITEL bzw. @IMPRESSUM mit den gesammelten Zeilen setzen."""
        nonlocal sammle
        if sammle is None:
            return
        art, z, widmung = sammle[:3]; sammle = None
        while z and not z[-1].strip(): z.pop()
        if art == "TITEL":
            z = [t.strip() for t in z if t.strip()]
            story.extend(titelseite(z[0] if z else E.TITEL, " · ".join(z[1:])))   # weitere Zeilen: mit « · » angehängt
        else:
            story.extend(impressum(z, widmung))

    liste = Liste()
    for ln in lines:
        if liste.punkte and not (not isinstance(ln, tuple) and (not ln.strip() or LISTE.match(ln.rstrip()))):
            story += liste.ende()
        if sammle is not None:
            if not isinstance(ln, tuple) and ln.strip() == "@HINWEIS" and sammle[0] == "IMPRESSUM":
                del sammle[3:]; sammle[1].append(""); continue      # folgende Zeilen = Hinweis unten im Impressum
            if isinstance(ln, tuple) and ln[0] == "WIDMUNG" and sammle[0] == "IMPRESSUM":
                sammle[2] = " ".join(t.strip() for t in ln[2] if t.strip()); continue
            if not isinstance(ln, tuple) and ln.strip() == "@WIDMUNG" and sammle[0] == "IMPRESSUM":
                sammle.append("widmung"); continue          # folgende Zeilen = Widmung
            if not isinstance(ln, tuple) and len(sammle) > 3 and not ln.lstrip().startswith(("#", "@")):
                sammle[2] = (sammle[2] + " " + ln.strip()).strip(); continue
            if isinstance(ln, tuple) or ln.lstrip().startswith(("#", "@")):
                vorspann_fertig()
            else:
                sammle[1].append(ln); continue
        if isinstance(ln, tuple) or (ln.strip() and (ln.lstrip().startswith(("#", ">", "~", "- ", "@"))
                                                     or LISTE.match(ln.rstrip()))):
            flush(); ausgeben()
        if isinstance(ln, tuple) and ln[0] == "ZEITSTRAHL":
            story += zeitstrahl_tabelle(ln[2]); continue
        if not isinstance(ln, tuple) and ln.lstrip().startswith("@#"):
            story += tabelle(ln); continue
        if isinstance(ln, tuple) and ln[0] == "WIDMUNG":
            raise M.Fehler("::: widmung gehört direkt unter @IMPRESSUM.")
        if isinstance(ln, tuple) and ln[0] == "FOTO" and foto_quelle(ln[2]) and foto_info(ln[2])[0]:
            nr = len(QUELLEN) + 1
            QUELLEN.append((nr, foto_info(ln[2])[1] or ln[1], foto_quelle(ln[2])))
            story.append(QuellenMarke(nr))
        if isinstance(ln, tuple):          # Kasten, offene Stelle, Notiz, Foto, Mitte, Zusammen
            teile = {"UZ": uz_kasten, "OFFEN": offen_kasten, "PH": platzhalter, "FOTO": foto, "MITTE": mitte,
                     "ZUSAMMEN": zusammen}[ln[0]](ln[1], ln[2])
            if teile and isinstance(teile[0], tuple) and teile[0][0] == "FLOAT":
                _, t, seite, bw = teile[0]
                schwebe.update(teile=t, seite=seite, bw=bw, paras=[])
            else:
                story += teile
            continue
        s = ln.rstrip()
        if not s.strip():
            flush(); continue
        if s.startswith(("# ", "## ")):
            IM_ANHANG = False
        if s.startswith("# ") and "|" not in s:
            # Kapitel auf oberster Ebene (Anhang, Zeitstrahl, Über den Autor …): neue Seite, eigener Eintrag
            flush(); t = s[2:].strip()
            p = Paragraph(inline(t), ZEIT_STIL); p._toc = (0, t)
            story += [NextPageTemplate("body"), PageBreak(), p]
            first = False
        elif s.startswith("# "):
            flush()
            if s.count("|") < 2:
                raise M.Fehler(f"{TEXT}, Zeile {getattr(ln, 'nr', '?')}: Teil braucht die Form "
                               "«# Teil 1|Titel|Untertitel».")
            teile_ = [x.strip() for x in s[2:].split("|")] + ["", ""]
            num, title, sub, teilbild = teile_[0], teile_[1], teile_[2], teile_[3] or None
            story += [NextPageTemplate("part"), PageBreak(),
                      PartMarker(num, title, sub, teilbild), NextPageTemplate("body"), PageBreak()]
            teil_gesehen = True
            first = True
        elif s.startswith("### "):
            flush()
            story.append(CondPageBreak(30 * mm))   # Unterüberschrift nie allein unten auf der Seite
            story.append(Paragraph(inline(s[4:]), h3))
        elif s.startswith("## "):
            flush()
            t = s[3:]
            if first and not teil_gesehen:
                story += [NextPageTemplate("body"), PageBreak()]
            elif not first:
                story.append(CondPageBreak(45 * mm))
            p = Paragraph(inline(t), h2 if not first else ParagraphStyle("h2f", parent=h2, spaceBefore=0))
            p._toc = (1, t)
            story.append(p); first = False
        elif s.startswith("> "):
            flush(); story.append(KeepTogether([Spacer(1, 6), Ornament(), Paragraph(inline(s[2:]), quote),
                                                Ornament(), Spacer(1, 14)]))
        elif s.startswith("~ "):
            flush(); story.append(Paragraph(inline(s[2:]), note))
        elif LISTE.match(s):
            flush(); liste.punkt(LISTE.match(s))
        elif s.startswith("@MOTTO "):
            flush()
            story += [NextPageTemplate("plain"), PageBreak(), MottoSeite(inline(s[7:])),
                      NextPageTemplate("body")]
        elif s.startswith("@KOPF"):
            flush(); story.append(KopfZusatz(s[5:].strip()))
        elif s.startswith("@PLATZ "):
            flush(); story.append(CondPageBreak(float(s.split()[1]) * mm))   # neue Seite, wenn weniger Platz
        elif s == "@TITEL":
            sammle = ["TITEL", [], ""]
        elif s == "@IMPRESSUM":
            sammle = ["IMPRESSUM", [], ""]
        elif s == "@WIDMUNG":
            raise M.Fehler(f"{TEXT}, Zeile {getattr(ln, 'nr', '?')}: @WIDMUNG gehört direkt unter @IMPRESSUM.")
        elif s == "@HINWEIS":
            raise M.Fehler(f"{TEXT}, Zeile {getattr(ln, 'nr', '?')}: @HINWEIS gehört direkt nach @IMPRESSUM oder @WIDMUNG.")
        elif s.startswith("@KERNSATZ"):
            vorspann["kernsatz"] = True
            t = inline_einfach(s[9:].strip())
            story += ([PageBreak(), MottoSeite(t), PageBreak()] if DRUCK else [MottoSeite(t), PageBreak()])
        elif s == "@INHALTSVERZEICHNIS":
            if DRUCK and not vorspann["kernsatz"]:
                story.append(PageBreak())
            toc = TableOfContents(); toc.levelStyles = [toc1, toc2]; toc.dotsMinLevel = 0
            story += [Paragraph(E.WORT_INHALT, INHALT_STIL), NextPageTemplate("tocfolge"), toc]
        elif s.startswith("@PORTRAIT "):
            # @PORTRAIT bild.png | Bildtext : rundes Foto mit Ring
            story += portrait(None, [s[10:]])
        elif s.startswith("@QR-PAAR "):
            # @QR-PAAR url | Text ;; url | Text : zwei (oder drei) QR-Codes nebeneinander
            story += qr_reihe(None, s[9:].split(";;"))
        elif s.startswith("@QR "):
            # @QR url | Text : QR-Code mit klickbarem Link darunter
            url, _, text = s[4:].partition("|"); url = url.strip(); text = (text or url).strip()
            if "www." in text:
                w = text[text.index("www."):].split()[0]
                text = text.replace(w, f'<a href="{url}" color="{hexfarbe("akzent")}">{w}</a>')
            qr = QrCodeWidget(url); qb = qr.getBounds(); qs = 23 * mm
            dq = Drawing(qs, qs, transform=[qs / (qb[2] - qb[0]), 0, 0, qs / (qb[3] - qb[1]), 0, 0]); dq.add(qr)
            story.append(KeepTogether([Spacer(1, 4), dq, Spacer(1, 2),
                                       Paragraph(text, ParagraphStyle("qrt", parent=body, alignment=TA_LEFT))]))
        elif s.startswith("@ZITAT "):
            # Zitat wie «> », aber ohne Verzierung
            flush(); story.append(KeepTogether([Spacer(1, 6), Paragraph(inline(s[7:]), quote), Spacer(1, 14)]))
        elif s.startswith("@UNTEN "):
            flush(); story.append(ZitatUnten(inline(s[7:])))
        elif s == "@UMBRUCH-RECHTS":
            # neue Seite; im Druck zusätzlich eine leere linke Seite, falls nötig
            from reportlab.platypus.flowables import DocIf
            story += [Umbruch()] + ([DocIf("doc.page % 2 == 0", [PageBreak()])] if DRUCK else [])
        elif s.startswith("@ABSTAND"):
            story.append(Spacer(1, float((s.split() + ["8"])[1]) * mm))
        elif s.startswith(("@LOTUS-UNTEN", "@ZIER-UNTEN")):
            # Lotusblüte zentriert ganz unten auf die aktuelle Seite; danach geht es auf der nächsten Seite weiter
            flush(); story.append(LotusUnten(float(s.split()[1]) * mm if len(s.split()) > 1 else 10 * mm))
        elif s.startswith(("@LOTUS-TRENNER", "@ZIER-TRENNER")):
            # kleine Lotusblüte ohne eigenen Platzbedarf, mittig in die Lücke vor der nächsten Überschrift
            flush(); story.append(LotusTrenner(float(s.split()[1]) * mm if len(s.split()) > 1 else 6 * mm))
        elif s.split()[0] in ("@LOTUS", "@ZIER"):
            # @LOTUS 12 = kleine Lotusblüte, zentriert (Zahl = Breite in mm)
            flush()
            from reportlab.platypus import Image as Image_
            lb = float(s.split()[1]) * mm if len(s.split()) > 1 else 12 * mm
            story += [Spacer(1, 1 * mm), Image_(bild(LOTUS), lb, lb * LOTUS_RATIO, mask="auto"), Spacer(1, 1 * mm)]
        elif s == "@SEITENMITTE":
            flush(); story.append(SeiteMitte())
        elif s == "@UMBRUCH":
            flush(); story.append(Umbruch())
        elif s == "@RUECKSEITE":
            flush()
            if not bn_gesetzt:
                story += bildnachweis(); bn_gesetzt = True
            if not DRUCK:  # im Druck ist die Rückseite Teil des Umschlags
                story += [NextPageTemplate("back"), PageBreak(), Spacer(1, 1)]
        elif s == "@BILDNACHWEIS":
            flush(); story += bildnachweis(); bn_gesetzt = True
        elif s == "@STICHWORTE":
            flush()
            if not bn_gesetzt:
                story += bildnachweis(); bn_gesetzt = True
            story += stichwortverzeichnis()
        elif s.lstrip().startswith("@"):
            raise M.Fehler(f"{TEXT}, Zeile {getattr(ln, 'nr', '?')}: unbekannter Befehl «{s.strip()}».")
        else:
            para.append(s.strip())
    story += liste.ende()
    flush(); ausgeben(); vorspann_fertig()
    if not bn_gesetzt:
        story += bildnachweis()
    IM_ANHANG = False      # Bildtexte werden erst beim Umbruch gesetzt: dort wieder normal markieren
    # Druck: auf Mindest-/gerade Seitenzahl auffüllen (Notizseiten, zuletzt eine Seite mit Lotus)
    extra = getattr(build, "auffuellen", 0) if DRUCK else 0
    for i in range(extra):
        story += [NextPageTemplate("notizen" if i < extra - 1 else "leer"), PageBreak(), Spacer(1, 1)]
    if ausgleich is None:
        # 1. Durchlauf: Elemente nummerieren und ihre Lage aufzeichnen
        for i, f in enumerate(story):
            f._lr = i
            for g in getattr(f, "_content", []) if isinstance(f, KeepTogether) else []:
                g._lr = i
        doc.lr_info = {}
        doc.multiBuild(story, **({"canvasmaker": mache} if mache else {}))
        return doc, story
    neu = []
    for i, f in enumerate(story):
        if i in ausgleich:
            neu.append(Spacer(1, ausgleich[i]))
        neu.append(f)
    doc.multiBuild(neu, **({"canvasmaker": mache} if mache else {}))
    return doc.page   # Seitenzahl des fertigen PDFs


_split_orig = Flowable.splitOn
def _split_mit_nummer(self, *a, **k):
    """Geteilte Elemente (z. B. ein Kasten über zwei Seiten) behalten ihre Nummer für den Seitenausgleich."""
    teile = _split_orig(self, *a, **k)
    i = getattr(self, "_lr", None)
    if i is not None:
        for t in teile or []:
            try: t._lr = i
            except Exception: pass
    return teile
Flowable.splitOn = _split_mit_nummer


class KopfZusatz(Flowable):
    """@KOPF Text: ersetzt in der Kopfzeile das Kapitel (z. B. «Ecuador»); @KOPF allein beendet es."""
    def __init__(self, text):
        super().__init__(); self.text = text
    def wrap(self, aw, ah):
        return 0, 0
    def draw(self):
        pass


class SeiteMitte(Flowable):
    """@SEITENMITTE: Inhalt dieser Seite (auch mit Überschrift) senkrecht zentrieren."""
    def wrap(self, aw, ah):
        return 0, 0
    def draw(self):
        pass


class Umbruch(PageBreak):
    """Von Hand gesetzter Seitenwechsel (@UMBRUCH); die Seite davor wird ausgeglichen."""


def seitenausgleich(doc, story):
    """Letzte Seite vor einem neuen Teil (oder vor der Motto-Seite): Den freien Platz unten
    auf die Abstände verteilen, vor allem um Zitate, Bilder und Überschriften herum."""
    info = doc.lr_info
    ziele = [i for i, f in enumerate(story) if isinstance(f, (PartMarker, MottoSeite, Umbruch, MitteBlock))]
    ausgleich = {}
    for z in ziele:
        inhalt = [i for i in range(z) if i in info and not isinstance(story[i], (PageBreak, CondPageBreak, Spacer))]
        if not inhalt: continue
        letzte = max(inhalt)
        seite = info[letzte][1]
        frei = info[letzte][2] - info[letzte][3]
        if isinstance(story[z], MitteBlock) and z in info and info[z][0] <= seite:
            continue          # zentrierter Block steht noch auf derselben Seite
        sm = [i for i in inhalt if isinstance(story[i], SeiteMitte) and info[i][0] == seite]
        if sm:                # @SEITENMITTE: ganzen Inhalt der Seite nur senkrecht zentrieren
            if frei > 6 * mm:
                ausgleich[sm[0]] = (frei - 4) / 2
            continue
        if frei < 15 or frei > 0.75 * (H - TOP - BOT):
            continue
        def deko(i):
            f = story[i]
            if isinstance(f, KeepTogether) and any(isinstance(g, Ornament) for g in f._content): return True
            return type(f).__name__ in ("FlexBild", "Image") or \
                (isinstance(f, KeepTogether) and any(type(g).__name__ in ("FlexBild", "Image") for g in f._content))
        from reportlab.platypus.doctemplate import ActionFlowable
        def vorgaenger(i):
            # direkt vorangehendes Inhaltselement; None, wenn es nicht erfasst wurde (z. B. geteilter Absatz)
            k = [k for k in range(i) if not isinstance(story[k], (PageBreak, CondPageBreak, Spacer, ActionFlowable))]
            return k[-1] if k and k[-1] in info else None
        luecken = {}
        for i in inhalt:
            j = vorgaenger(i)
            if j is None: continue
            if info[i][0] != seite or info[j][1] != seite: continue
            w = 3 if deko(i) or deko(j) else 2 if getattr(story[i], "_toc", None) else 1
            luecken[i] = w
        if not luecken: continue
        # Fliesstext-Abstände nur wenig dehnen, um Zitate, Bilder und Überschriften mehr
        grenze = {1: 5 * mm, 2: 12 * mm, 3: 42 * mm}
        wert = {i: 0.0 for i in luecken}
        rest = frei - 4
        for _ in range(10):
            offen = [i for i in luecken if wert[i] < grenze[luecken[i]] - 0.01]
            if rest < 0.5 or not offen: break
            pro = rest / sum(luecken[i] for i in offen)
            for i in offen:
                d = min(pro * luecken[i], grenze[luecken[i]] - wert[i])
                wert[i] += d; rest -= d
        for i, v in wert.items():
            if v > 0.5: ausgleich[i] = v
        # Bleibt noch Platz und beginnt die Seite nicht mit einer Überschrift: Inhalt senkrecht zentrieren
        erste = [i for i in inhalt if info[i][0] == seite and i not in luecken]
        if rest > 6 * mm and erste and not getattr(story[erste[0]], "_toc", None):
            j = vorgaenger(erste[0])
            if j is not None and info[j][1] < seite:
                ausgleich[erste[0]] = ausgleich.get(erste[0], 0) + rest / 2
    return ausgleich


def build(out):
    if os.environ.get("BUCH_SCHNELL") == "1":       # sh build.sh schnell: ein Durchgang, kein Seitenausgleich
        return _build(out)[0].page
    doc, story = _build(out)
    return _build(out, seitenausgleich(doc, story))


def zeitstrahl_zeilen(inhalt):
    """Zeilen eines «::: zeitstrahl»-Blocks:  1974 | Geboren in Bern"""
    rows = []
    for z in inhalt:
        if "|" in z:
            a, b = z.split("|", 1)
            rows.append((a.strip(), b.strip()))
    return rows


def zeitstrahl_block(titel, inhalt):
    rows = zeitstrahl_zeilen(inhalt)
    titel = titel or getattr(E, "WORT_ZEITSTRAHL", "Zeitstrahl")
    cs = ParagraphStyle("c", parent=body, fontSize=8.6, leading=11, spaceAfter=0, alignment=TA_LEFT)
    ys = ParagraphStyle("y", parent=cs, fontName=schrift("titel"), textColor=GOLD)
    global IM_ANHANG
    alt, IM_ANHANG = IM_ANHANG, True
    data = [[Paragraph(inline(a), ys), Paragraph(inline(b), cs)] for a, b in rows]
    IM_ANHANG = alt
    t = Table(data, colWidths=[22 * mm, W - IN - OUT - 22 * mm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, -2), 0.3, farbe("linie")),
        ("TOPPADDING", (0, 0), (-1, -1), 2.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2),
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))
    p = Paragraph(titel, ZEIT_STIL); p._toc = (0, titel)
    # Folgeseite beginnt auf der Höhe der Tabelle von Seite 1 (unter der Überschrift)
    return [PageBreak(), p, NextPageTemplate("zeitfolge"), t, NextPageTemplate("body")]


def zeitstrahl_tabelle(inhalt):
    """«::: zeitstrahl»: Zeilen «Jahr | Text» als Tabelle (Überschrift davor mit «# Zeitstrahl»)."""
    rows = zeitstrahl_zeilen(inhalt)
    cs = ParagraphStyle("c", parent=body, fontSize=8.6, leading=11, spaceAfter=0, alignment=TA_LEFT)
    ys = ParagraphStyle("y", parent=cs, fontName=schrift("titel"), textColor=GOLD)
    data = [[Paragraph(inline_einfach(a), ys), Paragraph(inline_einfach(b), cs)] for a, b in rows]
    t = Table(data, colWidths=[22 * mm, W - IN - OUT - 22 * mm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, -2), 0.3, farbe("linie")),
        ("TOPPADDING", (0, 0), (-1, -1), 2.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2),
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))
    # Folgeseite beginnt auf der Höhe der Tabelle von Seite 1 (unter der Überschrift)
    return [NextPageTemplate("zeitfolge"), t, NextPageTemplate("body")]



# --- Tabellen aus tabellen/*.csv (pureSATZ 2.12) ------------------------------------------
class QuerTabelle(Flowable):
    """Tabelle um 90° gedreht auf der hochformatigen Seite (Buch zum Lesen drehen)."""
    def __init__(self, t):
        super().__init__(); self.t = t

    def wrap(self, aw, ah):
        self.aw = aw
        self.tw, self.th = self.t.wrap(ah, aw)
        return aw, self.tw

    def split(self, aw, ah):
        teile = self.t.split(ah, aw)
        return [QuerTabelle(x) for x in teile] if len(teile) > 1 else []

    def draw(self):
        c = self.canv
        c.saveState()
        c.translate((self.aw - self.th) / 2 + self.th, 0)
        c.rotate(90)
        self.t.drawOn(c, 0, 0)
        c.restoreState()


_TAB_GEMELDET = set()


def _tab_text(t):
    return re.sub(r"<[^>]+>", "", t.replace("**", ""))


def tabelle(zeile):
    """Flowables für eine Zeile «@#name [quer|hoch]»."""
    import tabellen as T
    name, richtung = T.verweis(zeile) or (zeile.strip()[2:].strip(), "")
    pfad = T.alle(BASE).get(name)
    if not pfad:
        raise M.Fehler("; ".join(T.pruefe(BASE, zeile)))
    d = T.lies(pfad)
    if d["fehler"]:
        raise M.Fehler("; ".join(d["fehler"]))
    a = var()
    ein = lambda t: (a.ersetze(t) if "{" in t else t) or ""
    kopf = [ein(k) for k in d["kopf"]]
    reihen = [[ein(x) for x in r] for r in d["zeilen"]]
    rechts = [all(T.ist_zahl(r[i]) for r in reihen if r[i].strip()) and any(r[i].strip() for r in reihen)
              for i in range(len(kopf))]
    f_kopf, f_text = schrift("titel"), schrift("text")
    pad = 2 * 4.0 + 3          # Zellränder + Sicherheit, damit kein Wort zerrissen wird

    def breiten(gr, verfuegbar):
        """Spaltenbreiten für Schriftgrösse gr, oder None, wenn es nicht passt."""
        maxw, minw = [], []
        for i, k in enumerate(kopf):
            zellen = [(k, f_kopf)] + [(r[i], f_text) for r in reihen]
            maxw.append(max(pdfmetrics.stringWidth(_tab_text(t), f, gr) for t, f in zellen) + pad)
            minw.append(max(max((pdfmetrics.stringWidth(w, f, gr) for w in _tab_text(t).split() or [""]), default=0)
                            for t, f in zellen) + pad)
        if sum(maxw) <= verfuegbar:
            extra = (verfuegbar - sum(maxw)) / len(maxw) if sum(maxw) > verfuegbar * 0.75 else 0
            return [w + extra for w in maxw]
        if sum(minw) <= verfuegbar:
            spiel = sum(m - n for m, n in zip(maxw, minw)) or 1
            return [n + (verfuegbar - sum(minw)) * (m - n) / spiel for m, n in zip(maxw, minw)]
        return None

    hoch_breite, quer_breite = W - IN - OUT, H - TOP - BOT
    groessen = (9, 8.5, 8, 7.5)
    wahl = None
    if richtung != "quer":
        wahl = next(((g, b, False) for g in groessen for b in [breiten(g, hoch_breite)] if b), None)
    if wahl is None and richtung != "hoch":
        wahl = next(((g, b, True) for g in groessen for b in [breiten(g, quer_breite)] if b), None)
    if wahl is None:                    # passt nirgends: kleinste Schrift, Breiten anteilig
        quer = richtung != "hoch"
        verf = quer_breite if quer else hoch_breite
        g = 7
        # längstes Wort pro Spalte als Mass: so werden kurze Spalten nicht zerrissen
        roh = [max(max((pdfmetrics.stringWidth(w, f, g) for w in _tab_text(t).split() or [""]), default=0)
                   for t, f in [(k, f_kopf)] + [(r[i], f_text) for r in reihen]) + pad for i, k in enumerate(kopf)]
        wahl = (g, [w * verf / sum(roh) for w in roh], quer)
        if sum(roh) > verf and name not in _TAB_GEMELDET:
            _TAB_GEMELDET.add(name)
            print(f"Hinweis: Tabelle «{name}» ist sehr breit – kleinste Schrift, lange Wörter können umbrechen.")
    gr, spalten, quer = wahl
    gesamt = sum(spalten)
    zs = ParagraphStyle("tz", parent=body, fontSize=gr, leading=gr * 1.32, spaceAfter=0, alignment=TA_LEFT)
    zr = ParagraphStyle("tzr", parent=zs, alignment=2)
    ks = ParagraphStyle("tk", parent=zs, fontName=f_kopf, textColor=BLAU)
    kr = ParagraphStyle("tkr", parent=ks, alignment=2)
    ts = ParagraphStyle("tt", parent=body, fontName=f_kopf, fontSize=gr + 1.5, leading=(gr + 1.5) * 1.3,
                        textColor=BLAU, spaceAfter=0, alignment=TA_LEFT)
    qs = ParagraphStyle("tq", parent=zs, fontName=schrift("text_kursiv"), fontSize=gr - 0.8, textColor=SOFT)
    daten = [[Paragraph(inline(ein(d["titel"])), ts)] + [""] * (len(kopf) - 1),
             [Paragraph(inline(k), kr if rechts[i] else ks) for i, k in enumerate(kopf)]]
    daten += [[Paragraph(inline(x), zr if rechts[i] else zs) for i, x in enumerate(r)] for r in reihen]
    stil = [("SPAN", (0, 0), (-1, 0)), ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 2.4), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.6),
            ("LEFTPADDING", (0, 0), (0, 0), 0), ("BOTTOMPADDING", (0, 0), (-1, 0), 5),
            ("LINEBELOW", (0, 1), (-1, 1), 0.8, GOLD),
            ("LINEBELOW", (0, 2), (-1, -1), 0.3, farbe("linie"))]
    for i in range(2, len(daten)):
        if i % 2:
            stil.append(("BACKGROUND", (0, i), (-1, i), farbe("kasten")))
    if d["quelle"]:
        daten.append([Paragraph(inline(ein(d["quelle"])), qs)] + [""] * (len(kopf) - 1))
        stil += [("SPAN", (0, -1), (-1, -1)), ("LINEBELOW", (0, -2), (-1, -2), 0.6, GOLD),
                 ("LEFTPADDING", (0, -1), (0, -1), 0), ("TOPPADDING", (0, -1), (-1, -1), 4)]
    t = Table(daten, colWidths=spalten, repeatRows=2, hAlign="LEFT")
    t.setStyle(TableStyle(stil))
    if quer:
        return [PageBreak(), QuerTabelle(t), PageBreak()]
    if len(reihen) <= 12:                     # kleine Tabelle nie trennen (lieber ganz auf die nächste Seite)
        return [Spacer(1, 4), KeepTogether([t]), Spacer(1, 8)]
    return [Spacer(1, 4), t, Spacer(1, 8)]


def inline_einfach(t):
    """Wie inline(), aber ohne Stichwortmarken (Titelei, Impressum, Zeitstrahl, QR-Texte)."""
    t = re.sub(r"&(?!amp;|lt;|gt;|quot;|#)", "&amp;", links(t))
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)


def zeilen_html(zeilen):
    """Zeilen untereinander (<br/>), Leerzeile = Abstand (<br/><br/>)."""
    out, leer = [], False
    for z in zeilen:
        if getattr(z, "nr", 0) == -1:          # Ende eines ::: nur-Blocks
            continue
        if not z.strip():
            leer = bool(out); continue
        out.append(("<br/><br/>" if leer else "<br/>" if out else "") + inline_einfach(z.strip()))
        leer = False
    return "".join(out)


def titelseite(titel, untertitel):
    return [Spacer(1, 50 * mm * min(S, 1.6)),
            Paragraph(inline_einfach(titel), ParagraphStyle("t", fontName=schrift("titel"), fontSize=18,
                      leading=24, textColor=DEEP, alignment=TA_CENTER)),
            Spacer(1, 4),
            Paragraph(inline_einfach(untertitel), ParagraphStyle("st", fontName=schrift("text_kursiv"),
                      fontSize=11, leading=15, textColor=SOFT, alignment=TA_CENTER)),
            Spacer(1, 8), Ornament()]


class ZitatUnten(Flowable):
    """@UNTEN Text: füllt den Rest der Seite und setzt den Text kursiv, zentriert an den unteren Rand."""
    def __init__(self, text):
        super().__init__(); self.text = text
    def _p(self, aw):
        p = Paragraph(self.text, ParagraphStyle("unten", fontName=schrift("text_kursiv"), fontSize=9.6, leading=13.5,
                                                textColor=BLAU, alignment=TA_CENTER))
        w, h = p.wrap(aw - 20 * mm, 1000)
        return p, h
    def wrap(self, aw, ah):
        self.aw, self.ah = aw, ah
        _, h = self._p(aw)
        if ah < h + 10 * mm:          # zu wenig Platz: auf die nächste Seite
            return aw, h + 10 * mm
        return aw, ah - 0.5
    def split(self, aw, ah):
        return []
    def draw(self):
        p, h = self._p(self.aw)
        p.drawOn(self.canv, 10 * mm, 2 * mm)


class ImpressumSeite(Flowable):
    """Impressum-Seite: Angaben unten auf der Seite; Widmung kursiv, waagrecht mittig im unteren Drittel.
    logo: Bild der Plattform links über den Angaben (Variable impressum-logo, nur Druck)."""
    def __init__(self, widmung, angaben, logo=None):
        super().__init__(); self.widmung = widmung; self.angaben = angaben; self.logo = logo
    def wrap(self, aw, ah):
        self.aw, self.ah = aw, ah
        self.ah_ang = self.angaben.wrap(aw, ah)[1]
        self.w = None
        if self.widmung:
            self.w = Paragraph(self.widmung, ParagraphStyle("widm", fontName=schrift("text_kursiv"), fontSize=9,
                                                            leading=13, textColor=BLAU, alignment=TA_CENTER))
            self.wh = self.w.wrap(aw - 16 * mm, ah)[1]
        return aw, ah - 1
    def draw(self):
        self.angaben.drawOn(self.canv, 0, 0)
        if self.logo:              # Logo knapp über dem Text: Höhe 1,5 × Schrift, Abstand zwei Zeilen (2.24.1)
            from reportlab.lib.utils import ImageReader
            iw, ih = ImageReader(self.logo).getSize()
            st = self.angaben.style
            h = IMPRESSUM_LOGO_HOEHE * st.fontSize; b = h * iw / ih
            self.canv.drawImage(self.logo, 0, self.ah_ang + 2 * st.leading, b, h, mask="auto")
        if self.w:
            self.w.drawOn(self.canv, 8 * mm, (self.ah / 3 - self.wh) / 2)   # mittig im unteren Drittel (2.24.2)


IMPRESSUM_LOGO_HOEHE = 1.5    # × Schriftgrösse des Impressums


def impressum_logo():
    """impressum-logo (Druckdatei oder Variablen-Datei): PNG aus bilder/, None = kein Logo."""
    n = V("impressum-logo").strip()
    if not n:
        return None
    pfad = finde(n, ("bilder",))
    if not pfad or not os.path.exists(pfad):
        raise SystemExit(f"Variable «impressum-logo»: {n} fehlt im Ordner bilder/.")
    return bild(pfad)


def impressum(zeilen, widmung):
    """Druck: Impressum links unten (Logo oben), Widmung auf eigener Seite rechts, im unteren Drittel.
    Bildschirm: Impressum zentriert, Widmung auf eigener Seite."""
    html = zeilen_html(zeilen)
    if DRUCK:
        # Seite 2 (links): Impressum unten, Logo der Plattform oben. Seite 3 (rechts): Widmung allein.
        out = [PageBreak(), ImpressumSeite("", Paragraph(html, ParagraphStyle(
            "imp", parent=small, alignment=TA_LEFT, fontSize=7.6, leading=11)), impressum_logo())]
        if widmung:
            out += [PageBreak(), ImpressumSeite(inline_einfach(widmung), Paragraph("", small))]
        return out
    out = [Spacer(1, 25 * mm * min(S, 1.6)), Paragraph(html, ParagraphStyle("imp", parent=small, alignment=TA_CENTER)),
           PageBreak()]
    if widmung:   # eigene Seite, Satz unten (gleicher Abstand wie oben)
        out += [ImpressumSeite("", Paragraph("<i>" + inline_einfach(widmung) + "</i>",
                                             ParagraphStyle("widm2", parent=small, alignment=TA_CENTER))),
                PageBreak()]
    return out


def zusammen(titel, inhalt):
    """«::: zusammen»: Absätze, Aufzählungen und Zitate, die nie auf zwei Seiten getrennt werden."""
    teile, para, liste = [], [], Liste()
    for z in inhalt + [""]:
        t = z.strip()
        m = LISTE.match(z.rstrip()) if t else None
        if m:
            if para:
                teile.append(Paragraph(inline(" ".join(para)), body)); para = []
            liste.punkt(m); continue
        if t:
            teile += liste.ende()
        if not t or t.startswith(("> ", "~ ")):
            if para:
                teile.append(Paragraph(inline(" ".join(para)), body)); para = []
            if t.startswith("> "):
                teile += [Ornament(), Paragraph(inline(t[2:]), quote), Ornament()]
            elif t.startswith("~ "):
                teile.append(Paragraph(inline(t[2:]), note))
        else:
            para.append(t)
    teile += liste.ende()
    return [KeepTogether(teile)] if teile else []


def seite_kopf(titel, _):
    """«::: seite Titel»: neue Seite mit Überschrift (im Inhaltsverzeichnis wie «Über den Autor»)."""
    p = Paragraph(inline(titel), ParagraphStyle("sh", parent=h2, spaceBefore=0))
    p._toc = (0, titel)
    return [PageBreak(), p]


def qrbox(url, label):
    qr = QrCodeWidget(url)
    b = qr.getBounds(); s = 23 * mm
    d = Drawing(s, s, transform=[s / (b[2] - b[0]), 0, 0, s / (b[3] - b[1]), 0, 0]); d.add(qr)
    return [d, Paragraph(label, ParagraphStyle("ql", parent=small, alignment=TA_CENTER, fontSize=8, leading=10.5))]


def qr_reihe(_, zeilen):
    """qr: https://… | Beschriftung   (bis zu drei nebeneinander)"""
    boxen = []
    for z in zeilen:
        url, _, label = z.partition("|")
        boxen.append(qrbox(url.strip(), inline_einfach(label.strip() or url.strip())))
    out = [Spacer(1, 6)]
    for i in range(0, len(boxen), 3):
        reihe = boxen[i:i + 3]
        cw = (W - IN - OUT) / len(reihe)
        qt = Table([reihe], colWidths=[cw] * len(reihe))
        qt.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
        out.append(qt)
    return out


class RundesFoto(Flowable):
    """Rundes Portrait mit feinem Ring."""
    def __init__(self, path, size):
        super().__init__(); self.path, self.size = path, size
    def wrap(self, aw, ah):
        self.aw = aw; return aw, self.size + 6
    def draw(self):
        c = self.canv; x = (self.aw - self.size) / 2
        c.drawImage(bild(self.path), x, 3, self.size, self.size, mask="auto")
        c.setStrokeColor(BLAU); c.setLineWidth(1.2)
        c.circle(x + self.size / 2, 3 + self.size / 2, self.size / 2 + 2.5, stroke=1, fill=0)


def portrait(_, zeilen):
    """portrait: datei.png | Bildtext   (rundes Bild, zentriert)"""
    datei, _, text = zeilen[0].partition("|")
    pfad = finde(datei.strip())
    if not pfad:
        return gestrichelt("BILD FEHLT", "", "Datei: " + datei.strip()) if ENTWURF else []
    out = [Spacer(1, 18), RundesFoto(pfad, 48 * mm)]
    if text.strip():
        out.append(Paragraph(inline(text.strip()), ParagraphStyle("cap", parent=small, alignment=TA_CENTER,
                             fontName=schrift("text_kursiv"), spaceBefore=6, spaceAfter=22)))
    return out


def offene_stellen():
    """Alle «::: offen…»- und Platzhalter-Blöcke im Manuskript (auch in eingebundenen Geschichten)."""
    out = []
    zeilen = [z for _, z in M.lies(os.path.join(BASE, TEXT))[1]]
    nummern = [n for n, _ in M.lies(os.path.join(BASE, TEXT))[1]]
    for i, z in enumerate(zeilen):
        s = z.strip()
        if s.startswith(":::") and s != ":::":
            art = s[3:].strip().split(" ", 1)[0].lower()
            if art.startswith("offen") or art.startswith("platzhalter"):
                text = s[3:].strip()[len(art):].strip()
                k = i + 1
                while not text and k < len(zeilen) and zeilen[k].strip() != ":::":
                    text = zeilen[k].strip(); k += 1
                out.append((nummern[i], art, text[:60] + ("…" if len(text) > 60 else "")))
    return out


def zeige_offene_stellen():
    liste = offene_stellen()
    if not liste:
        return
    print(f"\nOffene Stellen ({len(liste)}):" + ("" if ENTWURF else "   ACHTUNG: Druckfassung! offen = normal gedruckt, Notizen fehlen"))
    for nr, art, text in liste:
        print(f"  Zeile {str(nr):4}  {art:13} «{text}»")


if __name__ == "__main__":
    # Aufruf:  python3 motor/build.py       -> Ausgabe A (offiziell)
    #          python3 motor/build.py dc    -> Ausgabe B (zweite Ausgabe)
    waehle(sys.argv[1] if len(sys.argv) > 1 else None)
    ordner = os.path.join(BASE, ausgabe()["ordner"])
    os.makedirs(ordner, exist_ok=True)
    ziel = os.environ.get("BUCH_ZIEL") or os.path.join(ordner, ausgabe()["datei"] + ".pdf")   # Leseprobe/Korrektur: Zwischendatei
    n = build(ziel)
    print(f"Fertig: {os.path.relpath(ziel, BASE)} ({n} Seiten)")
    if os.environ.get("BUCH_BOOKLET") == "bildschirm":      # Booklet zum Selberdrucken (bauen.py)
        try:
            import booklet
            b = os.path.join(ordner, ausgabe()["datei"] + "_booklet.pdf")
            blaetter = booklet.erstelle([ziel], b, leise=True)
            print(f"Booklet: {os.path.relpath(b, BASE)} ({blaetter} Blätter A4, kurze Kante wenden)")
        except SystemExit as e:
            print(f"Hinweis: kein Booklet – {e}")
