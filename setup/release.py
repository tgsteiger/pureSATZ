#!/usr/bin/env python3
"""
release.py – neue Motor-Version freigeben (Aufruf: sh release.sh im Ordner pureSATZ, ab 2.84).

1. zeigt Version, CHANGELOG-Eintrag und geänderte Dateien
2. fragt «Übernehmen?»
3. Selbsttest (nur Menü/Hilfe geändert: Frage, ob überspringen)
4. git add / commit / push
5. alle Bücher daneben (../ und ../buecher/): sh update.sh lokal ja
"""
import glob
import os
import re
import subprocess
import sys

HIER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Nur diese Dateien geändert = Selbsttest darf übersprungen werden (Menü, Hilfe, Texte)
LEICHT = ("motor/menu.py", "motor/HILFE.md", "motor/CHANGELOG.md", "motor/VERSION", "hilfe.html", "hilfe-ki.md",
          "README.md", "readme.txt", "START.md", "INSTALLATION.md", "GITHUB.md", "ERSTES-BUCH.md")


def git(*a):
    return subprocess.run(["git"] + list(a), cwd=HIER, capture_output=True, text=True).stdout


def ja(text, standard=False):
    """Frage mit Empfehlung: ↵ = standard (grosser Buchstabe in [J/n] bzw. [j/N])."""
    try:
        a = input(text + (" [J/n]: " if standard else " [j/N]: ")).strip().lower()
    except EOFError:
        return standard
    return standard if not a else a in ("j", "ja", "y")


def main():
    os.chdir(HIER)
    version = open("motor/VERSION", encoding="utf-8").read().strip()
    alt = git("show", "HEAD:motor/VERSION").strip()
    dateien = [z[3:].strip().strip('"') for z in git("status", "--porcelain").splitlines() if z.strip()]
    if not dateien:
        print("Nichts geändert – nichts zu tun.")
        return
    eintrag, dabei = [], False                       # neuester Abschnitt im CHANGELOG
    for z in open("motor/CHANGELOG.md", encoding="utf-8"):
        if re.match(r"##\s+\d", z):
            if dabei:
                break
            dabei = True
        if dabei:
            eintrag.append(z.rstrip())
    print(f"\npureSATZ {alt} → {version}" + ("   ⚠ Version nicht erhöht: Bücher werden nicht aktualisiert" if version == alt else ""))
    print("\n".join(eintrag).strip())
    print("\nGeändert:\n  " + "\n  ".join(dateien))
    if not ja("\nÜbernehmen? (empfohlen: ↵)", True):
        print("Nichts gemacht.")
        return

    leicht = all(d in LEICHT or d.startswith(("_backup/", "docs/")) for d in dateien)
    if leicht and not ja("Nur Menü/Hilfe/Texte geändert – Selbsttest nicht nötig (empfohlen: ↵). Trotzdem testen?"):
        print("Selbsttest übersprungen.")
    else:
        print("\nSelbsttest läuft (ca. 2 Minuten) …", flush=True)
        log = os.path.join(HIER, "_backup", "selbsttest-letzter.txt")
        os.makedirs(os.path.dirname(log), exist_ok=True)
        with open(log, "w", encoding="utf-8") as f:
            r = subprocess.run([sys.executable, os.path.join("test", "selbsttest.py")], stdin=subprocess.DEVNULL,
                               stdout=f, stderr=subprocess.STDOUT)
        zeilen = open(log, encoding="utf-8", errors="replace").read().strip().splitlines()
        if r.returncode or not any("SELBSTTEST IN ORDNUNG" in z for z in zeilen):
            print("\n".join(zeilen[-20:]))
            print(f"\n✗ Selbsttest nicht in Ordnung – nichts hochgeladen. Ganzer Bericht: {log}")
            sys.exit(1)
        print("✓ " + zeilen[-1])

    titel = next((z[2:].strip() for z in eintrag if z.startswith("- ")), "")
    text = f"{version}: {titel}"[:90]
    git("add", "-A")
    c = subprocess.run(["git", "commit", "-m", text], cwd=HIER)
    p = subprocess.run(["git", "push"], cwd=HIER)
    if c.returncode or p.returncode:
        sys.exit("✗ git commit/push hat nicht geklappt (siehe oben).")
    print(f"✓ GitHub: {text}")

    if version == alt:
        return
    oben = os.path.dirname(HIER)
    buecher = sorted({os.path.dirname(os.path.dirname(v)) for v in
                      glob.glob(os.path.join(oben, "*", "motor", "VERSION")) +
                      glob.glob(os.path.join(oben, "buecher", "*", "motor", "VERSION"))
                      if os.path.dirname(os.path.dirname(v)) != HIER})
    for b in buecher:
        if os.path.exists(os.path.join(b, "update.sh")):
            print(f"\n=== {os.path.basename(b)} ===", flush=True)
            subprocess.run(["sh", "update.sh", "lokal", "ja"], cwd=b)
    print("\n✓ Fertig. Bauen im Menü des Buchs (s).")


if __name__ == "__main__":
    main()
