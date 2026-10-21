#!/usr/bin/env python3
"""
update.py – prüft, ob es einen neueren Motor gibt, und setzt ihn ins Buch ein (wird von update.sh aufgerufen).

    sh update.sh            prüfen, Neuerungen zeigen, fragen, aktualisieren   (Windows: update.bat)
    sh update.sh pruefen    nur prüfen, nichts ändern
    sh update.sh ja         ohne Rückfrage aktualisieren

    sh update.sh lokal      aus dem Ordner ../pureSATZ neben dem Buch holen (ohne GitHub)

Der neue Motor kommt direkt von GitHub (Repository «pureSATZ»). Ein lokaler Ordner pureSATZ
ist dafür nicht nötig. Geholt wird mit git und der eigenen GitHub-Anmeldung, also klappt es auch bei
einem privaten Repository, wenn man dazu eingeladen ist.

Ersetzt wird NUR der Ordner motor/. Die Buch-Dateien (MD, Stichworte, Fotos, Bilder, Einstellungen)
bleiben unberührt. Der alte Motor bleibt als motor-alt-<version>/ liegen (kommt nicht zu GitHub).
Fehlende Hilfsdateien im Buch (z. B. update.sh) werden ergänzt, bestehende nie überschrieben.

Andere Quelle: Umgebungsvariable PURESATZ_QUELLE=https://github.com/<name>/<repo>.git oder ein Ordner.
"""
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from datetime import datetime
try:                                            # Windows: «sh build.sh» in Meldungen als «.\build.bat»
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "."))
    import plattform
    plattform.windows_befehle()
except ImportError:
    pass

QUELLE = (os.environ.get("PURESATZ_QUELLE") or os.environ.get("LEERES_BUCH_QUELLE")
          or "https://github.com/tgsteiger/pureSATZ.git")
MOTOR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(MOTOR)
HILFSDATEIEN = ("update.sh", "update.bat", "sync.sh", "sync.bat", "build.sh", "build.bat",
                "cleanup.sh", "cleanup.bat", "sicherung.sh", "sicherung.bat", "neu.sh", "neu.bat")
# Erzeugte Dateien, die nicht zu GitHub gehören (werden in .gitignore ergänzt, falls sie fehlen)
IGNORIEREN = ("geschichten-uebersicht.html", "geschichten/UEBERSICHT.md", "_geschichten-sammlung.md", "hilfe.html")


def version(ordner):
    p = os.path.join(ordner, "VERSION")
    return open(p, encoding="utf-8").read().strip() if os.path.exists(p) else "0"


def vtuple(v):
    try:
        return tuple(int(x) for x in v.split("."))
    except ValueError:
        return (0,)


def git(*args, cwd=None):
    return subprocess.run(["git"] + list(args), cwd=cwd, capture_output=True, text=True,
                          encoding="utf-8", errors="replace",
                          env=dict(os.environ, GIT_TERMINAL_PROMPT="0"))


def weg(pfad):
    """Ordner löschen – auch schreibgeschützte git-Dateien unter Windows."""
    def schreibbar(f, p, _):
        os.chmod(p, stat.S_IWRITE)
        f(p)
    shutil.rmtree(pfad, onerror=schreibbar)


def hole(ziel):
    """Neuesten Stand holen – aus einem Ordner (kopieren) oder von GitHub (nur motor/ und vorlage/)."""
    if os.path.isdir(QUELLE):
        if not os.path.isdir(os.path.join(QUELLE, "motor")):
            return f"Im Ordner {QUELLE} gibt es keinen Ordner motor/."
        for teil in ("motor", "vorlage"):
            if os.path.isdir(os.path.join(QUELLE, teil)):
                shutil.copytree(os.path.join(QUELLE, teil), os.path.join(ziel, teil),
                                ignore=shutil.ignore_patterns("__pycache__"))
        return None
    r = git("clone", "--quiet", "--depth", "1", "--filter=blob:none", "--sparse", QUELLE, ziel)
    if r.returncode == 0 and git("sparse-checkout", "set", "motor", "vorlage", cwd=ziel).returncode == 0:
        return None
    shutil.rmtree(ziel, ignore_errors=True)
    r = git("clone", "--quiet", "--depth", "1", QUELLE, ziel)             # älteres git: ganz holen
    return None if r.returncode == 0 else (r.stdout + r.stderr).strip()


def neuerungen(changelog, alt):
    """Abschnitte aus CHANGELOG.md, die neuer sind als die eigene Version."""
    if not os.path.exists(changelog):
        return []
    zeilen, dabei = [], False
    for z in open(changelog, encoding="utf-8"):
        m = re.match(r"##\s+(\d+(?:\.\d+)*)", z)
        if m:
            dabei = vtuple(m.group(1)) > vtuple(alt)
        if dabei:
            zeilen.append(z.rstrip())
    while zeilen and not zeilen[-1].strip():
        zeilen.pop()
    return zeilen


def frage(text):
    try:
        return input(text).strip().lower() in ("", "j", "ja", "y", "yes")
    except EOFError:
        return False


def main():
    global QUELLE
    a = [x.lower() for x in sys.argv[1:]]
    if "lokal" in a:
        QUELLE = os.path.join(os.path.dirname(BASE), "pureSATZ")
    nur_pruefen = "pruefen" in a or "prüfen" in a
    ohne_frage = "ja" in a
    if not os.path.isdir(QUELLE) and not shutil.which("git"):
        sys.exit("git fehlt. Linux: sudo apt install git · Mac: xcode-select --install · Windows: winget install Git.Git")

    alt = version(MOTOR)
    print(f"Motor in diesem Buch: {alt}")
    wo = "im Ordner " + QUELLE if os.path.isdir(QUELLE) else "auf GitHub"
    print(f"Suche den neuesten Motor {wo} …", flush=True)
    tmp = tempfile.mkdtemp(prefix="pureSATZ-update-")
    try:
        quelle = os.path.join(tmp, "pureSATZ")
        fehler = hole(quelle)
        if fehler:
            sys.exit("Quelle nicht erreichbar oder kein Zugriff auf\n  " + QUELLE + "\n"
                     "Prüfen: Internet? Bei GitHub angemeldet (gh auth login bzw. Token)? Zum Repository eingeladen?\n"
                     + fehler)
        neu_motor = os.path.join(quelle, "motor")
        neu = version(neu_motor)
        print(f"Neuester Motor {wo}: {neu}")

        if vtuple(neu) < vtuple(alt):
            print(f"Dein Motor ist NEUER als der {wo}. Bitte die Korrektur in pureSATZ übernehmen "
                  "und dort hochladen – sonst geht sie beim nächsten Update verloren.")
            return
        if vtuple(neu) == vtuple(alt):
            print("Der Motor ist aktuell – nichts zu tun.")
            return

        liste = neuerungen(os.path.join(neu_motor, "CHANGELOG.md"), alt)
        if liste:
            print("\nNeu seit " + alt + ":")
            for z in liste[:40]:
                print("  " + z)
            if len(liste) > 40:
                print(f"  … (mehr in motor/CHANGELOG.md nach dem Update)")
        if nur_pruefen:
            print(f"\nUpdate verfügbar: {alt} -> {neu}. Einspielen mit:  sh update.sh   (Windows: update.bat)")
            return
        if not ohne_frage and not (sys.stdin.isatty() and frage(f"\nMotor jetzt auf {neu} aktualisieren? [ja]/nein: ")):
            print("Nichts geändert.")
            return

        # Alten Motor beiseitelegen, neuen einsetzen
        sicherung = os.path.join(BASE, f"motor-alt-{alt}")
        if os.path.exists(sicherung):
            sicherung += f"-{datetime.now():%Y%m%d%H%M%S}"
        os.chdir(BASE)                    # wir laufen selbst aus motor/ heraus
        shutil.move(MOTOR, sicherung)
        try:
            shutil.copytree(neu_motor, MOTOR, ignore=shutil.ignore_patterns("__pycache__"))
        except Exception:
            shutil.rmtree(MOTOR, ignore_errors=True)
            shutil.move(sicherung, MOTOR)
            raise
        print(f"\nMotor aktualisiert: {alt} -> {neu} (alter Motor in {os.path.basename(sicherung)}/)")

        # Fehlende Hilfsdateien ergänzen (nie überschreiben)
        vorlage = os.path.join(quelle, "vorlage")
        for f in HILFSDATEIEN:
            q, z = os.path.join(vorlage, f), os.path.join(BASE, f)
            if os.path.exists(q) and not os.path.exists(z):
                shutil.copy2(q, z)
                print(f"  neu im Buch: {f}")
        gi = os.path.join(BASE, ".gitignore")
        if os.path.exists(gi):
            alt_gi = open(gi, encoding="utf-8").read()
            fehlt = [x for x in IGNORIEREN if x not in alt_gi.split("\n")]
            if fehlt:
                with open(gi, "a", encoding="utf-8") as fh:
                    fh.write(("" if alt_gi.endswith("\n") else "\n") + "# pureSATZ 2.11: Geschichten-Übersicht (wird erzeugt)\n"
                             + "\n".join(fehlt) + "\n")
                print("  .gitignore ergänzt: " + ", ".join(fehlt))

        # Python-Umgebung prüfen (neue Pakete?)
        subprocess.run([sys.executable, os.path.join(MOTOR, "einrichten.py")], cwd=BASE)
        print("\nFertig. Jetzt testen:  sh build.sh schnell")
        if os.path.isdir(os.path.join(BASE, ".git")):
            print("Danach für die anderen Computer:  sh sync.sh")
    finally:
        if os.path.exists(tmp):
            weg(tmp)


if __name__ == "__main__":
    main()
