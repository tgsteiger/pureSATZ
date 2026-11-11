#!/usr/bin/env python3
"""
hoerbuch.py – Hörbuch mit einer Azure-Stimme (pureSATZ ab 2.68, vertonen ab 2.69.8, nur Linux, Testphase).
Im Menü: hb. Im Ordner audio/ des Buchs:  sh hb.sh <befehl>   (ohne Befehl: diese Übersicht)
"""
KURZ = """Hörbuch – Befehle im Ordner audio/ (sh hb.sh …):

  Alles in einem
    sh hb.sh komplett                 texte → vertonen → paket → hoerprobe (tempo=-5% geht auch)
  Probieren
    sh hb.sh probe                    probe.txt mit der eingestellten Stimme
    sh hb.sh probe 2 -10%             Stimme 2, Tempo −10 %      (l = Stimmen-Liste, alle = alle Stimmen)
    sh hb.sh probe probe-namen.txt    anderer Probetext (eigene Datei im Ordner audio/)
    sh hb.sh woerter                  «## KLINGEN FALSCH» aus aussprache-<stimme>.txt anhören
  Hörbuch
    sh hb.sh texte                    Texte aus der Buch-MD → txt-md/ (zeigt, welche sich geändert haben)
    sh hb.sh vertonen                 MP3 für alles, was fehlt oder geändert ist
    sh hb.sh vertonen tempo=-5%       dasselbe mit anderem Tempo (eigener Ordner …-t-5-k…)
    sh hb.sh liste                    Kapitel mit Kürzel
    sh hb.sh 0201,0304                diese Kapitel neu vertonen (04 = ganzer Teil 4, stimme=2, tempo=-5%)
  Weitergeben (→ audio/verkauf/)
    sh hb.sh paket                    ZIP: Kapitel-MP3s (Mono, PAKET_KBIT), M4B mit Kapiteln, Playlist, Cover, LIESMICH
    sh hb.sh hoerprobe                Ansage + erste Minuten eines Kapitels (HOERPROBE in audio.conf)
    sh hb.sh hoerprobe 0201 2         Kapitel 02.01, 2 Minuten
  Sonst
    sh hb.sh schluessel               Azure-Schlüssel eingeben (→ ~/.bashrc)
    sh hb.sh pruefen                  Azure-Paket, Schlüssel, ffmpeg prüfen
  Anhören und nachsehen
    mpv probe-ollie-t-8.mp3                       (Name steht nach jedem Lauf da)
    mpv mp3-md-azure-ollie-t-8-k128/02.01*        ein Kapitel
    tail -30 mp3-md-azure-ollie-t-8-k128/einstellungen.txt   letzter Lauf
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
                HB_JAHR=var.get("jahr", ""), HB_COVER=cover[-1] if cover else "")


def texte():
    """Buch-MD (Geschichten eingesetzt, normale Fassung) → audio/txt-md/, dazu die Ansage als 00.00.00.
    Nur geänderte Texte werden ersetzt – so erkennt «vertonen» sie am Datum (Text neuer als MP3)."""
    import filecmp
    import tempfile
    import manuskript as M
    md, var = buch()
    _, zeilen = M.lies(md)                                  # Text nach BUCHSTART, @@-Geschichten eingesetzt
    tmp = os.path.join(DATEN, "_buch-hoerbuch.md")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write("\n".join(z for _, z in zeilen) + "\n")
    ziel = os.path.join(DATEN, "txt-md")
    os.makedirs(ziel, exist_ok=True)
    neu = tempfile.mkdtemp(prefix="_txt-neu-", dir=DATEN)    # zuerst hierhin, dann vergleichen
    try:
        platz = ";".join(f"{k}={v}" for k, v in var.items() if v and ";" not in v and "\\" not in v)
        p = subprocess.run(["bash", os.path.join(DIR, "md2txt.sh")], cwd=DATEN, capture_output=True, text=True,
                           env=dict(os.environ, MD=tmp, ZIEL=neu, PLATZHALTER=platz, VERSION="normal"))
        print("".join(z + "\n" for z in p.stdout.splitlines() if not z.startswith("Fertig:")) + p.stderr, end="")
        if p.returncode:
            return p.returncode
        for schl, datei in (("AZURE_ANSAGE", "00.00.00_Ansage.txt"), ("AZURE_ABSPANN", "99.00.00_Abspann.txt")):
            ansage = konf().get(schl, "")                  # Ansage am Anfang, Abspann am Schluss (leer = keiner)
            for k, v in var.items():
                ansage = ansage.replace("{%s}" % k, v)
            if ansage.strip():
                with open(os.path.join(neu, datei), "w", encoding="utf-8") as f:
                    f.write(ansage.strip() + "\n")
        alt = {os.path.basename(x) for x in glob.glob(os.path.join(ziel, "*.txt"))}
        frisch = sorted(os.path.basename(x) for x in glob.glob(os.path.join(neu, "*.txt")))
        anders = [n for n in frisch if n not in alt or not filecmp.cmp(os.path.join(neu, n), os.path.join(ziel, n), shallow=False)]
        weg = sorted(alt - set(frisch))
        for n in anders:
            shutil.copy(os.path.join(neu, n), os.path.join(ziel, n))
        for n in weg:
            os.remove(os.path.join(ziel, n))
    finally:
        shutil.rmtree(neu, ignore_errors=True)
    if not alt:
        print(f"Texte: {len(frisch)} Kapitel in txt-md/")
    elif not anders and not weg:
        print("Keine Änderung – alle Texte wie vorher.")
    if alt and anders:
        print(f"Geändert: {len(anders)} Kapitel")
        for n in anders[:15]:
            print("  " + n)
        if len(anders) > 15:
            print(f"  … und {len(anders) - 15} weitere")
    if weg:
        print("Entfernt (Kapitel umbenannt oder gelöscht): " + ", ".join(weg))
    if anders:
        print("Vertonen:  sh hb.sh vertonen   (Menü: hb → v)")
    return 0


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
    k = getpass.getpass("  Schlüssel einfügen (Rechtsklick → Einfügen – es erscheint nichts) [Enter = behalten]: ").strip() or alt
    if k and (len(k) < 32 or not k.isalnum()):                # z. B. falscher Text aus der Zwischenablage
        print("\033[1;31m✗ Das ist kein Azure-Schlüssel\033[0m (nur Buchstaben und Ziffern, mind. 32) – nichts geändert.")
        return False
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


def komplett(rest):
    """Ganzer Ablauf; hält beim ersten Fehler an. Am Schluss die Hörprobe abspielen (mpv, falls da)."""
    try:
        import azure.cognitiveservices.speech  # noqa: F401
    except ImportError:
        sys.exit("Azure-Paket fehlt – im Menü hb → c (prüfen) installieren.")
    _, var = buch()
    env = umgebung(var)
    schritte = [("1/4 Texte", None),
                ("2/4 Vertonen", [os.path.join(DIR, "txt2mp3-azure.py"), "md"] + rest),
                ("3/4 Paket", [os.path.join(DIR, "paket.py"), "paket"]),
                ("4/4 Hörprobe", [os.path.join(DIR, "paket.py"), "hoerprobe"])]
    for name, cmd in schritte:
        print(f"\n── {name} ──")
        rc = texte() if cmd is None else subprocess.run([sys.executable] + cmd, cwd=DATEN, env=env).returncode
        if rc:
            print(f"Abgebrochen bei «{name[4:]}» – Meldung oben. Danach wieder:  sh hb.sh komplett")
            return rc
    probe = os.path.join(DATEN, "verkauf", "hoerprobe.mp3")
    if shutil.which("mpv") and os.path.exists(probe) and sys.stdin.isatty():
        print("Hörprobe läuft (mpv-Fenster)")
        subprocess.Popen(["mpv", "--force-window=yes", probe], stdin=subprocess.DEVNULL,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return 0


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
    if befehl == "komplett":                                # Ablauf in einem: texte → vertonen → paket → hoerprobe
        return komplett(rest)
    if befehl in ("paket", "hoerprobe"):                   # braucht kein Azure, nur ffmpeg und fertige MP3s
        _, var = buch()
        return subprocess.run([sys.executable, os.path.join(DIR, "paket.py"), befehl] + rest, cwd=DATEN,
                              env=umgebung(var)).returncode
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
    elif befehl in ("vertonen", "alles"):                   # alles = alter Name
        cmd = [sys.executable, os.path.join(DIR, "txt2mp3-azure.py"), "md"] + rest
    else:                                                   # liste, Kürzel, stimme=…
        cmd = [sys.executable, os.path.join(DIR, "txt2mp3-azure.py"), "md", befehl] + rest
    return subprocess.run(cmd, cwd=DATEN, env=env).returncode       # Pfade in Meldungen ab audio/


if __name__ == "__main__":
    sys.exit(main())
