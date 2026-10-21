"""
Gemeinsamer Leser für das Manuskript (Buch-MD) und den Umschlag (Umschlag-MD).
Wird von build.py, build-broschuere.py und build-epub.py verwendet.

Aufbau der Buch-MD
------------------
1. Einstellungen oben, bis zur Überschrift «# BUCHSTART»:
       # VARIABLEN
       ## Buch
       - titel: Leben 1.0, 2.0, 3.0
       - untertitel-normal: Meine Reise …
       - untertitel-uz: Meine ganze Lebensreise …
       # BUCHSTART
   Überschriften und Sätze dazwischen sind Erklärungen. (Alte Form: Block zwischen «---».)
   Im Text: {titel}, {untertitel} … Gibt es «name-normal» und «name-uz», nimmt {name}
   automatisch den Wert der gebauten Fassung. Fehlt eine der beiden Varianten, ist sie leer.
   {isbn} ist besonders: im Druck isbn-buch (leer = «folgt»), im E-Book isbn-ebook.
   Eine Zeile, in der eine Variable leer bleibt, fällt ganz weg.

2. Blöcke  ::: art[-ausgabe] [Titel]  …  :::
   art:     nur, mitte, foto, offen, offen-notiz, zusammen, widmung, zeitstrahl,
            uz (heller Kasten der zweiten Ausgabe; «dc» geht auch)
   ausgabe: normal, uz (oder dc), bildschirm, druck, ebook, buch (Druck mit ISBN), privatdruck
   Ohne Endung erscheint der Block in allen Ausgaben.
"""
import os
import re

# Endungen der Blöcke und Variablen
TAGS = ("normal", "uz", "bildschirm", "druck", "ebook", "buch", "privatdruck")
ALT = {"v2": "normal", "offiziell": "normal", "dc": "uz"}   # andere Namen (::: nur-v2, ::: foto-dc …)
ARTEN = {"nur": None, "mitte": "MITTE", "foto": "FOTO", "platzhalter": "PH", "offen-notiz": "PH",
         "offen": "OFFEN", "zusammen": "ZUSAMMEN", "widmung": "WIDMUNG", "zeitstrahl": "ZEITSTRAHL",
         "uz": "UZ", "dc": "UZ"}


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


def _geschichten_einsetzen(pfad, zeilen_mit_nr):
    """Zeilen «@@name» durch die Geschichte geschichten/name.md ersetzen (pureSATZ 2.11).
    Ohne @@-Zeilen bleibt alles, wie es war."""
    import geschichten as G
    if not any(G.VERWEIS.match(z) for _, z in zeilen_mit_nr):
        return zeilen_mit_nr
    basis = os.path.dirname(os.path.abspath(pfad))
    vorhanden = G.alle(basis)
    sammlung = os.environ.get("BUCH_SAMMLUNG") == "1"
    out = []
    for nr, z in zeilen_mit_nr:
        m = G.VERWEIS.match(z)
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


VARIABLE = re.compile(r"^\s*(?:[-*]\s+)?([a-z][a-z0-9-]*)\s*:(?:\s+(.*?))?\s*$")
BUCHSTART = re.compile(r"^#{1,6}\s*=*\s*BUCHSTART\b", re.I)
BEFEHL_ALS_TITEL = re.compile(r"^#{1,6}\s+(@[A-Z].*)$")     # «## @TITEL» = «@TITEL»


def ist_buchstart(zeile):
    return bool(BUCHSTART.match(zeile.strip()))


def lies(pfad):
    """(variablen, [(nr, zeile)]) – Einstellungen oben, danach der Text mit Zeilennummern.

    Neue Form:  alles vor «# BUCHSTART» sind Einstellungen. Jede Zeile «- name: wert» (oder
                «name: wert») ist eine Variable; Überschriften und Sätze sind Erklärungen.
    Alte Form:  Variablenblock zwischen zwei Zeilen «---» ganz oben."""
    if pfad in _CACHE:
        return _CACHE[pfad]
    roh = open(pfad, encoding="utf-8").read().split("\n")
    var, start = {}, 0
    bs = next((i for i, z in enumerate(roh) if ist_buchstart(z)), None)
    if bs is not None:
        bereich, start = range(0, bs), bs + 1
    elif roh and roh[0].strip() == "---":
        ende = next((i for i in range(1, len(roh)) if roh[i].strip() == "---"), None)
        if ende is None:
            raise Fehler(f"{os.path.basename(pfad)}: Variablenblock oben wird nicht mit «---» geschlossen.")
        bereich, start = range(1, ende), ende + 1
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


def lies_variablen(pfad):
    """Variablen-Datei (<buch>-variablen.md): (variablen, stichworte).
    Jede Zeile «- name: wert» ist eine Variable. Unter einer Überschrift «STICHWORTE» ist jede
    Listenzeile ein Stichwort («- Seele | Seelen»). Überschriften und Sätze sind Erklärungen."""
    key = ("V", pfad)
    if key in _CACHE:
        return _CACHE[key]
    var, stw, in_stw = {}, [], False
    for z in open(pfad, encoding="utf-8").read().split("\n"):
        t = z.strip()
        if not t or t.startswith(("<!--", ">")):
            continue
        if t.startswith("#"):
            stufe = len(t) - len(t.lstrip("#"))
            if "STICHWORTE" in t.upper().lstrip("# "):
                in_stw, stw_stufe = True, stufe
            elif in_stw and stufe <= stw_stufe:
                in_stw = False
            continue
        if in_stw:
            if t.startswith(("- ", "* ")):
                stw.append(t[2:].strip())
            continue
        m = VARIABLE.match(t)
        if m:
            var[m.group(1)] = (m.group(2) or "").strip()
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
        """Wert einer Variablen für diese Ausgabe. None = unbekannt."""
        name = name.lower()
        if name == "isbn":
            if self.medium == "druck":
                return "" if self.privatdruck else (self.var.get("isbn-buch") or "folgt")
            return self.var.get("isbn-ebook", "") if self.medium == "ebook" else ""
        if name in self.var:
            return self.var[name]
        if any(f"{name}-{t}" in self.var for t in ("normal", "uz", "dc")):
            if self.fassung == "uz":
                return self.var.get(f"{name}-uz", self.var.get(f"{name}-dc", ""))
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
        neu = re.sub(r"\{([A-Za-z][A-Za-z0-9-]*)\}", ein, text)
        return None if leer else neu


def _art(kopf):
    """'foto-uz Titel' -> ('foto', 'uz', 'Titel')"""
    art, _, titel = kopf.strip().partition(" ")
    art = art.lower()
    tag = None
    if "-" in art:
        basis, _, t = art.rpartition("-")
        t = ALT.get(t, t)
        if t in TAGS and basis in ARTEN:
            art, tag = basis, t
    if art not in ARTEN:
        return None, None, titel
    return art, tag, titel.strip()


def zeilen(pfad, a, entwurf=False):
    """Text der Ausgabe a: Zeilen (str) und Blöcke als Tupel (ART, titel, [zeilen])."""
    name = os.path.basename(pfad)
    _, roh = lies(pfad)
    out, i = [], 0
    while i < len(roh):
        nr, s = roh[i]
        s = s.rstrip()
        if s.startswith(":::") and s.strip() != ":::":
            art, tag, titel = _art(s[3:])
            if art is None:
                raise Fehler(f"{_wo(name, nr)}: unbekannter Block «{s}».")
            inhalt, i = [], i + 1
            while i < len(roh) and roh[i][1].strip() != ":::":
                n2, z = roh[i]
                if z.strip().startswith(":::"):
                    raise Fehler(f"{_wo(name, nr)}: Block «{s}» wird nicht mit «:::» geschlossen.")
                z = a.ersetze(z.rstrip(), f"{_wo(name, n2)}")
                if z is not None:
                    inhalt.append(_zeile(z, n2))
                i += 1
            if i >= len(roh):
                raise Fehler(f"{_wo(name, nr)}: Block «{s}» wird nicht mit «:::» geschlossen.")
            i += 1
            zeigen = tag is None or tag in a.tags()
            if art in ("uz", "dc"):
                zeigen = a.fassung == "uz"
            if art in ("platzhalter", "offen-notiz"):     # Notiz an dich: nie gedruckt
                zeigen = zeigen and entwurf
            if not zeigen:
                continue
            titel = a.ersetze(titel, f"{_wo(name, nr)}") or ""
            if art == "offen" and not entwurf:            # Druckfassung: offener Text wird normal gedruckt
                art = "nur"
            elif art == "offen" and not titel:
                titel = {"normal": "· nur normal", "uz": "· nur zweite Ausgabe"}.get(tag, "")
            if art == "nur":
                out += inhalt + [_zeile("", -1)]    # -1 = Blockende (zählt im Impressum nicht als Leerzeile)
            else:
                out.append((ARTEN[art], titel, inhalt))
            continue
        m = BEFEHL_ALS_TITEL.match(s)
        if m:                                   # «## @TITEL» wirkt wie «@TITEL»
            s = m.group(1)
        z = a.ersetze(s, f"{_wo(name, nr)}")
        if z is not None:
            out.append(_zeile(z, nr))
        i += 1
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
        if s.startswith("# "):
            akt = (s[2:].strip().lower().replace("ü", "ue").replace("ä", "ae").replace("ö", "oe")
                   .replace("buchruecken", "ruecken"))
            teile[akt] = []
            continue
        m = VARIABLE.match(s)
        if not m or akt is None:
            continue                            # Überschrift oder erklärender Satz
        teile[akt].append((m.group(1), (m.group(2) or "").strip()))
    return teile


UMSCHLAG_SCHLUESSEL = {"titel", "untertitel", "autor", "stempel", "stempel-farbe", "fuss", "bild",
                       "slogan", "foto", "text", "auszug"}


def eins(teil, k, standard=""):
    for kk, w in teil:
        if kk == k:
            return w
    return standard


def alle(teil, k):
    return [w for kk, w in teil if kk == k]


# --------------------------------------------------------------------------- Befehle
# Alle @-Befehle der Buch-MD an einer Stelle (für Prüfung und Hilfe).
BEFEHLE = {
    "@TITEL":              "Titelseite; die nächsten Zeilen: Titel, Untertitel",
    "@IMPRESSUM":          "Impressum; die folgenden Zeilen (Leerzeile = Abstand)",
    "@WIDMUNG":            "Widmung direkt unter dem Impressum; die folgenden Zeilen (oder ::: widmung)",
    "@KERNSATZ":           "@KERNSATZ Satz – allein, mittig auf einer Seite",
    "@INHALTSVERZEICHNIS": "Inhaltsverzeichnis an dieser Stelle",
    "@ZITAT":              "@ZITAT Text – Zitat, zentriert, ohne Lotus",
    "@MOTTO":              "@MOTTO Text – Seite mit einem Satz in der Mitte",
    "@UNTEN":              "@UNTEN Text – kursiv unten auf die Seite",
    "@KOPF":               "@KOPF Text – Kopfzeile ersetzen; @KOPF allein beendet es",
    "@PLATZ":              "@PLATZ 40 – neue Seite, wenn weniger als 40 mm Platz bleibt",
    "@UMBRUCH":            "neue Seite",
    "@UMBRUCH-RECHTS":     "neue Seite, im Druck immer eine rechte Seite (z. B. vor einem Kapitel)",
    "@ABSTAND":            "@ABSTAND 8 – 8 mm Leerraum",
    "@SEITENMITTE":        "Inhalt dieser Seite senkrecht zentrieren",
    "@ZIER":               "@ZIER 12 – kleine Verzierung, zentriert (Breite in mm; Bild: Variable «zier»)",
    "@ZIER-UNTEN":         "@ZIER-UNTEN 10 – Verzierung unten auf die Seite, danach neue Seite",
    "@ZIER-TRENNER":       "kleine Verzierung in die Lücke vor der nächsten Überschrift",
    "@LOTUS":              "(gleich wie @ZIER)",
    "@LOTUS-UNTEN":        "(gleich wie @ZIER-UNTEN)",
    "@LOTUS-TRENNER":      "(gleich wie @ZIER-TRENNER)",
    "@QR":                 "@QR https://… | Text – QR-Code mit Link",
    "@QR-PAAR":            "@QR-PAAR url | Text ;; url | Text – zwei QR-Codes nebeneinander",
    "@PORTRAIT":           "@PORTRAIT bild.png | Bildtext – rundes Foto mit Ring",
    "@STICHWORTE":         "Stichwortverzeichnis (Liste: stichworte.txt)",
    "@BILDNACHWEIS":       "Bildnachweis (Fotos mit «quelle:»); ohne Zeile automatisch vor den Stichworten",
    "@RUECKSEITE":         "Rückseite (nur Bildschirm-PDF)",
    "@@name":              "Geschichte geschichten/name.md einbinden (eigene Zeile)",
    "@#name":              "Tabelle tabellen/name.csv einbinden; «@#name quer» / «@#name hoch» = Ausrichtung",
    "@ANHANG":             "(alt) wie «# Titel»",
}


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
                    if z[0] == "FOTO":
                        for t in z[2]:
                            if t.strip().lower().startswith("datei:"):
                                d = t.strip()[6:].strip()
                                da = finde(d) if finde else os.path.exists(os.path.join(basis, "fotos", d))
                                if d and not da:
                                    hinweise.append(f"Zeile {t.nr}: Foto fehlt noch: fotos/{d} "
                                                    "(Entwurf: Vorschlags-Kasten, Druck: wird weggelassen)")
                    continue
                s = z.strip()
                if s.startswith("@#"):                     # Tabelle (pureSATZ 2.12)
                    import tabellen as T
                    for f in T.pruefe(basis, s):
                        meldungen.append(f"Zeile {z.nr}: {f}")
                    continue
                if s.startswith("@"):
                    befehl = s.split()[0]
                    if befehl not in BEFEHLE:
                        meldungen.append(f"Zeile {z.nr}: unbekannter Befehl {befehl}")
                    elif befehl == "@PORTRAIT":
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
    try:                                          # Geschichten (pureSATZ 2.11): nicht oder doppelt eingebunden
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
    try:                                          # Aufzählung (2.16): einzelne Zeile «3. Mai …» = wohl keine
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
        print("Befehle:")
        for k, v in BEFEHLE.items():
            print(f"  {k:22} {v}")
