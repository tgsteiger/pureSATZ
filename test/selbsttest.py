#!/usr/bin/env python3
"""
selbsttest.py – prüft pureSATZ von A bis Z (läuft bei jedem «git push» auf GitHub: Linux, Mac, Windows).

Legt in einem leeren Ordner ein Testbuch an (wie setup/setup.sh), richtet die Python-Umgebung ein und baut:
final (Bildschirm-PDF, Buchblock, Hardcover- und Softcover-Umschlag, E-Book), schnell, leseprobe, korrektur,
sicherung, Geschichten (neu, einbinden, Sammel-PDF, Tippfehler), Druckangaben (druck=…, BoD). Danach wird geprüft, ob alle Dateien da sind. Fehler = Abbruch mit Meldung.

Auch von Hand möglich (im Ordner pureSATZ):   python3 test/selbsttest.py
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

HIER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))     # Ordner pureSATZ
OHNE_VENV = os.environ.get("SELBSTTEST_OHNE_VENV") == "1"               # Pakete schon installiert (lokaler Test)

START = """TITEL = Testbuch
UNTERTITEL = Ein Buch für den Selbsttest
AUTOR = Vorname Nachname
NAME = Testbuch
FORMAT = a5
BINDUNG = beide
ZWEITE_AUSGABE = ja
ZWEITE_NAME = Director's Cut
ORT = Ort
JAHR = 2027
WEBSITE = www.beispiel.ch
ADRESSE = Strasse 1, 3000 Bern
"""


def lauf(befehl, ordner):
    print("\n>>> " + " ".join(befehl), flush=True)
    r = subprocess.run(befehl, cwd=ordner, env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    if r.returncode:
        sys.exit(f"FEHLER: «{' '.join(befehl)}» endete mit Code {r.returncode}")


def main():
    tmp = tempfile.mkdtemp(prefix="pureSATZ-test-")
    lb = os.path.join(tmp, "pureSATZ")
    shutil.copytree(HIER, lb, ignore=shutil.ignore_patterns(".git", ".venv", "__pycache__"))
    with open(os.path.join(lb, "test-start.txt"), "w", encoding="utf-8") as f:
        f.write(START)
    lauf([sys.executable, os.path.join("setup", "setup.py"), "test-start.txt"] + (["--ohne-venv"] if OHNE_VENV else []), lb)
    buch = os.path.join(tmp, "Testbuch")
    # Hallo-Buch (2.14): erster Blick, ohne Fragen
    lauf([sys.executable, os.path.join("setup", "hallo.py"), "--nicht-oeffnen"] + (["--ohne-venv"] if OHNE_VENV else []), lb)
    lauf([sys.executable, os.path.join("motor", "hilfe.py")], lb)
    if OHNE_VENV:
        py = sys.executable
    else:
        py = os.path.join(buch, ".venv", "Scripts" if os.name == "nt" else "bin",
                          "python.exe" if os.name == "nt" else "python3")
    for art in (["komplett"], ["schnell"]):              # komplett = final + Leseprobe + Korrektur (2.20.1)
        lauf([py, os.path.join("motor", "bauen.py")] + art, buch)
    lauf([py, os.path.join("motor", "sicherung.py"), "lokal"], buch)
    # Druckangaben (2.19): Muster aus druck/, Testlauf BoD nur für die normale Fassung -> ausgabe-test/
    bd = os.path.join(buch, "druck", "bod-a5-hardcover.md")             # 2.22: Versatz mittesten
    with open(bd, encoding="utf-8") as f_:
        bd_text = f_.read()
    with open(bd, "w", encoding="utf-8") as f_:
        f_.write(bd_text.replace("- versatz-vertikal:\n", "- versatz-vertikal: -1.5\n", 1))
    lauf([py, os.path.join("motor", "bauen.py"), "nur-druck", "final", "druck=bod-a5-hardcover", "normal"], buch)

    # Geschichten (2.11): zwei anlegen, eine einbinden, Sammel-PDF, Tippfehler muss als Fehler kommen
    lauf([py, os.path.join("motor", "geschichten.py"), "Erste Geschichte"], buch)
    lauf([py, os.path.join("motor", "geschichten.py"), "Zweite Geschichte"], buch)
    md = os.path.join(buch, "Testbuch-buch.md")
    text = open(md, encoding="utf-8").read()
    with open(md, "w", encoding="utf-8") as f:
        f.write(text.replace("# Teil 1|", "@@erste-geschichte\n\n# Teil 1|", 1))
    # Tabellen (2.12): eine schmale, eine sehr breite (muss quer werden); Leseprobe nach Seiten, normal und zweite Ausgabe
    os.makedirs(os.path.join(buch, "tabellen"), exist_ok=True)
    with open(os.path.join(buch, "tabellen", "schmal.csv"), "w", encoding="utf-8") as f:
        f.write("Schmale Tabelle\nWas;Wie viel\nTee;2 Tassen\nWasser;1.5 l\nQuelle: Test\n")
    with open(os.path.join(buch, "tabellen", "breit.csv"), "w", encoding="utf-8") as f:
        f.write("Breite Tabelle\n" + ";".join(f"Spalte Nummer {i}" for i in range(12)) + "\n"
                + "\n".join(";".join(f"Langer Inhalt {r}-{i}" for i in range(12)) for r in range(6)) + "\n")
    text = text.replace("# Teil 1|", "@#schmal\n\n@# breit\n\n# Teil 1|", 1)
    with open(md, "w", encoding="utf-8") as f:
        f.write(text.replace("# Teil 1|", "@@erste-geschichte\n\n# Teil 1|", 1))
    vd = os.path.join(buch, "Testbuch-variablen.md")
    v = open(vd, encoding="utf-8").read()
    with open(vd, "w", encoding="utf-8") as f:
        f.write(v.replace("- leseprobe-seiten:\n", "- leseprobe-seiten: 5,7-8\n- leseprobe-seiten-uz: 6\n", 1)
                .replace("- foto-format:\n", "- foto-format: 3:2\n", 1)
                .replace("- md-history-behalten: 200\n", "- md-history-behalten: 3\n", 1)
                .replace("- ebook-epub2: nein\n", "- ebook-epub2: ja\n", 1))
    lauf([py, os.path.join("motor", "bauen.py"), "schnell"], buch)
    lauf([py, os.path.join("motor", "bauen.py"), "nur-ebook", "final"], buch)       # mit ebook-epub2: ja (2.20)
    lauf([py, os.path.join("motor", "bauen.py"), "leseprobe"], buch)
    lauf([py, os.path.join("motor", "bauen.py"), "geschichten", "uz"], buch)
    with open(md, "w", encoding="utf-8") as f:
        f.write(text.replace("# Teil 1|", "@@erste-geschichtx\n\n# Teil 1|", 1))
    r = subprocess.run([py, os.path.join("motor", "bauen.py"), "pruefen"], cwd=buch, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    tippfehler_erkannt = r.returncode != 0 and "@@erste-geschichte?" in (r.stdout + r.stderr)
    with open(md, "w", encoding="utf-8") as f:
        f.write(text.replace("# Teil 1|", "@@erste-geschichte\n\n# Teil 1|", 1))

    # Import aus LibreOffice (.odt) und Word (.docx) – Testphase
    importiert = []
    for endung in ("odt", "docx"):
        name = f"Import-{endung}"
        lauf([py, os.path.join("import", "import-text.py"), os.path.join(lb, "test", f"import-test.{endung}"), "--name", name,
              "--ohne-venv"], lb)
        ib = os.path.join(tmp, name)
        lauf([py, os.path.join("motor", "bauen.py"), "schnell"], ib)
        importiert.append(os.path.join(ib, "ausgabe-normal", f"{name}.pdf"))
        importiert.append(os.path.join(ib, "fotos"))

    normal, zweite = os.path.join(buch, "ausgabe-normal"), os.path.join(buch, "ausgabe-directors-cut")
    erwartet = [os.path.join(normal, n) for n in (
        "Testbuch.pdf", "Testbuch.epub", "Testbuch_Leseprobe.pdf", "Testbuch_Leseprobe.epub", "Testbuch_Korrektur.pdf",
        "shop-angaben.txt", "TESTBUCH_Buchblock.pdf", "TESTBUCH_Umschlag_Hardcover.pdf", "TESTBUCH_Umschlag_Hardcover.jpg",
        "TESTBUCH_Umschlag_Softcover.pdf", "TESTBUCH_Umschlag_Softcover.jpg", "TESTBUCH_Probedruck_booklet.pdf", "Testbuch_Mockup.jpg", "Testbuch_Vorderseite.jpg",
        "Testbuch_Cover-vorne.jpg", "Testbuch_Cover-hinten.jpg", "Testbuch_Inhalt.pdf", "Testbuch_Cover-vorne_900px.jpg")]
    erwartet += [os.path.join(zweite, "Testbuch_Directors-Cut.pdf"), os.path.join(zweite, "Testbuch_Directors-Cut.epub")]
    erwartet.append(os.path.join(normal, "Testbuch_EPUB2.epub"))          # epub2-light, auch für EPUBCheck
    fehlt = [os.path.relpath(p, buch) for p in erwartet if not os.path.exists(p) or os.path.getsize(p) == 0]
    fehlt += [os.path.relpath(p, tmp) for p in importiert if not os.path.exists(p)]
    fehlt += [f for f in ("update.sh", "update.bat", "neu.sh", "neu.bat", os.path.join("motor", "update.py"),
                          os.path.join("geschichten", "erste-geschichte.md"), os.path.join("geschichten", "UEBERSICHT.md"),
                          "geschichten-uebersicht.html", os.path.join("ausgabe-normal", "Testbuch_Geschichten.pdf"),
                          os.path.join("ausgabe-directors-cut", "Testbuch_Directors-Cut_Geschichten.pdf"), "hilfe.html")
              if not os.path.exists(os.path.join(buch, f))]
    lp_text = ""
    try:
        from pypdf import PdfReader
        lp = os.path.join(buch, "ausgabe-normal", "Testbuch_Leseprobe.pdf")
        if os.path.exists(lp) and "Breite Tabelle" not in "".join(p.extract_text() or "" for p in
                                                                   PdfReader(os.path.join(buch, "ausgabe-normal", "Testbuch.pdf")).pages):
            fehlt.append("Tabelle «breit» fehlt im PDF")
    except ImportError:
        pass
    if not os.path.exists(os.path.join(tmp, "Hallo-Buch", "ausgabe-normal", "Hallo-Buch.pdf")):
        fehlt.append("Hallo-Buch/ausgabe-normal/Hallo-Buch.pdf")
    else:
        try:
            from pypdf import PdfReader
            hallo_text = "".join(p.extract_text() or "" for p in PdfReader(
                os.path.join(tmp, "Hallo-Buch", "ausgabe-normal", "Hallo-Buch.pdf")).pages)
            if "Ein Buch entsteht" not in hallo_text:
                fehlt.append("Hallo-Buch: Muster-Tabelle «Ein Buch entsteht» fehlt im PDF")
            if not re.search(r"3\.\s*Dritter Schritt", hallo_text):
                fehlt.append("Hallo-Buch: nummerierte Aufzählung «3. Dritter Schritt» fehlt im PDF")
        except ImportError:
            pass
    if 'class="startk"' not in open(os.path.join(lb, "hilfe.html"), encoding="utf-8").read():
        fehlt.append("hilfe.html (pureSATZ): Knopf «Start» fehlt")
    zu = [f for f in os.listdir(os.path.join(buch, "_bildcache")) if "_1.500_" in f] if os.path.isdir(
        os.path.join(buch, "_bildcache")) else []
    if not zu:
        fehlt.append("foto-format 3:2: kein zugeschnittenes Foto in _bildcache/")
    hist = [f for f in os.listdir(os.path.join(buch, "md-history")) if f.startswith("Testbuch-buch_")]
    if len(hist) > 3:
        fehlt.append(f"md-history-behalten: 3, aber {len(hist)} Stände von Testbuch-buch.md")
    hh = os.path.join(buch, "hilfe.html")
    if os.path.exists(hh):
        ht = open(hh, encoding="utf-8").read()
        for muss in ('id="suche"', "Befehle (@)", "Variablen", "@@name", "Buchformate", "taschenbuch", "class=dies",
                     "tgsteiger.github.io/pureSATZ", "Andere Plattformen", "00-UEBERSICHT.txt"):
            if muss not in ht:
                fehlt.append(f"hilfe.html: «{muss}» fehlt")
    if not tippfehler_erkannt:
        fehlt.append("Prüfung: Tippfehler @@erste-geschichtx wurde nicht erkannt")
    for endung in ("odt", "docx"):
        md = open(os.path.join(tmp, f"Import-{endung}", f"Import-{endung}-buch.md"), encoding="utf-8").read()
        for muss in ("# Teil 1|Erster Teil|", "## Ein Kapitel", "**fettem Wort**", "- Punkt eins",
                     "text: Eine Sonne am Himmel", "> Alles ist bereits in dir."):
            if muss not in md:
                fehlt.append(f"Import-{endung}: «{muss}» fehlt in der Buch-MD")
    zips = [f for f in os.listdir(os.path.join(tmp, "Sicherungen"))] if os.path.isdir(os.path.join(tmp, "Sicherungen")) else []
    if not zips:
        fehlt.append("../Sicherungen/Testbuch_*.zip")
    else:
        with zipfile.ZipFile(os.path.join(tmp, "Sicherungen", zips[0])) as z:
            if "Testbuch/Testbuch-buch.md" not in z.namelist():
                fehlt.append("Testbuch-buch.md in der Sicherung")
    bod = os.path.join(buch, "ausgabe-test", "bod-a5-hardcover")
    # 2.21.1: nur eingebettete Schriften – geprüft mit dem Python des Buchs (dort sind reportlab und pypdf)
    pruef = ("import sys, json; sys.path.insert(0, 'motor'); import bauen\n"
             "print(json.dumps({f: bauen.nicht_eingebettet('ausgabe-normal/' + f) for f in sys.argv[1:]}))")
    r = subprocess.run([py, "-c", pruef, "TESTBUCH_Buchblock.pdf", "Testbuch.pdf", "TESTBUCH_Umschlag_Hardcover.pdf"],
                       cwd=buch, capture_output=True, text=True, encoding="utf-8", errors="replace",
                       env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    try:
        import json
        for pdf, funde in json.loads(r.stdout.strip().splitlines()[-1]).items():
            if funde:
                fehlt.append(f"{pdf}: nicht eingebettete Schrift {list(funde)}")
    except Exception:
        fehlt.append(f"Schriftprüfung nicht möglich ({(r.stderr or r.stdout).strip()[-300:]})")
    for f in ("TESTBUCH_Buchblock.pdf", "TESTBUCH_Umschlag_Hardcover.pdf", "bod-a5-hardcover.md"):
        if not os.path.exists(os.path.join(bod, f)):
            fehlt.append(f"ausgabe-test/bod-a5-hardcover/{f} (druck=bod-a5-hardcover)")
    ue = os.path.join(normal, "00-UEBERSICHT.txt")
    if not os.path.exists(ue) or "BEI DER DRUCKEREI" not in open(ue, encoding="utf-8").read():
        fehlt.append("ausgabe-normal/00-UEBERSICHT.txt (mit «BEI DER DRUCKEREI»)")
    if not os.path.exists(os.path.join(bod, "00-UEBERSICHT.txt")):
        fehlt.append("ausgabe-test/bod-a5-hardcover/00-UEBERSICHT.txt")
    if not os.path.exists(os.path.join(buch, "druck", "epubli-a5.md")):
        fehlt.append("druck/epubli-a5.md (Muster aus vorlage/druck/)")
    for e in ("Testbuch.epub", "Testbuch_EPUB2.epub", "Testbuch_Leseprobe.epub"):   # Rückseite als letzte Seite (2.23)
        ep = os.path.join(normal, e)
        if os.path.exists(ep) and "OEBPS/img/rueckseite.jpg" not in zipfile.ZipFile(ep).namelist():
            fehlt.append(f"{e}: Rückseite (ebook-rueckseite: bild) fehlt")
    try:
        from pypdf import PdfReader
        bb = os.path.join(bod, "TESTBUCH_Buchblock.pdf")
        if os.path.exists(bb) and not (PdfReader(bb).pages[2].extract_text() or "").strip():
            fehlt.append("BoD-Buchblock mit versatz-vertikal: Seite 3 ohne Text")
        if os.path.exists(bb):
            box = PdfReader(bb).pages[0].mediabox
            if (round(float(box.width) / 72 * 25.4), round(float(box.height) / 72 * 25.4)) != (148, 210):
                fehlt.append("BoD-Buchblock: erwartet 148 x 210 mm (ohne Beschnitt)")
        hc = os.path.join(bod, "TESTBUCH_Umschlag_Hardcover.pdf")
        if os.path.exists(hc):
            box = PdfReader(hc).pages[0].mediabox
            if round(float(box.height) / 72 * 25.4) != 250:
                fehlt.append("BoD-Umschlag: erwartet 250 mm hoch (Deckel 216 + 2 x 17 mm)")
    except ImportError:
        pass
    if fehlt:
        print("\nVorhanden:", *sorted(os.listdir(normal)), sep="\n  ")
        sys.exit("FEHLER – es fehlt:\n  " + "\n  ".join(fehlt))
    print(f"\nSELBSTTEST IN ORDNUNG ({sys.platform}, Python {sys.version.split()[0]}): {len(erwartet) + 1} Dateien und 2 Importe geprüft.")
    if os.environ.get("SELBSTTEST_BEHALTEN") == "1":          # für EPUBCheck auf GitHub: Liste der E-Books
        liste = os.path.join(os.environ.get("RUNNER_TEMP", tmp), "selbsttest-epubs.txt")
        with open(liste, "w", encoding="utf-8") as f:
            f.write("\n".join(p for p in erwartet if p.endswith(".epub")))
        print("E-Books für EPUBCheck:", liste)
    else:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
