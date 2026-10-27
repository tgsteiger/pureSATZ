#!/usr/bin/env python3
"""
hallo.py – der erste Blick auf pureSATZ: legt neben pureSATZ das Beispielbuch «Hallo-Buch» an,
baut es und öffnet das PDF. Aufruf im Ordner pureSATZ:

    sh hallo.sh                 (Windows: hallo.bat doppelklicken)

Gibt es Hallo-Buch schon, wird es nur neu gebaut (eigene Änderungen bleiben).
Mit --kette (Schritt 3 von START-…): erklärt kurz, fragt, baut ruhig und öffnet Ordner und PDF.
Zum Wegwerfen einfach den Ordner Hallo-Buch löschen. Werte: setup/hallo.txt.
"""
import contextlib
import glob
import io
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


def ja_frage(text):
    try:
        return input(text).strip().lower() in ("", "j", "ja")
    except EOFError:
        return False


def main():
    if sys.version_info < (3, 10):
        sys.exit(f"Python {sys.version.split()[0]} ist zu alt (nötig: 3.10 oder neuer). "
                 "Zuerst den Computer einrichten, siehe START.md, Schritt 2.")
    ohne_venv = "--ohne-venv" in sys.argv
    kette = "--kette" in sys.argv
    sys.path.insert(0, SETUP)
    import setup as S
    ordner = os.path.normpath(os.path.join(HIER, "..", NAME))
    if kette:
        print(f"""Jetzt entsteht ein Beispielbuch «{NAME}» neben pureSATZ:
  {ordner}
Es zeigt, was pureSATZ kann: Kapitel, Fotos, Tabellen, Umschlag. Beim ersten Mal dauert es
etwa eine Minute (Internet nötig). Danach öffnen sich der Ordner und das PDF.
Das Hallo-Buch ist nur zum Anschauen und Ausprobieren – es darf später weg.
""")
        if not ja_frage("Hallo-Buch jetzt anlegen? [Enter = ja, n = überspringen]: "):
            print("Übersprungen.")
            return
        print()
    else:
        print("=== Hallo-Buch: der erste Blick auf pureSATZ ===")
    still = contextlib.redirect_stdout(io.StringIO()) if kette else contextlib.nullcontext()
    if os.path.exists(os.path.join(ordner, f"{NAME}-buch.md")):
        print(f"{NAME} gibt es schon – es wird neu gebaut (deine Änderungen bleiben).")
    else:
        w = S.lese_werte(os.path.join(SETUP, "hallo.txt"))
        for k, _, vorgabe in S.FRAGEN:
            w.setdefault(k, vorgabe or "")
        with still:
            S.buch(ordner, w)
    with (contextlib.redirect_stdout(io.StringIO()) if kette else contextlib.nullcontext()):
        S.motor(ordner, venv=False)
    if ohne_venv:
        py = sys.executable
    else:
        py = os.path.join(ordner, ".venv", "Scripts" if os.name == "nt" else "bin",
                          "python.exe" if os.name == "nt" else "python3")
        if not os.path.exists(py):
            print("Einmalig: Python-Umgebung einrichten (Internet nötig, etwa 1 Minute) …", flush=True)
            subprocess.run([sys.executable, os.path.join("motor", "einrichten.py")], cwd=ordner, check=True)
    befehl = [py, os.path.join("motor", "bauen.py"), "schnell"]
    if kette:                                       # ruhig bauen, Meldungen nur bei einem Fehler
        print("Hallo-Buch wird gebaut …", flush=True)
        r = subprocess.run(befehl, cwd=ordner, capture_output=True, text=True, encoding="utf-8", errors="replace",
                           env=dict(os.environ, PYTHONIOENCODING="utf-8"))
        if r.returncode:
            print(r.stdout[-4000:], r.stderr[-4000:], sep="\n")
            raise subprocess.CalledProcessError(r.returncode, befehl)
    else:
        subprocess.run(befehl, cwd=ordner, check=True)
    pdfs = sorted(glob.glob(os.path.join(ordner, "ausgabe-normal", "*.pdf")), key=os.path.getmtime)
    if "--nicht-oeffnen" not in sys.argv:
        sys.path.insert(0, os.path.join(HIER, "motor"))
        import hilfe
        if kette:
            hilfe.oeffne(ordner)
        if pdfs:
            hilfe.oeffne(pdfs[-1])
    if kette:
        print(f"""
OK  Hallo-Buch fertig. Ordner und PDF sind offen.
Zum Ausprobieren: im Ordner {NAME} die Datei {NAME}-buch.md öffnen, einen Satz ändern –
wie neu gebaut wird, steht am Schluss. Das Hallo-Buch darf später weg.""")
        return
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
    if sys.stdin.isatty() and "--nicht-oeffnen" not in sys.argv:    # nächster Schritt: das eigene Buch
        if ja_frage("\nJetzt dein eigenes Buch anlegen? [Enter = ja, n = nein]: "):
            subprocess.run([sys.executable, os.path.join(SETUP, "setup.py")], cwd=HIER)


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError:
        sys.exit("\nHallo-Buch hat nicht geklappt (Meldung oben). Hilfe: START.md, «Wenn etwas nicht klappt». "
                 "Danach einfach nochmals starten.")
    except KeyboardInterrupt:
        sys.exit("\nAbgebrochen.")
