#!/usr/bin/env python3
"""
sync.py – Buchdaten zwischen Computern abgleichen über ein privates GitHub-Repository (wird von sync.sh aufgerufen).

    sh sync.sh        am Anfang und am Ende der Arbeit (Windows: sync.bat)

Ablauf: eigene Änderungen festhalten (commit mit Datum und Computername) → Stand von GitHub holen
(pull) → hochladen (push). Was in .gitignore steht (.venv, Ausgaben, Zwischenspeicher, md-history),
bleibt auf jedem Computer für sich.

Einmalig pro Buch (im Buchordner):
    git init -b main
    gh repo create <buchname> --private --source . --push
Auf einem anderen Computer (neben pureSATZ):
    gh repo clone <benutzer>/<buchname> <Buchordner>
"""
import os
import platform
import shutil
import subprocess
import sys
from datetime import datetime

MOTOR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(MOTOR)


def git(*args, pruefen=True):
    r = subprocess.run(["git"] + list(args), cwd=BASE, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if pruefen and r.returncode:
        raise RuntimeError((r.stdout + r.stderr).strip())
    return r


def geaendert():
    """Liste der geänderten Dateien (git status, kurz)."""
    return [z[3:] for z in git("status", "--porcelain").stdout.splitlines() if z.strip()]


def main():
    name = os.path.basename(BASE)
    if not shutil.which("git"):
        sys.exit("git fehlt. Linux: sudo apt install git · Mac: brew install git · Windows: winget install Git.Git")
    if not os.path.isdir(os.path.join(BASE, ".git")):
        sys.exit(f"Dieses Buch ist noch nicht mit GitHub verbunden. Einmalig im Buchordner:\n"
                 f"  git init -b main\n  gh repo create {name.lower()} --private --source . --push")
    if not git("remote", pruefen=False).stdout.strip():
        sys.exit(f"Kein GitHub-Ziel eingetragen. Einmalig:  gh repo create {name.lower()} --private --source . --push")

    # 1. Eigene Änderungen festhalten
    eigene = geaendert()
    if eigene:
        git("add", "-A")
        notiz = f"Stand {datetime.now():%d.%m.%Y %H:%M} von {platform.node() or 'Computer'}"
        r = git("commit", "-m", notiz, pruefen=False)
        if r.returncode:
            sys.exit("Commit ging nicht – sind Name und Mail für git eingetragen? (siehe pureSATZ/GITHUB.md, Schritt 3)\n"
                     + (r.stdout + r.stderr).strip())
        print(f"Eigene Änderungen ({len(eigene)}): " + ", ".join(eigene[:8]) + (" …" if len(eigene) > 8 else ""))

    # 2. Stand von GitHub holen (zusammenführen)
    vorher = git("rev-parse", "HEAD").stdout.strip()
    r = git("pull", "--no-rebase", "--no-edit", pruefen=False)
    if r.returncode:
        konflikt = [z[3:] for z in git("status", "--porcelain").stdout.splitlines() if z[:2] in ("UU", "AA")]
        if not konflikt:
            git("merge", "--abort", pruefen=False)
            sys.exit("Holen von GitHub ging nicht (Internet? Anmeldung: gh auth login):\n" + (r.stdout + r.stderr).strip())
        # Dieselbe Stelle auf zwei Computern geändert: eigene Version behalten, die andere daneben legen
        zeit = f"{datetime.now():%Y%m%d-%H%M}"
        daneben = []
        for f in konflikt:
            stamm, endung = os.path.splitext(f)
            andere = f"{stamm}_KONFLIKT-anderer-Computer_{zeit}{endung}"
            with open(os.path.join(BASE, andere), "wb") as h:
                h.write(subprocess.run(["git", "show", f":3:{f}"], cwd=BASE, capture_output=True).stdout)
            git("checkout", "--ours", "--", f)
            git("add", "--", f, andere)
            daneben.append(andere)
        git("commit", "--no-edit", "-m", f"Konflikt in {', '.join(konflikt)}: beide Versionen behalten")
        print("ACHTUNG: Dieselbe Stelle wurde auf zwei Computern geändert. Nichts geht verloren:")
        for f, d in zip(konflikt, daneben):
            print(f"  {f}  = deine Version (dieser Computer)\n  {d}  = Version vom anderen Computer")
        print("Bitte vergleichen, in die eigene Datei übernehmen, was fehlt, die KONFLIKT-Datei löschen und nochmals sh sync.sh.")
    neu = git("diff", "--name-only", vorher, "HEAD").stdout.split()
    if neu:
        print(f"Von GitHub geholt ({len(neu)}): " + ", ".join(neu[:8]) + (" …" if len(neu) > 8 else ""))

    # 3. Hochladen
    voraus = git("rev-list", "--count", "@{u}..HEAD", pruefen=False).stdout.strip()
    if voraus and voraus != "0":
        r = git("push", pruefen=False)
        if r.returncode:
            sys.exit("Hochladen ging nicht (Internet? Anmeldung: gh auth login):\n" + (r.stdout + r.stderr).strip())
        print("Hochgeladen.")
    if not eigene and not neu:
        print("Alles aktuell – nichts zu tun.")
    elif not neu:
        print("Fertig. Auf dem anderen Computer: sh sync.sh")
    else:
        print("Fertig. Tipp: sh build.sh schnell zeigt den neuen Stand.")


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as e:
        sys.exit(f"git meldet einen Fehler:\n{e}")
