#!/usr/bin/env python3
"""
personen.py – Personen im Buch finden und Seiten zum Gegenlesen zusammenstellen (pureSATZ ab 2.35).

Im Buchordner (über build.sh / build.bat):
    sh build.sh personen            Lese-PDFs durchsuchen → personen-seiten.txt (Personen mit Seiten und Zeilen)
    sh build.sh personen Thomas     check_Thomas_Gegenlesen.pdf (und …_Gegenlesen-uz.pdf) aus den fertigen Lese-PDFs

personen-seiten.txt ist Ergebnis und Eingabe zugleich:
    Thomas | Thom | Autor           Begriffe derselben Person in einer Zeile; der erste ist der Name (für die Datei)
    normal: 44-45,55 / uz: 60,74    Seiten fürs Check-PDF – eigene Seiten einfach dazuschreiben (bleiben stehen)
    --- Ecuador                     nie mehr vorschlagen
    > normal: S. 44 Z. 28 …         schreibt der Motor jedes Mal neu (Fundstellen mit Seite und Zeile)
Es wird nichts neu gebaut: gesucht wird in den vorhandenen Lese-PDFs (Seitenzahlen = gedruckte Seiten).
"""
import os
import re
from datetime import datetime

DATEI = "personen-seiten.txt"
WEG = "---"

ROLLEN = """Vater Mutter Papa Mama Mami Papi Grossvater Grossmutter Grosi Grossmami Grosspapi Grossätti Opa Oma
Bruder Schwester Tochter Sohn Onkel Tante Cousin Cousine Neffe Nichte Ehefrau Ehemann Exfrau Ex-Frau Exmann Ex-Mann
Freundin Seelenpartnerin Seelenpartner Partnerin Lebenspartnerin Schwiegermutter Schwiegervater Götti Gotte Patin
Pate Nachbarin Nachbar Lehrerin Lehrer Chefin Chef Therapeutin Therapeut Psychiater Psychiaterin Ärztin Arzt
Heilerin Heiler Schamanin Schamane Medizinfrau Medizinmann Yogini Guru Meisterin Mentor Mentorin""".split()

VORNAMEN = """Adrian Agnes Alain Albert Alex Alexander Alexandra Alfred Alice Alina Andrea Andreas Angela Anita Anja Anna
Anne Annemarie Anton Barbara Beat Beatrice Benjamin Bernhard Bettina Brigitte Bruno Carla Carmen Caroline Christa
Christian Christina Christine Christoph Claudia Cornelia Damir Daniel Daniela David Denise Dominik Doris Edith Elena
Elisabeth Elsa Emil Emma Erich Erika Ernst Esther Eva Fabian Felix Franz Franziska Fritz Gabriela Gabriele Georg
Gerhard Gertrud Gisela Gregor Hanna Hannah Hans Hansjörg Hanspeter Heidi Heinz Helen Helena Helene Helga Hugo Ida Ines
Irene Iris Isabelle Jakob Jan Jana Johann Johanna Johannes Jonas Josef Judith Julia Julian Jürg Jürgen Karin Karl
Katharina Katrin Kevin Klara Kurt Lara Laura Lea Lena Leon Lisa Lorenz Luca Lucas Lukas Luzia Manuel Manuela Marc
Marco Margrit Maria Marianne Mario Marion Markus Marlies Martha Martin Martina Mathias Matthias Max Melanie Melva
Michael Michaela Michel Michelle Monika Nadia Nadine Natalie Nicole Niklaus Nina Noah Nora Olivia Oliver Pascal
Patrick Patricia Paul Paula Peter Petra Philipp Pia Rahel Raphael Regina Reto Ruedi Rudolf Ruth Sabine Samuel Sandra
Sara Sarah Silvia Simon Simone Sonja Stefan Stefanie Stephan Susanne Tamara Theo Theres Therese Thomas Tobias Ueli
Urs Ursula Valentin Vera Verena Walter Werner Willi Yvonne Zoe Bradley Barbara Damian Mirjam Miriam Rebekka Ronja
Fiona Jasmin Selina Livia Noemi Seraina Flurina Gian Andri Res Röbi Housi Vreni Käthi Rösli Margrith""".split()

BUCHSTABE = r"[0-9A-Za-zÄÖÜäöüßÀ-ÿ]"


# --- PDF lesen ----------------------------------------------------------------------
def zeilen(pdf):
    """[[zeile, …] je Seite] – Text jeder Zeile von oben nach unten (wie die Zeilennummern im Korrektur-PDF)."""
    import pypdfium2 as pdfium
    doc = pdfium.PdfDocument(pdf)
    seiten = []
    for s in doc:
        tp = s.get_textpage()
        teile = []
        for i in range(tp.count_rects()):
            l, b, r, t = tp.get_rect(i)
            teile.append((b, l, tp.get_text_bounded(l, b, r, t)))
        z = []                                          # [y, [(x, text)]]
        for b, l, text in sorted(teile, key=lambda x: -x[0]):
            if z and z[-1][0] - b <= 6:                 # gleiche Höhe = eine Zeile
                z[-1][1].append((l, text))
            else:
                z.append([b, [(l, text)]])
        seiten.append([" ".join(t for _, t in sorted(st)).strip() for _, st in z])
    doc.close()
    return seiten


def kapitel(pdf):
    """{seite: Kapiteltitel} aus dem Inhaltsverzeichnis (Lesezeichen) des PDFs."""
    import io
    from pypdf import PdfReader
    import fassungen
    r = PdfReader(io.BytesIO(open(pdf, "rb").read()))
    kap = [(t, s) for t, s, kinder in fassungen._eintraege(r) if not kinder]
    out, aktuell = {}, ""
    for n in range(1, len(r.pages) + 1):
        for t, s in kap:
            if s == n:
                aktuell = t
        out[n] = aktuell
    return out


def muster(begriff):
    return re.compile(rf"(?<!{BUCHSTABE}){re.escape(begriff)}(?:s)?(?!{BUCHSTABE})")


VERZEICHNIS = ("stichwort", "register", "index")        # dort stehen Namen nur als Verweis


def treffer(seiten, begriffe, kap=None):
    """{seite: [zeile, …]} – Seite = gedruckte Seitenzahl (im Lese-PDF = Position, Seite 1 = Umschlag).
    Seiten im Stichwortverzeichnis zählen nicht."""
    ms = [muster(b) for b in begriffe if b]
    out = {}
    for n, zs in enumerate(seiten, 1):
        if kap and any(v in (kap.get(n) or "").lower() for v in VERZEICHNIS):
            continue
        for i, z in enumerate(zs, 1):
            if i == 1 and " · " in z:                   # Kopfzeile «Teil · Kapitel» zählt nicht
                continue
            naechste = zs[i] if i < len(zs) else ""
            verbunden = z[:-1] + naechste.split(" ")[0] if z.endswith("-") else z    # Trennung am Zeilenende
            if any(m.search(z) or m.search(verbunden) for m in ms):
                out.setdefault(n, []).append(i)
    return out


# --- personen-seiten.txt -------------------------------------------------------------
STELLEN = re.compile(r"\s{2,}\d+\s+Stellen?\b.*$", re.I)


def lies(pfad):
    """([[begriff, …], …], {weg}, {gruppe-nr: {fassung: "59-60, 63"}}) – Gruppen in der Reihenfolge der Datei."""
    gruppen, weg, zusatz = [], set(), {}
    if not os.path.exists(pfad):
        return gruppen, weg, zusatz
    liste, auto = {}, {}                                # «normal: 44,45» und gefundene Seiten aus «> normal: S. 44 …»
    for z in open(pfad, encoding="utf-8").read().split("\n"):
        m = re.match(r"(>\s*)?(normal|uz|unzensiert)\s*:(.*)$", z.strip(), re.I)
        if m and gruppen:
            f = "normal" if m.group(2).lower() == "normal" else "uz"
            if m.group(1):
                auto.setdefault(len(gruppen) - 1, {})[f] = {n for a, b in re.findall(r"S\.\s*(\d+)(?:-(\d+))?", m.group(3))
                                                            for n in range(int(a), int(b or a) + 1)}
            else:
                liste.setdefault(len(gruppen) - 1, {})[f] = m.group(3).strip()
            continue
        if not z.strip() or z[0] in " \t" or z.lstrip()[0] in "#>$":
            continue
        s = STELLEN.sub("", z.strip())
        if s.startswith("+") and gruppen:               # «+ uz: 59» = Seite von Hand dazu (zur Gruppe darüber)
            f, _, nr = s[1:].partition(":")
            zusatz.setdefault(len(gruppen) - 1, {})["uz" if f.strip().lower() in ("uz", "unzensiert") else "normal"] = nr.strip()
            continue
        if s.startswith(WEG):
            weg.update(b.strip() for b in s[len(WEG):].split("|") if b.strip() and b.strip() != "MusterName")
            continue
        begriffe = [b.strip() for b in STELLEN.sub("", s).split("|") if b.strip()]
        if begriffe:
            gruppen.append(begriffe)
    import fassungen
    for i, fs in liste.items():                         # eigene Seiten = in der Liste, aber nicht gefunden
        for f, text in fs.items():
            eigen = sorted(set(fassungen.seiten_lesen(text)) - auto.get(i, {}).get(f, set())
                           | set(fassungen.seiten_lesen(zusatz.get(i, {}).get(f, ""))))
            zusatz.setdefault(i, {})[f] = seiten_text(eigen)
    return gruppen, weg, zusatz


def alle_seiten(t, kap, gruppe, extra=""):
    """Seiten für Leseprobe und Gegenlesen: Fundstellen + ganze Kapitel mit einem Begriff im Titel + «+»-Seiten."""
    import fassungen
    titel = {kap.get(s) for s in t if kap.get(s) and any(b.lower() in kap[s].lower() for b in gruppe)}
    return sorted(set(t) | {s for s, k in kap.items() if k in titel} | set(fassungen.seiten_lesen(extra)))


def vorschlaege(base, bk, seiten_alle):
    """Begriffe, die im Buch vorkommen: Vornamen, Rollenwörter und Stichwörter mit Vornamen."""
    kandidaten = set(ROLLEN) | set(VORNAMEN)
    sw = bk.stichwort_datei()
    if sw:
        for z in open(os.path.join(base, sw), encoding="utf-8"):
            for teil in z.split("|"):
                t = teil.strip()
                if t and not t.startswith("#") and t.split()[0] in VORNAMEN:
                    kandidaten.add(t)
    gefunden = []
    for k in sorted(kandidaten):
        if any(treffer(s, [k], kp) for s, kp in seiten_alle):
            gefunden.append(k)
    # Vorname allein weglassen, wenn «Vorname Nachname» gefunden wurde
    voll = {k.split()[0] for k in gefunden if " " in k}
    return [k for k in gefunden if k not in voll]


def seiten_text(liste):
    import fassungen
    return fassungen.seiten_text(liste).replace(" ", "").replace("–", "-")


def quellen(base, bk):
    """[(fassung, kürzel, pfad)] der vorhandenen Lese-PDFs."""
    out = []
    for f, k in (("normal", "A"), ("uz", "B")):
        if f == "uz" and not bk.zweite_ausgabe():
            continue
        g = bk.AUSGABEN[k]
        p = os.path.join(base, g["ordner"], g["datei"] + ".pdf")
        if os.path.exists(p):
            out.append((f, k, p))
    if not out:
        raise SystemExit("> Kein Lese-PDF gefunden.\n$ sh build.sh final   (oder: sh build.sh nur-pdf final)")
    return out


def veraltet_hinweis(base, bk, pdfs):
    import geschichten as G
    texte = [os.path.join(base, d) for d in (bk.TEXT, bk.VARIABLEN) if d] + list(G.alle(base).values())
    neu = max((os.path.getmtime(t) for t in texte if os.path.exists(t)), default=0)
    if any(os.path.getmtime(p) < neu for _, _, p in pdfs):
        print("> Hinweis: Die Texte sind neuer als das Lese-PDF – Seiten können verschoben sein.\n"
              "$ sh build.sh final   (zuerst)")


def schreiben(base, bk, gruppen, weg, daten, neu_ab, pdfs, zusatz):
    titel = bk.V("titel")
    beispiel = gruppen[0][0] if gruppen else "Name"
    z = [f"# PERSONEN UND SEITEN – {titel} · {datetime.now():%d.%m.%Y %H:%M}",
         "> Begriffe derselben Person in eine Zeile, mit | getrennt. Der erste ist der Name (für die Datei).",
         "> normal: / uz: = Seiten fürs Check-PDF – eigene Seiten einfach dazuschreiben, z. B. normal: 44-45,47,55",
         "> Zeilen mit > schreibt pureSATZ jedes Mal neu: S. = gedruckte Seite, Z. = Zeile (wie im Korrektur-PDF).",
         f"> Keine Person: unten unter «KEINE PERSONEN» als «{WEG} Wort». Ganze Zeile gelöscht = wieder vorgeschlagen.",
         "> Dir fehlt ein Name oder Begriff? Als eigene Zeile hinzufügen und sh build.sh personen nochmals aufrufen.",
         "> Gesucht in: " + " · ".join(f"{os.path.relpath(p, base)} ({datetime.fromtimestamp(os.path.getmtime(p)):%d.%m.%Y %H:%M})"
                                      for _, _, p in pdfs),
         "$ sh build.sh personen   (Seiten neu, nach dem Korrigieren)",
         f"$ sh build.sh personen {beispiel}   (check_{_dateiname(beispiel)}_Gegenlesen.pdf)", "",
         "# GEFUNDENE PERSONEN UND BEGRIFFE", ""]
    for i, g in enumerate(gruppen):
        if i == neu_ab:
            z += [f"# NEU GEFUNDEN {datetime.now():%d.%m.%Y}", f"> prüfen, zusammennehmen oder mit «{WEG}» ausschliessen", ""]
        d = daten[i]
        n = sum(len(zs) for f in d for zs in d[f]["treffer"].values())
        kopf = " | ".join(g)
        z.append(f"{kopf:<46} {n} Stelle{'n' if n != 1 else ''}" + ("   ← kommt nicht vor" if n == 0 else ""))
        details = []
        for f in d:
            t, kap = d[f]["treffer"], d[f]["kapitel"]
            alle = alle_seiten(t, kap, g, zusatz.get(i, {}).get(f, ""))
            if alle:
                z.append(f"{f}: {seiten_text(alle)}")
            if t:
                stellen = [f"S. {s} Z. {', '.join(map(str, zs))}" if s > 1 else f"Umschlag Z. {', '.join(map(str, zs))}"
                           for s, zs in sorted(t.items())]
                stellen += [f"ganzes Kapitel S. {seiten_text([s for s, x in kap.items() if x == k])}"
                            for k in dict.fromkeys(kap.get(s, "") for s in sorted(t)) if k and any(b.lower() in k.lower() for b in g)]
                details.append(f"> {f}: {' · '.join(stellen)}")
        z += details
        z.append("")
    z += ["# KEINE PERSONEN", "> nicht mehr vorschlagen – Zeile löschen = wieder vorschlagen"] \
        + [f"{WEG} {w}" for w in sorted(weg, key=str.lower) or ["MusterName"]] + [""]
    with open(os.path.join(base, DATEI), "w", encoding="utf-8") as f:
        f.write("\n".join(z))


def _dateiname(name):
    return re.sub(r"[^0-9A-Za-zÄÖÜäöüß_-]+", "-", name.strip()).strip("-") or "Person"


def befehl(base, bk, argumente):
    """argumente: [] = Liste erstellen/aktualisieren · [Name] = Check-PDFs zum Gegenlesen."""
    pdfs = quellen(base, bk)
    veraltet_hinweis(base, bk, pdfs)
    print("Lese die Lese-PDFs …", flush=True)
    seiten = {f: zeilen(p) for f, _, p in pdfs}
    kap = {f: kapitel(p) for f, _, p in pdfs}
    pfad = os.path.join(base, DATEI)
    gruppen, weg, zusatz = lies(pfad)

    if argumente:                                   # sh build.sh personen Thomas
        name = " ".join(argumente).strip()
        g = next((g for g in gruppen if g[0].lower() == name.lower()), None) \
            or next((g for g in gruppen if any(b.lower() == name.lower() for b in g)), None)
        if not g:
            g = [name]
            print(f"«{name}» steht nicht in {DATEI} – suche nur dieses Wort.")
        gegenlesen(base, bk, g, pdfs, seiten, kap, zusatz.get(gruppen.index(g), {}) if g in gruppen else {})
        return

    autor = (bk.V("autor") or "").split()
    bekannt = {b.lower() for gr in gruppen for b in gr} | {w.lower() for w in weg} | {a.lower() for a in autor[:1]}
    neu = [k for k in vorschlaege(base, bk, [(seiten[f], kap[f]) for f in seiten]) if k.lower() not in bekannt]
    neu_ab = len(gruppen) if (gruppen and neu) else None
    gruppen += [[k] for k in neu]
    daten = [{f: {"treffer": treffer(seiten[f], g, kap[f]), "kapitel": kap[f]} for f in seiten} for g in gruppen]
    schreiben(base, bk, gruppen, weg, daten, neu_ab, pdfs, zusatz)
    print(f"{DATEI}: {len(gruppen)} Personen" + (f", davon {len(neu)} neu gefunden" if neu else ""))
    for i, (g, d) in enumerate(zip(gruppen, daten)):
        n = sum(len(zs) for f in d for zs in d[f]["treffer"].values())
        teile = [f"{f} {seiten_text(s)}" for f in d
                 for s in [alle_seiten(d[f]["treffer"], d[f]["kapitel"], g, zusatz.get(i, {}).get(f, ""))] if s]
        print(f"  {g[0]:<24} {n:>3} Stelle{'n' if n != 1 else ' '}  " + (" · ".join(teile) if teile else "– kommt nicht vor"))
    b = gruppen[0][0] if gruppen else "Name"
    print(f"\n> Prüfen und korrigieren: {DATEI}\n$ sh build.sh personen   (Seiten neu)\n$ sh build.sh personen {b}   (Check-PDF zum Gegenlesen)")


def gegenlesen(base, bk, gruppe, pdfs, seiten, kap, extra=None):
    import fassungen
    name = gruppe[0]
    erstellt = []
    for f, k, p in pdfs:
        t = treffer(seiten[f], gruppe, kap[f])
        nummern = [s for s in alle_seiten(t, kap[f], gruppe, (extra or {}).get(f, "")) if s > 1]
        if not nummern:
            continue
        r = fassungen.PdfReader(fassungen.io.BytesIO(open(p, "rb").read()))
        box = r.pages[0].mediabox
        zeilen_ = [f"Diese Seiten aus «{bk.V('titel', fassung=f)}»", f"erwähnen «{' / '.join(gruppe)}»:",
                   seiten_text(nummern).replace(",", ", "), "", f"Rückmeldung bitte an {bk.V('autor')}"]
        web = bk.V("website")
        if web:
            zeilen_.append(web)
        schluss = fassungen.schlussseite(float(box.width), float(box.height), "Danke fürs Gegenlesen", zeilen_,
                                         bk.schrift("titel"), bk.schrift("text"), bk.DEEP, bk.INK, "")
        ziel = os.path.join(os.path.dirname(p), f"check_{_dateiname(name)}_Gegenlesen{'-uz' if f == 'uz' else ''}.pdf")
        n, was = fassungen.leseprobe(p, ziel, None, schluss, mit_rueckseite=False, seiten=nummern)
        # wie das Korrektur-PDF: A4, Zeilennummern links, Notizlinien rechts (Rückmeldung «S. 41, Z. 7»)
        fassungen.korrektur(ziel, ziel, f"Gegenlesen · {name} · Seitenzahl unten auf der Buchseite verwenden",
                            schrift=bk.schrift("titel_normal"),        # Poppins: eingebettet, keine Warnung
                            markiert=treffer(zeilen(ziel), gruppe))    # Stellen der Person: rotes ▶
        from pypdf import PdfReader, PdfWriter
        w = PdfWriter(clone_from=PdfReader(ziel))
        w.add_metadata({"/Title": f"{bk.V('titel', fassung=f)} – zum Gegenlesen: {name}"})
        with open(ziel, "wb") as d:
            w.write(d)
        erstellt.append(ziel)
        print(f"Gegenlesen · {'Unzensiert' if f == 'uz' else 'normal'}: {os.path.relpath(ziel, base)} ({n} Seiten, {was})")
    if not erstellt:
        print(f"«{name}» kommt in den Lese-PDFs nicht vor – kein Check-PDF erstellt.")
