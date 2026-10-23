#!/usr/bin/env python3
"""
aufraeumen.py – entfernt im Buchordner, was nicht mehr gebraucht wird (wird von cleanup.sh aufgerufen).

    sh cleanup.sh            zeigt die Liste und fragt, bevor etwas gelöscht wird
    sh cleanup.sh ausgaben   zusätzlich die Ausgabeordner (lassen sich mit sh build.sh final neu erstellen)

Gelöscht werden nur bekannte, entbehrliche Dinge:
  Zwischenspeicher (_bildcache, _druckbilder, __pycache__, _epub_tmp, _tmp.pdf),
  Sicherungen (_backup/, *.backup), alte Motoren (motor-alt-*), stichworte-vorschlag.txt;
  mit «ausgaben»: auch alte Ausgabeordner «ausgabe-…», die zu keiner Fassung mehr gehören (2.26).
NIE gelöscht: md-history/, die MD-Dateien, stichworte-*.txt, fotos/, bilder/, motor/, .venv/,
und alles, was das Skript nicht kennt.
"""
import os
import shutil
import sys
try:                                            # Windows: «sh build.sh» in Meldungen als «.\build.bat»
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "."))
    import plattform
    plattform.windows_befehle()
except ImportError:
    pass

MOTOR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(MOTOR)
sys.path.insert(0, MOTOR)
SCHUETZEN = {"md-history", "fotos", "bilder", "motor", ".venv", "fonts"}


def groesse(p):
    if os.path.isfile(p):
        return os.path.getsize(p)
    return sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(p) for f in fs
               if os.path.isfile(os.path.join(r, f)))


def lesbar(n):
    for e in ("Bytes", "KB", "MB", "GB"):
        if n < 1024 or e == "GB":
            return f"{n:.0f} {e}" if e == "Bytes" else f"{n:.1f} {e}"
        n /= 1024


def ausgabeordner():
    try:
        import build as bk
        ordner = {bk.AUSGABEN["A"]["ordner"]}
        if bk.zweite_ausgabe():
            ordner.add(bk.AUSGABEN["B"]["ordner"])
        return ordner
    except SystemExit:
        return set()


def kandidaten(mit_ausgaben):
    liste = []
    for name in ("_bildcache", "_druckbilder", "__pycache__", "_backup", "stichworte-vorschlag.txt"):
        if os.path.exists(os.path.join(BASE, name)):
            liste.append(name)
    for name in sorted(os.listdir(BASE)):
        if name.startswith("motor-alt-") and os.path.isdir(os.path.join(BASE, name)):
            liste.append(name)
    if os.path.isdir(os.path.join(MOTOR, "__pycache__")):
        liste.append("motor/__pycache__")
    for ordner in ("", "druck", "motor"):                      # Sicherungskopien *.backup (2.26)
        pfad = os.path.join(BASE, ordner)
        if os.path.isdir(pfad):
            for name in sorted(os.listdir(pfad)):
                if name.endswith(".backup") and os.path.isfile(os.path.join(pfad, name)):
                    liste.append(f"{ordner}/{name}" if ordner else name)
    ausgaben = ausgabeordner()
    for o in sorted(ausgaben):
        for rest in ("_epub_tmp", "_tmp.pdf", "_tmp_leseprobe.pdf", "_tmp_korrektur.pdf"):
            if os.path.exists(os.path.join(BASE, o, rest)):
                liste.append(f"{o}/{rest}")
    if mit_ausgaben:
        liste += [o for o in sorted(ausgaben | {"ausgabe-test"}) if os.path.isdir(os.path.join(BASE, o))]
        if ausgaben:                                            # alte Ausgabeordner ohne Fassung (2.26)
            liste += [n for n in sorted(os.listdir(BASE)) if n.startswith("ausgabe-") and n not in ausgaben
                      and n != "ausgabe-test" and os.path.isdir(os.path.join(BASE, n))]
    # Sicherheit: nie etwas Geschütztes, nie ausserhalb des Buchordners
    return [p for p in liste if p.split("/")[0] not in SCHUETZEN or p == "motor/__pycache__"
            or (p.startswith("motor/") and p.endswith(".backup"))]


def main():
    mit_ausgaben = "ausgaben" in [a.lower() for a in sys.argv[1:]]
    liste = kandidaten(mit_ausgaben)
    if not liste:
        print("Nichts aufzuräumen – alles sauber.")
        return
    print(f"Aufräumen in {BASE}\n")
    total = 0
    for p in liste:
        g = groesse(os.path.join(BASE, p)); total += g
        print(f"  {lesbar(g):>10}  {p}{'/' if os.path.isdir(os.path.join(BASE, p)) else ''}")
    print(f"  {lesbar(total):>10}  gesamt\n")
    print("Bleibt immer: md-history/, MD-Dateien, stichworte-*.txt, fotos/, bilder/, motor/, .venv/"
          + ("" if mit_ausgaben else ", Ausgabeordner"))
    try:
        antwort = input("\nDiese Dateien und Ordner löschen? ja/nein [nein]: ").strip().lower()
    except EOFError:
        antwort = ""
    if antwort not in ("ja", "j", "yes", "y"):
        print("Nichts gelöscht."); return
    for p in liste:
        ziel = os.path.join(BASE, p)
        if os.path.isdir(ziel):
            shutil.rmtree(ziel)
        elif os.path.exists(ziel):
            os.remove(ziel)
    print(f"Gelöscht: {len(liste)} Einträge, {lesbar(total)} frei.")


if __name__ == "__main__":
    main()
