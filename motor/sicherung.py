#!/usr/bin/env python3
"""
sicherung.py – ganzes Buch als ZIP sichern (wird von sicherung.sh aufgerufen).

    sh sicherung.sh               an alle eingetragenen Ziele
    sh sicherung.sh lokal         nur nach «sicherung-lokal»
    sh sicherung.sh cloud         nur nach «sicherung-cloud»
    sh sicherung.sh lokal cloud   an beide

Ziele stehen in der Variablen-Datei unter # TECHNIK:
    - sicherung-lokal: ../Sicherungen                       (relativ zum Buchordner oder mit ~ bzw. /)
    - sicherung-cloud: ~/Nextcloud/Buchprojekte/Sicherungen
    - sicherung-behalten: 10                                (nur die 10 neuesten ZIPs behalten; leer = alle)

Dateiname: <buchname>_JJJJMMTTHHMMSS.zip, z. B. MeinBuch_20261019153012.zip
Im ZIP: alle MD- und TXT-Dateien, fotos/, bilder/, md-history/, motor/, Skripte – und von den Ausgaben
nur das Bildschirm-PDF jeder Ausgabe (als Überblick). Nicht im ZIP: .venv, Zwischenspeicher, alte Motoren,
alle anderen Ausgabedateien (lassen sich mit «sh build.sh final» neu erstellen).
"""
import os
import sys
import zipfile
from datetime import datetime

MOTOR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(MOTOR)
sys.path.insert(0, MOTOR)
import build as bk          # noqa: E402

WEGLASSEN = {".venv", "_bildcache", "_druckbilder", "__pycache__", "_backup", "_epub_tmp", ".git"}


def ziele(wahl):
    """{"lokal": pfad, "cloud": pfad} je nach Wahl; ohne Wahl alle eingetragenen."""
    alle = {}
    for art in ("lokal", "cloud"):
        w = bk.V("sicherung-" + art).strip().strip('"\'«»').strip()     # Anführungszeichen sind erlaubt
        if w:
            w = os.path.expanduser(w)
            alle[art] = os.path.normpath(w if os.path.isabs(w) else os.path.join(BASE, w))
    if not wahl:
        return alle
    fehlt = [a for a in wahl if a not in alle]
    if fehlt:
        raise SystemExit("Kein Ziel eingetragen für: " + ", ".join(fehlt) + "\nIn der Variablen-Datei unter "
                         "# TECHNIK ergänzen, z. B.:  - sicherung-" + fehlt[0] + ": ~/Nextcloud/Sicherungen")
    return {a: alle[a] for a in wahl}


def ordner_bereit(pfad):
    """Zielordner anlegen – aber nur, wenn es den Ort darüber gibt (z. B. ~/Nextcloud ist eingebunden)."""
    if os.path.isdir(pfad):
        return True
    oben = pfad
    while not os.path.isdir(oben):
        oben = os.path.dirname(oben)
    if oben in ("/", os.path.expanduser("~")) or oben == os.path.dirname(os.path.expanduser("~")):
        return False                       # nicht einmal der Hauptordner existiert (Cloud nicht da?)
    os.makedirs(pfad, exist_ok=True)
    return True


def dateien(ausschluss):
    """(voller Pfad, Name im ZIP) aller Dateien, die gesichert werden."""
    ausgabe_ordner, pdfs = set(), set()
    for k in ("A", "B") if bk.zweite_ausgabe() else ("A",):
        g = bk.AUSGABEN[k]
        ausgabe_ordner.add(g["ordner"]); pdfs.add(os.path.join(g["ordner"], g["datei"] + ".pdf"))
    for wurzel, ordner, namen in os.walk(BASE):
        rel = os.path.relpath(wurzel, BASE)
        oben = rel.split(os.sep)[0]
        ordner[:] = sorted(o for o in ordner if o not in WEGLASSEN and not o.startswith("motor-alt-")
                           and os.path.join(wurzel, o) not in ausschluss)
        for n in sorted(namen):
            pfad = os.path.join(wurzel, n)
            relp = os.path.normpath(os.path.join(rel, n))
            if oben in ausgabe_ordner and relp not in pdfs:
                continue                    # von den Ausgaben nur das Bildschirm-PDF
            if n.endswith((".pyc", ".zip", ".backup", "~")) or n.startswith("_tmp") or n == "stichworte-vorschlag.txt":
                continue
            yield pfad, relp


def alte_loeschen(ordner):
    """Nur die neuesten «sicherung-behalten» ZIPs dieses Buchs behalten (leer oder 0 = alle behalten)."""
    import re
    try:
        n = int(bk.V("sicherung-behalten", "0") or 0)
    except ValueError:
        return 0
    if n <= 0:
        return 0
    muster = re.compile(re.escape(bk.NAME) + r"_\d{14}\.zip$")       # nur eigene Sicherungen, nie andere Dateien
    zips = sorted(f for f in os.listdir(ordner) if muster.fullmatch(f))
    for f in zips[:-n]:
        os.remove(os.path.join(ordner, f))
    return max(0, len(zips) - n)


def lesbar(n):
    return f"{n / 1024 / 1024:.1f} MB" if n > 1024 * 1024 else f"{n / 1024:.0f} KB"


def main():
    wahl = [a.lower() for a in sys.argv[1:] if a.lower() in ("lokal", "cloud")]
    unbekannt = [a for a in sys.argv[1:] if a.lower() not in ("lokal", "cloud")]
    if unbekannt:
        raise SystemExit(f"Unbekannt: {' '.join(unbekannt)}\n" + __doc__)
    z = ziele(wahl)
    if not z:
        raise SystemExit("Noch kein Sicherungsziel eingetragen. In der Variablen-Datei unter # TECHNIK z. B.:\n"
                         "  - sicherung-lokal: ../Sicherungen\n  - sicherung-cloud: ~/Nextcloud/Sicherungen")
    name = f"{bk.NAME}_{datetime.now():%Y%m%d%H%M%S}.zip"
    liste = list(dateien(set(z.values())))
    if not any(p.endswith(".pdf") and os.sep in r for p, r in liste):
        print("Hinweis: noch kein Bildschirm-PDF vorhanden (sh build.sh) – gesichert wird trotzdem.")
    fehler = 0
    for art, ordner in z.items():
        if not ordner_bereit(ordner):
            print(f"FEHLER {art}: Ordner nicht erreichbar: {ordner}  (Cloud eingebunden? Pfad richtig?)")
            fehler += 1
            continue
        ziel = os.path.join(ordner, name)
        tmp = ziel + ".tmp"
        with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zf:
            for pfad, relp in liste:
                zf.write(pfad, os.path.join(bk.NAME, relp))
        os.replace(tmp, ziel)
        print(f"Sicherung {art}: {ziel}  ({len(liste)} Dateien, {lesbar(os.path.getsize(ziel))})")
        weg = alte_loeschen(ordner)
        if weg:
            print(f"   {weg} ältere Sicherung(en) gelöscht (behalten: {bk.V('sicherung-behalten')})")
    if fehler:
        sys.exit(1)


if __name__ == "__main__":
    main()
