#!/usr/bin/env python3
"""
bauen.py – steuert den Bau des Buchs (wird von build.sh aufgerufen).

Aufruf (im Buchordner, mit der Python-Umgebung .venv):
    python motor/bauen.py                 alles als Entwurf: Bildschirm-PDF, Druckdateien, E-Book
    python motor/bauen.py final           alles als Druckfassung (offene Stellen, Notizen, Vorschläge ausgeblendet)
    python motor/bauen.py komplett        final + Leseprobe + Korrektur in einem Durchgang (vor Bestellung/Veröffentlichung)
    python motor/bauen.py nur-pdf         nur Bildschirm-PDFs (Entwurf)
    python motor/bauen.py nur-pdf final   nur Bildschirm-PDFs (Druckfassung)
Booklets zum Selberdrucken entstehen automatisch: im «final» der Probedruck aus der Druckfassung
(<kurz>_Probedruck_booklet.pdf), sonst aus dem Bildschirm-PDF (<datei>_booklet.pdf).
    python motor/bauen.py nur-druck [final]   nur Druckdateien (Buchblock, Umschlag)
    python motor/bauen.py nur-ebook [final]   nur E-Books
    python motor/bauen.py schnell         nur Lese-PDFs, so schnell wie möglich (beim Schreiben)
    python motor/bauen.py leseprobe       Leseprobe: Umschlag, Titelei, erste Kapitel (Variable «leseprobe»)
    python motor/bauen.py leseprobe uz 18,20-22   einmalig diese Seiten, nur diese Fassung (normal | uz)
    python motor/bauen.py korrektur [final]   Korrekturfassung: A4, Zeilennummern, Rand für Notizen
    python motor/bauen.py sicherung       nur die MD-Dateien nach md-history/ sichern
    python motor/bauen.py pruefen         nur die MD prüfen
    python motor/bauen.py personen        Personen in den Lese-PDFs finden → personen-seiten.txt (Seiten, Zeilen)
    python motor/bauen.py personen Thomas   check_Thomas_Gegenlesen.pdf aus den fertigen Lese-PDFs
    python motor/bauen.py stand "Name"    jetzigen Stand festhalten (staende/) · ohne Name: alle Stände zeigen
    python motor/bauen.py aenderungen ["Name" ["Name2"]]   was sich seit dem (letzten) Stand geändert hat → …_Aenderungen.pdf
    python motor/bauen.py geschichten [uz]   Sammel-PDF aller Geschichten aus geschichten/ (normal; mit uz auch unzensiert)
    python motor/bauen.py hilfe           hilfe.html erzeugen und im Browser öffnen
    python motor/bauen.py mockup          Werbebilder (…_Mockup.jpg, …_Vorderseite.jpg) aus dem Bildschirm-PDF
    python motor/bauen.py final druck=bod-a5-normal [normal|uz]
                                          Test: nur Druckdateien mit einer anderen Datei aus druck/,
                                          nach ausgabe-test/<datei>/; mit «normal» oder «uz» nur diese Fassung
Vor jedem Bau: Sicherung nach md-history/ und Prüfung der MD. Gebaut wird parallel.
"""
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime
try:                                            # Windows: «sh build.sh» in Meldungen als «.\build.bat»
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "."))
    import plattform
    plattform.windows_befehle()
except ImportError:
    pass

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
    import geschichten as G                 # Geschichten mitsichern
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


def mockups():
    """Werbebilder aus dem Bildschirm-PDF jeder Ausgabe: …_Mockup.jpg und …_Vorderseite.jpg."""
    try:
        import mockup
    except ImportError:
        return
    for a in ausgaben():
        aus = bk.AUSGABEN["B" if a == "uz" else "A"]
        pdf = os.path.join(BASE, aus["ordner"], aus["datei"] + ".pdf")
        if not os.path.exists(pdf):
            print(f"Mockup: {os.path.relpath(pdf, BASE)} fehlt – zuerst sh build.sh nur-pdf final")
            continue
        try:
            for p in mockup.erzeuge(pdf, bk.V("mockup-hintergrund", "#E9EEF4, #C9D3DF") or "#E9EEF4, #C9D3DF"):
                print("Mockup:", os.path.relpath(p, BASE))
        except Exception as e:                       # nie den Bau verhindern
            print(f"Hinweis: Mockup nicht erstellt ({e})")


def hilfe(oeffnen=False):
    """hilfe.html im Buchordner (Hilfe mit Suche)."""
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
    """Sammel-PDF: alle Geschichten aus geschichten/ (Reihenfolge wie im Buch, dann wie angelegt), mit Stand im Titel."""
    import geschichten as G
    alle = G.alle(BASE)
    if not alle:
        sys.exit("Keine Geschichten im Ordner geschichten/. Neue Geschichte:  sh neu.sh \"Titel\"")
    reihe = G.reihe(BASE, os.path.join(BASE, bk.TEXT))
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
    druck_pruefen()
    try:
        bk.foto_hinweise()                  # Fotos mit zu wenig Pixeln
    except Exception as e:                  # nie den Bau verhindern
        print(f"Hinweis: Fotos nicht geprüft ({e})")


NUR_FASSUNG = None          # «normal» oder «uz» zusammen mit druck=… oder leseprobe: nur diese Fassung bauen
LESEPROBE_SEITEN = None     # «sh build.sh leseprobe 18,20,23»: Seiten von der Kommandozeile (vor den Variablen)
SEITEN_MUSTER = r"\d[\d\s,\-–]*"


def ausgaben():
    alle = ["normal", "uz"] if bk.zweite_ausgabe() else ["normal"]
    return [a for a in alle if a == NUR_FASSUNG] if NUR_FASSUNG in alle else alle


def druck_pruefen():
    """Druckdateien (druck/…md): vorhanden? unbekannte Namen?"""
    fehler, hinweise = [], []
    for a in ausgaben():
        d = bk.druck_datei(a)
        if not d:
            continue
        pfad = os.path.join(BASE, d)
        if not os.path.exists(pfad):
            fehler.append(f"Druckangaben {name(a)}: {d} fehlt")
            continue
        for k in M.lies_variablen(pfad)[0]:
            basis = k
            for t in ("-normal", "-uz", "-dc"):
                if k.endswith(t):
                    basis = k[:-len(t)]
            if basis not in bk.DRUCK_NAMEN and not basis.startswith("impressum-"):     # impressum-…: Zeilen fürs Impressum
                hinweise.append(f"{d}: unbekannter Name «{k}» (wird nicht verwendet)")
        try:
            v = M.Ausgabe(bk.alle_variablen(a, druck=True), a, "druck")
            bk.format_angaben(v("format"), v("seite"))
            for n in ("barcode-groesse", "deckel-hardcover"):
                bk.masse_mm(v(n), n)
            if v("barcode-bild") and not bk.finde(v("barcode-bild"), ("bilder",)):
                fehler.append(f"{d}: barcode-bild {v('barcode-bild')} fehlt im Ordner bilder/")
            if v("impressum-logo") and not bk.finde(v("impressum-logo"), ("bilder",)):
                fehler.append(f"{d}: impressum-logo {v('impressum-logo')} fehlt im Ordner bilder/")
        except SystemExit as e:
            fehler.append(f"{d}: {e}")
    for a in ausgaben():                                # Plattform-Datei des E-Books
        d = bk.ebook_datei(a)
        if d and not os.path.exists(os.path.join(BASE, d)):
            fehler.append(f"E-Book-Angaben {name(a)}: {d} fehlt ({{druck-datei}} unter «## Ausgabe: E-Book»)")
    for h in sorted(set(hinweise)):
        print("Hinweis: " + h)
    if fehler:
        sys.exit("FEHLER in den Druckangaben:\n  " + "\n  ".join(sorted(set(fehler))))


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
        V = lambda n, s="": bk.druck_V(n, s, a)        # mit Druckangaben (druck/…md)
        E = lambda n: M.Ausgabe(bk.alle_variablen(a), a, "ebook")(n) if bk.ebook_erstellen(a) else ""
        block = os.path.join(BASE, g["ordner"], g["kuerzel"] + "_Buchblock.pdf")
        seiten = len(PdfReader(block).pages) if PdfReader and os.path.exists(block) else "?"
        zeilen = [f"Titel:          {V('titel')}", f"Untertitel:     {V('untertitel')}", f"Autor:          {V('autor')}",
                  f"Format:         {bk.format_angaben(V('format'), V('seite'))[1]['name']}, {V('bindung', 'hardcover')}, {seiten} Seiten",
                  f"Papier:         {V('papier')}",
                  f"ISBN Buch:      {V('isbn') if V('isbn') not in ('folgt', '') else '(noch keine)'}",
                  f"ISBN E-Book:    {E('isbn') or ('(noch keine)' if bk.ebook_erstellen(a) else '(kein E-Book)')}",
                  f"Sprache:        {V('sprache', 'de')}", f"Kategorie:      {V('shop-kategorie')}",
                  f"Schlagwörter:   {V('shop-schlagwoerter')}",
                  f"Preis Buch:     {V('preis') or V('preis-buch')}", f"Preis E-Book:   {E('preis') or E('preis-ebook')}",
                  f"Shop-Link:      {V('shop-link')}", "",
                  "Beschreibung:", V("shop-beschreibung") or "(in der Variablen-Datei unter «## Shop» eintragen)"]
        ziel = os.path.join(BASE, g["ordner"], "shop-angaben.txt")
        os.makedirs(os.path.dirname(ziel), exist_ok=True)
        with open(ziel, "w", encoding="utf-8") as f:
            f.write("\n".join(zeilen) + "\n")
        print(f"Shop-Angaben: {os.path.relpath(ziel, BASE)}")


# --- 00-UEBERSICHT.txt -----------------------------------------------------
def _datei_info(pfad):
    """Kurzangabe zu einer Datei: Seiten und Masse (PDF), Pixel (JPG/PNG)."""
    try:
        if pfad.lower().endswith(".pdf"):
            from pypdf import PdfReader
            r = PdfReader(pfad); box = r.pages[0].mediabox
            return f"{len(r.pages)} S., {round(float(box.width) / 72 * 25.4, 1):g} x {round(float(box.height) / 72 * 25.4, 1):g} mm"
        if pfad.lower().endswith((".jpg", ".jpeg", ".png")):
            from PIL import Image
            with Image.open(pfad) as im:
                return f"{im.size[0]} x {im.size[1]} px"
    except Exception:
        pass
    return ""


def ausgabe_uebersicht(art, final, test=None):
    """00-UEBERSICHT.txt in jedem Ausgabeordner: welche Datei wofür, FINAL/ENTWURF, Datum (nie den Bau verhindern)."""
    try:
        _uebersicht(art, final, test)
    except Exception as e:
        print(f"Hinweis: 00-UEBERSICHT.txt nicht erstellt ({e})")


def _uebersicht(art, final, test):
    ordner = {}
    for a in ausgaben():
        g = bk.AUSGABEN["B" if a == "uz" else "A"]
        o = os.path.join(BASE, "ausgabe-test", test) if test else os.path.join(BASE, g["ordner"])
        ordner.setdefault(o, []).append((a, g))
    jetzt = datetime.now()
    for o, liste in ordner.items():
        if not os.path.isdir(o):
            continue
        vorhanden = sorted(f for f in os.listdir(o) if os.path.isfile(os.path.join(o, f))
                           and f != "00-UEBERSICHT.txt" and not f.startswith("_tmp"))
        gebraucht = set()
        z = []
        alt = ""                                            # Stand der Druckdateien aus der letzten Übersicht
        if os.path.exists(os.path.join(o, "00-UEBERSICHT.txt")):
            alt = next((x[x.index("Druckdateien: "):] for x in open(os.path.join(o, "00-UEBERSICHT.txt"), encoding="utf-8").read().split("\n")
                        if "Druckdateien: " in x), "")
        zeile = lambda n: (f"  {n:<52} {datetime.fromtimestamp(os.path.getmtime(os.path.join(o, n))):%d.%m. %H:%M}"
                           + (f"   {_datei_info(os.path.join(o, n))}" if _datei_info(os.path.join(o, n)) else ""))
        for a, g in liste:
            K, D = g["kuerzel"], g["datei"]
            v = lambda n, s="": bk.druck_V(n, s, a)
            plattform = v("plattform", "epubli").strip().lower()
            druck = bk.druck_datei(a)
            z += [f"# {bk.V('titel', fassung=a)} – {g['name']}".upper() + (f" · TEST {test}" if test else ""),
                  f"> Letzter Bau: {'FINAL (Druckfassung)' if final else 'ENTWURF (offene Stellen sichtbar)'} · "
                  f"«{art}» · {jetzt:%d.%m.%Y %H:%M} · pureSATZ {open(os.path.join(MOTOR, 'VERSION')).read().strip()}",
                  "> " + ((f"Druck: {druck} · " if druck else "")
                          + (f"Druckdateien: {'FINAL (Druckfassung)' if final else 'ENTWURF – nicht hochladen!'} · {jetzt:%d.%m.%Y %H:%M}"
                             if art in ("alles", "nur-druck", "komplett") else (alt or "Druckdateien: noch nicht gebaut"))),
                  "> Bei jeder Datei Datum und Uhrzeit – so siehst du, ob sie vom letzten Bau stammt.", ""]
            hc = f"{K}_Umschlag_Hardcover"; sc = f"{K}_Umschlag_Softcover"
            gruppen = [      # (Titel, Erklärung, Dateien, Befehl wenn etwas fehlt)
                ("BEI DER DRUCKEREI HOCHLADEN", "epubli: Buchblock als PDF, Umschlag als JPG" if plattform == "epubli" else plattform,
                 [f"{K}_Buchblock.pdf", hc + ".jpg", hc + ".pdf", sc + ".jpg", sc + ".pdf"], "sh build.sh final"),
                ("E-BOOK", "Wix-Shop, tolino, XinXii, KDP … · …_EPUB2.epub nur, wo EPUB 2 verlangt wird",
                 [f"{D}.epub", f"{D}_EPUB2.epub", f"{D}_Inhalt.pdf", f"{D}_Cover-vorne.jpg"]
                 + [f"{D}_Cover-vorne_{px}px.jpg" for px in COVER_GROESSEN] + [f"{D}_Cover-hinten.jpg"],
                 "sh build.sh nur-ebook final"),
                ("ZUM LESEN, VERSCHICKEN UND KORRIGIEREN", "", [f"{D}.pdf", f"{D}_Leseprobe.pdf", f"{D}_Leseprobe.epub",
                 f"{D}_Korrektur.pdf", f"{D}_Geschichten.pdf", f"{D}_Aenderungen.pdf"], None),
                ("GEGENLESEN", "", sorted(n for n in vorhanden if n.startswith("check_")), "sh build.sh personen Name"),
                ("WERBUNG", "Webseite, Newsletter", [f"{D}_Mockup.jpg", f"{D}_Vorderseite.jpg"], "sh build.sh mockup"),
                ("SELBER DRUCKEN", "A4 quer, kurze Kante wenden", [f"{K}_Probedruck_booklet.pdf", f"{D}_booklet.pdf"], None),
                ("TEXTE FÜR DEN SHOP", "", ["shop-angaben.txt"], "sh build.sh final"),
            ]
            if test:
                gruppen = gruppen[:1]
            if not bk.ebook_erstellen(a):
                gruppen = [(("E-BOOK", "keines («{erstellen}: nein»)", [], None) if ti == "E-BOOK" else (ti, er, n, b))
                           for ti, er, n, b in gruppen]
            for titel, erklaerung, namen, befehl in gruppen:
                if titel == "GEGENLESEN" and not namen:
                    continue                                # erscheint erst, wenn es Check-PDFs gibt
                da = [n for n in namen if n in vorhanden]
                gebraucht.update(da)
                z.append(f"# {titel}")
                if erklaerung:
                    z.append(f"> {erklaerung}")
                z += [zeile(n) for n in da]
                if not da and namen:
                    z += ["> noch keine"] + ([f"$ {befehl}"] if befehl else [])
                elif titel.startswith("ZUM LESEN"):
                    for was, b, n in (("Leseprobe", "leseprobe", f"{D}_Leseprobe.pdf"),
                                      ("Korrektur-PDF", "korrektur", f"{D}_Korrektur.pdf")):
                        if n not in vorhanden:
                            z.append(f"$ sh build.sh {b:<34}  (fehlt: {was})")
                z.append("")
        rest = [n for n in vorhanden if n not in gebraucht]
        if rest:
            z += ["# WEITERE DATEIEN", "> zur Auswahl, z. B. Vorder-/Rückseite einzeln, Kopie der Druckdatei"]
            z += [zeile(n) for n in rest] + [""]
        z.append("> Mehr: hilfe.html → «Was im Ausgabeordner liegt»")
        with open(os.path.join(o, "00-UEBERSICHT.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(z) + "\n")
        print(f"Übersicht: {os.path.relpath(os.path.join(o, '00-UEBERSICHT.txt'), BASE)}")


# --- Zusatzdateien für Shops ------------------------------------------------
COVER_GROESSEN = (2000, 1600, 900)          # lange Seite in Pixel: …_Cover-vorne_2000px.jpg usw.


def ebook_weg(a):
    """E-Book-Dateien eines früheren Baus entfernen, wenn diese Fassung kein E-Book hat."""
    g = bk.AUSGABEN["B" if a == "uz" else "A"]
    stamm = os.path.join(BASE, g["ordner"], g["datei"])
    for n in [".epub", "_EPUB2.epub", "_Inhalt.pdf", "_Cover-vorne.jpg", "_Cover-hinten.jpg"] + \
             [f"_Cover-vorne_{px}px.jpg" for px in COVER_GROESSEN]:
        if os.path.exists(stamm + n):
            os.remove(stamm + n)


def ghostscript():
    """Ghostscript suchen: gs (Linux, Mac) bzw. gswin64c (Windows, auch wenn nicht im PATH)."""
    gs = shutil.which("gs") or shutil.which("gswin64c") or shutil.which("gswin32c")
    if not gs and sys.platform == "win32":
        import glob
        for basis in (os.environ.get("ProgramFiles", r"C:\Program Files"), os.environ.get("ProgramFiles(x86)", "")):
            treffer = sorted(glob.glob(os.path.join(basis, "gs", "gs*", "bin", "gswin*c.exe"))) if basis else []
            if treffer:
                return treffer[-1]
    return gs


def farbmodus_druck(test=None):
    """{farbmodus}: cmyk in der Druckdatei: Buchblock und Umschlag (PDF) mit Ghostscript nach CMYK umwandeln.
    Nur bei final/komplett. Lese-PDF, E-Book, Leseprobe und JPGs bleiben RGB. Jeder Bau setzt die Druck-PDFs neu
    aus den Originalbildern – umgewandelt wird also immer nur einmal, nichts wird mehrfach umgerechnet."""
    for a in ausgaben():
        if bk.druck_V("farbmodus", "rgb", a).strip().lower() != "cmyk":
            continue
        gs = ghostscript()
        if not gs:
            befehl = {"darwin": "brew install ghostscript   (ohne Homebrew: sudo port install ghostscript)",
                      "win32": "winget install ArtifexSoftware.GhostScript"}.get(sys.platform, "sudo apt install ghostscript")
            print("> Hinweis: {farbmodus}: cmyk braucht Ghostscript – nicht gefunden, Druckdateien bleiben RGB.\n"
                  f"$ {befehl}")
            return
        g = bk.AUSGABEN["B" if a == "uz" else "A"]
        o = os.path.join(BASE, "ausgabe-test", test) if test else os.path.join(BASE, g["ordner"])
        K = g["kuerzel"]
        for n in (f"{K}_Buchblock.pdf", f"{K}_Umschlag_Hardcover.pdf", f"{K}_Umschlag_Softcover.pdf"):
            p = os.path.join(o, n)
            if not os.path.exists(p):
                continue
            tmp = os.path.join(o, "_tmp_cmyk.pdf")
            r = subprocess.run([gs, "-q", "-dNOPAUSE", "-dBATCH", "-dSAFER", "-sDEVICE=pdfwrite",
                                "-dPDFSETTINGS=/prepress", "-dAutoRotatePages=/None",
                                "-sColorConversionStrategy=CMYK", "-dProcessColorModel=/DeviceCMYK",
                                "-dDownsampleColorImages=false", "-dDownsampleGrayImages=false",
                                "-dDownsampleMonoImages=false", f"-sOutputFile={tmp}", p],
                               capture_output=True, text=True)
            if r.returncode == 0 and os.path.exists(tmp):
                os.replace(tmp, p)
                print(f"CMYK · {name(a)}: {os.path.relpath(p, BASE)}")
            else:
                if os.path.exists(tmp):
                    os.remove(tmp)
                print(f"> Hinweis: CMYK-Umwandlung ging nicht ({n}), Datei bleibt RGB: {(r.stderr or '').strip()[:200]}")


def zusatz_dateien(art):
    """<datei>_Inhalt.pdf (Inhaltsverzeichnis-Seiten aus dem Lese-PDF, z. B. für XinXii) und das Titelbild
    …_Cover-vorne.jpg in kleineren Grössen. Nie den Bau verhindern."""
    for a in ausgaben():
        g = bk.AUSGABEN["B" if a == "uz" else "A"]
        stamm = os.path.join(BASE, g["ordner"], g["datei"])
        try:
            if not bk.ebook_erstellen(a):
                continue
            if art in ("alles", "nur-pdf") and os.path.exists(stamm + ".pdf"):
                n = inhalt_pdf(stamm + ".pdf", stamm + "_Inhalt.pdf")
                if n:
                    print(f"Inhaltsverzeichnis · {name(a)}: {os.path.relpath(stamm + '_Inhalt.pdf', BASE)} ({n} Seite(n))")
            if art in ("alles", "nur-ebook") and os.path.exists(stamm + "_Cover-vorne.jpg"):
                from PIL import Image
                with Image.open(stamm + "_Cover-vorne.jpg") as im:
                    bild = im.convert("RGB")
                for px in COVER_GROESSEN:
                    k = bild.copy(); k.thumbnail((px, px), Image.LANCZOS)
                    k.save(f"{stamm}_Cover-vorne_{px}px.jpg", "JPEG", quality=90, dpi=(300, 300))
                print(f"Titelbild · {name(a)}: …_Cover-vorne_" + "px, _".join(map(str, COVER_GROESSEN)) + "px.jpg")
        except Exception as e:
            print(f"Hinweis: Zusatzdateien {name(a)} nicht erstellt ({e})")


def inhalt_pdf(quelle, ziel):
    """Seiten des Inhaltsverzeichnisses (mit Punktlinien, vor dem ersten Kapitel) als eigenes PDF. 0 = keines gefunden."""
    import re
    import fassungen
    from pypdf import PdfReader, PdfWriter
    r = PdfReader(quelle)
    bis = fassungen.erste_inhaltsseite(r) - 1               # Seite vor dem ersten Kapitel (Seiten ab 1)
    punkte = re.compile(r"(\.\s+){5,}")
    seiten = [i for i in range(min(bis, len(r.pages))) if punkte.search(r.pages[i].extract_text() or "")]
    if not seiten:
        return 0
    w = PdfWriter()
    for i in range(seiten[0], seiten[-1] + 1):
        w.add_page(r.pages[i])
        if "/Annots" in w.pages[-1]:
            del w.pages[-1]["/Annots"]                       # Links ins Buch gibt es hier nicht
    w.add_metadata({"/Title": f"{bk.V('titel')} – Inhaltsverzeichnis", "/Author": bk.V("autor")})
    with open(ziel, "wb") as f:
        w.write(f)
    return seiten[-1] - seiten[0] + 1


def nicht_eingebettet(pdf):
    """{Schrift: [Seiten]} aller nicht eingebetteten Schriften eines PDFs (wie die Prüfung der Druckereien)."""
    from pypdf import PdfReader
    funde = {}
    for nr, seite in enumerate(PdfReader(pdf).pages, 1):
        res = seite.get("/Resources")
        fonts = res.get_object().get("/Font") if res else None
        for f in (fonts.get_object().values() if fonts else []):
            f = f.get_object()
            ds = [f] + [d.get_object() for d in f.get("/DescendantFonts", [])]
            eingebettet = any(any(k in (d.get("/FontDescriptor") or {}) for k in ("/FontFile", "/FontFile2", "/FontFile3"))
                              for d in ds)
            if not eingebettet and f.get("/Subtype") != "/Type3":
                funde.setdefault(str(f.get("/BaseFont", "?")).lstrip("/"), []).append(nr)
    return funde


def schriften_pruefen(test=None):
    """Warnung, wenn ein Druck- oder Lese-PDF nicht eingebettete Schriften enthält."""
    try:
        ordner = [os.path.join(BASE, "ausgabe-test", test)] if test else \
            sorted({os.path.join(BASE, bk.AUSGABEN["B" if a == "uz" else "A"]["ordner"]) for a in ausgaben()})
        for o in ordner:
            for f in sorted(os.listdir(o)) if os.path.isdir(o) else []:
                if f.endswith(".pdf") and not f.startswith("_tmp") and "_Korrektur" not in f:
                    for name_, seiten in nicht_eingebettet(os.path.join(o, f)).items():
                        print(f"WARNUNG: {os.path.relpath(os.path.join(o, f), BASE)}: Schrift «{name_}» nicht eingebettet "
                              f"(Seiten {seiten[0]}–{seiten[-1]}) – Druckereien melden das.")
    except Exception as e:
        print(f"Hinweis: Schriften nicht geprüft ({e})")


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
            import re
            if kap and re.fullmatch(SEITEN_MUSTER, kap) and re.search(r"[,\-–]", kap):
                seiten, kap = seiten or kap, ""     # «leseprobe: 17,18-22» = Seiten (eine Zahl allein = Kapitel)
            if LESEPROBE_SEITEN:
                seiten = LESEPROBE_SEITEN
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
            n = fassungen.korrektur(tmp, ziel, f"{bk.V('titel', fassung=a)} · {name(a)}", schrift=bk.schrift("titel_normal"))
            print(f"Korrektur · {name(a)}: {os.path.relpath(ziel, BASE)} ({n} Seiten auf A4)")
        os.remove(tmp)


def farbschema_zeigen():
    """Gewähltes Farbschema anzeigen (am Anfang und am Ende des Baus), nur wenn das Buch Farbschemas hat."""
    for name in M.FARBSCHEMA_NAME.values():
        print(f"Farben: {name}")


def pdf_liste(seit):
    """Am Schluss: alle PDFs und E-Books, die dieser Bau erstellt hat, mit dem Öffnen-Befehl des Systems."""
    neu = []
    for d in sorted(os.listdir(BASE)):
        o = os.path.join(BASE, d)
        if not (d.startswith("ausgabe") and os.path.isdir(o)):
            continue
        for wurzel, _, dateien in os.walk(o):
            for f in sorted(dateien):
                p = os.path.join(wurzel, f)
                if f.lower().endswith((".pdf", ".epub")) and not f.startswith("_tmp") and os.path.getmtime(p) >= seit - 1:
                    neu.append(os.path.relpath(p, BASE).replace(os.sep, "/"))
    if neu:
        print("\n> Neue PDFs und E-Books:")
        for p in neu:
            print("  " + (f'"{p}"' if " " in p else p))
        oeffnen = {"darwin": "open", "win32": 'start ""'}.get(sys.platform, "xdg-open")
        print(f"$ {oeffnen} <Datei>   (öffnen mit dem Standardprogramm)")


def main():
    import geschichten
    geschichten.hilfsdateien(BASE)          # neu.sh / neu.bat, .gitignore
    global NUR_FASSUNG
    for nr in M.FARBSCHEMA_FEHLT.values():   # «{farbschema}: 5» ohne Abschnitt «### Farbschema 5»
        print(f"Hinweis: Farbschema {nr} fehlt – nehme Schema 1.")
    farbschema_zeigen()
    druck = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.lower().startswith("druck=")), None)
    args = [a.lower() for a in sys.argv[1:] if not a.lower().startswith("druck=")]
    if druck:                               # andere Druckdatei zum Testen (gilt für alle Teilschritte)
        os.environ["BUCH_DRUCK_DATEI"] = druck
        NUR_FASSUNG = next((a for a in args if a in ("normal", "uz")), None)
    final = "final" in args
    art = next((a for a in args if a not in ("final", "uz", "normal")), "alles")
    komplett = art == "komplett"            # final + Leseprobe + Korrektur
    if komplett:
        art, final = "alles", True
    if druck and art in ("alles", "nur-druck"):
        art = "nur-druck"                   # Testlauf: nur Druckdateien, nach ausgabe-test/<datei>/
    if art == "sicherung":
        sicherung(); return
    if art == "pruefen":
        pruefen(); return
    if art == "personen":                   # Personen und Seiten, Check-PDFs zum Gegenlesen (personen.py)
        import personen
        roh = sys.argv[1:]
        i = next(k for k, x in enumerate(roh) if x.lower() == art)
        personen.befehl(BASE, bk, roh[i + 1:])
        return
    if art in ("stand", "aenderungen", "änderungen"):    # Stände festhalten und vergleichen (staende.py)
        import staende
        roh = sys.argv[1:]
        i = next(k for k, x in enumerate(roh) if x.lower() == art)
        staende.befehl(BASE, bk, ["aenderungen" if art == "änderungen" else art] + roh[i + 1:])
        return
    if art == "mockup":
        mockups(); ausgabe_uebersicht(art, final); return
    if art == "hilfe":
        hilfe(oeffnen=True); return
    if art == "geschichten":
        start = time.time()
        sicherung()
        sammlung("uz" in args)
        ausgabe_uebersicht(art, False)
        print(f"\nFertig in {time.time() - start:.0f} Sekunden.")
        return
    if art == "schnell":                  # nur Lese-PDFs, ein Durchgang, ohne Booklet/Statistik/Prüfung
        start = time.time()
        sicherung()
        env = dict(os.environ, BUCH_FINAL="1" if final else "0", BUCH_BOOKLET="", BUCH_SCHNELL="1")
        parallel([(f"Schnell · {name(a)}", "build.py", a) for a in ausgaben()], env)
        ausgabe_uebersicht(art, final)
        print(f"\nFertig in {time.time() - start:.0f} Sekunden (schnell: ohne Seitenausgleich – für den Druck: final).")
        return
    if art in ("leseprobe", "korrektur"):
        import re
        if art == "leseprobe":              # «sh build.sh leseprobe uz 18,20,23»
            global LESEPROBE_SEITEN
            LESEPROBE_SEITEN = next((a for a in sys.argv[1:] if re.fullmatch(SEITEN_MUSTER, a.strip())), None)
            NUR_FASSUNG = next((a for a in args if a in ("normal", "uz")), None)
            if LESEPROBE_SEITEN:
                print(f"Leseprobe mit den Seiten {LESEPROBE_SEITEN}" + (f" · nur {NUR_FASSUNG}" if NUR_FASSUNG else ""))
        start = time.time()
        sicherung(); pruefen()
        fassung(art, final or art == "leseprobe")       # Leseprobe immer ohne offene Stellen und Notizen
        ausgabe_uebersicht(art, final or art == "leseprobe")
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
          f"· Format {bk.FMT['name']} · Bindung {bk.druck_V('bindung', 'hardcover', 'normal')}")
    for a in ausgaben():
        if bk.druck_datei(a) and art in ("alles", "nur-druck"):
            print(f"Druckangaben {name(a)}: {bk.druck_datei(a)}")
    schritte = []
    for a in ausgaben():
        if art in ("alles", "nur-pdf"):
            schritte.append((f"Bildschirm-PDF · {name(a)}", "build.py", a))
        if art in ("alles", "nur-druck"):
            schritte.append((f"Druckdateien · {name(a)}", "build-broschuere.py", a))
        if art in ("alles", "nur-ebook") and bk.ebook_erstellen(a):
            schritte.append((f"E-Book · {name(a)}", "build-epub.py", a))
        elif art in ("alles", "nur-ebook"):
            print(f"E-Book {name(a)}: keines («{{erstellen}}: nein»)")
            ebook_weg(a)
    parallel(schritte, env)
    bk.ENTWURF = not final
    if art in ("alles", "nur-druck"):       # {farbmodus}: cmyk in der Druckdatei (Plattform), nur bei final
        if final:
            farbmodus_druck(os.path.splitext(os.path.basename(bk.druck_datei()))[0] if druck else None)
        elif any(bk.druck_V("farbmodus", "rgb", a).strip().lower() == "cmyk" for a in ausgaben()):
            print("> Hinweis: Entwurf – Druckdateien bleiben RGB. CMYK (Ghostscript) nur mit final oder komplett.")
    zusatz_dateien(art)
    statistik()
    if final and art in ("alles", "nur-pdf"):
        mockups()
    if art == "alles" and final:
        print()
        shop_angaben()
        kontrast_pruefen()
    if komplett:
        print("\n=== Leseprobe und Korrektur ===")
        fassung("leseprobe", True)
        fassung("korrektur", True)
    bk.zeige_offene_stellen()
    if art in ("alles", "nur-pdf", "nur-druck"):
        schriften_pruefen(os.path.splitext(os.path.basename(bk.druck_datei()))[0] if druck else None)
    ausgabe_uebersicht("komplett" if komplett else art, final, os.path.splitext(os.path.basename(bk.druck_datei()))[0] if druck else None)
    ordner = ", ".join(bk.AUSGABEN["B" if a == "uz" else "A"]["ordner"] + "/" for a in ausgaben())
    if druck:
        ordner = "ausgabe-test/" + os.path.splitext(os.path.basename(bk.druck_datei()))[0] + "/"
    print(f"\nFertig in {time.time() - start:.0f} Sekunden. Ordner: {ordner}")


if __name__ == "__main__":
    _start = time.time()
    main()
    pdf_liste(_start)
    farbschema_zeigen()
