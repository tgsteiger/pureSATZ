#!/usr/bin/env python3
"""
bauen.py – steuert den Bau des Buchs (wird von build.sh aufgerufen).

Aufruf (im Buchordner, mit der Python-Umgebung .venv):
    python motor/bauen.py                 alles als Entwurf: Bildschirm-PDF, Druckdateien, E-Book
    python motor/bauen.py final           alles als Druckfassung (offene Stellen, Notizen, Vorschläge ausgeblendet)
    python motor/bauen.py nur-pdf         nur Bildschirm-PDFs (Entwurf)
    python motor/bauen.py nur-pdf final   nur Bildschirm-PDFs (Druckfassung)
Booklets zum Selberdrucken entstehen automatisch: im «final» der Probedruck aus der Druckfassung
(<kurz>_Probedruck_booklet.pdf), sonst aus dem Bildschirm-PDF (<datei>_booklet.pdf).
    python motor/bauen.py nur-druck [final]   nur Druckdateien (Buchblock, Umschlag)
    python motor/bauen.py nur-ebook [final]   nur E-Books
    python motor/bauen.py schnell         nur Lese-PDFs, so schnell wie möglich (beim Schreiben)
    python motor/bauen.py leseprobe       Leseprobe: Umschlag, Titelei, erste Kapitel (Variable «leseprobe»)
    python motor/bauen.py korrektur [final]   Korrekturfassung: A4, Zeilennummern, Rand für Notizen
    python motor/bauen.py sicherung       nur die MD-Dateien nach md-history/ sichern
    python motor/bauen.py pruefen         nur die MD prüfen
    python motor/bauen.py geschichten [uz]   Sammel-PDF aller Geschichten aus geschichten/ (normal; mit uz auch unzensiert)
    python motor/bauen.py hilfe           hilfe.html erzeugen und im Browser öffnen
Vor jedem Bau: Sicherung nach md-history/ und Prüfung der MD. Gebaut wird parallel.
"""
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime

MOTOR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(MOTOR)
sys.path.insert(0, MOTOR)
import build as bk          # noqa: E402  (liest die Buch-MD)
import manuskript as M      # noqa: E402


def sicherung():
    """Variablen-, Buch- und Umschlag-MD sowie die Stichwort-Datei mit Zeitstempel nach md-history/ kopieren."""
    ordner = os.path.join(BASE, "md-history")
    os.makedirs(ordner, exist_ok=True)
    zeit = f"{datetime.now():%Y%m%d-%H-%M-%S}"
    for datei in (bk.VARIABLEN, bk.TEXT, bk.UMSCHLAG, bk.stichwort_datei()):
        if datei and os.path.exists(os.path.join(BASE, datei)):
            stamm, endung = os.path.splitext(datei)
            shutil.copy2(os.path.join(BASE, datei), os.path.join(ordner, f"{stamm}_{zeit}{endung}"))
    import geschichten as G                 # Geschichten (pureSATZ 2.11) mitsichern
    for name, p in G.alle(BASE).items():
        z = os.path.join(ordner, "geschichten", f"{name}_{zeit}.md")
        os.makedirs(os.path.dirname(z), exist_ok=True)
        shutil.copy2(p, z)
    print(f"Sicherung: md-history/…_{zeit}.md")
    aufraeumen_history(ordner)
    uebersicht()
    hilfe()


def aufraeumen_history(ordner):
    """Variable «md-history-behalten: 200»: pro Datei nur die neuesten N Stände behalten (leer = alle)."""
    import re
    try:
        n = int(bk.V("md-history-behalten", "").strip() or 0)
    except ValueError:
        return
    if n <= 0:
        return
    weg = 0
    for wurzel in (ordner, os.path.join(ordner, "geschichten")):
        if not os.path.isdir(wurzel):
            continue
        gruppen = {}
        for f in os.listdir(wurzel):
            m = re.match(r"^(.*)_(\d{8}-\d{2}-\d{2}-\d{2})(\.\w+)$", f)
            if m:
                gruppen.setdefault((m.group(1), m.group(3)), []).append((m.group(2), f))
        for staende in gruppen.values():
            for _, f in sorted(staende)[:-n]:
                os.remove(os.path.join(wurzel, f)); weg += 1
    if weg:
        print(f"md-history: {weg} ältere Stände entfernt (behalten: je {n}).")


def hilfe(oeffnen=False):
    """hilfe.html im Buchordner (Hilfe mit Suche, pureSATZ 2.13)."""
    try:
        import hilfe as H
        farben = {n: bk.hexfarbe(n) for n in ("papier", "text", "leise", "haupt", "akzent")}
        ziel = H.erzeuge(BASE, bk.V("titel") or "Buch", os.path.join(BASE, bk.VARIABLEN) if bk.VARIABLEN else None,
                         farben, oeffnen)
        if oeffnen:
            print(f"Hilfe: {os.path.relpath(ziel, BASE)} (im Browser geöffnet)")
    except Exception as e:                       # die Hilfe darf nie einen Bau verhindern
        print(f"Hinweis: hilfe.html nicht erstellt ({e})")


def uebersicht(zeigen=False):
    """geschichten-uebersicht.html und geschichten/UEBERSICHT.md – nur wenn es den Ordner geschichten/ gibt."""
    import geschichten as G
    farben = {n: bk.hexfarbe(n) for n in ("papier", "text", "leise", "haupt", "akzent")}
    if G.uebersicht(BASE, os.path.join(BASE, bk.TEXT), bk.V("titel") or "Buch", farben, zeigen) is not None:
        print("Geschichten-Übersicht: geschichten-uebersicht.html")


def sammlung(mit_uz):
    """Sammel-PDF: alle Geschichten aus geschichten/, alphabetisch, mit Stand im Titel."""
    import geschichten as G
    alle = G.alle(BASE)
    if not alle:
        sys.exit("Keine Geschichten im Ordner geschichten/. Neue Geschichte:  sh neu.sh \"Titel\"")
    reihe = sorted(alle, key=lambda n: G.lies(alle[n])[0].lower())
    tmp = "_geschichten-sammlung.md"
    with open(os.path.join(BASE, tmp), "w", encoding="utf-8") as f:
        f.write("## @TITEL\n{titel}\nSammlung aller Geschichten\n\n## @INHALTSVERZEICHNIS\n\n"
                + "\n\n".join("@@" + n for n in reihe) + "\n")
    try:
        fassungen_ = ["normal"] + (["uz"] if mit_uz and bk.zweite_ausgabe() else [])
        schritte = []
        for a in fassungen_:
            g = bk.AUSGABEN["B" if a == "uz" else "A"]
            os.makedirs(os.path.join(BASE, g["ordner"]), exist_ok=True)
            ziel = os.path.join(BASE, g["ordner"], g["datei"] + "_Geschichten.pdf")
            schritte.append((f"Geschichten · {name(a)}", "build.py", a,
                             {"BUCH_TEXT": tmp, "BUCH_ZIEL": ziel, "BUCH_SAMMLUNG": "1"}))
        env = dict(os.environ, BUCH_FINAL="0", BUCH_BOOKLET="", BUCH_SCHNELL="1")
        parallel(schritte, env)
        if mit_uz and not bk.zweite_ausgabe():
            print("Hinweis: dieses Buch hat keine zweite Ausgabe – nur die normale Fassung gebaut.")
    finally:
        os.remove(os.path.join(BASE, tmp))


def pruefen():
    M.pruefen(BASE, bk.TEXT, bk.UMSCHLAG, bk.finde, bk.alle_variablen())
    try:
        bk.foto_hinweise()                  # Fotos mit zu wenig Pixeln (pureSATZ 2.15)
    except Exception as e:                  # nie den Bau verhindern
        print(f"Hinweis: Fotos nicht geprüft ({e})")


def ausgaben():
    return ["normal", "uz"] if bk.zweite_ausgabe() else ["normal"]


def name(a):
    return bk.AUSGABEN["B" if a == "uz" else "A"]["name"]


def parallel(schritte, env):
    """Schritte gleichzeitig starten; Meldungen danach in der gewohnten Reihenfolge zeigen."""
    laeufe = []
    for titel, skript, a, *extra in schritte:
        cmd = [sys.executable, os.path.join(MOTOR, skript)] + (["uz"] if a == "uz" else [])
        e = dict(env, **extra[0]) if extra else env
        e["PYTHONIOENCODING"] = "utf-8"           # Umlaute und «» auch unter Windows
        laeufe.append((titel, subprocess.Popen(cmd, cwd=BASE, env=e, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                               text=True, encoding="utf-8", errors="replace")))
    fehler = []
    for titel, p in laeufe:
        aus, _ = p.communicate()
        print(f"\n=== {titel} ===")
        print(aus.rstrip())
        if p.returncode:
            fehler.append(titel)
    if fehler:
        print("\n*** FEHLER in: " + ", ".join(fehler))
        sys.exit(1)


def statistik():
    """Wörter, Lesezeit und Seiten pro Teil (aus Text und Bildschirm-PDF)."""
    import re
    try:
        from pypdf import PdfReader
    except ImportError:
        PdfReader = None
    print("\nStatistik:")
    for a in ausgaben():
        var = M.Ausgabe(bk.alle_variablen(), a, "bildschirm")
        teile, akt = [], ["Titelei / Vorwort", 0]
        for z in M.zeilen(os.path.join(BASE, bk.TEXT), var, entwurf=False):
            if isinstance(z, tuple):
                if z[0] in ("UZ", "MITTE", "ZUSAMMEN", "OFFEN"):
                    akt[1] += sum(len(re.findall(r"\w+", t)) for t in z[2])
                continue
            t = z.strip()
            if t.startswith("# "):
                teile.append(akt); akt = [t[2:].split("|")[0].strip() + (" " + t.split("|")[1].strip() if "|" in t else ""), 0]
                continue
            if not t or t.startswith(("@", ":::")):
                continue
            akt[1] += len(re.findall(r"\w+", re.sub(r"<[^>]+>|\{[^}]*\}|\[([^\]]*)\]\([^)]*\)", r"\1", t)))
        teile.append(akt)
        teile = [x for x in teile if x[1]]
        gesamt = sum(x[1] for x in teile)
        g = bk.AUSGABEN["B" if a == "uz" else "A"]
        pdf = os.path.join(BASE, g["ordner"], g["datei"] + ".pdf")
        seiten = {}
        if PdfReader and os.path.exists(pdf):
            r = PdfReader(pdf)
            marken = [(o.title, r.get_destination_page_number(o) + 1) for o in r.outline if not isinstance(o, list)]
            for i, (t, von) in enumerate(marken):
                bis = marken[i + 1][1] if i + 1 < len(marken) else len(r.pages)
                seiten[t] = bis - von
        zahl = lambda n: f"{n:,}".replace(",", "'")
        print(f"  {name(a)}: {zahl(gesamt)} Wörter, Lesezeit ca. {gesamt // 200 // 60} h {gesamt // 200 % 60} min")
        for t, w in teile:
            s = next((n for k, n in seiten.items() if k.split(":")[0].split("·")[-1].strip() in t or t.endswith(k)), None)
            print(f"     {zahl(w):>7} Wörter" + (f"  {s:>3} S." if s else "        ") + f"  {t}")


def kontrast_pruefen():
    """Lesbarkeit der Textfarben aus # LAYOUT (WCAG: mind. 4,5:1). Rechnet nur Farbpaare – kostet nichts."""
    texte = [("text", "Text"), ("leise", "leise Schrift"), ("haupt", "Überschriften"), ("akzent", "Teil-Nummern, Jahre")]
    gruende = [("#FFFFFF", "Seite"), (bk.hexfarbe("papier"), "Papier/Umschlag"), (bk.hexfarbe("kasten"), "Kasten")]
    schwach = []
    for n, was in texte:
        f = bk.hexfarbe(n)
        zu_wenig = [(wo, bk.kontrast(f, g)) for g, wo in gruende if bk.kontrast(f, g) < 4.5]
        if zu_wenig:
            schwach.append((n, was, f, zu_wenig, bk.lesbare_farbe(f, [g for g, _ in gruende])))
    if not schwach:
        print("Kontrast: alle Textfarben gut lesbar (mind. 4,5:1).")
        return
    print("Kontrast (Hinweis, nichts geändert; Schmuck wie Linien und Zier darf heller sein):")
    for n, was, f, zu_wenig, vorschlag in schwach:
        werte = ", ".join(f"{k:.1f}:1 auf {wo}" for wo, k in zu_wenig)
        print(f"  farbe-{n} {f} ({was}): {werte} – für Text z. B. {vorschlag}"
              + (" · im E-Book schon korrigiert" if n == "akzent" else ""))


def shop_angaben():
    """Angaben zum Kopieren für epubli, tolino, KDP: <ausgabeordner>/shop-angaben.txt"""
    try:
        from pypdf import PdfReader
    except ImportError:
        PdfReader = None
    for a in ausgaben():
        g = bk.AUSGABEN["B" if a == "uz" else "A"]
        V = lambda n, s="": bk.V(n, s, a)
        block = os.path.join(BASE, g["ordner"], g["kuerzel"] + "_Buchblock.pdf")
        seiten = len(PdfReader(block).pages) if PdfReader and os.path.exists(block) else "?"
        zeilen = [f"Titel:          {V('titel')}", f"Untertitel:     {V('untertitel')}", f"Autor:          {V('autor')}",
                  f"Format:         {bk.FMT['name']}, {V('bindung', 'hardcover')}, {seiten} Seiten",
                  f"Papier:         {V('papier')}",
                  f"ISBN Buch:      {V('isbn-buch') or '(noch keine)'}", f"ISBN E-Book:    {V('isbn-ebook') or '(noch keine)'}",
                  f"Sprache:        {V('sprache', 'de')}", f"Kategorie:      {V('shop-kategorie')}",
                  f"Schlagwörter:   {V('shop-schlagwoerter')}",
                  f"Preis Buch:     {V('preis-buch')}", f"Preis E-Book:   {V('preis-ebook')}",
                  f"Shop-Link:      {V('shop-link')}", "",
                  "Beschreibung:", V("shop-beschreibung") or "(in der Variablen-Datei unter «## Shop» eintragen)"]
        ziel = os.path.join(BASE, g["ordner"], "shop-angaben.txt")
        os.makedirs(os.path.dirname(ziel), exist_ok=True)
        with open(ziel, "w", encoding="utf-8") as f:
            f.write("\n".join(zeilen) + "\n")
        print(f"Shop-Angaben: {os.path.relpath(ziel, BASE)}")


def zwischendatei(a, art):
    g = bk.AUSGABEN["B" if a == "uz" else "A"]
    ordner = os.path.join(BASE, g["ordner"])
    os.makedirs(ordner, exist_ok=True)
    return os.path.join(ordner, f"_tmp_{art}.pdf"), os.path.join(ordner, g["datei"])


def fassung(art, final):
    """Leseprobe oder Korrekturfassung: Bildschirm-PDF in eine Zwischendatei bauen, dann umformen."""
    import fassungen
    env = dict(os.environ, BUCH_FINAL="1" if final else "0", BUCH_BOOKLET="")
    schritte = [(f"{art.capitalize()} · {name(a)}", "build.py", a, {"BUCH_ZIEL": zwischendatei(a, art)[0]})
                for a in ausgaben()]
    # Leseprobe: Seiten (leseprobe-seiten), sonst Kapitel (leseprobe), sonst 4 Seiten nach dem Inhalt
    lp = {}
    if art == "leseprobe":
        for a in ausgaben():
            v = M.Ausgabe(bk.alle_variablen(), a, "ebook")
            alle_v = bk.alle_variablen()      # «-uz» gilt vor dem allgemeinen Wert
            seiten = (alle_v.get(f"leseprobe-seiten-{a}") or v("leseprobe-seiten")).strip()
            kap = (alle_v.get(f"leseprobe-{a}") or v("leseprobe")).strip()
            lp[a] = ("seiten", fassungen.seiten_lesen(seiten)) if seiten else (("kapitel", kap) if kap else ("seiten", None))
        schritte += [(f"Leseprobe E-Book · {name(a)}", "build-epub.py", a, {"BUCH_LESEPROBE": lp[a][1]})
                     for a in ausgaben() if lp[a][0] == "kapitel"]          # Kapitel: E-Book gleich mitbauen
    parallel(schritte, env)
    if art == "leseprobe":
        epub = []
        for a in ausgaben():
            if lp[a][0] == "seiten":
                tmp = zwischendatei(a, art)[0]
                if lp[a][1] is None:                  # Standard: 4 Seiten nach dem Inhaltsverzeichnis
                    r = fassungen.PdfReader(fassungen.io.BytesIO(open(tmp, "rb").read()))
                    start = fassungen.erste_inhaltsseite(r)
                    lp[a] = ("seiten", list(range(start, min(start + 4, len(r.pages)))))
                titel = fassungen.kapitel_der_seiten(tmp, lp[a][1])
                epub.append((f"Leseprobe E-Book · {name(a)}", "build-epub.py", a,
                             {"BUCH_LESEPROBE": "seiten", "BUCH_LESEPROBE_KAPITEL": "\n".join(titel)}))
        if epub:
            parallel(epub, env)
    print()
    for a in ausgaben():
        tmp, stamm = zwischendatei(a, art)
        if art == "leseprobe":
            var = M.Ausgabe(bk.alle_variablen(), a, "druck")
            zeilen, link = fassungen.leseprobe_angaben(bk, a)
            r = fassungen.PdfReader(fassungen.io.BytesIO(open(tmp, "rb").read()))
            box = r.pages[0].mediabox
            schluss = fassungen.schlussseite(float(box.width), float(box.height), "Ende der Leseprobe", zeilen,
                                             bk.schrift("titel"), bk.schrift("text"), bk.DEEP, bk.INK, link)
            hinten = any(z.strip() == "@RUECKSEITE" for z in open(os.path.join(BASE, bk.TEXT), encoding="utf-8"))
            ziel = stamm + "_Leseprobe.pdf"
            n, was = fassungen.leseprobe(tmp, ziel, lp[a][1] if lp[a][0] == "kapitel" else None, schluss, hinten,
                                         seiten=lp[a][1] if lp[a][0] == "seiten" else None)
            print(f"Leseprobe · {name(a)}: {os.path.relpath(ziel, BASE)} ({n} Seiten, {was})")
        else:
            ziel = stamm + "_Korrektur.pdf"
            n = fassungen.korrektur(tmp, ziel, f"{bk.V('titel', fassung=a)} · {name(a)}")
            print(f"Korrektur · {name(a)}: {os.path.relpath(ziel, BASE)} ({n} Seiten auf A4)")
        os.remove(tmp)


def main():
    import geschichten
    geschichten.hilfsdateien(BASE)          # neu.sh / neu.bat, .gitignore (pureSATZ 2.11)
    args = [a.lower() for a in sys.argv[1:]]
    final = "final" in args
    art = next((a for a in args if a not in ("final", "uz")), "alles")
    if art == "sicherung":
        sicherung(); return
    if art == "pruefen":
        pruefen(); return
    if art == "hilfe":
        hilfe(oeffnen=True); return
    if art == "geschichten":
        start = time.time()
        sicherung()
        sammlung("uz" in args)
        print(f"\nFertig in {time.time() - start:.0f} Sekunden.")
        return
    if art == "schnell":                  # nur Lese-PDFs, ein Durchgang, ohne Booklet/Statistik/Prüfung
        start = time.time()
        sicherung()
        env = dict(os.environ, BUCH_FINAL="1" if final else "0", BUCH_BOOKLET="", BUCH_SCHNELL="1")
        parallel([(f"Schnell · {name(a)}", "build.py", a) for a in ausgaben()], env)
        print(f"\nFertig in {time.time() - start:.0f} Sekunden (schnell: ohne Seitenausgleich – für den Druck: final).")
        return
    if art in ("leseprobe", "korrektur"):
        start = time.time()
        sicherung(); pruefen()
        fassung(art, final or art == "leseprobe")       # Leseprobe immer ohne offene Stellen und Notizen
        print(f"\nFertig in {time.time() - start:.0f} Sekunden.")
        return
    if art not in ("alles", "nur-pdf", "nur-druck", "nur-ebook"):
        print(__doc__); sys.exit(1)
    # Booklets: im «final» der Probedruck aus der Druckfassung, sonst aus dem Bildschirm-PDF
    booklet = "druck" if (art == "alles" and final) else ("bildschirm" if art in ("alles", "nur-pdf") else "")
    env = dict(os.environ, BUCH_FINAL="1" if final else "0", BUCH_BOOKLET=booklet)
    start = time.time()
    sicherung()
    pruefen()
    print("Modus:", "FINAL (Druckfassung)" if final else "ENTWURF (offene Stellen und Notizen sichtbar)",
          f"· Format {bk.FMT['name']} · Bindung {bk.V('bindung', 'hardcover')}")
    schritte = []
    for a in ausgaben():
        if art in ("alles", "nur-pdf"):
            schritte.append((f"Bildschirm-PDF · {name(a)}", "build.py", a))
        if art in ("alles", "nur-druck"):
            schritte.append((f"Druckdateien · {name(a)}", "build-broschuere.py", a))
        if art in ("alles", "nur-ebook"):
            schritte.append((f"E-Book · {name(a)}", "build-epub.py", a))
    parallel(schritte, env)
    bk.ENTWURF = not final
    statistik()
    if art == "alles" and final:
        print()
        shop_angaben()
        kontrast_pruefen()
    bk.zeige_offene_stellen()
    ordner = ", ".join(bk.AUSGABEN["B" if a == "uz" else "A"]["ordner"] + "/" for a in ausgaben())
    print(f"\nFertig in {time.time() - start:.0f} Sekunden. Ordner: {ordner}")


if __name__ == "__main__":
    main()
