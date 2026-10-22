#!/usr/bin/env python3
"""
setup.py – ein neues Buch anlegen oder ein bestehendes auf den neuesten Motor bringen.

Im Ordner pureSATZ (Windows: setup\\setup.bat statt sh setup/setup.sh):
    sh setup/setup.sh                  fragt alles nacheinander ab
    sh setup/setup.sh start.txt        nimmt die Werte aus setup/start.txt und fragt nur, was fehlt
    sh setup/setup.sh motor ../Buch    bringt nur den neuesten Motor ins Buch (alter bleibt als motor-alt-…)
    sh setup/setup.sh ../Buch          ergänzt in einem bestehenden Buchordner, was fehlt

Das neue Buch liegt danach neben «pureSATZ» (z. B. ../Mein-Buch/) mit:
  Mein-Buch-variablen.md  Angaben, Technik, Layout
  Mein-Buch-buch.md       Titelei und ein Demo-Kapitel mit allen Möglichkeiten
  Mein-Buch-umschlag.md   Vorderseite, Buchrücken, Rückseite
  stichworte-Mein-Buch.txt, fotos/, bilder/, build.sh, README.md, motor/, .venv/
Bestehende Dateien werden NIE überschrieben.
"""
import os
import re
import shutil
import subprocess
import sys
from datetime import date
try:                                            # Windows: «sh build.sh» in Meldungen als «.\build.bat»
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "motor"))
    import plattform
    plattform.windows_befehle()
except ImportError:
    pass

HIER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))     # Ordner pureSATZ (setup.py liegt in setup/)
VORLAGE = os.path.join(HIER, "vorlage")
MOTOR = os.path.join(HIER, "motor")
FORMATE = ("a5", "taschenbuch", "sachbuch", "a4", "quadrat")

FRAGEN = [
    ("TITEL", "Titel des Buchs", None),
    ("UNTERTITEL", "Untertitel", ""),
    ("AUTOR", "Autorin / Autor", None),
    ("NAME", "Technischer Buchname (Ordner und Dateinamen, ohne Leerzeichen)", None),
    ("FORMAT", "Format: a5 · taschenbuch · sachbuch · a4 · quadrat", "a5"),
    ("BINDUNG", "Bindung: hardcover · softcover", "hardcover"),
    ("ZWEITE_AUSGABE", "Zweite Ausgabe anlegen (z. B. Director's Cut, Unzensiert)? ja/nein", "nein"),
    ("ZWEITE_NAME", "Name der zweiten Ausgabe", "Director's Cut"),
    ("ORT", "Ort", "Bern"),
    ("JAHR", "Erscheinungsjahr", str(date.today().year)),
    ("WEBSITE", "Website", "www.beispiel.ch"),
    ("ADRESSE", "Verlagsadresse fürs Impressum (Strasse, PLZ Ort, E-Mail)", "Strasse 1, 3000 Bern, mail@beispiel.ch"),
]


def slug(t):
    """«Leben 1.0, 2.0» -> «Leben-1.0-2.0» (für Ordner und Dateinamen)."""
    for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("Ä", "Ae"), ("Ö", "Oe"), ("Ü", "Ue"), ("ß", "ss"),
                 ("'", ""), ("’", "")):
        t = t.replace(a, b)
    t = re.sub(r"[^A-Za-z0-9.]+", "-", t).strip("-.")
    return t or "Buch"


def lese_werte(pfad):
    """start.txt lesen: SCHLÜSSEL = Wert, # = Kommentar."""
    w = {}
    if pfad and os.path.exists(pfad):
        for z in open(pfad, encoding="utf-8"):
            z = z.split("#", 1)[0].strip()
            if "=" in z:
                k, v = z.split("=", 1)
                w[k.strip().upper()] = v.strip()
    return w


def frage(text, vorgabe):
    try:
        a = input(f"{text}" + (f" [{vorgabe}]" if vorgabe else "") + ": ").strip()
    except EOFError:
        a = ""
    return a or (vorgabe or "")


def ja(w):
    return str(w).strip().lower() in ("ja", "j", "yes", "y", "true", "1")


# --------------------------------------------------------------------------- Motor
def version(ordner):
    p = os.path.join(ordner, "VERSION")
    return open(p).read().strip() if os.path.exists(p) else "0"


def vtuple(v):
    try:
        return tuple(int(x) for x in v.split("."))
    except ValueError:
        return (0,)


def motor(ordner, venv=True):
    """Motor ins Buch kopieren bzw. aktualisieren und die Python-Umgebung einrichten."""
    ziel = os.path.join(ordner, "motor")
    neu = version(MOTOR)
    if os.path.isdir(ziel):
        alt = version(ziel)
        if vtuple(neu) > vtuple(alt):
            sicherung = os.path.join(ordner, f"motor-alt-{alt}")
            shutil.move(ziel, sicherung)
            shutil.copytree(MOTOR, ziel, ignore=shutil.ignore_patterns("__pycache__"))
            print(f"  Motor aktualisiert: {alt} -> {neu} (alter Motor in {os.path.basename(sicherung)}/)")
        else:
            print(f"  Motor {alt} ist aktuell (Vorlage: {neu}).")
    else:
        shutil.copytree(MOTOR, ziel, ignore=shutil.ignore_patterns("__pycache__"))
        print(f"  Motor {neu} kopiert.")
    for f in ("update.sh", "update.bat"):                 # neue Hilfsdateien in älteren Büchern ergänzen
        if not os.path.exists(os.path.join(ordner, f)):
            shutil.copy2(os.path.join(VORLAGE, f), os.path.join(ordner, f))
            print(f"  neu im Buch: {f}")
    if venv:
        subprocess.run([sys.executable, os.path.join(ziel, "einrichten.py")], cwd=ordner, check=True)


# --------------------------------------------------------------------------- Buch
def schreibe(pfad, inhalt, meldung):
    if os.path.exists(pfad) and os.path.getsize(pfad) > 0:
        print(f"  bleibt:   {meldung} (existiert schon)")
        return False
    with open(pfad, "w", encoding="utf-8") as f:
        f.write(inhalt)
    print(f"  neu:      {meldung}")
    return True


def kopiere(quelle, ziel, meldung):
    if os.path.exists(ziel):
        print(f"  bleibt:   {meldung} (existiert schon)")
        return
    shutil.copy2(quelle, ziel)
    print(f"  neu:      {meldung}")


def platzhalter(w):
    zweitname = w.get("ZWEITE_NAME") or "Director's Cut"
    kuerzel = re.sub(r"[^A-Z0-9]", "", slug(w["NAME"]).upper())[:8] or "BUCH"
    zweitkurz = "".join(x[0] for x in re.findall(r"[A-Za-z]+", zweitname.replace("'", ""))).upper()[:3] or "Z"
    fmt = w.get("FORMAT", "a5").lower()
    if fmt not in FORMATE:
        raise SystemExit(f"Unbekanntes Format «{fmt}». Möglich: " + ", ".join(FORMATE))
    bindung = w.get("BINDUNG", "hardcover").lower()
    if bindung not in ("hardcover", "softcover", "beide"):
        raise SystemExit(f"Unbekannte Bindung «{bindung}». Möglich: hardcover, softcover")
    return dict(TITEL=w["TITEL"], UNTERTITEL=w.get("UNTERTITEL", ""), AUTOR=w["AUTOR"], NAME=w["NAME"],
                ORT=w.get("ORT", ""), JAHR=w.get("JAHR", str(date.today().year)), WEBSITE=w.get("WEBSITE", ""),
                ADRESSE=w.get("ADRESSE", ""), FORMAT=fmt, BINDUNG=bindung,
                RUECKEN="3" if bindung == "softcover" else "6",
                ZWEITE="ja" if ja(w.get("ZWEITE_AUSGABE", "nein")) else "nein",
                ZWEITNAME=zweitname, ZWEITLABEL=zweitname.upper(), ZWEITDATEI=slug(zweitname),
                ZWEITORDNER=slug(zweitname).lower(), ZWEITKURZ=zweitkurz, KUERZEL=kuerzel)


def fuelle(text, d):
    for k, v in d.items():
        text = text.replace("@@" + k + "@@", v)
    return text


def buch(ordner, w):
    d = platzhalter(w)
    os.makedirs(ordner, exist_ok=True)
    print(f"\nBuch in {os.path.abspath(ordner)}")
    for o in ("fotos", "bilder", "fonts", "md-history", "geschichten", "tabellen", "druck"):
        os.makedirs(os.path.join(ordner, o), exist_ok=True)
    vorhanden = [f for f in os.listdir(ordner) if f.endswith("-buch.md")]
    name = vorhanden[0][:-8] if len(vorhanden) == 1 else d["NAME"]
    for teil, text in (("variablen", "Angaben, Technik, Layout"),
                       ("buch", "Titelei und Demo-Kapitel"), ("umschlag", "Vorderseite, Buchrücken, Rückseite")):
        schreibe(os.path.join(ordner, f"{name}-{teil}.md"),
                 fuelle(open(os.path.join(VORLAGE, teil + ".md"), encoding="utf-8").read(), d), f"{name}-{teil}.md ({text})")
    kopiere(os.path.join(VORLAGE, "stichworte-buch.txt"), os.path.join(ordner, f"stichworte-{name}.txt"),
            f"stichworte-{name}.txt (Stichwortverzeichnis)")
    for f in ("build.sh", "cleanup.sh", "sicherung.sh", "sync.sh", "update.sh", "neu.sh",
              "build.bat", "cleanup.bat", "sicherung.bat", "sync.bat", "update.bat", "neu.bat", "README.md", "CHECKLISTE.md"):
        kopiere(os.path.join(VORLAGE, f), os.path.join(ordner, f), f)
    for f in ("LIESMICH.txt", "muster.csv"):
        kopiere(os.path.join(VORLAGE, "tabellen", f), os.path.join(ordner, "tabellen", f), f"tabellen/{f}")
    for f in sorted(os.listdir(os.path.join(VORLAGE, "druck"))):       # Druckangaben-Muster (pureSATZ 2.19)
        kopiere(os.path.join(VORLAGE, "druck", f), os.path.join(ordner, "druck", f), f"druck/{f}")
    kopiere(os.path.join(VORLAGE, "geschichten", "LIESMICH.txt"), os.path.join(ordner, "geschichten", "LIESMICH.txt"),
            "geschichten/LIESMICH.txt (einzelne Geschichten sammeln)")
    kopiere(os.path.join(VORLAGE, "buch.gitignore"), os.path.join(ordner, ".gitignore"),
            ".gitignore (was nicht zu GitHub kommt)")
    schreibe(os.path.join(ordner, "readme4ki.txt"),
             fuelle(open(os.path.join(VORLAGE, "readme4ki.txt"), encoding="utf-8").read(), dict(d, NAME=name)),
             "readme4ki.txt (Anleitung für eine andere KI)")
    for o in ("fotos", "bilder"):
        for f in os.listdir(os.path.join(VORLAGE, "beispiel", o)):
            kopiere(os.path.join(VORLAGE, "beispiel", o, f), os.path.join(ordner, o, f), f"{o}/{f}")
    return name


def buchpfad(p):
    """Buchordner: zuerst ab dem aktuellen Ordner, sonst ab pureSATZ (z. B. ../MeinBuch)."""
    if os.path.isabs(p) or os.path.isdir(p):
        return p
    return os.path.normpath(os.path.join(HIER, p))


def main():
    a = sys.argv[1:]
    venv = "--ohne-venv" not in a
    a = [x for x in a if not x.startswith("--")]
    if a[:1] == ["motor"]:
        if len(a) < 2:
            print(__doc__); sys.exit(1)
        ziel = buchpfad(a[1])
        if not os.path.isdir(ziel):
            sys.exit(f"Buchordner nicht gefunden: {os.path.abspath(ziel)}")
        print(f"Motor für {os.path.abspath(ziel)}")
        motor(ziel, venv); return
    if a and not a[0].endswith(".txt") and os.path.isdir(buchpfad(a[0])):   # bestehender Buchordner
        ordner = buchpfad(a[0])
        w = lese_werte(a[1] if len(a) > 1 else None)
        w.setdefault("TITEL", os.path.basename(os.path.abspath(ordner)).replace("-", " "))
        w.setdefault("AUTOR", "Vorname Nachname")
        w.setdefault("NAME", os.path.basename(os.path.abspath(ordner)))
        buch(ordner, w); motor(ordner, venv); return

    datei = a[0] if a else None
    if datei and not os.path.exists(datei):          # start.txt: aktueller Ordner, sonst setup/, sonst pureSATZ
        for o in (os.path.join(HIER, "setup"), HIER):
            if os.path.exists(os.path.join(o, datei)):
                datei = os.path.join(o, datei)
                break
    w = lese_werte(datei)
    print("=== Neues Buch ===" + (f"  (Werte aus {datei})" if datei else ""))
    for k, text, vorgabe in FRAGEN:
        if k == "ZWEITE_NAME" and not ja(w.get("ZWEITE_AUSGABE", "nein")):
            continue
        if k == "NAME":
            vorgabe = slug(w.get("TITEL", ""))
        if k in w and w[k]:
            continue
        w[k] = frage(text, vorgabe)
        if not w[k] and vorgabe is None:
            raise SystemExit(f"{text} fehlt.")
    w["NAME"] = slug(w["NAME"])
    ordner = os.path.normpath(os.path.join(HIER, "..", w["NAME"]))

    print("\nZusammenfassung:")
    for k, _, _ in FRAGEN:
        if k in w:
            print(f"  {k:15} {w[k]}")
    print(f"  {'Buchordner':15} {ordner}")
    if sys.stdin.isatty() and not ja(frage("\nSo anlegen? ja/nein", "ja")):
        print("Abgebrochen."); return
    name = buch(ordner, w)
    motor(ordner, venv)
    print(f"""
Fertig. Das Buch liegt in: {ordner}
  {name + '-variablen.md':30} Angaben, Technik, Layout
  {name + '-buch.md':30} das Buch (mit Demo-Kapitel)
  {name + '-umschlag.md':30} Vorderseite, Buchrücken, Rückseite
  {'stichworte-' + name + '.txt':30} Stichwortverzeichnis
Weiter:
  cd "{ordner}"
  sh build.sh            alles als Entwurf (Demo ansehen: Ordner ausgabe-normal/)
  sh build.sh final      Druckfassung""")


if __name__ == "__main__":
    main()
