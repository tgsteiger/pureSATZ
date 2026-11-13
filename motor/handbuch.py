#!/usr/bin/env python3
"""
handbuch.py – das Buch «pureSATZ Handbuch» aus der Hilfe erzeugen (ab 2.76).

Einmal anlegen (Buchordner neben pureSATZ):
    sh setup/setup.sh handbuch/handbuch.txt             im Ordner pureSATZ
    cd ../pureSATZ-Handbuch && sh build.sh handbuch     schaltet {buch-aus-hilfe}: ja ein und baut
Danach macht jeder Bau («sh build.sh …», Menü) die Buch-MD neu aus der Hilfe. Nicht von Hand ändern –
Korrekturen in den Quellen (Ordner pureSATZ):
    START.md, motor/HILFE.md                 die Kapitel (Gruppen = Teile, Abschnitte = Kapitel)
    handbuch/einleitung.md                   Einleitung (nur im Buch)
    handbuch/stichworte.txt                  Stichwortverzeichnis
    INSTALLATION.md, LIZENZ.md               Anhang
Spickzettel, Befehle, Blöcke und Buchformate kommen direkt aus dem Motor.
Im Buch fallen weg: «Meine Hilfe», «Variablen dieses Buchs» und Text in «::: nur-webhilfe» … «:::».
Text in «::: nur-handbuch» … «:::» steht nur im Buch. Tabellen werden zu tabellen/h-NNN.csv.
"""
import csv
import glob
import io
import os
import re
import sys
import unicodedata

MOTOR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, MOTOR)
import hilfe as H          # noqa: E402

SCHALTER = re.compile(r"^\s*\{buch-aus-hilfe\}\s*:\s*ja\b", re.I | re.M)
ZAUN = "`" * 3
LISTE = re.compile(r"^\s*(?:[-*]|\d+\.)\s+\S")
UNTERTITEL = {"Erste Schritte": "Vom ersten PDF zum eigenen Buch", "Schreiben": "Text, Bilder, Tabellen, Geschichten",
              "Gestalten": "Seiten, Farben, Verzeichnisse", "Bauen und Drucken": "Vom Buchblock zur Druckerei",
              "E-Book": "Für tolino, Kindle und andere", "Werkzeuge": "Sichern, abgleichen, mit KI arbeiten",
              "Nachschlagen": "Befehle, Blöcke, Begriffe"}
WEG = ("Meine Hilfe", "Variablen dieses Buchs")
ZEICHEN = {"→": "›", "←": "‹", "↔": "‹›", "↑": "Pfeil hoch", "↓": "Pfeil runter", "↵": "Enter", "─": "–",
           "▶": "Play", "♀": "w", "♂": "m", "✎ ": "", "✎": "", "✔": "ja", "✗": "x",
           "💾 ": "", "📋 ": "", "🗑 ": "", "💾": "", "📋": "", "🗑": ""}   # fehlen in Lora und Poppins


def zeichen(t, nur_emoji=False):
    """Zeichen, die Lora und Poppins nicht haben, ersetzen (Code-Blöcke in DejaVu Sans Mono: nur Emojis)."""
    for a, b in ZEICHEN.items():
        if not nur_emoji or ord(a[0]) > 0xFFFF:
            t = t.replace(a, b)
    return t


def variablen_datei(basis):
    d = sorted(glob.glob(os.path.join(basis, "*-variablen.md")))
    return d[0] if d else None


def aktiv(basis):
    """Ist dieser Buchordner das Handbuch ({buch-aus-hilfe}: ja)?"""
    v = variablen_datei(basis)
    return bool(v and SCHALTER.search(open(v, encoding="utf-8").read()))


def einschalten(basis):
    """{buch-aus-hilfe}: ja in die Variablen-Datei schreiben (einmalig, bei «sh build.sh handbuch»)."""
    v = variablen_datei(basis)
    if not v:
        raise SystemExit("Handbuch: keine Variablen-Datei (*-variablen.md) – zuerst das Buch anlegen: "
                         "im Ordner pureSATZ «sh setup/setup.sh handbuch/handbuch.txt».")
    t = open(v, encoding="utf-8").read()
    if not SCHALTER.search(t):
        try:                                       # Druckdatei aus handbuch/handbuch.txt (DRUCK = …)
            werte = dict(re.findall(r"^\s*([A-Z_]+)\s*=\s*(.*?)\s*$", _lies(os.path.join(quelle(basis), "handbuch",
                                                                                     "handbuch.txt")), re.M))
        except SystemExit:
            werte = {}
        d = werte.get("DRUCK", "")
        if d and os.path.exists(os.path.join(basis, "druck", d + ".md")):
            t = re.sub(r"^(\{druck-datei\}:).*$", rf"\1 {d}", t, count=1, flags=re.M)
            print(f"Handbuch: Druckdatei {d}.")
        t = re.sub(r"^\s*\{buch-aus-hilfe\}\s*:.*\n?", "", t, flags=re.M | re.I)
        t = t.rstrip("\n") + ("\n\n## Handbuch\n{buch-aus-hilfe}: ja\n"
                              "> {buch-aus-hilfe}: ja = die Buch-MD entsteht bei jedem Bau neu aus der Hilfe von pureSATZ "
                              "(motor/handbuch.py) – nicht von Hand ändern\n")
        open(v, "w", encoding="utf-8").write(t)
        print(f"Handbuch: {os.path.basename(v)} – {{buch-aus-hilfe}}: ja eingetragen.")


def quelle(basis):
    p = os.path.normpath(os.path.join(basis, "..", "pureSATZ"))
    if not (os.path.exists(os.path.join(p, "START.md")) and os.path.isdir(os.path.join(p, "handbuch"))):
        raise SystemExit("Handbuch: Ordner pureSATZ (mit START.md und handbuch/) nicht gefunden – "
                         f"er muss neben dem Buchordner liegen: {p}")
    return p


def _lies(p):
    return open(p, encoding="utf-8").read().replace("\r\n", "\n") if os.path.exists(p) else ""


# --------------------------------------------------------------------------- Markdown zerlegen
def abschnitte(text, standard):
    """Markdown → [(gruppe, [(titel, md)])], getrennt an «# Gruppe» und «## Abschnitt» (nicht in Code-Blöcken)."""
    gruppen, akt, code = [], None, False
    for z in text.split("\n"):
        if z.lstrip().startswith(ZAUN):
            code = not code
        m = None if code or z.lstrip().startswith(ZAUN) else re.match(r"^(#{1,2})\s+(.*)$", z)
        if m and len(m.group(1)) == 1:                 # Text direkt unter «# Gruppe»: Abschnitt mit ihrem Namen
            akt = [m.group(2).strip(), []]; gruppen.append((akt[0], [akt])); continue
        if m:
            if not gruppen:
                gruppen.append((standard, []))
            akt = [m.group(2).strip(), []]; gruppen[-1][1].append(akt); continue
        if akt is not None:
            akt[1].append(z)
    return [(g, [(t, "\n".join(z).strip("\n")) for t, z in a if "\n".join(z).strip()]) for g, a in gruppen]


def k(t):
    """Schlüssel wie in hilfe.html (Links per Abschnittsname)."""
    t = "".join(c for c in unicodedata.normalize("NFD", t.lower()) if unicodedata.category(c) != "Mn")
    t = t.replace("ae", "a").replace("oe", "o").replace("ue", "u").replace("ß", "ss")
    return re.sub(r"[^a-z0-9]+", "", t)


def kurz(titel):
    """«Hörbuch: Ablauf» → «Ablauf» (im Teil Hörbuch)."""
    return re.sub(r"^Hörbuch:\s*", "", titel)


class Umsetzer:
    """Hilfe-Markdown → Buch-Markdown (pureSATZ)."""

    def __init__(self, basis, titel):
        self.basis, self.titel, self.nr = basis, titel, 0
        self.ordner = os.path.join(basis, "tabellen")
        os.makedirs(self.ordner, exist_ok=True)
        for alt in glob.glob(os.path.join(self.ordner, "h-*.csv")):
            os.remove(alt)

    def verweis(self, text, anker):
        ziel = next((t for t in self.titel if k(anker) in k(t)), None)
        if not ziel:
            return text
        ziel = kurz(ziel)
        if text.lstrip().startswith(("→", "←")):
            return f"→ «{ziel}»"
        return f"«{ziel}»" if k(text) in k(ziel) else f"{text} (→ «{ziel}»)"

    def inline(self, t):
        teile = re.split(r"(`[^`]*`)", t)
        for j, x in enumerate(teile):
            if x.startswith("`") and x.endswith("`") and len(x) > 1:
                continue
            x = re.sub(r"\[([^\]]+)\]\(#([^)\s]+)\)", lambda m: self.verweis(m.group(1), m.group(2)), x)
            x = re.sub(r"(?<![\w*])\*([^*\s][^*]*?)\*(?![\w*])", r"\1", x)      # *kursiv* → normal
            x = re.sub(r"\s*\{⏱[^}]*\}", "", x)                                 # Dauer im Fahrplan
            x = re.sub(r"^(\s*(?:[-*]|\d+\.)\s+)\[[ xX]\]\s+", r"\1", x)        # «- [ ] » → «- »
            teile[j] = x
        return "".join(teile)

    def tabelle(self, kopf, reihen):
        self.nr += 1
        name = f"h-{self.nr:03d}"
        if not any(c.strip() for c in kopf) and reihen:     # Tabelle ohne Überschriften: erste Zeile nimmt ihren Platz
            kopf, reihen = reihen[0], reihen[1:]
        zell = lambda r: [zeichen(self.inline(c.replace("\\|", "|"))) for c in r]
        puffer = io.StringIO()
        w = csv.writer(puffer, delimiter=";", lineterminator="\n")
        puffer.write("sep=;\n\n")                     # Zeile 1 leer = Tabelle ohne Titel
        w.writerow(zell(kopf))
        for r in reihen:
            w.writerow(zell(r + [""] * (len(kopf) - len(r)))[:len(kopf)])
        open(os.path.join(self.ordner, name + ".csv"), "w", encoding="utf-8").write(puffer.getvalue())
        return f"@#{name} hoch"

    def md(self, text):
        out, z, i, code, bloecke = [], text.split("\n"), 0, False, []
        zell = lambda r: [c.strip() for c in re.split(r"(?<!\\)\|", r.strip().strip("|"))]
        while i < len(z):
            s = z[i].strip()
            if s.startswith(ZAUN):
                code = not code
                out.append(ZAUN if code else ZAUN); i += 1; continue
            if code:
                out.append(zeichen(z[i].rstrip(), nur_emoji=True)); i += 1; continue
            if s == "::: nur-webhilfe":
                while i < len(z) and z[i].strip() != ":::":
                    i += 1
                i += 1; continue
            if s in ("::: nur-handbuch", "::: kacheln"):
                bloecke.append(s); i += 1; continue
            if s == ":::" and bloecke:
                bloecke.pop(); i += 1; continue
            if s in ("---", "***"):
                i += 1; continue
            if s.startswith("|") and i + 1 < len(z) and re.match(r"^\|[\s:|-]+\|$", z[i + 1].strip()):
                kopf, i, reihen = zell(s), i + 2, []
                while i < len(z) and z[i].strip().startswith("|"):
                    reihen.append(zell(z[i])); i += 1
                out += ["", self.tabelle(kopf, reihen), ""]; continue
            if (z[i].startswith("  ") and s and out and LISTE.match(out[-1])
                    and not LISTE.match(z[i])):              # Fortsetzung eines Listenpunkts: an ihn anhängen
                out[-1] += " " + zeichen(self.inline(s))
                i += 1; continue
            out.append(zeichen(self.inline(z[i].rstrip()))); i += 1
        return "\n".join(out).strip("\n")


# --------------------------------------------------------------------------- Teile aus dem Motor
def _md_tabelle(kopf, reihen):
    zelle = lambda t: str(t).replace("|", "\\|")
    return "\n".join(["| " + " | ".join(kopf) + " |", "|" + "---|" * len(kopf)]
                     + ["| " + " | ".join(zelle(x) for x in r) + " |" for r in reihen])


def motor_teile():
    import manuskript as M
    teile = [("Spickzettel", "Die häufigsten Befehle im Buchordner (Windows: `build.bat` statt `sh build.sh`).\n\n"
              + _md_tabelle(["Befehl", "Wofür"], [(f"`{b}`", t) for b, t in H.SPICKZETTEL]))]
    b = ["Jeder Befehl steht auf einer eigenen Zeile, genau so geschrieben (GROSS). `## @TITEL` wirkt wie `@TITEL`.",
         "", "### Seite sieht nicht gut aus? – Lösungen", "",
         _md_tabelle(["Problem", "Lösung"], H.LOESUNGEN)]
    gezeigt = set()
    for titel, eintraege in H.BEFEHL_GRUPPEN:
        reihen = []
        for e in eintraege:
            if isinstance(e, tuple):
                reihen.append((f"`{e[0]}`", e[1]))
            elif e in M.BEFEHLE:
                reihen.append((f"`{M.BEFEHLE[e][0]}`", M.BEFEHLE[e][1])); gezeigt.add(e)
        b += ["", f"### {titel}", "", _md_tabelle(["Schreibweise", "Wirkung"], reihen)]
    teile.append(("Befehle (@)", "\n".join(b)))
    teile.append(("Blöcke (:::)", "Ein Block beginnt mit `::: art` und endet mit einer Zeile `:::`.\n\n"
                  + _md_tabelle(["Block", "Wirkung"], [(f"`{a}`", w) for a, w in H.BLOECKE])))
    quelle_ = _lies(os.path.join(MOTOR, "build.py"))
    f = re.findall(r'^\s*"([a-z0-9]+)":\s*dict\(name="([^"]+)",\s*seite=\((\d+),\s*(\d+)\).*?rand=\((\d+),\s*(\d+),'
                   r'\s*(\d+),\s*(\d+)\),\s*text=\(([\d.]+),', quelle_, re.M)
    if f:
        teile.append(("Buchformate", "In der Variablen-Datei: `{format}: a5` oder ein eigenes Mass `{format}: 150 x 215` "
                      "(mm). Ränder und Schrift rechnet der Motor selbst.\n\n" + _md_tabelle(
                          ["format", "Name", "Seite", "Textbreite", "Schrift"],
                          [(f"`{a}`", n, f"{b_} × {h} mm", f"{int(b_) - int(ri) - int(ra)} mm", f"{pt} pt")
                           for a, n, b_, h, ri, ra, _, _, pt in f])))
    netz = [("Webseite", H.WEBSEITE), ("GitHub", H.GITHUB), ("Fehler melden, Fragen", H.GITHUB + "/issues"),
            ("Lizenz", H.GITHUB + "/blob/main/LIZENZ.md")]
    teile.append(("pureSATZ im Netz", _md_tabelle(["Was", "Adresse"], [(n, u.replace("https://", "")) for n, u in netz])
                  + "\n\nNeuen Motor holen: `sh update.sh` (holt ihn von GitHub, ohne Konto)."))
    return teile


# --------------------------------------------------------------------------- Buch-MD schreiben
def erzeuge(basis):
    ps = quelle(basis)
    version = _lies(os.path.join(MOTOR, "VERSION")).strip()
    gruppen = abschnitte(_lies(os.path.join(ps, "START.md")), "Erste Schritte")
    gruppen += abschnitte(_lies(os.path.join(ps, "motor", "HILFE.md")), "Schreiben")
    gruppen.insert(0, ("Nachschlagen", motor_teile()))          # Motor-Teile vor «Tipps aus der Praxis»
    gruppen = [(g, [(t, h) for t, h in a if t not in WEG]) for g, a in H.zusammen(gruppen)
               if not g.startswith(("Meine Hilfe", "Einrichten"))]
    alle_titel = [t for _, a in gruppen for t, _ in a]
    u = Umsetzer(basis, alle_titel)

    out = ["## @TITEL", "{titel}", "{untertitel}", "", "## @IMPRESSUM", "", "## @INHALTSVERZEICHNIS", ""]
    ein = _lies(os.path.join(ps, "handbuch", "einleitung.md")).replace("{version}", version)
    ein = "\n".join(z for z in ein.split("\n") if not z.startswith(">"))
    for g, a in abschnitte(ein, "Einleitung"):
        out += [f"## {g}", ""]
        for t, h in a:
            out += [f"### {t}", "", u.md(h), ""]
    for nr, (g, a) in enumerate(gruppen, 1):
        titel = re.sub(r"\s*\(.*\)$", "", g)
        sub = UNTERTITEL.get(titel) or (re.search(r"\((.*)\)$", g).group(1) if "(" in g else "")
        out += [f"# Teil {nr}|{titel}|{sub}", ""]
        for t, h in a:
            out += [f"## {kurz(t)}", "", u.md(h), ""]
    out += ["# |Anhang|Installation und Lizenz", ""]
    for datei, eigen in (("INSTALLATION.md", "Installation"), ("LIZENZ.md", "Lizenz")):
        for g, a in abschnitte(_lies(os.path.join(ps, datei)), eigen):
            if datei == "LIZENZ.md":
                out += ["## Lizenz", ""] + sum(([f"### {t}", "", u.md(h), ""] for t, h in a), [])
            else:
                out += sum(([f"## {t}", "", u.md(h), ""] for t, h in a), [])
    out += ["@STICHWORTE", ""]
    text = re.sub(r"\n{3,}", "\n\n", "\n".join(out))

    v = variablen_datei(basis)
    name = os.path.basename(v)[:-len("-variablen.md")]
    ziel = os.path.join(basis, f"{name}-buch.md")
    kopf = ("> Wird bei jedem Bau neu erzeugt (motor/handbuch.py) – nicht hier ändern, sondern in der Hilfe:\n"
            "> pureSATZ/START.md, pureSATZ/motor/HILFE.md, pureSATZ/handbuch/\n\n# BUCHSTART\n\n")
    if _lies(ziel) != kopf + text:
        open(ziel, "w", encoding="utf-8").write(kopf + text)
    umschlag = os.path.join(ps, "handbuch", "umschlag.md")       # Umschlagtexte: auch aus pureSATZ/handbuch/
    if os.path.exists(umschlag):
        open(os.path.join(basis, f"{name}-umschlag.md"), "w", encoding="utf-8").write(_lies(umschlag))
    stw = os.path.join(ps, "handbuch", "stichworte.txt")
    if os.path.exists(stw):
        open(os.path.join(basis, f"stichworte-{name}.txt"), "w", encoding="utf-8").write(_lies(stw))
    print(f"Handbuch: {name}-buch.md aus der Hilfe (pureSATZ {version}) – {len(gruppen)} Teile, "
          f"{len(alle_titel)} Kapitel, {u.nr} Tabellen.")
    return ziel


if __name__ == "__main__":
    b = os.path.dirname(MOTOR)
    einschalten(b)
    erzeuge(b)
