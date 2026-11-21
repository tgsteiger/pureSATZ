"""
Gemeinsamer Leser für das Manuskript (Buch-MD), die Variablen-Datei und den Umschlag (Umschlag-MD).
Wird von build.py, build-broschuere.py und build-epub.py verwendet.

Variablen
---------
1. In der Variablen-Datei «{name}: wert», im Text {name}. «> …» = Erklärung.
   Gibt es «name-normal» und «name-uz», nimmt {name} automatisch den Wert der gebauten Fassung.
   «name-druck», «name-ebook», «name-bildschirm» = nur in diesem Medium; der genauere Name gewinnt.
   Unter «## Ausgabe: Druck normal» (… unzensiert, E-Book, E-Book unzensiert, PDF) gilt ein Wert nur für diese
   Ausgabe (intern «name-druck-normal»). {isbn}: die ISBN der Ausgabe.
   Eine Zeile, in der eine Variable leer bleibt, fällt ganz weg.
   Ein leeres «## @IMPRINT» füllt der Motor selbst (IMPRESSUM_VORLAGE).

2. Befehle (pureSATZ 3.0)  @[FASSUNG-]NAME[-GRÖSSE][-ORT[-HÖHE]][-STIL] Text  – zerlegt von befehl().
   Bereiche  @NAME [Titel] … @END: @UC @NORMAL @EBOOK @PRINT @SCREEN (Fassung), @UC-BLOCK, @DRAFT, @NOTE,
   @KEEP-TOGETHER, @TIMELINE, @DECORATE-REST. zeilen() liefert sie als Tupel, die Fassung ist schon ausgewählt.
"""
import os
import re

# Endungen der Blöcke und Variablen
TAGS = ("normal", "uz", "bildschirm", "druck", "ebook", "buch", "privatdruck")


class Fehler(SystemExit):
    pass


class Zeile(str):
    """Textzeile, die ihre Zeilennummer in der MD kennt (für Fehlermeldungen)."""
    nr = 0


def _zeile(text, nr):
    z = Zeile(text); z.nr = nr; return z


class Nr(int):
    """Zeilennummer einer eingebundenen Geschichte: rechnet wie eine Zahl, zeigt aber die Datei
    («12 in geschichten/schutzschild.md»), damit Fehlermeldungen auf die richtige Datei zeigen."""
    def __new__(cls, nr, datei):
        n = super().__new__(cls, nr); n.datei = datei; return n

    def __str__(self):
        return f"{int(self)} in {self.datei}"

    __repr__ = __str__


def _wo(name, nr):
    """«buch.md, Zeile 12» – bei eingebundenen Geschichten deren Datei."""
    return f"{nr.datei}, Zeile {int(nr)}" if isinstance(nr, Nr) else f"{name}, Zeile {nr}"


CODE_ZAUN = "```"          # Code-Block: Zeilen zwischen «```» und «```» bleiben wörtlich
                           # «```nur-uz» … = nur in dieser Ausgabe (wie «::: nur-uz»)


def anker(t):
    """Sprungmarke einer Überschrift: «Farben für den Druck» → «farbenfurdendruck» (Links [Text](#Farben-fuer-den-Druck))."""
    import unicodedata
    t = "".join(c for c in unicodedata.normalize("NFD", t.lower()) if unicodedata.category(c) != "Mn")
    t = t.replace("ae", "a").replace("oe", "o").replace("ue", "u").replace("ß", "ss")
    return re.sub(r"[^a-z0-9]+", "", t)


def im_code(zeilen):
    """Menge der Indizes, die in einem Code-Block liegen (mit den ```-Zeilen selbst)."""
    drin, aus = False, set()
    for i, z in enumerate(zeilen):
        z = z[1] if isinstance(z, tuple) else z
        if z.lstrip().startswith(CODE_ZAUN):
            aus.add(i); drin = not drin
        elif drin:
            aus.add(i)
    return aus


def _geschichten_einsetzen(pfad, zeilen_mit_nr):
    """Zeilen «@@name» durch die Geschichte geschichten/name.md ersetzen.
    Ohne @@-Zeilen bleibt alles, wie es war."""
    import geschichten as G
    code = im_code(zeilen_mit_nr)
    if not any(G.VERWEIS.match(z) for i, (_, z) in enumerate(zeilen_mit_nr) if i not in code):
        return zeilen_mit_nr
    basis = os.path.dirname(os.path.abspath(pfad))
    vorhanden = G.alle(basis)
    sammlung = os.environ.get("BUCH_SAMMLUNG") == "1"
    out = []
    for i, (nr, z) in enumerate(zeilen_mit_nr):
        m = G.VERWEIS.match(z) if i not in code else None
        if not m:
            out.append((nr, z)); continue
        name = m.group(1)
        if name not in vorhanden:
            import difflib
            tipp = difflib.get_close_matches(name, list(vorhanden), n=1)
            raise Fehler(f"{os.path.basename(pfad)}, Zeile {nr}: Geschichte «@@{name}» nicht gefunden "
                         f"(erwartet: geschichten/{name}.md)." + (f" Gemeint: @@{tipp[0]}?" if tipp else ""))
        datei = os.path.relpath(vorhanden[name], basis).replace(os.sep, "/")
        titel, kopf, text = G.lies(vorhanden[name])
        for n2, z2 in text:
            if G.VERWEIS.match(z2):
                raise Fehler(f"{datei}, Zeile {n2}: Eine Geschichte kann keine andere Geschichte einbinden (@@).")
            if sammlung and z2.strip().startswith("## ") and G.stand(kopf):
                z2 = z2.rstrip() + " · " + G.STAND_TEXT[G.stand(kopf)]
            out.append((Nr(n2, datei), z2))
        out.append((Nr(len(text) + 1, datei), ""))      # Leerzeile: nächste Geschichte beginnt sauber
    return out


# --------------------------------------------------------------------------- Lesen
_CACHE = {}


VARIABLE = re.compile(r"^\s*\{?([a-z][a-z0-9-]*)\}?\s*:(?:\s+(.*?))?\s*$")   # «{name}: wert» (auch «name: wert»)
BUCHSTART = re.compile(r"^#{1,6}\s*=*\s*BUCHSTART\b", re.I)


def ist_buchstart(zeile):
    return bool(BUCHSTART.match(zeile.strip()))


def lies(pfad):
    """(variablen, [(nr, zeile)]) – Einstellungen oben, danach der Text mit Zeilennummern.

    Ohne Variablen-Datei: alles vor «# BUCHSTART» sind Einstellungen (z. B. Handbuch). Jede Zeile
    «{name}: wert» ist eine Variable; Überschriften und Sätze sind Erklärungen."""
    if pfad in _CACHE:
        return _CACHE[pfad]
    roh = open(pfad, encoding="utf-8").read().split("\n")
    var, start = {}, 0
    bs = next((i for i, z in enumerate(roh) if ist_buchstart(z)), None)
    if bs is not None:
        bereich, start = range(0, bs), bs + 1
    else:
        bereich = range(0)
    for i in bereich:
        z = roh[i].strip()
        if not z or z.startswith(("#", ">", "<!--", "---")):
            continue
        m = VARIABLE.match(z)
        if m:
            var[m.group(1)] = (m.group(2) or "").strip()
    _CACHE[pfad] = (var, _geschichten_einsetzen(pfad, [(i + 1, roh[i]) for i in range(start, len(roh))]))
    return _CACHE[pfad]


AUSGABE_KOPF = re.compile(r"^ausgabe\s*:\s*(.+)$", re.I)       # «## Ausgabe: Druck normal»
ROHDATEN_KOPF = re.compile(r"coverrechner|rohdaten", re.I)       # «## Coverrechner (Rohdaten)»: keine Variablen (liest rohdaten2cover.py)
SCHEMA_KOPF = re.compile(r"^farbschema\s*(\d+)\b", re.I)          # «### Farbschema 2: dunkler für den Druck»
FARBSCHEMA_FEHLT = {}                                             # Pfad -> gewählte Nummer ohne Abschnitt
FARBSCHEMA_NAME = {}                                              # Pfad -> «Farbschema 2: dunkler für den Druck»


def ausgabe_abschnitt(titel):
    """«Druck unzensiert» -> ('druck', 'uz'); «E-Book» -> ('ebook', None); «PDF» -> ('bildschirm', None)."""
    t = titel.lower()
    if "pdf" in t or "bildschirm" in t:
        medium = "bildschirm"
    elif "e-book" in t or "ebook" in t:
        medium = "ebook"
    elif "druck" in t or "buch" in t:
        medium = "druck"
    else:
        return None
    w = set(re.findall(r"[a-zäöü']+", t))
    fassung = "uz" if w & {"unzensiert", "uz", "zweite", "dc", "director's", "directors"} else \
        "normal" if "normal" in w else None
    return medium, fassung


def lies_variablen(pfad):
    """Variablen-Datei (<buch>-variablen.md) oder Plattform-Datei (druck/…md): (variablen, stichworte).
    Jede Zeile «{name}: wert» ist eine Variable, «> …» eine Erklärung.
    Unter «## Ausgabe: Druck normal» (… unzensiert, E-Book, PDF) gilt ein Wert nur für diese Ausgabe:
    er wird intern «name-druck-normal» genannt. Ein Abschnitt «Coverrechner (Rohdaten)» wird nicht gelesen.
    «{farbschema}: 2» = die Werte unter «### Farbschema 1» gelten als Grundlage, die unter «### Farbschema 2»
    ersetzen sie; andere Farbschemas werden übergangen.
    Unter «STICHWORTE» ist jede Listenzeile ein Stichwort («- Seele | Seelen»)."""
    key = ("V", pfad)
    if key in _CACHE:
        return _CACHE[key]
    var, stw, schemas, titel_schema = {}, [], {}, {}
    bereich = None          # (art, stufe, medium, fassung): art = stw | roh | ausgabe | schema
    for z in open(pfad, encoding="utf-8").read().split("\n"):
        t = z.strip()
        if not t or t.startswith(("<!--", ">")):
            continue
        if t.startswith("#"):
            stufe = len(t) - len(t.lstrip("#"))
            titel = t.lstrip("# ").strip()
            if bereich and stufe <= bereich[1]:
                bereich = None
            if bereich is None:
                aus = AUSGABE_KOPF.match(titel)
                if "STICHWORTE" in titel.upper():
                    bereich = ("stw", stufe, None, None)
                elif ROHDATEN_KOPF.search(titel):
                    bereich = ("roh", stufe, None, None)
                elif SCHEMA_KOPF.match(titel):
                    bereich = ("schema", stufe, SCHEMA_KOPF.match(titel).group(1), None)
                    schemas.setdefault(bereich[2], {})
                    titel_schema.setdefault(bereich[2], titel)
                elif aus and ausgabe_abschnitt(aus.group(1)):
                    bereich = ("ausgabe", stufe) + ausgabe_abschnitt(aus.group(1))
            continue
        if bereich and bereich[0] == "roh":
            continue
        if bereich and bereich[0] == "stw":
            if t.startswith(("- ", "* ")):
                stw.append(t[2:].strip())
            continue
        m = VARIABLE.match(t)
        if m and bereich and bereich[0] == "schema":
            schemas[bereich[2]][m.group(1)] = (m.group(2) or "").strip()
            continue
        if m:
            name = m.group(1)
            if bereich and bereich[0] == "ausgabe":
                name = f"{name}-{bereich[2]}" + (f"-{bereich[3]}" if bereich[3] else "")
            var[name] = (m.group(2) or "").strip()
    if schemas:
        wahl = (var.get("farbschema") or "1").strip()
        wahl = str(int(wahl)) if wahl.isdigit() else wahl
        if wahl not in schemas:
            FARBSCHEMA_FEHLT[pfad] = wahl
            wahl = "1"
        FARBSCHEMA_NAME[pfad] = titel_schema.get(wahl, f"Farbschema {wahl}")
        var.update(schemas.get("1", {}))
        if wahl != "1":
            var.update(schemas[wahl])
    _CACHE[key] = (var, stw)
    return _CACHE[key]


class Ausgabe:
    """Welche Fassung (normal/uz) für welches Medium (bildschirm/druck/ebook) gebaut wird."""
    def __init__(self, var, fassung="normal", medium="bildschirm", privatdruck=False):
        self.var, self.fassung, self.medium, self.privatdruck = var, fassung, medium, privatdruck

    def tags(self):
        t = {self.fassung, self.medium}
        if self.medium == "druck":
            t.add("privatdruck" if self.privatdruck else "buch")
        return t

    def wert(self, name, standard=None):
        """Wert einer Variablen für diese Ausgabe. None = unbekannt.
        Reihenfolge: name-medium-fassung (Abschnitt «## Ausgabe: …»), name-medium, name,
        dann name-normal / name-uz."""
        name = name.lower()
        if name == "isbn" and self.medium == "druck" and self.privatdruck:
            return ""
        eigen = (f"{name}-{self.medium}-{self.fassung}", f"{name}-{self.medium}")
        for k in eigen:
            if k in self.var:
                return self.var[k]
        if name == "isbn":
            return "folgt" if self.medium == "druck" else ""
        if name in self.var:
            return self.var[name]
        if any(f"{name}-{m}" in self.var or f"{name}-{m}-{f}" in self.var
               for m in ("druck", "ebook", "bildschirm") for f in ("normal", "uz")):
            return ""
        if any(f"{name}-{t}" in self.var for t in ("normal", "uz")):
            if self.fassung == "uz":
                return self.var.get(f"{name}-uz", "")
            return self.var.get(f"{name}-normal", "")
        return standard

    def __call__(self, name, standard=""):
        w = self.wert(name)
        return standard if w in (None, "") else w

    def ersetze(self, text, wo=""):
        """{variable} einsetzen. Gibt None zurück, wenn eine Variable leer ist (Zeile fällt weg)."""
        leer = False

        def ein(m):
            nonlocal leer
            w = self.wert(m.group(1))
            if w is None:
                raise Fehler(f"{wo}: unbekannte Variable {{{m.group(1)}}}. "
                             "Bitte oben im Variablenblock eintragen.")
            if w == "":
                leer = True
            return w
        teile = re.split(r"(`[^`]+`)", text)         # in `Code` bleibt {name} stehen
        neu = "".join(x if x.startswith("`") and x.endswith("`") and len(x) > 1 else
                      re.sub(r"\{([A-Za-z][A-Za-z0-9-]*)\}", ein, x) for x in teile)
        return None if leer else neu


# --------------------------------------------------------------------------- Befehle (pureSATZ 3.0)
# Bauplan @[FASSUNG-]NAME[-GRÖSSE][-ORT[-HÖHE]][-STIL] Text – an dieser einen Stelle zerlegt (befehl), alle nutzen es.
FASSUNG = {"UC": "uz", "NORMAL": "normal", "N": "normal", "EBOOK": "ebook", "PRINT": "druck", "SCREEN": "bildschirm"}
NAMEN = ("DECORATE-LOGO", "DECORATE-TEXT", "DECORATE-PAGE", "DECORATE", "LOGO", "SPACER",
         "NEWPAGE", "PAGE-CENTER", "HEADER", "ASIDE", "QR-RIGHT", "QR", "BLOCK", "DRAFT", "NOTE", "KEEP-TOGETHER",
         "TIMELINE", "END", "PICTURE-CREDITS", "PICTURE", "TITLE", "IMPRINT", "NOTICE", "DEDICATION", "CONTENTS",
         "INDEX", "LIST-PICTURES", "LIST-TABLES", "BACK-COVER")
ORT = ("REST", "BOTTOM", "GAP", "RIGHT", "LEFT")
TITELEI = ("TITLE", "IMPRINT", "NOTICE", "DEDICATION", "CONTENTS", "INDEX", "LIST-PICTURES", "LIST-TABLES",
           "PICTURE-CREDITS", "BACK-COVER")
BEREICHE = ("BLOCK", "DRAFT", "NOTE", "KEEP-TOGETHER", "TIMELINE")     # … @END (dazu @UC usw. und @DECORATE-REST)
STIL = {"ITALIC": "zitat", "UPRIGHT": "aufrecht", "UPRIGHT MAIN": "blau"}   # Wert wie bei {decorate-stil}
BEFEHL_ZEILE = re.compile(r"^(#{1,6}\s+)?@([A-Z][A-Z0-9-]*)(?:\s+(.*))?$")


class Befehl:
    """Eine Befehlszeile, zerlegt: @UC-LOGO-8-BOTTOM-10 -> tag 'uz', name 'LOGO', zahl '8', ort 'BOTTOM', hoehe '10'."""
    def __init__(self, kopf, tag, name, rest, text=""):
        self.kopf, self.tag, self.name, self.rest, self.text = kopf, tag, name, rest, text
        self.zahl = self.ort = self.hoehe = None
        self.woerter = []
        self.nur = set()        # Fassung hinten (@DECORATE-REST-UC): nur die Gestaltung gilt dort, der Text überall

    def mm(self, standard):
        """Zahl im Namen (mm), sonst der Standard."""
        return float(self.zahl) if self.zahl else standard

    @property
    def bereich(self):
        """Beginnt einen Bereich (… @END)? @DECORATE-REST Satz ist ein Bereich mit einer Zeile."""
        return self.name in BEREICHE or (self.name == "DECORATE" and self.ort in ("REST", "BOTTOM"))

    @property
    def stil(self):
        """«zitat», «aufrecht», «blau» oder None (dann gilt {decorate-stil})."""
        return STIL.get(" ".join(w for w in self.woerter if w in ("ITALIC", "UPRIGHT", "MAIN")))

    def zeile(self, kopf=True):
        """Die Zeile ohne Fassung: «@UC-ASIDE Text» -> «@ASIDE Text»."""
        return (self.kopf if kopf else "") + "@" + self.rest + ((" " + self.text) if self.text else "")


def befehl(s, wo=""):
    """Zeile -> Befehl, oder None, wenn sie kein Befehl ist (Text, @@geschichte, @#tabelle, @PORTRAIT).
    Ein falscher Bauplan gibt einen Fehler mit Zeilennummer."""
    m = BEFEHL_ZEILE.match(s.strip())
    if not m:
        return None
    kopf, token, text = m.group(1) or "", m.group(2), (m.group(3) or "").strip()
    tag, rest = None, token
    for k, t in FASSUNG.items():
        if token == k:
            return Befehl(kopf, t, "", token, text)
        if token.startswith(k + "-"):
            tag, rest = t, token[len(k) + 1:]
    name = next((n for n in NAMEN if rest == n or rest.startswith(n + "-")), None)
    if name is None:
        return None
    b = Befehl(kopf, tag, name, rest, text)
    for w in [x for x in rest[len(name):].split("-") if x]:
        if re.fullmatch(r"\d+(?:[.,]\d+)?", w):
            z = w.replace(",", ".")
            if b.ort == "BOTTOM" and b.hoehe is None:
                b.hoehe = z
            elif b.zahl is None and b.ort is None:
                b.zahl = z
            else:
                raise Fehler(f"{wo}: @{token} – die Zahl {w} passt hier nicht.")
        elif w in ORT and b.ort is None:
            b.ort = w
        elif w in FASSUNG:
            b.nur.add(FASSUNG[w])
        else:
            b.woerter.append(w)
    _pruefe(b, token, wo)
    return b


def _pruefe(b, token, wo):
    def nein(was):
        raise Fehler(f"{wo}: @{token} – {was}.")
    n, w = b.name, b.woerter
    if b.nur and (n != "DECORATE" or b.tag):
        nein("die Fassung hinten gibt es nur bei @DECORATE (vorne: alles nur dort, hinten: nur die Verzierung)")
    if n in TITELEI and b.tag:
        nein("die Titelei gibt es ohne Fassung")
    elif n == "PICTURE" and b.ort not in (None, "RIGHT", "LEFT"):
        nein("ein Bild steht im Text, RIGHT oder LEFT")
    elif n == "BLOCK" and b.tag != "uz":
        nein("den Block gibt es nur als @UC-BLOCK")
    elif n == "DECORATE":
        st = " ".join(x for x in w if x in ("ITALIC", "UPRIGHT", "MAIN"))
        if any(x not in ("ABOVE", "ITALIC", "UPRIGHT", "MAIN") for x in w) or (st and st not in STIL):
            nein("unbekannter Teil (möglich: ABOVE, REST, BOTTOM-34, ITALIC, UPRIGHT, UPRIGHT-MAIN, am Ende UC oder NORMAL)")
        if b.ort not in ("REST", "BOTTOM"):
            if b.ort or "ABOVE" in w or st:
                nein("ABOVE und der Stil gehen (noch) nur mit REST oder BOTTOM")
            if not b.text:
                nein("Text fehlt (ohne Text: @DECORATE-LOGO)")
    elif n == "DECORATE-LOGO" and (b.zahl or b.ort or w):
        nein("die Grösse des Logos in der Linie kommt später")
    elif n == "DECORATE-TEXT" and (w or b.hoehe or b.ort not in (None, "BOTTOM")):
        nein("möglich: @DECORATE-TEXT Text oder @DECORATE-TEXT-BOTTOM Text")
    elif n == "LOGO":
        if w or b.hoehe:
            nein("möglich: @LOGO-12, @LOGO-10-BOTTOM, @LOGO-8-REST, @LOGO-6-GAP")
        if b.ort not in (None, "BOTTOM", "REST", "GAP"):
            nein("Ort: REST, BOTTOM oder GAP")


def _bis_end(roh, i, name, b):
    """Zeilen eines Bereichs bis @END: (Liste [(nr, zeile)], Index nach @END). Kein Bereich im Bereich."""
    nr = roh[i][0]
    inhalt, i = [], i + 1
    while i < len(roh):
        n2, z = roh[i]
        c = befehl(z, _wo(name, n2)) if z.lstrip().startswith("@") else None
        if c and c.name == "END":
            return inhalt, i + 1
        if c and (c.bereich or c.name == ""):
            raise Fehler(f"{_wo(name, nr)}: Bereich @{b.rest} wird nicht mit @END geschlossen "
                         f"(kein Bereich im Bereich, Zeile {n2}).")
        inhalt.append((n2, z)); i += 1
    raise Fehler(f"{_wo(name, nr)}: Bereich @{b.rest} wird nicht mit @END geschlossen.")


UMBRUCH_LINIE = re.compile(r"^\s*-{3,}\s*$")      # «---» = @NEWPAGE (Markdown)


def markdown_zeilen(roh):
    """Markdown-Schreibweisen vor dem Lesen umsetzen:
    «\\» am Zeilenende = Zeilenumbruch im Absatz (wie <br/>; die nächste Zeile gehört zum selben Absatz),
    eine Zeile «---» = neue Seite (wie @NEWPAGE)."""
    out, i, code = [], 0, im_code(roh)
    while i < len(roh):
        nr, s = roh[i]
        t = s.rstrip()
        if i in code:
            out.append((nr, t)); i += 1; continue
        while t.endswith("\\") and not t.endswith("\\\\") and i + 1 < len(roh) and roh[i + 1][1].strip():
            i += 1
            t = t[:-1].rstrip() + "<br/>" + roh[i][1].strip()
            t = t.rstrip()
        if UMBRUCH_LINIE.match(t):
            t = "@NEWPAGE"
        out.append((nr, t))
        i += 1
    return out


IMPRESSUM_KOPF = re.compile(r"^\s*(?:#{1,6}\s+)?@IMPRINT\s*$")
IMPRESSUM_VORLAGE = ["© {jahr} {autor}", "{website}", "", "{impressum-herstellung}", "{impressum-satz1}",
                     "{impressum-satz2}", "", "{impressum-rechte}", "", "{impressum-hinweis}", "",
                     "{impressum-kontakt}", "", "{auflage}", "ISBN {isbn}"]


def impressum_einsetzen(roh, a):
    """Leeres «## @IMPRINT»: der Motor setzt die Zeilen selbst ein (IMPRESSUM_VORLAGE).
    Zeilen mit einer Variablen, die das Buch nicht kennt, fallen weg."""
    out, code = [], im_code(roh)
    for i, (nr, s) in enumerate(roh):
        out.append((nr, s))
        if i in code or not IMPRESSUM_KOPF.match(s):
            continue
        naechste = next((z for _, z in roh[i + 1:] if z.strip()), "")
        if naechste and not naechste.lstrip().startswith(("#", "@")):
            continue                                    # eigene Zeilen unter @IMPRINT
        for v in IMPRESSUM_VORLAGE:
            if any(a.wert(n) is None for n in re.findall(r"\{([a-z][a-z0-9-]*)\}", v)):
                continue
            out.append((nr, v))
    return out


def zeilen(pfad, a, entwurf=False):
    """Text der Ausgabe a: Zeilen (str) und Bereiche als Tupel (NAME, titel, [zeilen]).
    NAME: BLOCK, DRAFT, NOTE, KEEP-TOGETHER, TIMELINE, DECORATE-REST (titel = der Befehl), PICTURE, CODE.
    @UC … @END usw. und die Vorsilbe @UC-… wählen die Fassung aus; danach steht der Befehl ohne Vorsilbe da."""
    name = os.path.basename(pfad)
    _, roh = lies(pfad)
    roh = impressum_einsetzen(markdown_zeilen(roh), a)
    out, i, offen = [], 0, None             # offen: Zeile, in der ein Bereich @UC … beginnt (wird gezeigt)
    while i < len(roh):
        nr, s = roh[i]
        s = s.rstrip()
        wo = _wo(name, nr)
        if s.lstrip().startswith(CODE_ZAUN):    # Code-Block: wörtlich, ohne Variablen
            inhalt, i = [], i + 1
            while i < len(roh) and not roh[i][1].lstrip().startswith(CODE_ZAUN):
                inhalt.append(_zeile(roh[i][1].rstrip(), roh[i][0])); i += 1
            if i >= len(roh):
                raise Fehler(f"{wo}: Code-Block wird nicht mit «{CODE_ZAUN}» geschlossen.")
            info = s.strip()[3:].strip()
            i += 1
            if info.lower().startswith("nur-"):          # «```nur-uz»: nur in dieser Ausgabe
                tag = info[4:].lower()
                info = ""
                if tag in TAGS and tag not in a.tags():
                    continue
            out.append(("CODE", info, inhalt))
            continue
        b = befehl(s, wo) if s.lstrip().startswith(("@", "#")) else None
        if b is None:
            z = a.ersetze(s, wo)
            if z is not None:
                out.append(_zeile(z, nr))
            i += 1
            continue
        if b.name == "":                        # @UC … @END: nur in dieser Fassung
            if offen is not None:
                raise Fehler(f"{wo}: @{b.rest} – kein Bereich im Bereich (offen seit Zeile {offen}).")
            if b.tag in a.tags():
                offen, i = nr, i + 1
            else:
                i = _bis_end(roh, i, name, b)[1]
            continue
        if b.name == "END":
            if offen is None:
                raise Fehler(f"{wo}: @END ohne Bereich.")
            offen = None
            out.append(_zeile("", -1))          # -1 = Bereichsende (zählt im Impressum nicht als Leerzeile)
            i += 1
            continue
        if b.name == "PICTURE" and b.kopf:      # «#### @PICTURE-60-RIGHT Titel» … bis zur ersten Leerzeile
            inhalt = ([_zeile("breite: " + b.zahl, nr)] if b.zahl else []) \
                + ([_zeile("fluss: " + ("rechts" if b.ort == "RIGHT" else "links"), nr)] if b.ort else [])
            i += 1
            while i < len(roh) and roh[i][1].strip() and not roh[i][1].lstrip().startswith(("#", "@")):
                n2, z = roh[i]
                z = z.strip()
                if z[:2] in ("- ", "* "):
                    z = z[2:].strip()
                z = a.ersetze(z, _wo(name, n2))
                if z is not None:
                    inhalt.append(_zeile(z, n2))
                i += 1
            if b.tag is None or b.tag in a.tags():
                out.append(("PICTURE", a.ersetze(b.text, wo) or "", inhalt))
            continue
        if b.bereich:
            if b.tag and offen is not None:
                raise Fehler(f"{wo}: @{b.rest} – kein Bereich im Bereich (offen seit Zeile {offen}).")
            if b.name == "DECORATE" and b.text:          # @DECORATE-REST Satz: ein Absatz
                teil, i = [(nr, b.text)], i + 1
            else:
                teil, i = _bis_end(roh, i, name, b)
            inhalt = [_zeile(z, n2) for n2, z in ((n2, a.ersetze(z.rstrip(), _wo(name, n2))) for n2, z in teil)
                      if z is not None]
            zeigen = b.tag is None or b.tag in a.tags()
            if b.name == "BLOCK":
                zeigen = a.fassung == "uz"
            if b.name == "NOTE":                        # Notiz an dich: nie gedruckt
                zeigen = zeigen and entwurf
            if not zeigen:
                continue
            if b.name == "DECORATE" and b.nur and not b.nur & a.tags():    # andere Fassung: gewöhnliche Absätze
                out += inhalt + [_zeile("", -1)]
                continue
            if b.name == "DECORATE":
                out.append(("DECORATE-REST", b, inhalt))
                continue
            titel = a.ersetze(b.text, wo) or ""
            if b.name == "DRAFT" and not entwurf:        # Druckfassung: offener Text wird normal gedruckt
                out += inhalt + [_zeile("", -1)]
                continue
            if b.name == "DRAFT" and not titel:
                titel = {"normal": "· nur normal", "uz": "· nur zweite Ausgabe"}.get(b.tag, "")
            out.append((b.name, titel, inhalt))
            continue
        if b.tag:                               # @UC-ASIDE Text: nur in dieser Fassung
            if offen is not None:
                raise Fehler(f"{wo}: @{b.tag.upper()}-… steht in einem Bereich, der schon nur für eine Fassung gilt.")
            if b.tag in a.tags():
                z = a.ersetze(b.zeile(), wo)
                if z is not None:
                    out.append(_zeile(z, nr))
                out.append(_zeile("", -1))
            i += 1
            continue
        if b.name == "DECORATE" and b.nur and not b.nur & a.tags():    # @DECORATE-UC Satz: hier ein Absatz
            s = b.text
        if b.kopf and b.name != "DECORATE-PAGE":         # «## @TITLE» wirkt wie «@TITLE»
            s = b.zeile(kopf=False)
        z = a.ersetze(s, wo)
        if z is not None:
            out.append(_zeile(z, nr))
        i += 1
    if offen is not None:
        raise Fehler(f"{_wo(name, offen)}: Bereich wird nicht mit @END geschlossen.")
    return out


def umschlag(pfad, a):
    """Umschlag-MD: {'vorderseite': [(schluessel, wert), …], 'rueckseite': […]}."""
    teile, akt, kommentar = {}, None, False
    for z in zeilen(pfad, a):
        if isinstance(z, tuple):
            raise Fehler(f"{os.path.basename(pfad)}: im Umschlag sind nur «::: nur-…»-Blöcke möglich.")
        s = z.strip()
        if kommentar or s.startswith("<!--"):        # <!-- Kommentar, auch über mehrere Zeilen -->
            kommentar = "-->" not in s
            continue
        if not s:
            continue
        if s.startswith("#"):                    # «# Vorderseite» oder «## Vorderseite»
            name = (s.lstrip("#").strip().lower().replace("ü", "ue").replace("ä", "ae").replace("ö", "oe")
                    .replace("buchruecken", "ruecken"))
            if name in UMSCHLAG_TEILE:
                akt = name; teile[akt] = []
            continue
        m = VARIABLE.match(s)
        if not m or akt is None:
            continue                            # Überschrift, «> Erklärung» oder erklärender Satz
        k, w = m.group(1), (m.group(2) or "").strip()
        basis, _, endung = k.rpartition("-")    # «fuss-druck: …» nur im Druck, «text-uz: …» nur zweite Ausgabe
        if basis and endung in TAGS:
            if endung not in a.tags():
                continue
            k = basis
        teile[akt].append((k, w))
    return teile


UMSCHLAG_TEILE = {"vorderseite", "ruecken", "rueckseite"}


UMSCHLAG_SCHLUESSEL = {"titel", "untertitel", "autor", "stempel", "stempel-farbe", "fuss", "bild",
                       "slogan", "foto", "text", "auszug"}


def eins(teil, k, standard=""):
    for kk, w in teil:
        if kk == k:
            return w
    return standard


def alle(teil, k):
    return [w for kk, w in teil if kk == k]


def pruefen(basis, text, umschlag_datei=None, finde=None, var=None):
    """Prüft die MD für alle Ausgaben: Variablen, Blöcke, Befehle, Teile, Fotos, Umschlag."""
    pfad = os.path.join(basis, text)
    if var is None:
        var, _ = lies(pfad)
    meldungen, hinweise = [], []
    for fassung in ("normal", "uz"):
        for medium, privat in (("bildschirm", False), ("druck", False), ("druck", True), ("ebook", False)):
            a = Ausgabe(var, fassung, medium, privat)
            for z in zeilen(pfad, a, entwurf=True):
                if isinstance(z, tuple):
                    if z[0] == "PICTURE":
                        for t in z[2]:
                            if t.strip().lower().startswith("datei:"):
                                d = t.strip()[6:].strip()
                                da = finde(d) if finde else os.path.exists(os.path.join(basis, "fotos", d))
                                if d and not da:
                                    hinweise.append(f"Zeile {t.nr}: Foto fehlt noch: fotos/{d} "
                                                    "(Entwurf: Vorschlags-Kasten, Druck: wird weggelassen)")
                    continue
                s = z.strip()
                if s.startswith("@#"):                     # Tabelle
                    import tabellen as T
                    for f in T.pruefe(basis, s):
                        meldungen.append(f"Zeile {z.nr}: {f}")
                    continue
                if s.startswith("@"):
                    wort = s.split()[0]
                    if wort == "@PICTURE" or wort.startswith("@PICTURE-") and wort != "@PICTURE-CREDITS":
                        meldungen.append(f"Zeile {z.nr}: ein Bild beginnt mit «#### {wort} Titel»")
                    elif wort != "@PORTRAIT" and befehl(s, f"Zeile {z.nr}") is None:
                        meldungen.append(f"Zeile {z.nr}: unbekannter Befehl {wort}")
                    elif wort == "@PORTRAIT":
                        d = s[10:].partition("|")[0].strip()
                        if not (finde(d) if finde else os.path.exists(os.path.join(basis, d))):
                            meldungen.append(f"Zeile {z.nr}: Bild fehlt: {d}")
                elif s.startswith("# ") and "|" in s and s.count("|") not in (2, 3):
                    meldungen.append(f"Zeile {z.nr}: Teil braucht die Form «# Teil 1|Titel|Untertitel» "
                                     "(oder mit Bild: «…|Untertitel|bild.jpg»)")
            if umschlag_datei and os.path.exists(os.path.join(basis, umschlag_datei)):
                for teil in umschlag(os.path.join(basis, umschlag_datei), a).values():
                    for k, _ in teil:
                        if k not in UMSCHLAG_SCHLUESSEL:
                            meldungen.append(f"{umschlag_datei}: unbekannter Schlüssel «{k}». Möglich: "
                                             + ", ".join(sorted(UMSCHLAG_SCHLUESSEL)))
    try:                                          # Geschichten: nicht oder doppelt eingebunden
        import geschichten as G
        if os.path.isdir(G.ordner(basis)):
            benutzt = [n for _, n in G.verweise(pfad)]
            for n in sorted(set(benutzt)):
                if benutzt.count(n) > 1:
                    hinweise.append(f"Geschichte @@{n} ist {benutzt.count(n)}× eingebunden.")
            frei = [n for n in G.alle(basis) if n not in benutzt]
            if frei:
                hinweise.append(f"Noch nicht im Buch ({len(frei)}): " + ", ".join("@@" + n for n in frei))
    except SystemExit as e:
        meldungen.append(str(e))
    try:                                          # Aufzählung: einzelne Zeile «3. Mai …» = wohl keine
        roh = open(pfad, encoding="utf-8").read().split("\n")
        ist = lambda z: bool(re.match(r"^ *(-|\d{1,3}\.)\s", z))
        for i, z in enumerate(roh):
            m = re.match(r"^(\d{1,3})\.\s", z)
            if not m or m.group(1) == "1":
                continue
            vor = next((roh[j] for j in range(i - 1, -1, -1) if roh[j].strip()), "")
            nach = next((roh[j] for j in range(i + 1, len(roh)) if roh[j].strip()), "")
            nachbarn = [vor, nach]
            if not any(ist(n) for n in nachbarn):
                hinweise.append(f"Zeile {i + 1}: «{z[:30]}…» wird als Aufzählung gesetzt. Normaler Text? "
                                f"Dann {m.group(1)}\\. schreiben.")
    except OSError:
        pass
    try:                                          # 3.0: Buch noch in der alten Schreibweise?
        import umbenennen as U
        alt = open(pfad, encoding="utf-8").read()
        if U.umstellen(alt) != alt:
            hinweise.append("alte Schreibweise (vor 3.0) – geht weiter. Umstellen: Menü um")
    except (ImportError, OSError):
        pass
    meldungen = list(dict.fromkeys(meldungen))
    for h in dict.fromkeys(hinweise):
        print("Hinweis: " + h)
    if meldungen:
        raise Fehler(f"{text}:\n  " + "\n  ".join(meldungen))
    print(f"Prüfung {text}: in Ordnung.")


if __name__ == "__main__":
    import sys
    if sys.argv[1:2] == ["pruefen"]:
        import build
        pruefen(build.BASE, build.TEXT, build.UMSCHLAG, build.finde, build.alle_variablen())
    else:
        print(__doc__)
        print("Befehle: " + " ".join("@" + n for n in NAMEN) + " · Fassung: " + " ".join("@" + f for f in FASSUNG))
