#!/usr/bin/env python3
"""
menu.py – Menü mit den häufigsten Befehlen (ab 2.50, Buchstaben 2.51). Aufruf im Buchordner: sh menu.sh (Windows: menu.bat)

Ein Buchstabe pro Befehl, b / m / p / o / g mit Untermenü. ↑ ↓ = letzte Eingaben, Enter = zurück, q = beenden.
Ganze Befehle gehen auch: final · leseprobe uz 18,20 · personen Eltern.
MD, PDF und Ordner öffnen im eigenen Programm (das Menü wartet nicht), Bauen läuft hier im Fenster.
Ton und Verlauf stehen in .menu (kommt nicht zu GitHub). Klang: klang.wav im Buchordner, sonst Piepton.
"""
import glob
import os
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
LOKAL = os.path.isdir(os.path.join(os.path.dirname(BASE), "pureSATZ", "motor"))
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


def skript(name, *args):
    """sync / update über die Startdateien des Buchs (wie von Hand)."""
    cmd = ["cmd", "/c", name + ".bat"] if WIN else ["sh", name + ".sh"]
    return lauf(cmd + list(args))


def bauen(*args):
    return lauf([sys.executable, os.path.join(MOTOR, "bauen.py")] + [a for a in args if a != "entwurf"])


def lauf(cmd):
    t = time.time()
    try:
        r = subprocess.run(cmd, cwd=BASE).returncode
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
    wav = os.path.join(BASE, "klang.wav")
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
    print("\n" + links + f"Ton {'ein' if ton else 'aus'}".rjust(67 - len(links)))
    print(" " + "─" * 66)
    zeilen = [("s", "schnell"), ("k", "komplett"), ("b", "bauen …"), ("m", "MD öffnen …"),
              ("p", "PDF …"), ("o", "Ordner …"), ("g", "gegenlesen …"), ("a", "änderungen"),
              ("sy", "sync"), ("u", "update")] + ([("ul", "update lokal")] if LOKAL else []) + \
             [("t", "Ton ein/aus"), ("h", "hilfe"), ("q", "beenden")]
    raster(zeilen)
    print(" " + "─" * 66)


def raster(zeilen):
    for i in range(0, len(zeilen), 4):
        print(("  " + "".join(f"{k:<3}{t:<14}" for k, t in zeilen[i:i + 4])).rstrip())


def main():
    global ton
    einstellungen()
    while True:
        zeige()
        e = frage(" Wahl (↑ = letzte Befehle): ", merken=True)
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
        elif w == "t":
            ton = not ton
            print(f"  Ton {'ein' if ton else 'aus'}")
        elif w == "h":
            bauen("hilfe")
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
