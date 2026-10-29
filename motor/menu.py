#!/usr/bin/env python3
"""
menu.py – Menü mit den häufigsten Befehlen (ab 2.50, Buchstaben 2.51). Aufruf im Buchordner: sh menu.sh (Windows: menu.bat)

Ein Buchstabe pro Befehl, b / m / p / o / g mit Untermenü. ↑ ↓ = letzte Eingaben, Enter = zurück, q = beenden.
Ganze Befehle gehen auch: final · leseprobe uz 18,20 · personen Eltern.
MD, PDF und Ordner öffnen im eigenen Programm (das Menü wartet nicht), Bauen läuft hier im Fenster.
Klang (!) und Verlauf stehen in .menu (kommt nicht zu GitHub). Klang: motor/klang.wav (oder klang.wav im Buchordner), sonst Piepton.
sh menu.sh verknuepfung = Starter mit Lotus auf den Schreibtisch (n → v im Menü).
"""
import glob
import os
import shlex
import shutil
import subprocess
import sys
import time
try:
    import readline                     # ↑ ↓ unter Linux und Mac (Windows kann es von sich aus)
except ImportError:
    readline = None

MOTOR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(MOTOR)
WIN, MAC = sys.platform == "win32", sys.platform == "darwin"
EINST = os.path.join(BASE, ".menu")
PURESATZ = os.path.join(os.path.dirname(BASE), "pureSATZ")
LOKAL = os.path.isdir(os.path.join(PURESATZ, "motor"))
BEFEHLE = ("schnell", "komplett", "final", "entwurf", "leseprobe", "korrektur", "nur-pdf", "nur-druck", "nur-ebook",
           "pruefen", "personen", "stand", "aenderungen", "änderungen", "geschichten", "hilfe", "mockup", "sicherung")
MD = {"b": ("Buch", "*-buch.md"), "v": ("Variablen", "*-variablen.md"), "u": ("Umschlag", "*-umschlag.md"),
      "w": ("Stichworte", "stichworte-*.txt"), "h": ("meine Hilfe", "meine-hilfe.md")}
WEG = ("check_", "_Buchblock", "_Cover", "_Umschlag", "_booklet", "_Inhalt", "_Aenderungen", "_Leseprobe", "_Korrektur",
       "_tmp")
ton = True


def einstellungen(speichern=False):
    global ton
    if speichern:
        n = readline.get_current_history_length() if readline else 0
        verlauf = [readline.get_history_item(i) for i in range(max(1, n - 49), n + 1)] if readline else []
        with open(EINST, "w", encoding="utf-8") as f:
            f.write("ton=" + ("ein" if ton else "aus") + "\n" + "".join(v + "\n" for v in verlauf if v))
    elif os.path.exists(EINST):
        zeilen = open(EINST, encoding="utf-8").read().splitlines()
        ton = not (zeilen and zeilen[0] == "ton=aus")
        for z in zeilen[1:]:
            if readline:
                readline.add_history(z)


def frage(text, merken=False):
    """Eingabe; nur Befehle im Hauptmenü kommen in den Verlauf (↑)."""
    n = readline.get_current_history_length() if readline else 0
    try:
        e = input(text).strip()
    except EOFError:
        return "q"
    if readline:
        neu = readline.get_current_history_length() > n
        merken = merken and e.lower() not in ("", "q") and (n == 0 or readline.get_history_item(n) != e)
        if neu and not merken:
            readline.remove_history_item(n)
        elif merken and not neu:
            readline.add_history(e)
    return e


def oeffnen(pfad):
    if not pfad or not os.path.exists(pfad):
        print("  Noch nicht vorhanden – zuerst bauen.")
    elif WIN:
        os.startfile(pfad)
    else:
        subprocess.Popen(["open" if MAC else "xdg-open", pfad], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def skript(name, *args, ordner=BASE, mac=None):
    """Startdateien aufrufen wie von Hand: sync, update im Buch; setup, hallo, START in ../pureSATZ."""
    if WIN:
        cmd = ["cmd", "/c", name + ".bat"]
    else:
        cmd = ["bash" if mac else "sh", (mac if MAC and mac else name + ".sh")]
    return lauf(cmd + list(args), ordner)


def bauen(*args):
    return lauf([sys.executable, os.path.join(MOTOR, "bauen.py")] + [a for a in args if a != "entwurf"])


def lauf(cmd, ordner=BASE):
    t = time.time()
    try:
        r = subprocess.run(cmd, cwd=ordner).returncode
    except KeyboardInterrupt:                   # Ctrl+C bricht nur den Befehl ab, nicht das Menü
        r = 1
    d = int(time.time() - t)
    print(("\nFertig" if r == 0 else "\nFehler – siehe Meldungen oben") + f" ({d // 60} Min. {d % 60} s)")
    klang()
    return r


def klang():
    """klang.wav im Buchordner abspielen (ohne zu warten), sonst Piepton."""
    if not ton:
        return
    wav = next((p for p in (os.path.join(BASE, "klang.wav"), os.path.join(MOTOR, "klang.wav")) if os.path.exists(p)), "")
    try:
        if os.path.exists(wav) and WIN:
            import winsound
            return winsound.PlaySound(wav, winsound.SND_FILENAME | winsound.SND_ASYNC)
        spieler = next((s for s in (["afplay"] if MAC else ["paplay", "aplay"]) if shutil.which(s)), None)
        if os.path.exists(wav) and spieler:
            return subprocess.Popen([spieler, wav], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass
    print("\a", end="", flush=True)


def pdfs():
    """Lese-PDFs, Leseprobe und Korrektur aus den Ausgabeordnern (nur was es gibt)."""
    out = {}
    for ordner in sorted(glob.glob(os.path.join(BASE, "ausgabe-*"))):
        if ordner.endswith("ausgabe-test"):
            continue
        uz = not ordner.endswith("ausgabe-normal")
        haupt = [p for p in glob.glob(os.path.join(ordner, "*.pdf")) if not any(w in os.path.basename(p) for w in WEG)]
        if not haupt:
            continue
        h = min(haupt, key=lambda p: len(os.path.basename(p)))[:-4]
        for k, n, p in (("n", "normal", h + ".pdf"), ("l", "leseprobe", h + "_Leseprobe.pdf"),
                        ("r", "korrektur", h + "_Korrektur.pdf")):
            if os.path.exists(p):
                if uz:
                    k, n = ("u", "unzensiert") if k == "n" else (k + "u", n + " uz")
                out[k] = (n, p)
    return out


def untermenue(titel, eintraege):
    """eintraege: {Taste: (Text, Pfad oder None)} – gibt die gewählte Taste zurück, None = zurück."""
    print(f"\n {titel}")
    raster([(k, t) for k, (t, _) in eintraege.items()] + [("z", "zurück")])
    e = frage(" Wahl: ").lower()
    return e if e in eintraege else None


def zeige():
    buch = next(iter(glob.glob(os.path.join(BASE, "*-buch.md"))), "Buch")
    version = open(os.path.join(MOTOR, "VERSION"), encoding="utf-8").read().strip()
    links = f" pureSATZ {version} · {os.path.basename(buch)[:-8]}"
    print("\n" + links + f"Klang (!) {'ein' if ton else 'aus'}".rjust(67 - len(links)))
    print(" " + "─" * 66)
    zeilen = [("s", "schnell"), ("k", "komplett"), ("b", "bauen …"), ("m", "MD öffnen …"),
              ("p", "PDF …"), ("o", "Ordner …"), ("g", "gegenlesen …"), ("a", "änderungen"),
              ("sy", "sync"), ("u", "update")] + ([("ul", "update lokal")] if LOKAL else []) + \
             [("n", "neu …"), ("t", "Terminal"), ("?", "Quickies"), ("h", "hilfe"), ("q", "beenden")]
    raster(zeilen)
    print(" " + "─" * 66)


def raster(zeilen):
    for i in range(0, len(zeilen), 4):
        print(("  " + "".join(f"{k:<3}{t:<14}" for k, t in zeilen[i:i + 4])).rstrip())


def quickies():
    """Befehle zum Tippen – aus dem Spickzettel der Hilfe (hilfe.py), ohne «sh build.sh» davor."""
    from hilfe import SPICKZETTEL
    liste = [(b[12:], t) for b, t in SPICKZETTEL if b.startswith("sh build.sh ") and b.split()[2] in BEFEHLE]
    liste.append(("leseprobe uz 18,20", "Leseprobe nur mit diesen Seiten, nur Unzensiert"))
    breit = max(len(b) for b, _ in liste) + 2
    rest = max(20, min(90, shutil.get_terminal_size((90, 24)).columns) - breit - 3)   # Zeile höchstens 90 Zeichen
    print("\n Quickies – im Menü tippen (ohne Menü: sh build.sh … davor)")
    for befehl, text in liste:
        print(f"  {befehl:<{breit}}{text if len(text) <= rest else text[:rest - 1] + '…'}")
    print(" Ganze Hilfe: h (hilfe.html im Browser)")
    frage(" Enter = zurück ")


def terminal():
    """Neues Terminal im Buchordner öffnen; das Menü wartet nicht."""
    if WIN:
        return subprocess.Popen(["cmd"], cwd=BASE, creationflags=subprocess.CREATE_NEW_CONSOLE)
    if MAC:
        return subprocess.Popen(["open", "-a", "Terminal", BASE])
    for t in ("x-terminal-emulator", "gnome-terminal", "konsole", "xfce4-terminal", "xterm"):
        if shutil.which(t):
            return subprocess.Popen([t], cwd=BASE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("  Kein Terminal gefunden – Rechtsklick in den Buchordner → «Im Terminal öffnen».")


def schreibtisch():
    """Schreibtisch-Ordner (Linux: xdg-user-dir, z. B. ~/Schreibtisch; Windows auch mit OneDrive)."""
    try:
        if WIN:
            return subprocess.run(["powershell", "-NoProfile", "-Command", "[Environment]::GetFolderPath('Desktop')"],
                                  capture_output=True, text=True).stdout.strip()
        if not MAC and shutil.which("xdg-user-dir"):
            return subprocess.run(["xdg-user-dir", "DESKTOP"], capture_output=True, text=True).stdout.strip()
    except OSError:
        pass
    return next((p for p in (os.path.join(os.path.expanduser("~"), d) for d in ("Desktop", "Schreibtisch"))
                 if os.path.isdir(p)), "")


def verknuepfung():
    """Starter mit Lotus, der dieses Menü öffnet: Linux .desktop (Startmenü), Windows .lnk, Mac .command."""
    name = os.path.basename(next(iter(glob.glob(os.path.join(BASE, "*-buch.md"))), "Buch-buch.md"))[:-8]
    orte = [BASE] + ([schreibtisch()] if frage(" Auch auf den Schreibtisch? [n = nein | Enter = ja]: ").lower() != "n"
                     else [])
    png, ico = (os.path.join(MOTOR, "bilder", f) for f in ("lotus.png", "lotus.ico"))
    if not WIN and not MAC:                    # Linux: Startmenü statt Buchordner (dort startet .desktop nicht)
        orte[0] = os.path.join(os.path.expanduser("~"), ".local", "share", "applications")
    for ort in orte:
        if not ort or not os.path.isdir(ort):
            print("  Schreibtisch nicht gefunden – Starter nur im Buchordner bzw. Startmenü.")
            continue
        if WIN:
            p, q = os.path.join(ort, f"{name} Menü.lnk"), lambda s: s.replace("'", "''")
            subprocess.run(["powershell", "-NoProfile", "-Command",
                            f"$s=(New-Object -ComObject WScript.Shell).CreateShortcut('{q(p)}');"
                            f"$s.TargetPath='{q(os.path.join(BASE, 'menu.bat'))}';$s.WorkingDirectory='{q(BASE)}';"
                            f"$s.IconLocation='{q(ico)}';$s.Save()"])
        else:
            p = os.path.join(ort, f"{name} Menü.command" if MAC else f"puresatz-{name}.desktop")
            with open(p, "w", encoding="utf-8") as f:
                f.write(f'#!/bin/sh\ncd "{BASE}" && exec sh menu.sh\n' if MAC else
                        f'[Desktop Entry]\nType=Application\nName={name} Menü\nComment=pureSATZ-Menü für {name}\n'
                        f'Exec=sh "{os.path.join(BASE, "menu.sh")}"\nPath={BASE}\nIcon={png}\nTerminal=true\n')
            os.chmod(p, 0o755)
            hilfe = (["osascript", "-l", "JavaScript", "-e", 'ObjC.import("AppKit");$.NSWorkspace.sharedWorkspace'
                      f'.setIconForFileOptions($.NSImage.alloc.initWithContentsOfFile({png!r}),{p!r},0)'] if MAC
                     else ["gio", "set", p, "metadata::trusted", "true"])
            if shutil.which(hilfe[0]):
                subprocess.run(hilfe, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"  Starter: {p}")
    if not WIN and not MAC and len(orte) > 1:
        print("  Schreibtisch: beim ersten Mal Rechtsklick auf das Lotus-Icon → «Start erlauben».")


def main():
    global ton
    if sys.argv[1:2] == ["verknuepfung"]:
        return verknuepfung()
    einstellungen()
    while True:
        zeige()
        print(" Wahl oder Befehl (z. B. final · ↑ = letzte):")
        e = frage(" Eingabe: ", merken=True)
        w = e.lower()
        if w in ("", "z"):
            continue
        if w == "q":
            break
        if w == "s":
            bauen("schnell")
        elif w == "k":
            bauen("komplett")
        elif w == "b":
            k = untermenue("bauen …", {"l": ("leseprobe", 0), "r": ("korrektur", 0), "n": ("nur-pdf", 0),
                                       "e": ("nur-ebook", 0), "pr": ("pruefen", 0), "st": ("Stand merken", 0)})
            if k == "st":
                name = frage(" Name des Stands: ")
                bauen("stand", *([name] if name else []))
            elif k:
                bauen({"l": "leseprobe", "r": "korrektur", "n": "nur-pdf", "e": "nur-ebook", "pr": "pruefen"}[k])
        elif w == "m":
            md = {k: (t, next(iter(sorted(glob.glob(os.path.join(BASE, m)))), None)) for k, (t, m) in MD.items()}
            k = untermenue("MD öffnen …", {k: v for k, v in md.items() if v[1]})
            if k:
                oeffnen(md[k][1])
        elif w == "p":
            liste = pdfs()
            if not liste:
                print("  Noch kein PDF – zuerst bauen (s).")
            elif len(liste) == 1:
                oeffnen(next(iter(liste.values()))[1])
            else:
                k = untermenue("PDF …", liste)
                if k:
                    oeffnen(liste[k][1])
        elif w == "o":
            ordner = {k: (t, os.path.join(BASE, d)) for k, t, d in (("b", "Buchordner", ""), ("n", "normal", "ausgabe-normal"),
                      ("u", "unzensiert", "ausgabe-unzensiert"), ("d", "druck", "druck"))}
            k = untermenue("Ordner …", {k: v for k, v in ordner.items() if os.path.isdir(v[1])})
            if k:
                oeffnen(ordner[k][1])
        elif w == "g":
            k = untermenue("gegenlesen …", {"l": ("Liste neu", 0), "c": ("check-PDF …", 0), "t": ("Textdatei", 0)})
            if k == "l":
                bauen("personen")
            elif k == "t":
                oeffnen(os.path.join(BASE, "personen-seiten.txt"))
            elif k == "c":
                name, seit = frage(" Name: "), time.time()
                if name and bauen("personen", name) == 0:
                    for p in glob.glob(os.path.join(BASE, "ausgabe-*", f"check_{name}_*.pdf")):
                        if os.path.getmtime(p) >= seit - 1:
                            oeffnen(p)
        elif w == "a":
            seit = time.time()
            if bauen("aenderungen") == 0:
                neu = [p for p in glob.glob(os.path.join(BASE, "ausgabe-*", "*_Aenderungen.pdf"))
                       if os.path.getmtime(p) >= seit - 1]
                for p in neu:
                    oeffnen(p)
        elif w == "sy":
            skript("sync")
        elif w in ("u", "ul"):
            if skript("update", *(["lokal"] if w == "ul" else [])) == 0:
                einstellungen(speichern=True)
                if WIN:                                                  # neues Menü laden
                    sys.exit(subprocess.call([sys.executable, os.path.abspath(__file__)]))
                os.execv(sys.executable, [sys.executable, os.path.abspath(__file__)])
        elif w == "!":
            ton = not ton
            print(f"  Klang {'ein' if ton else 'aus'}")
            klang()                                   # Probe beim Einschalten
        elif w == "t":
            terminal()
        elif w == "?":
            quickies()
        elif w == "n":
            neu = {"b": ("neues Buch", 0), "h": ("Hallo-Buch", 0), "e": ("einrichten", 0)} if LOKAL else {}
            k = untermenue("neu …", {**neu, "v": ("Verknüpfung", 0)})
            if k == "v":
                verknuepfung()
            elif k:
                vorher = set(os.listdir(os.path.dirname(BASE)))
                {"b": lambda: skript(os.path.join("setup", "setup"), ordner=PURESATZ),
                 "h": lambda: skript("hallo", ordner=PURESATZ),
                 "e": lambda: skript("START-Windows" if WIN else "START-Linux", ordner=PURESATZ,
                                     mac="START-Mac.command")}[k]()
                for d in sorted(set(os.listdir(os.path.dirname(BASE))) - vorher):
                    print(f"  Neues Buch: ../{d} – dort sh menu.sh")
        elif w == "h":
            bauen("hilfe")
        elif w.split()[0] in ("xdg-open", "open", "start"):   # wie im Terminal: Datei öffnen, ohne zu warten
            for teil in shlex.split(e, posix=not WIN)[1:]:
                oeffnen(os.path.join(BASE, os.path.expanduser(teil.strip('"'))))
        elif w.split()[0] in BEFEHLE:          # ganzer Befehl: final · leseprobe uz 18,20 · personen Eltern
            bauen(*e.split())
        else:
            print(f"  Unbekannt: {e}")
        einstellungen(speichern=True)
    einstellungen(speichern=True)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
