#!/usr/bin/env python3
"""
hilfe.py – erzeugt hilfe.html: die ganze Hilfe von pureSATZ als eine Seite mit Suche (ab 2.13).

Quellen (Markdown, nur dort pflegen – die HTML-Seite entsteht daraus):
    motor/HILFE.md        Hilfe zum Schreiben und Bauen (kommt mit jedem Motor-Update);
                          «# Gruppe» = gelber Titel in der Navigation, «## Abschnitt» darunter
    meine-hilfe.md        eigene Praxis-Notizen im Buchordner (freiwillig, «Mein Alltag»)
    Befehle, Blöcke       direkt aus dem Motor (manuskript.py)
    Variablen             aus der Variablen-Datei des Buchs (mit den aktuellen Werten)
Im Ordner pureSATZ zusätzlich: ERSTES-BUCH.md, INSTALLATION.md, GITHUB.md.
Ganz oben (Knopf «Start»): START.md aus dem Ordner pureSATZ – Checkliste und Hallo-Buch für den Anfang.

Aufruf:  sh build.sh hilfe   (erzeugen und im Browser öffnen) – entsteht ausserdem bei jedem Bau.
"""
import html
import os
import re
import sys
from datetime import datetime
try:                                            # Windows: «sh build.sh» in Meldungen als «.\build.bat»
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "."))
    import plattform
    plattform.windows_befehle()
except ImportError:
    pass

MOTOR = os.path.dirname(os.path.abspath(__file__))
WEBSEITE = "https://tgsteiger.github.io/pureSATZ/"
GITHUB = "https://github.com/tgsteiger/pureSATZ"

SPICKZETTEL = [
    ("sh sync.sh", "Am Anfang und am Ende: Stand mit den anderen Computern abgleichen"),
    ("sh build.sh schnell", "Beim Schreiben: nur die Lese-PDFs, in wenigen Sekunden"),
    ("sh build.sh", "Alles als Entwurf: PDF, Druckdateien, E-Book"),
    ("sh build.sh final", "Druckfassung (mit Seitenbilanz und Shop-Angaben)"),
    ("sh build.sh komplett", "Vor Bestellung/Veröffentlichung: final + Leseprobe + Korrektur in einem Durchgang"),
    ("sh build.sh pruefen", "Nur prüfen: Variablen, Befehle, Fotos, Geschichten, Tabellen"),
    ("sh build.sh leseprobe", "Leseprobe als PDF und E-Book (einmalig andere Seiten: sh build.sh leseprobe uz 18,20,23)"),
    ("sh build.sh korrektur", "Korrekturfassung: A4, Zeilennummern, Rand für Notizen"),
    ('sh neu.sh "Titel"', "Neue Geschichte in geschichten/"),
    ("sh neu.sh", "Übersicht aller Geschichten (auch geschichten-uebersicht.html)"),
    ('sh neu.sh tabelle "Titel"', "Neue Tabelle in tabellen/"),
    ("sh build.sh geschichten", "Sammel-PDF aller Geschichten (mit «uz» auch unzensiert)"),
    ('sh build.sh stand "Name"', "Jetzigen Stand festhalten, z. B. bei einer Bestellung (ohne Name: alle Stände)"),
    ("sh build.sh aenderungen", "Was hat sich seit dem letzten Stand geändert? → …_Aenderungen.pdf"),
    ("sh build.sh personen", "Personen im Buch mit Seiten und Zeilen → personen-seiten.txt (zum Korrigieren)"),
    ("sh build.sh personen Thomas", "check_Thomas_Gegenlesen.pdf: seine Seiten zum Gegenlesen (aus den fertigen Lese-PDFs)"),
    ("sh update.sh", "Neuen Motor von GitHub holen (lokal: sh update.sh lokal)"),
    ("sh sicherung.sh", "Ganzes Buch als ZIP sichern (alte Fassungen einzelner Dateien: Ordner md-history/)"),
    ("sh cleanup.sh", "Aufräumen: alte Motoren und Zwischenspeicher löschen, entfernen (delete) – fragt zuerst, "
                      "md-history/ und Texte bleiben"),
    ("sh build.sh hilfe", "Diese Hilfe neu erzeugen und öffnen"),
    ("sh build.sh mockup", "Werbebild: Vorder- und Rückseite mit Schatten (…_Mockup.jpg) für Webseite, Newsletter, Shop "
                           "(grosse Cover-Bilder für E-Book-Shops entstehen mit dem E-Book: …_Cover-vorne.jpg)"),
]

BLOECKE = [
    ("::: nur-uz", "Text nur in der zweiten Ausgabe (auch -normal, -bildschirm, -druck, -ebook, -buch, -privatdruck)"),
    ("::: uz Titel", "Heller Kasten «Unzensiert» – nur in der zweiten Ausgabe"),
    ("::: mitte", "Text mittig auf einer eigenen Seite (z. B. Überleitung)"),
    ("#### @FOTO Titel", "Foto: darunter datei:, text:, alt:, breite:, fluss:, quelle: (je eine Zeile); Ende = Leerzeile"),
    ("::: zusammen", "Zeilen bleiben auf derselben Seite"),
    ("::: offen", "Noch offener Text: im Entwurf gelb, im Druck normal"),
    ("::: offen-notiz", "Notiz an dich: nur im Entwurf sichtbar, nie gedruckt"),
    ("::: widmung", "Widmung (direkt unter @IMPRESSUM)"),
    ("::: zeitstrahl", "Zeilen «Jahr | Text» als Zeitstrahl-Tabelle"),
    (":::", "Ende eines Blocks (eigene Zeile)"),
]


# --- Markdown → HTML (klein, ohne Zusatzpaket) -------------------------------------------
def _inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"`([^`]+)`", lambda m: "<code>" + m.group(1).replace("&lt;br/&gt;", "&lt;br&#47;&gt;") + "</code>", t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<![\w*])\*([^*\s][^*]*?)\*(?![\w*])", r"<i>\1</i>", t)
    t = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', t)
    return t.replace("&lt;br/&gt;", "<br>")


def _windows(code):
    """Linux/Mac-Befehle in Windows-Befehle (PowerShell) umschreiben."""
    zeilen = [z for z in code.split("\n") if "mac-einrichten" not in z]
    code = "\n".join(re.sub(r"(einrichten\.sh)\s+#\s*Linux\s*$", r"\1", z) for z in zeilen)
    code = re.sub(r"\bpython3 --version\b", "py --version", code)
    z = re.sub(r"\bsh setup/setup\.sh\b", r".\\setup\\setup.bat", code)
    z = re.sub(r"\bsh import/import-text\.sh\b", r".\\import\\import-text.bat", z)
    z = re.sub(r"\bbash pc-einrichten/(\w+)-einrichten\.sh\b", r".\\pc-einrichten\\win-einrichten.bat", z)
    z = re.sub(r"\bsh ([\w-]+)\.sh\b", r".\\\1.bat", z)
    z = re.sub(r"\bpython3 motor/([\w-]+)\.py", r"py motor\\\1.py", z)
    return z


def _code(text):
    """Codeblock mit Linux- und Windows-Fassung (Umschalter oben) und Kopier-Knopf."""
    lx, win = html.escape(text), html.escape(_windows(text))
    teil = (f'<code class="lx">{lx}</code>' + (f'<code class="win">{win}</code>' if win != lx else
                                                  f'<code class="win">{lx}</code>'))
    return f'<div class="code"><button class="kopie" title="kopieren">kopieren</button><pre>{teil}</pre></div>'


def _plan(x):
    """«{⏱ 3–6 Wochen · fertig −8}» am Ende eines Listenpunkts: Dauer anzeigen und (mit Zieldatum) das Datum
    «bis spätestens» = Zieldatum ± Wochen («fertig −45 Tage» = in Tagen). Ohne Angabe bleibt der Punkt unverändert."""
    m = re.search(r"\s*\{⏱\s*([^·}]*?)\s*(?:·\s*fertig\s*([+\-−]?\s*\d+)\s*(Tage?)?)?\s*\}\s*$", x)
    if not m:
        return x, ""
    zusatz = f'<span class="dauer">⏱ {html.escape(m.group(1))}</span>' if m.group(1) else ""
    if m.group(2):
        n = int(m.group(2).replace("−", "-").replace(" ", ""))
        zusatz += f'<span class="bis" data-t="{n if m.group(3) else 7 * n}"></span>'
    return x[:m.start()], zusatz


def _li(x):
    """Listenpunkt; «[ ] Text» wird ein Häkchen zum Anklicken (merkt sich der Browser)."""
    x, plan = _plan(x)
    m = re.match(r"^\[( |x|X)\]\s+(.*)$", x)
    if not m:
        return f"<li>{_inline(x)}{plan}</li>"
    return (f'<li class="haken"><label><input type="checkbox"{" checked" if m.group(1) != " " else ""}> '
            f'<span>{_inline(m.group(2))}</span></label>{plan}</li>')


def md_html(text):
    """Markdown → Liste von (ebene, titel, html) Abschnitten (getrennt an # und ##)."""
    abschnitte, titel, ebene, out = [], "", 1, []
    zeilen = text.replace("\r\n", "\n").split("\n")
    i, absatz, liste = 0, [], None

    def absatz_ende():
        nonlocal absatz
        if absatz:
            out.append("<p>" + _inline(" ".join(absatz)) + "</p>"); absatz = []

    def liste_ende():
        nonlocal liste
        if liste:
            out.append(f"<{liste[0]}>" + "".join(_li(x) for x in liste[1]) + f"</{liste[0]}>")
            liste = None

    def schnitt(neu_ebene, neu_titel):
        nonlocal titel, ebene, out
        absatz_ende(); liste_ende()
        if out or titel:
            abschnitte.append((ebene, titel, "\n".join(out)))
        titel, ebene, out = neu_titel, neu_ebene, []

    while i < len(zeilen):
        z = zeilen[i]
        s = z.strip()
        if s.startswith("```"):
            absatz_ende(); liste_ende()
            code, i = [], i + 1
            while i < len(zeilen) and not zeilen[i].strip().startswith("```"):
                code.append(zeilen[i]); i += 1
            out.append(_code("\n".join(code))); i += 1
            continue
        m = re.match(r"^(#{1,4})\s+(.*)$", s)
        if m:
            n, t = len(m.group(1)), m.group(2).strip()
            if n <= 2:
                schnitt(n, t)
            else:
                absatz_ende(); liste_ende()
                out.append(f"<h{n + 1}>{_inline(t)}</h{n + 1}>")
            i += 1; continue
        if s.startswith("|") and i + 1 < len(zeilen) and re.match(r"^\|[\s:|-]+\|$", zeilen[i + 1].strip()):
            absatz_ende(); liste_ende()
            zell = lambda r: [c.strip() for c in re.split(r"(?<!\\)\|", r.strip().strip("|"))]
            kopf = zell(s); i += 2; reihen = []
            while i < len(zeilen) and zeilen[i].strip().startswith("|"):
                reihen.append(zell(zeilen[i])); i += 1
            out.append("<table><thead><tr>" + "".join(f"<th>{_inline(c.replace(chr(92) + '|', '|'))}</th>" for c in kopf)
                       + "</tr></thead><tbody>" + "".join("<tr>" + "".join(
                           f"<td>{_inline(c.replace(chr(92) + '|', '|'))}</td>" for c in r) + "</tr>" for r in reihen)
                       + "</tbody></table>")
            continue
        m = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)$", z)
        if m and not s.startswith("---"):
            absatz_ende()
            art = "ol" if m.group(2)[0].isdigit() else "ul"
            if liste and liste[0] != art:
                liste_ende()
            if not liste:
                liste = (art, [])
            liste[1].append(m.group(3))
            i += 1
            while i < len(zeilen) and zeilen[i].startswith("  ") and zeilen[i].strip() and \
                    not re.match(r"^\s*([-*]|\d+\.)\s+", zeilen[i]):
                liste[1][-1] += " " + zeilen[i].strip(); i += 1
            continue
        if s == "::: kacheln":                  # Liste als Kacheln, mit Knopf «drucken»
            absatz_ende(); liste_ende()
            out.append('<div class="kacheln"><button class="kopie druck" title="nur diesen Abschnitt drucken">drucken</button>')
            i += 1; continue
        if s == ":::":
            absatz_ende(); liste_ende(); out.append("</div>"); i += 1; continue
        if s.startswith(">"):
            absatz_ende(); liste_ende()
            out.append(f"<blockquote>{_inline(s.lstrip('> '))}</blockquote>"); i += 1; continue
        if not s:
            absatz_ende(); liste_ende(); i += 1; continue
        if s in ("---", "***"):
            absatz_ende(); liste_ende(); i += 1; continue
        liste_ende()
        absatz.append(s); i += 1
    schnitt(1, "")
    return [a for a in abschnitte if a[1] or a[2].strip()]


# --- Automatische Abschnitte ---------------------------------------------------------------
BEFEHL_GRUPPEN = [      # Gruppen in hilfe.html; Einträge ohne @ (Markdown) stehen als (Schreibweise, Wirkung) dabei
    ("Titelei", ["@TITEL", "@IMPRESSUM", "@HINWEIS", "@WIDMUNG", "@KERNSATZ", "@INHALTSVERZEICHNIS"]),
    ("Seite, Umbruch, Kopfzeile", ["@UMBRUCH", "@UMBRUCH-RECHTS", "@PLATZ", "@ABSTAND", "@SEITENMITTE", "@KOPF"]),
    ("Text hervorheben (von leicht bis stark)", [("~ Satz", "kursive Randbemerkung, klein"),
                                                 "@ZITAT", "@ZITAT-ZIER", "@UNTEN", "@MOTTO"]),
    ("Verzierung", ["@ZIER", "@ZIER-UNTEN", "@ZIER-TRENNER"]),
    ("Bilder, Links, Tabellen, Geschichten", ["@FOTO", "@PORTRAIT", "@QR", "@QR-PAAR", "@#name", "@@name"]),
    ("Verzeichnisse und Schluss", ["@STICHWORTE", "@BILDNACHWEIS", "@RUECKSEITE"]),
]
BEFEHL_VERSTECKT = {"@LOTUS", "@LOTUS-UNTEN", "@LOTUS-TRENNER", "@ANHANG"}     # gehen noch, stehen nicht in der Hilfe

LOESUNGEN = [
    ("Ein einzelner Satz rutscht allein auf die nächste Seite",
     "«@PLATZ 70» vor die letzte Überschrift davor (sie geht dann mit auf die neue Seite) – oder den Absatz kürzen"),
    ("Neue Seite erzwingen", "«---» auf eigener Zeile (davor eine Leerzeile)"),
    ("Kapitel soll auf einer rechten Seite beginnen", "«@UMBRUCH-RECHTS» davor"),
    ("Überschrift steht allein unten auf der Seite", "«@PLATZ 50» vor die Überschrift"),
    ("Seite mit wenig Text wirkt verloren", "«@SEITENMITTE» an den Anfang der Seite"),
    ("Grosse Lücke unten auf der Seite", "Foto kleiner («breite: 60»), Text kürzen oder «@ZIER-UNTEN»"),
    ("Mehr Luft zwischen zwei Absätzen", "«@ABSTAND 8» (8 mm)"),
    ("Text soll nicht getrennt werden", "Block «::: zusammen» … «:::»"),
]


def befehle_html():
    sys.path.insert(0, MOTOR)
    import manuskript as M

    def reihe(k, v):
        return f"<tr><td><code>{html.escape(k)}</code></td><td>{html.escape(v)}</td></tr>"
    out = ["<p>Jeder Befehl steht auf einer eigenen Zeile, genau so geschrieben (GROSS). "
           "<code>## @TITEL</code> wirkt wie <code>@TITEL</code>. Links steht die ganze Zeile, wie sie im Buch steht.</p>",
           "<h3>Seite sieht nicht gut aus? – Lösungen</h3>",
           "<table><thead><tr><th>Problem</th><th>Lösung</th></tr></thead><tbody>"
           + "".join(f"<tr><td>{html.escape(p)}</td><td>{html.escape(l)}</td></tr>" for p, l in LOESUNGEN)
           + "</tbody></table>"]
    gezeigt = set()
    for titel, eintraege in BEFEHL_GRUPPEN:
        reihen = []
        for e in eintraege:
            if isinstance(e, tuple):
                reihen.append(reihe(*e))
            elif e in M.BEFEHLE:
                reihen.append(reihe(*M.BEFEHLE[e])); gezeigt.add(e)
        out.append(f"<h3>{html.escape(titel)}</h3><table><thead><tr><th>Schreibweise</th><th>Wirkung</th></tr></thead>"
                   f"<tbody>{''.join(reihen)}</tbody></table>")
    rest = [k for k in M.BEFEHLE if k not in gezeigt and k not in BEFEHL_VERSTECKT]
    if rest:
        out.append("<h3>Weitere</h3><table><tbody>" + "".join(reihe(*M.BEFEHLE[k]) for k in rest) + "</tbody></table>")
    return "\n".join(out)


def bloecke_html():
    reihen = "".join(f"<tr><td><code>{html.escape(k)}</code></td><td>{html.escape(v)}</td></tr>" for k, v in BLOECKE)
    return ("<p>Ein Block beginnt mit <code>::: art</code> und endet mit einer Zeile <code>:::</code>.</p>"
            f"<table><thead><tr><th>Block</th><th>Wirkung</th></tr></thead><tbody>{reihen}</tbody></table>")


def variablen_html(pfad):
    """Variablen der Buch-Datei, gruppiert nach Überschriften, mit Erklärung und aktuellem Wert."""
    if not pfad or not os.path.exists(pfad):
        return ""
    teile, gruppe, erkl, reihen = [], "", [], []

    def fertig():
        if reihen or erkl:
            teile.append((gruppe, " ".join(erkl), list(reihen)))
    for z in open(pfad, encoding="utf-8").read().split("\n"):
        s = z.strip()
        m = re.match(r"^(#{1,4})\s+(.*)$", s)
        if m:
            fertig(); gruppe, erkl, reihen = m.group(2), [], []
            continue
        m = re.match(r"^(?:[-*]\s+)?\{?([a-z][a-z0-9-]*)\}?\s*:\s*(.*)$", s)
        if m:
            reihen.append((m.group(1), m.group(2)))
        elif s:
            erkl.append(s[1:].strip() if s.startswith(">") else s)
    fertig()
    out = [f"<p>Aus <code>{html.escape(os.path.basename(pfad))}</code> – mit den Werten dieses Buchs. "
           "Namen vor dem Doppelpunkt nie ändern, nur den Wert. Unter «Ausgabe: …» gilt ein Wert nur für diese Ausgabe; "
           "<code>{name-uz}</code> = Wert für die zweite Ausgabe. Im Buch steht derselbe Name als <code>{name}</code>.</p>"]
    for g, e, r in teile:
        if not r and not e:
            continue
        out.append(f"<h3>{_inline(g)}</h3>" + (f"<p class='leise'>{_inline(e)}</p>" if e else ""))
        if r:
            out.append("<table><tbody>" + "".join(
                f"<tr><td><code>{html.escape(k)}</code></td><td>{html.escape(v) or '<span class=leise>–</span>'}</td></tr>"
                for k, v in r) + "</tbody></table>")
    return "\n".join(out)


def formate_html(variablen=None):
    """Buchformate direkt aus motor/build.py (FORMATE), das Format dieses Buchs hervorgehoben."""
    quelle = _lies(os.path.join(MOTOR, "build.py"))
    reihen = re.findall(r'^\s*"([a-z0-9]+)":\s*dict\(name="([^"]+)",\s*seite=\((\d+),\s*(\d+)\).*?rand=\((\d+),\s*(\d+),'
                        r'\s*(\d+),\s*(\d+)\),\s*text=\(([\d.]+),', quelle, re.M)
    if not reihen:
        return ""
    aktuell = ""
    if variablen and os.path.exists(variablen):
        m = re.search(r"^(?:[-*]\s+)?\{?format\}?\s*:\s*(\S+)", _lies(variablen), re.M)
        aktuell = m.group(1).strip().lower() if m else ""
    zeilen = []
    for k, name, b, h, ri, ra, _, _, pt in reihen:
        tb = int(b) - int(ri) - int(ra)
        dies = k == aktuell
        zeilen.append(f"<tr{' class=dies' if dies else ''}><td><code>{k}</code>{' ← dieses Buch' if dies else ''}</td>"
                      f"<td>{html.escape(name)}</td><td>{b} × {h} mm</td><td>{tb} mm</td><td>{pt} pt</td>"
                      f"<td>{tb * 12} px</td></tr>")
    return ("<p>In der Variablen-Datei: <code>{format}: a5</code> oder ein eigenes Mass <code>{format}: 150 x 215</code> (mm). "
            "Ränder und Schrift rechnet der Motor selbst (Masse laut epubli). Bindung, Rücken und Beschnitt stehen in der "
            "Plattform-Datei in <code>druck/</code>; dort auch ein abweichendes Druckformat.</p>"
            "<table><thead><tr><th>format</th><th>Name</th><th>Seite</th><th>Textbreite</th><th>Schrift</th>"
            "<th>Foto ganze Breite</th></tr></thead><tbody>" + "".join(zeilen) + "</tbody></table>"
            "<p class='leise'>Foto ganze Breite = nötige Pixel für 300 dpi (Breite in mm × 12).</p>")


def netz_html():
    """Abschnitt «pureSATZ im Netz»: Webseite, GitHub, Download, Fehler melden, Kontakt (auch über die Suche)."""
    reihen = [
        ("Webseite", WEBSEITE, "Download, die fünf Schritte für Linux, Mac und Windows, diese Hilfe online"),
        ("GitHub", GITHUB, "Quelltext, neueste Version, Änderungen (CHANGELOG)"),
        ("Download (ZIP)", GITHUB + "/archive/refs/heads/main.zip",
         "neuester Stand; Ordner «pureSATZ-main» in «pureSATZ» umbenennen"),
        ("Fehler melden, Fragen", GITHUB + "/issues", "Issues auf GitHub (öffentlich)"),
        ("Lizenz", GITHUB + "/blob/main/LIZENZ.md", "kostenlos für eigene Bücher, Quelltext einsehbar"),
    ]
    t = "".join(f'<tr><td>{n}</td><td><a href="{u}">{html.escape(u.replace("https://", ""))}</a></td>'
                f"<td>{html.escape(x)}</td></tr>" for n, u, x in reihen)
    return (f"<table><tbody>{t}<tr><td>E-Mail</td><td><a class=mail href=#>puresatz (at) gsteiger.ch</a></td>"
            "<td>Kontakt, Lizenzanfragen (GPL-3.0)</td></tr></tbody></table>"
            "<p>Neuen Motor holen: <code>sh update.sh</code> (holt ihn von GitHub, ohne Konto).</p>")


def spick_html():
    return "".join(_code(b) .replace('<div class="code">', f'<div class="code spick" data-text="{html.escape(t)}">')
                   + f'<p class="spicktext">{html.escape(t)}</p>' for b, t in SPICKZETTEL)


# --- Seite ---------------------------------------------------------------------------------
def seite(titel, gruppen, farben, version, start=False):
    nav, inhalt, nr = [], [], 0
    for gtitel, abschnitte in gruppen:
        if not abschnitte:
            continue
        nav.append(f'<p class="ngruppe">{html.escape(gtitel)}</p>')
        for t, h in abschnitte:
            nr += 1
            nav.append(f'<a href="#a{nr}">{_inline(t)}</a>')
            inhalt.append(f'<section id="a{nr}"><h2>{_inline(t)}</h2>{h}</section>')
    f = farben
    return f"""<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>pureSATZ Hilfe – {html.escape(titel)}</title>
<style>
@font-face{{font-family:Poppins;src:url(motor/fonts/Poppins-Regular.ttf)}}
@font-face{{font-family:Poppins;font-weight:500;src:url(motor/fonts/Poppins-Medium.ttf)}}
@font-face{{font-family:Lora;src:url(motor/fonts/Lora-Regular.ttf)}}
@font-face{{font-family:Lora;font-weight:bold;src:url(motor/fonts/Lora-Bold.ttf)}}
:root{{--papier:{f['papier']};--text:{f['text']};--leise:{f['leise']};--haupt:{f['haupt']};--akzent:{f['akzent']};
--karte:#fff;--linie:#e7dfd0;--code:#f4efe4;--mark:#f7e3a8}}
@media (prefers-color-scheme:dark){{:root{{--papier:#1d1b19;--text:#ece6dc;--leise:#b4ab9f;--haupt:#9db7ec;
--karte:#2a2724;--linie:#3b3732;--code:#24211e;--mark:#6b5a24}}}}
*{{box-sizing:border-box}} html{{scroll-padding-top:70px}}
body{{margin:0;background:var(--papier);color:var(--text);font:16px/1.55 Lora,Georgia,serif}}
header{{position:sticky;top:0;z-index:5;background:var(--papier);border-bottom:1px solid var(--linie);
display:flex;flex-wrap:wrap;gap:10px;align-items:center;padding:10px 16px}}
header h1{{font:500 18px Poppins,system-ui,sans-serif;color:var(--haupt);margin:0;flex:1 1 auto}}
header small{{color:var(--leise);font-weight:400}}
#suche{{flex:1 1 260px;max-width:420px;padding:8px 12px;border:1px solid var(--linie);border-radius:18px;
background:var(--karte);color:var(--text);font:15px Poppins,system-ui,sans-serif}}
.os button,button.kopie{{font:13px Poppins,system-ui,sans-serif;border:1px solid var(--linie);background:var(--karte);
color:var(--text);border-radius:14px;padding:4px 10px;cursor:pointer}} .os button.aktiv{{border-color:var(--akzent);color:var(--akzent)}}
.wrap{{display:flex;max-width:1200px;margin:0 auto}}
nav{{flex:0 0 230px;position:sticky;top:58px;align-self:flex-start;max-height:calc(100vh - 60px);overflow:auto;
padding:16px 8px 40px 16px;font:14px/1.4 Poppins,system-ui,sans-serif}}
nav a{{display:block;color:var(--text);text-decoration:none;padding:3px 6px;border-radius:6px}}
nav a:hover{{background:var(--karte);color:var(--haupt)}} nav .ngruppe{{color:var(--akzent);margin:14px 0 4px 6px;font-size:12px;
text-transform:uppercase;letter-spacing:.06em}}
main{{flex:1;min-width:0;padding:8px 16px 80px}}
section{{background:var(--karte);border:1px solid var(--linie);border-radius:10px;padding:6px 18px 12px;margin:14px 0}}
section h2{{font:500 20px Poppins,system-ui,sans-serif;color:var(--haupt)}} h3,h4,h5{{font-family:Poppins,system-ui,sans-serif;
font-weight:500;color:var(--haupt)}} a{{color:var(--haupt)}}
code{{font:13.5px ui-monospace,Menlo,Consolas,monospace;background:var(--code);padding:1px 4px;border-radius:4px}}
.code{{position:relative;margin:10px 0}} .code pre{{background:var(--code);border-radius:8px;padding:10px 12px;overflow-x:auto;margin:0}}
.code pre code{{background:none;padding:0;white-space:pre}} button.kopie{{position:absolute;right:6px;top:6px;opacity:.8}}
body.win .lx, body:not(.win) .win{{display:none}}
table{{border-collapse:collapse;width:100%;margin:8px 0;font-size:14.5px;display:block;overflow-x:auto}}
th,td{{text-align:left;vertical-align:top;padding:6px 8px;border-bottom:1px solid var(--linie)}} th{{font:500 13.5px Poppins,system-ui,sans-serif;color:var(--leise)}}
blockquote{{border-left:3px solid var(--akzent);margin:8px 0;padding:2px 12px;color:var(--leise)}}
.leise{{color:var(--leise)}} mark{{background:var(--mark);color:inherit;border-radius:3px}}
a.startk{{font:500 13px Poppins,system-ui,sans-serif;border:1px solid var(--akzent);background:var(--akzent);color:#fff;
border-radius:14px;padding:4px 12px;text-decoration:none}}
li.haken{{list-style:none;margin:14px 0 4px -22px}} li.haken label{{cursor:pointer}}
li.haken input{{width:17px;height:17px;vertical-align:-3px;margin-right:6px;accent-color:var(--akzent)}}
li.haken input:checked+span{{color:var(--leise)}}
tr.dies td{{background:var(--code);font-weight:bold}}
.kacheln{{position:relative;padding-top:6px}} .kacheln>button.druck{{position:absolute;right:0;top:-38px}}
.kacheln ol,.kacheln ul{{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:10px;padding:0;margin:8px 0;
counter-reset:k}}
.kacheln li.haken{{list-style:none;margin:0;border:1px solid var(--linie);border-radius:10px;padding:10px 12px;
background:var(--papier);counter-increment:k}}
.kacheln li.haken{{position:relative;padding-right:30px}}
.kacheln li.haken label{{display:block}} .kacheln li.haken label::before{{content:counter(k);position:absolute;right:10px;top:9px;
font:500 13px Poppins,system-ui,sans-serif;color:var(--akzent)}}
.kacheln li.haken:has(input:checked){{opacity:.6}}
.kacheln .dauer,.kacheln .bis{{display:block;font:13px Poppins,system-ui,sans-serif;color:var(--leise);margin-top:6px}}
.kacheln .bis{{color:var(--haupt);font-weight:500}} .kacheln .bis:empty{{display:none}}
.kacheln .ziel{{display:inline-block;font:14px Poppins,system-ui,sans-serif;margin:4px 0 2px}}
.kacheln .ziel input{{font:14px Poppins,system-ui,sans-serif;padding:3px 6px;border:1px solid var(--linie);border-radius:8px;
background:var(--karte);color:var(--text);margin-left:6px}}
@media print{{header,nav,footer,#leer,button{{display:none!important}} body{{background:#fff;color:#000}}
body.nur main section:not(.drucke){{display:none}} section{{border:0;margin:0}}
.kacheln ol,.kacheln ul{{grid-template-columns:1fr 1fr}} .kacheln li.haken{{break-inside:avoid;background:#fff}}}}
.spick{{margin:8px 0 0}} .spicktext{{margin:2px 0 10px 4px;color:var(--leise);font-size:14px}}
#leer{{display:none;color:var(--leise);padding:20px}} footer{{color:var(--leise);font-size:13px;padding:10px 0}}
@media (max-width:760px){{nav{{display:none}} main{{padding:8px 10px 60px}}}}
</style></head><body>
<header><h1>pureSATZ Hilfe · {html.escape(titel)} <small>Motor {html.escape(version)}</small></h1>
<input id="suche" type="search" placeholder="Suchen … (Taste /)" autocomplete="off">
<span class="os">{'<a class="startk" href="#a1">Start</a> ' if start else ''}<button data-os="lx" class="aktiv">Linux/Mac</button> <button data-os="win">Windows</button></span></header>
<div class="wrap"><nav>{"".join(nav)}</nav><main>{"".join(inhalt)}
<p id="leer">Nichts gefunden.</p>
<footer><a href="{WEBSEITE}">Webseite</a> · <a href="{GITHUB}">GitHub</a> · <a href="{GITHUB}/issues">Fehler melden</a> · <a class=mail href=#>puresatz (at) gsteiger.ch</a><br>
Erstellt {datetime.now():%d.%m.%Y %H:%M} von pureSATZ {html.escape(version)} · neu mit «sh build.sh hilfe» · Quellen: START.md, motor/HILFE.md, meine-hilfe.md, Variablen-Datei</footer>
</main></div>
<script>
document.querySelectorAll('a.mail').forEach(m=>{{const a=['puresatz','gsteiger.ch'].join('@');m.textContent=a;m.href='mailto:'+a}});
const norm=t=>t.toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'');
const norm2=t=>norm(t).replace(/ae/g,'a').replace(/oe/g,'o').replace(/ue/g,'u').replace(/ß/g,'ss');
const secs=[...document.querySelectorAll('main section')],navs=[...document.querySelectorAll('nav a')];
secs.forEach(s=>{{s._orig=s.innerHTML;s._text=norm2(s.textContent)}});
const such=document.getElementById('suche');
function markiere(el,woerter){{const w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT);const knoten=[];
while(w.nextNode())knoten.push(w.currentNode);for(const n of knoten){{const t=n.nodeValue,nt=norm(t);let pos=[];
for(const x of woerter){{let i=nt.indexOf(x);while(i>=0){{pos.push([i,i+x.length]);i=nt.indexOf(x,i+x.length)}}}}
if(!pos.length)continue;pos.sort((a,b)=>a[0]-b[0]);const f=document.createDocumentFragment();let a=0;
for(const [s,e] of pos){{if(s<a)continue;f.append(t.slice(a,s));const m=document.createElement('mark');m.textContent=t.slice(s,e);f.append(m);a=e}}
f.append(t.slice(a));n.parentNode.replaceChild(f,n)}}}}
such.addEventListener('input',()=>{{const w=norm(such.value).split(/\\s+/).filter(Boolean);let n=0;
const passt=(s,alle)=>alle?w.every(x=>s._text.includes(norm2(x))):w.some(x=>s._text.includes(norm2(x)));
let alle=true;if(w.length>1&&!secs.some(s=>passt(s,true)))alle=false;   // kein Abschnitt mit allen Wörtern: eines genügt
secs.forEach((s,i)=>{{s.innerHTML=s._orig;const ok=passt(s,alle);s.style.display=ok?'':'none';
navs[i].style.display=ok?'':'none';if(ok){{n++;if(w.length)markiere(s,w)}}}});
document.getElementById('leer').style.display=n?'none':'block';knoepfe();}});
document.addEventListener('keydown',e=>{{if(e.key==='/'&&document.activeElement!==such){{e.preventDefault();such.focus()}}
if(e.key==='Escape'){{such.value='';such.dispatchEvent(new Event('input'))}}}});
document.querySelectorAll('.os button').forEach(b=>b.onclick=()=>{{document.body.classList.toggle('win',b.dataset.os==='win');
document.querySelectorAll('.os button').forEach(x=>x.classList.toggle('aktiv',x===b));
try{{localStorage.setItem('ps-os',b.dataset.os)}}catch(e){{}}}});
try{{if(localStorage.getItem('ps-os')==='win')document.querySelector('[data-os=win]').click()}}catch(e){{}}
function knoepfe(){{document.querySelectorAll('button.kopie').forEach(b=>b.onclick=()=>{{
const c=b.parentNode.querySelector(document.body.classList.contains('win')?'.win':'.lx');
const t=c.textContent;(navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(
()=>{{b.textContent='kopiert ✓';setTimeout(()=>b.textContent='kopieren',1200)}},
()=>{{const r=document.createRange();r.selectNodeContents(c);getSelection().removeAllRanges();getSelection().addRange(r)}})}})}}
knoepfe();
function haken(){{let h={{}};try{{h=JSON.parse(localStorage.getItem('ps-haken')||'{{}}')}}catch(e){{}}
document.querySelectorAll('li.haken input').forEach(c=>{{const k=c.parentNode.textContent.trim().slice(0,60);
if(k in h)c.checked=h[k];c.onchange=()=>{{h[k]=c.checked;try{{localStorage.setItem('ps-haken',JSON.stringify(h))}}catch(e){{}}}}}})}}
haken();such.addEventListener('input',haken);
document.querySelectorAll('.kacheln').forEach(k=>{{if(!k.querySelector('.bis'))return;
const l=document.createElement('label');l.className='ziel';l.innerHTML='📅 Mein Zieldatum (Erscheinen oder Vernissage), freiwillig: <input type="date">';
k.insertBefore(l,k.querySelector('ol,ul'));const d=l.querySelector('input');
const rechne=()=>{{let z=d.value;try{{localStorage.setItem('ps-ziel',z)}}catch(e){{}}
k.querySelectorAll('.bis').forEach(b=>{{if(!z){{b.textContent='';return}}const t=new Date(z+'T12:00');t.setDate(t.getDate()+(+b.dataset.t));
b.textContent='📅 bis spätestens '+t.toLocaleDateString('de-CH',{{weekday:'short',day:'numeric',month:'short',year:'numeric'}})}})}};
try{{d.value=localStorage.getItem('ps-ziel')||''}}catch(e){{}}d.addEventListener('input',rechne);rechne()}});
document.addEventListener('click',e=>{{const b=e.target.closest('button.druck');if(!b)return;const s=b.closest('section');
s.classList.add('drucke');document.body.classList.add('nur');window.print();
s.classList.remove('drucke');document.body.classList.remove('nur')}});
</script></body></html>
"""


def _lies(p):
    return open(p, encoding="utf-8").read() if p and os.path.exists(p) else ""


def start_datei(basis):
    """START.md (Checkliste für den Anfang): im Ordner selbst, im Ordner pureSATZ dieses Motors oder daneben."""
    for p in (os.path.join(basis, "START.md"), os.path.join(os.path.dirname(MOTOR), "START.md"),
              os.path.join(basis, "..", "pureSATZ", "START.md")):
        if os.path.exists(p):
            return p
    return None


def erzeuge(basis, buchtitel=None, variablen=None, farben=None, oeffnen=False):
    """hilfe.html im Ordner basis schreiben. Buchordner (mit Variablen-Datei) oder Ordner pureSATZ."""
    version = _lies(os.path.join(MOTOR, "VERSION")).strip()
    gruppen = []
    start = [(t, h) for _, t, h in md_html(_lies(start_datei(basis))) if t and h.strip()]
    if start:
        gruppen.append(("Start", start))
    meine = os.path.join(basis, "meine-hilfe.md")
    gruppen.append(("Alltag", [("Spickzettel", spick_html())]
                    + [(t, h) for _, t, h in md_html(_lies(meine)) if t and h.strip()]))
    # HILFE.md: «# Gruppe» = gelber Titel in der Navigation, «## Abschnitt» darunter
    hilfe_gruppen = []
    for e, t, h in md_html(_lies(os.path.join(MOTOR, "HILFE.md"))):
        if e == 1 and t:
            hilfe_gruppen.append((t, []))
            if h.strip():
                hilfe_gruppen[-1][1].append((t, h))
        elif t and h.strip():
            if not hilfe_gruppen:
                hilfe_gruppen.append(("Schreiben und Bauen", []))
            hilfe_gruppen[-1][1].append((t, h))
    gruppen += [g for g in hilfe_gruppen if g[1]]
    nachschlagen = [("Befehle (@)", befehle_html()), ("Blöcke (:::)", bloecke_html()),
                    ("Buchformate", formate_html(variablen))]
    if variablen:
        nachschlagen.append(("Variablen dieses Buchs", variablen_html(variablen)))
    nachschlagen.append(("pureSATZ im Netz (GitHub, Webseite)", netz_html()))
    gruppen.append(("Nachschlagen", nachschlagen))
    if not variablen:                       # Ordner pureSATZ: Installation und GitHub
        extra = []
        for datei in ("ERSTES-BUCH.md", "INSTALLATION.md", "GITHUB.md", "LIZENZ.md"):
            extra += [(t, h) for e, t, h in md_html(_lies(os.path.join(basis, datei))) if t]
        gruppen.append(("Einrichten und GitHub", extra))
    farben = dict(dict(papier="#FBF6EC", text="#2E2A26", leise="#6E655C", haupt="#1E428A", akzent="#B8873B"),
                  **(farben or {}))
    ziel = os.path.join(basis, "hilfe.html")
    with open(ziel, "w", encoding="utf-8") as fh:
        fh.write(seite(buchtitel or "pureSATZ", gruppen, farben, version, start=bool(start)))
    if oeffnen:
        oeffne(ziel)
    return ziel


def oeffne(pfad):
    import subprocess
    import webbrowser
    try:
        if sys.platform.startswith("win"):
            os.startfile(pfad)                                   # noqa
        elif sys.platform == "darwin":
            subprocess.Popen(["open", pfad])
        else:
            subprocess.Popen(["xdg-open", pfad], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        webbrowser.open("file://" + os.path.abspath(pfad))


if __name__ == "__main__":
    # Im Ordner pureSATZ:  python3 motor/hilfe.py   → pureSATZ/hilfe.html
    oben = os.path.dirname(MOTOR)
    print("Hilfe:", os.path.relpath(erzeuge(oben, oeffnen="--oeffnen" in sys.argv), oben))
