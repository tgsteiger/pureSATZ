#!/usr/bin/env python3
"""
hoerbuch.py – Hörbuch mit einer Azure-Stimme (pureSATZ ab 2.68, nur Linux, Testphase).
Im Menü: hb. Im Ordner audio/ des Buchs:  sh hb.sh <befehl>   (ohne Befehl: diese Übersicht)
"""
KURZ = """Hörbuch – Befehle im Ordner audio/ (sh hb.sh …):

  Probieren
    sh hb.sh probe                    probe.txt mit der eingestellten Stimme
    sh hb.sh probe 2 -10%             Stimme 2, Tempo −10 %      (l = Stimmen-Liste, alle = alle Stimmen)
    sh hb.sh probe probe-namen.txt    anderer Probetext (eigene Datei im Ordner audio/)
    sh hb.sh woerter                  «## KLINGEN FALSCH» aus aussprache-<stimme>.txt anhören
  Hörbuch
    sh hb.sh texte                    Texte aus der Buch-MD → txt-md/ (nach Änderungen im Buch)
    sh hb.sh liste                    Kapitel mit Kürzel
    sh hb.sh alles                    ganzes Hörbuch (fertige werden übersprungen)
    sh hb.sh 0201,0304                nur diese Kapitel neu     (04 = ganzer Teil 4, stimme=2 = andere Stimme)
  Sonst
    sh hb.sh schluessel               Azure-Schlüssel eingeben (→ ~/.bashrc)
    sh hb.sh pruefen                  Azure-Paket, Schlüssel, ffmpeg prüfen
  Anhören und nachsehen
    mpv probe-ollie-de-de-r-8.mp3                 (Name steht nach jedem Lauf da)
    mpv mp3-md-azure-ollie/02.01*                 ein Kapitel
    tail -30 mp3-md-azure-ollie/einstellungen.txt letzter Lauf
Mehr: Hilfe «Hörbuch: Befehle zum Kopieren» (sh menu.sh → hb → h)"""
import glob
import os
import shutil
import subprocess
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
MOTOR = os.path.dirname(DIR)
BASE = os.path.dirname(MOTOR)
DATEN = os.path.join(BASE, "audio")
sys.path.insert(0, MOTOR)


def anlegen():
    """audio/ mit audio.conf und Aussprache-Muster anlegen; Bestehendes bleibt."""
    os.makedirs(DATEN, exist_ok=True)
    for f in os.listdir(os.path.join(DIR, "vorlage")):
        ziel = os.path.join(DATEN, f)
        if not os.path.exists(ziel):
            shutil.copy(os.path.join(DIR, "vorlage", f), ziel)
            print(f"  neu: audio/{f}")


def buch():
    """(Buch-MD, Variablen) – <name>-buch.md und <name>-variablen.md im Buchordner."""
    import manuskript as M
    md = next(iter(sorted(glob.glob(os.path.join(BASE, "*-buch.md")))), None)
    if not md:
        sys.exit("Keine Buch-MD (…-buch.md) im Buchordner gefunden.")
    vd = md[:-len("-buch.md")] + "-variablen.md"
    var = M.lies_variablen(vd)[0] if os.path.exists(vd) else {}
    var.update({k: v for k, v in M.lies(md)[0].items() if k not in var})
    for k, v in list(var.items()):                          # wie der Bau: {untertitel} = {untertitel-normal}
        if k.endswith("-normal") and not var.get(k[:-7]):
            var[k[:-7]] = v
    return md, var


def umgebung(var):
    """Angaben fürs Vorlesen: Titel, Autor, Cover (Umschlag vorne, falls gebaut)."""
    cover = sorted(glob.glob(os.path.join(BASE, "ausgabe-normal", "*_Vorderseite.jpg")), key=os.path.getmtime)
    return dict(os.environ, AUDIO_DIR=DATEN, HB_TITEL=var.get("titel", ""), HB_AUTOR=var.get("autor", ""),
                HB_COVER=cover[-1] if cover else "")


def texte():
    """Buch-MD (Geschichten eingesetzt, normale Fassung) → audio/txt-md/, dazu die Ansage als 00.00.00."""
    import manuskript as M
    md, var = buch()
    _, zeilen = M.lies(md)                                  # Text nach BUCHSTART, @@-Geschichten eingesetzt
    tmp = os.path.join(DATEN, "_buch-hoerbuch.md")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write("\n".join(z for _, z in zeilen) + "\n")
    ziel = os.path.join(DATEN, "txt-md")
    os.makedirs(ziel, exist_ok=True)
    for p in glob.glob(os.path.join(ziel, "*.txt")):
        os.remove(p)
    platz = ";".join(f"{k}={v}" for k, v in var.items() if v and ";" not in v and "\\" not in v)
    r = subprocess.run(["bash", os.path.join(DIR, "md2txt.sh")], cwd=DATEN,
                       env=dict(os.environ, MD=tmp, ZIEL=ziel, PLATZHALTER=platz, VERSION="normal")).returncode
    ansage = konf().get("AZURE_ANSAGE", "")
    for k, v in var.items():
        ansage = ansage.replace("{%s}" % k, v)
    if r == 0 and ansage.strip():
        with open(os.path.join(ziel, "00.00.00_Ansage.txt"), "w", encoding="utf-8") as f:
            f.write(ansage.strip() + "\n")
        print("  Ansage: 00.00.00_Ansage.txt")
    return r


def konf():
    import re
    conf = {}
    for z in open(os.path.join(DATEN, "audio.conf"), encoding="utf-8"):
        m = re.match(r'^([A-Z0-9_]+)="([^"]*)"', z.strip())
        if m:
            conf[m.group(1)] = m.group(2)
    return conf


def schluessel():
    """Azure-Schlüssel und Region abfragen und in ~/.bashrc eintragen (alte Zeilen ersetzt, Sicherung .bashrc.bak)."""
    import getpass
    rc = os.path.expanduser("~/.bashrc")
    alt, reg = os.environ.get("AZURE_SPEECH_KEY", ""), os.environ.get("AZURE_SPEECH_REGION", "switzerlandnorth")
    print("Azure-Schlüssel " + (f"(jetzt …{alt[-4:]})" if alt else "(noch keiner)") +
          " – portal.azure.com → Speech-Ressource → «Schlüssel und Endpunkt» → Schlüssel 1")
    k = getpass.getpass("  Schlüssel einfügen (Strg+Shift+V – es erscheint nichts) [Enter = behalten]: ").strip() or alt
    if not k:
        print("Kein Schlüssel – nichts geändert."); return False
    reg = input(f"  Region [Enter = {reg}]: ").strip() or reg
    zeilen = open(rc, encoding="utf-8").read().splitlines() if os.path.exists(rc) else []
    if zeilen:
        shutil.copy(rc, rc + ".bak")
    zeilen = [z for z in zeilen if not z.strip().startswith(("export AZURE_SPEECH_KEY=", "export AZURE_SPEECH_REGION="))]
    zeilen += [f"export AZURE_SPEECH_KEY='{k}'", f"export AZURE_SPEECH_REGION='{reg}'"]
    with open(rc, "w", encoding="utf-8") as f:
        f.write("\n".join(zeilen) + "\n")
    os.environ["AZURE_SPEECH_KEY"], os.environ["AZURE_SPEECH_REGION"] = k, reg
    print(f"OK  Schlüssel …{k[-4:]} · Region {reg} in ~/.bashrc (Sicherung ~/.bashrc.bak). Gilt ab sofort im Menü")
    print("    und in jedem neuen Terminal. Nie in eine Datei im Buch oder zu GitHub geben.")
    return True


def pruefen():
    ok = True
    try:
        import azure.cognitiveservices.speech  # noqa: F401
        print("OK  Azure-Paket")
    except ImportError:
        ok = False
        print("Fehlt: Azure-Paket.")
        if input("  Jetzt installieren? [n = nein | Enter = ja]: ").strip().lower() not in ("n", "nein"):
            ok = subprocess.run([sys.executable, "-m", "pip", "install", "azure-cognitiveservices-speech"]).returncode == 0
    for prog in ("ffmpeg", "mpv"):
        if shutil.which(prog):
            print(f"OK  {prog}")
        else:
            ok = ok and prog == "mpv"                       # mpv nur zum Anhören
            print(f"Fehlt: {prog} – installieren mit:  sudo apt install {prog}")
    if os.environ.get("AZURE_SPEECH_KEY"):
        print(f"OK  Azure-Schlüssel (Region {os.environ.get('AZURE_SPEECH_REGION', 'switzerlandnorth')})")
    else:
        print("Fehlt: AZURE_SPEECH_KEY")
        ok = schluessel() and ok
    return ok


def main():
    if not sys.platform.startswith("linux"):
        sys.exit("Das Hörbuch gibt es vorerst nur unter Linux.")
    anlegen()
    a = sys.argv[1:] or ["hilfe"]
    befehl, rest = a[0], a[1:]
    if befehl in ("hilfe", "-h", "--help"):
        print(KURZ); return 0
    if befehl == "schluessel":
        return 0 if schluessel() else 1
    if befehl == "pruefen":
        return 0 if pruefen() else 1
    if befehl == "texte":
        return texte()
    if befehl == "woerter":
        befehl = "aussprache"
    if not glob.glob(os.path.join(DATEN, "txt-md", "*.txt")) and befehl not in ("aussprache", "probe"):
        print("Noch keine Texte – zuerst:  texte")
        if texte():
            return 1
    if befehl != "liste":
        try:
            import azure.cognitiveservices.speech  # noqa: F401
        except ImportError:
            sys.exit("Azure-Paket fehlt – im Menü hb → c (prüfen) installieren.")
    _, var = buch()
    env = umgebung(var)
    if befehl in ("aussprache", "probe"):
        cmd = [sys.executable, os.path.join(DIR, "probe-azure.py")] + (["aussprache"] if befehl == "aussprache" else []) + rest
    elif befehl == "alles":
        cmd = [sys.executable, os.path.join(DIR, "txt2mp3-azure.py"), "md"] + rest
    else:                                                   # liste, Kürzel, stimme=…
        cmd = [sys.executable, os.path.join(DIR, "txt2mp3-azure.py"), "md", befehl] + rest
    return subprocess.run(cmd, cwd=DATEN, env=env).returncode       # Pfade in Meldungen ab audio/


if __name__ == "__main__":
    sys.exit(main())
