#!/usr/bin/env python3
"""
hallo.py – der erste Blick auf pureSATZ: legt neben pureSATZ das Beispielbuch «Hallo-Buch» an,
baut es und öffnet das PDF. Aufruf im Ordner pureSATZ:

    sh hallo.sh                 (Windows: hallo.bat doppelklicken)

Gibt es Hallo-Buch schon, wird es nur neu gebaut (eigene Änderungen bleiben).
Zum Wegwerfen einfach den Ordner Hallo-Buch löschen. Werte: setup/hallo.txt.
"""
import glob
import os
import subprocess
import sys
try:                                            # Windows: «sh build.sh» in Meldungen als «.\build.bat»
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "motor"))
    import plattform
    plattform.windows_befehle()
except ImportError:
    pass

SETUP = os.path.dirname(os.path.abspath(__file__))
HIER = os.path.dirname(SETUP)
NAME = "Hallo-Buch"


def main():
    if sys.version_info < (3, 10):
        sys.exit(f"Python {sys.version.split()[0]} ist zu alt (nötig: 3.10 oder neuer). "
                 "Zuerst den Computer einrichten, siehe START.md, Schritt 2.")
    ohne_venv = "--ohne-venv" in sys.argv
    sys.path.insert(0, SETUP)
    import setup as S
    ordner = os.path.normpath(os.path.join(HIER, "..", NAME))
    print("=== Hallo-Buch: der erste Blick auf pureSATZ ===")
    if os.path.exists(os.path.join(ordner, f"{NAME}-buch.md")):
        print(f"{NAME} gibt es schon – es wird neu gebaut (deine Änderungen bleiben).")
    else:
        w = S.lese_werte(os.path.join(SETUP, "hallo.txt"))
        for k, _, vorgabe in S.FRAGEN:
            w.setdefault(k, vorgabe or "")
        S.buch(ordner, w)
    S.motor(ordner, venv=False)
    if ohne_venv:
        py = sys.executable
    else:
        py = os.path.join(ordner, ".venv", "Scripts" if os.name == "nt" else "bin",
                          "python.exe" if os.name == "nt" else "python3")
        if not os.path.exists(py):
            print("\nEinmalig: Python-Umgebung einrichten (Internet nötig, etwa 1 Minute) …", flush=True)
            subprocess.run([sys.executable, os.path.join("motor", "einrichten.py")], cwd=ordner, check=True)
    subprocess.run([py, os.path.join("motor", "bauen.py"), "schnell"], cwd=ordner, check=True)
    pdfs = sorted(glob.glob(os.path.join(ordner, "ausgabe-normal", "*.pdf")), key=os.path.getmtime)
    if pdfs and "--nicht-oeffnen" not in sys.argv:
        sys.path.insert(0, os.path.join(HIER, "motor"))
        import hilfe
        hilfe.oeffne(pdfs[-1])
    win = os.name == "nt"
    bau = ".\\build.bat schnell" if win else "sh build.sh schnell"
    neu = ".\\setup\\setup.bat" if win else "sh setup/setup.sh"
    print(f"""
Geschafft! Das PDF: {pdfs[-1] if pdfs else os.path.join(ordner, 'ausgabe-normal')}

Ausprobieren:  {NAME}-buch.md im Ordner {NAME} öffnen, einen Satz ändern, speichern, dann
  cd "{ordner}"
  {bau}
Eigenes Buch:  im Ordner pureSATZ  {neu}
Hallo-Buch wegwerfen: den Ordner {NAME} löschen. Ganze Hilfe: hilfe.html""")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError:
        sys.exit("\nHallo-Buch hat nicht geklappt (Meldung oben). Hilfe: START.md, «Wenn etwas nicht klappt». "
                 "Danach einfach nochmals starten.")
    except KeyboardInterrupt:
        sys.exit("\nAbgebrochen.")
