#!/usr/bin/env python3
"""
menu.py – Menü mit den häufigsten Befehlen (ab 2.50, Buchstaben 2.51). Aufruf im Buchordner: sh menu.sh (Windows: menu.bat)

Ein Buchstabe pro Befehl, m / g / t / c / w / p / o / n mit Untermenü; Geschichten mit festem Kürzel (g → e). ↑ ↓ = letzte Eingaben, Enter = zurück, q = beenden.
Ganze Befehle gehen auch: final · leseprobe uz 18,20 · personen Eltern.
MD, PDF und Ordner öffnen im eigenen Programm (das Menü wartet nicht), Bauen läuft hier im Fenster.
Klang (!) und Verlauf stehen in .menu (kommt nicht zu GitHub). Klang: motor/klang.wav (oder klang.wav im Buchordner), sonst Piepton.
sh menu.sh verknuepfung = Starter mit Lotus auf den Schreibtisch (n → v im Menü).
"""
import glob
import os
import re
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
      "s": ("Stichworte", "stichworte-*.txt"), "h": ("meine Hilfe", "meine-hilfe.md")}
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


def lauf(cmd, ordner=BASE, env=None):
    t = time.time()
    try:
        r = subprocess.run(cmd, cwd=ordner, env=env).returncode
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
                        ("k", "korrektur", h + "_Korrektur.pdf")):
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
    e = "ü" if e == "u" and "ü" in eintraege and "u" not in eintraege else e      # ohne ü-Taste
    return e if e in eintraege else None


def kuerzel(alle=None, datei=None):
    """{Kürzel: (name, pfad)} aller Geschichten (oder Tabellen). Kürzel bleiben fest (…/kuerzel.txt), frei
    gewordene werden wieder vergeben. Neues Kürzel: h · he · hig (Anfänge der Wörter) · hei · …"""
    if alle is None:
        try:
            import geschichten as G
            alle = G.alle(BASE)
        except (ImportError, SystemExit) as f:
            print(f"  {f}")
            return {}
        datei = os.path.join(BASE, "geschichten", "kuerzel.txt")
    alt = {}
    if os.path.exists(datei):
        for z in open(datei, encoding="utf-8").read().splitlines():
            t = z.split(None, 1)
            if len(t) == 2 and not z.startswith("#") and t[0] not in alt.values():
                alt[t[1].strip()] = t[0].lower()
    km = {n: k for n, k in alt.items() if n in alle}
    vergeben = set(km.values()) | {"z"}
    for n in sorted(alle, key=lambda n: os.path.getmtime(alle[n])):      # neue: wie angelegt
        if n not in km:
            w = [x for x in re.split(r"[^a-zäöüß]+", n.lower()) if x] or ["g"]
            a = "".join(w)
            kand = [a[:1], a[:2], "".join(x[0] for x in w)[:3], a[:3]] + [a[0] + c for c in a[1:]]
            km[n] = next((k for k in kand if k not in vergeben),
                         next(f"{a[0]}{i}" for i in range(1, 999) if f"{a[0]}{i}" not in vergeben))
            vergeben.add(km[n])
    if km != alt:
        with open(datei, "w", encoding="utf-8") as f:
            f.write("# Kürzel fürs Menü (… → e). Bleiben fest, von Hand änderbar.\n"
                    + "".join(f"{k:<4}{n}\n" for n, k in km.items()))
    return {k: (n, alle[n]) for n, k in km.items()}


def geschichte_oeffnen():
    import geschichten as G
    ks = kuerzel()
    if not ks:
        print("  Noch keine Geschichte – g → n.")
        return
    if os.path.exists(ALLE):
        return print(SPERRE)
    nach, drin = {n: k for k, (n, _) in ks.items()}, {n for _, n in G.verweise(buchdatei())}
    print("\n Geschichte öffnen …")
    for n in G.reihe(BASE, buchdatei()):
        titel, kopf, _ = G.lies(ks[nach[n]][1])
        print(f"  {nach[n]:<4}{titel[:40]:<42}{G.stand(kopf):<14}{'' if n in drin else 'nicht im Buch'}".rstrip())
    print("  z   zurück")
    e = frage(" Wahl: ").lower()
    if e in ks:
        oeffnen(ks[e][1])


ALLE = os.path.join(BASE, "geschichten-alle.md")
DEMO = "Dieses Demo-Kapitel zeigt alle Möglichkeiten"
SPERRE = "  ⚠ Alle Geschichten liegen in geschichten-alle.md – zuerst g → a zurückholen."


def buchdatei():
    return next(iter(glob.glob(os.path.join(BASE, "*-buch.md"))), None)


def einordnen(extra=None):
    """g → b: fehlende Geschichten als @@-Zeilen in den Block «## Noch einordnen» (Buch-Reihenfolge bleibt).
    extra = eigene Zeilen statt Geschichten, z. B. ["@#preise"] nach t → n."""
    import geschichten as G
    buch, kopf = buchdatei(), "## Noch einordnen"
    v = G.verweise(buch)
    fehlt = extra or ["@@" + n for n in G.reihe(BASE, buch) if n not in {n for _, n in v}]
    if not buch or not fehlt:
        return print("  Alle Geschichten sind im Buch.")
    z = open(buch, encoding="utf-8").read().split("\n")
    s = [x.strip() for x in z]
    neu = sum((["", x] for x in fehlt), [])
    demo = not extra and DEMO in "\n".join(z) and "## Vorwort" in s and any(x.startswith("# ") and "anhang" in x.lower() for x in s)
    if demo and frage(" Das Buch enthält noch den Demo-Inhalt. Durch deine Geschichten ersetzen? "
                      "[j = ja | Enter = nein] ").lower() == "j":
        bauen("sicherung")
        if "## Ein Teil mit eigenem Bild" in s:                  # Beispielkapitel im Anhang
            b = s.index("## Ein Teil mit eigenem Bild")
            del z[b:next((i for i in range(b + 1, len(s)) if s[i].startswith("#")), len(s))]
            s = [x.strip() for x in z]
        a = next(i for i, x in enumerate(s) if x.startswith("# ") and "anhang" in x.lower())
        z[s.index("## Vorwort"):a] = ["## Vorwort", "", "Hier kommt dein Vorwort.", "", "# Teil 1|Geschichten|"] + neu + [""]
        open(buch, "w", encoding="utf-8").write("\n".join(z))
        return print("  Demo-Inhalt ersetzt durch: " + ", ".join(fehlt) + "\n  → ansehen: s schnell, dann p")
    bauen("sicherung")
    if kopf in s:                                   # Block gibt es schon: hinten anhängen
        k = s.index(kopf)
        ende = next((i for i in range(k + 1, len(s)) if s[i].startswith("#")), len(s))
        pos = max([i + 1 for i in range(k + 1, ende) if s[i].startswith(("@@", "@#"))] or [k + 1])
    else:                                           # nach der letzten @@-Zeile, sonst vor den Anhang, sonst ans Ende
        pos = v[-1][0] if v else next((i for i, x in enumerate(s) if x.startswith("# ") and "anhang" in x.lower()), len(s))
        pos += 1 if v and pos < len(s) and s[pos] == ":::" else 0          # nicht in einen ::: nur-uz-Block
        neu = ["", kopf] + neu + ([""] if not v and pos < len(s) else [])
    z[pos:pos] = neu
    open(buch, "w", encoding="utf-8").write("\n".join(z))
    print(f"  Ins Buch (ab Zeile {pos + 2}, «{kopf}»): " + ", ".join(fehlt) + "\n  → ansehen: s schnell, dann p")


def tabellen_menue():
    """g → t / m → t: Tabellen bearbeiten, neu anlegen, Ordner – wie bei den Geschichten."""
    ordner = os.path.join(BASE, "tabellen")
    liste = lambda: {os.path.basename(p)[:-4]: p for p in sorted(glob.glob(os.path.join(ordner, "*.csv")))}
    datei = os.path.join(ordner, "kuerzel.txt")
    k = untermenue("Tabellen …", {"e": ("bearbeiten …", 0), "n": ("neue Tabelle", 0), "o": ("Ordner", 0)})
    if k == "e":
        ks = kuerzel(liste(), datei)
        if not ks:
            return print("  Noch keine Tabelle – n.")
        print("\n Tabelle öffnen …")
        for kz, (n, _) in ks.items():
            print(f"  {kz:<4}{n}")
        print("  z   zurück")
        e = frage(" Wahl: ").lower()
        if e in ks:
            oeffnen(ks[e][1])
    elif k == "n":
        titel, vorher = frage(" Titel: "), set(liste())
        if titel and skript("neu", "tabelle", titel) == 0:
            for kz, (n, p) in kuerzel(liste(), datei).items():
                if n not in vorher:
                    print(f"  Kürzel {kz}: {n}")
                    einordnen([f"@#{n}"])
                    oeffnen(p)
    elif k == "o":
        os.makedirs(ordner, exist_ok=True)
        oeffnen(ordner)


def alle_in_einer_datei():
    """g → a: alle Geschichten in geschichten-alle.md – beim zweiten Mal zurück in die Einzeldateien."""
    import geschichten as G
    alle = G.alle(BASE)
    if not os.path.exists(ALLE):
        if not alle:
            return print("  Noch keine Geschichte – g → n.")
        with open(ALLE, "w", encoding="utf-8") as f:
            f.write("> Alle Geschichten in einer Datei. Text frei ändern – die Zeilen «@@@ name» nicht ändern.\n"
                    "> Zurück in die Einzeldateien: Menü g → a.\n\n"
                    + "".join(f"@@@ {n}\n{open(alle[n], encoding='utf-8').read().strip()}\n\n" for n in G.reihe(BASE, buchdatei())))
        print("  geschichten-alle.md geschrieben – Einzeldateien sind gesperrt, bis g → a zurückholt.")
        return oeffnen(ALLE)
    bauen("sicherung")
    teile = re.split(r"^@@@ *(\S+) *$", open(ALLE, encoding="utf-8").read(), flags=re.M)
    namen, geaendert = teile[1::2], []
    for n, text in zip(namen, teile[2::2]):
        if n in alle and text.strip() != open(alle[n], encoding="utf-8").read().strip():
            open(alle[n], "w", encoding="utf-8").write(text.strip() + "\n")
            geaendert.append(n)
    os.makedirs(os.path.join(BASE, "md-history"), exist_ok=True)
    os.replace(ALLE, os.path.join(BASE, "md-history", f"geschichten-alle_{time.strftime('%Y%m%d-%H-%M-%S')}.md"))
    print("  Zurückgeholt, geändert: " + (", ".join(geaendert) or "keine"))
    for text, liste in (("nicht in der Datei, unverändert", [n for n in alle if n not in namen]),
                        ("unbekannt, nicht übernommen", [n for n in namen if n not in alle])):
        if liste:
            print(f"  ⚠ {text}: " + ", ".join(liste))


def zeige():
    buch = next(iter(glob.glob(os.path.join(BASE, "*-buch.md"))), "Buch")
    version = open(os.path.join(MOTOR, "VERSION"), encoding="utf-8").read().strip()
    links = f" pureSATZ {version} · {os.path.basename(buch)[:-8]}"
    print("\n" + links + f"Klang (!) {'ein' if ton else 'aus'}".rjust(68 - len(links)))
    spalten = [("Schreiben", [("m", "MD öffnen …"), ("g", "Geschichten …"), ("t", "Tabellen …"),
                             ("c", "check / gegenlesen …")]),
               ("Bauen", [("s", "schnell  (Lese-PDF)"), ("k", "komplett (vor dem Druck)"), ("w", "weitere …")]),
               ("Ansehen", [("p", "PDF öffnen …"), ("o", "Ordner öffnen …"), ("a", "änderungen")]),
               ("Abgleichen", [("sy", "sync   (GitHub)"), ("u", "update" + (" (ul lokal)" if LOKAL else ""))])]
    for (t1, z1), (t2, z2) in (spalten[:2], spalten[2:]):
        print(f" ── {t1} " + "─" * (30 - len(t1)) + f"   ── {t2} " + "─" * (30 - len(t2)))
        for a, b in zip(z1 + [("", "")] * 3, z2 + [("", "")] * 3):
            if a[0] or b[0]:
                print(f"  {a[0]:<3}{a[1]:<33}{b[0]:<3}{b[1]}".rstrip())
    print(" ── Weiteres:  n neu · > Terminal · : Befehle · h hilfe · ! Klang · q beenden")
    if os.path.exists(ALLE):
        print(SPERRE)


def raster(zeilen):
    b = max(16, max(len(t) for _, t in zeilen) + 2)                     # Spalten so breit wie der längste Text
    for i in range(0, len(zeilen), 4 if b <= 16 else 3):
        print(("  " + "".join(f"{k:<3}{t:<{b}}" for k, t in zeilen[i:i + (4 if b <= 16 else 3)])).rstrip())


def befehle():
    """: Befehle zum Tippen – aus dem Spickzettel der Hilfe (hilfe.py); die Eingabe geht danach direkt ans Menü."""
    from hilfe import SPICKZETTEL
    liste = [(b[12:], t) for b, t in SPICKZETTEL if b.startswith("sh build.sh ") and b.split()[2] in BEFEHLE]
    liste.append(("leseprobe uz 18,20", "Leseprobe nur mit diesen Seiten, nur Unzensiert"))
    breit = max(len(b) for b, _ in liste) + 2
    rest = max(20, min(90, shutil.get_terminal_size((90, 24)).columns) - breit - 3)   # Zeile höchstens 90 Zeichen
    print("\n Befehle – hier tippen (ohne Menü: sh build.sh … davor)")
    for befehl, text in liste:
        print(f"  {befehl:<{breit}}{text if len(text) <= rest else text[:rest - 1] + '…'}")
    print(" Ganze Hilfe: h (hilfe.html im Browser)")
    return frage(" Eingabe (Enter = zurück): ", merken=True)


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
    naechste = ""
    while True:
        if naechste:                                  # Eingabe aus «: Befehle»
            e, naechste = naechste, ""
        else:
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
        elif w == "w":
            k = untermenue("weitere …", {"l": ("Leseprobe", 0), "k": ("Korrektur", 0), "p": ("nur-pdf", 0),
                                         "e": ("nur E-Book", 0), "c": ("prüfen", 0), "s": ("Stand merken", 0)})
            if k == "s":
                name = frage(" Name des Stands: ")
                bauen("stand", *([name] if name else []))
            elif k:
                bauen({"l": "leseprobe", "k": "korrektur", "p": "nur-pdf", "e": "nur-ebook", "c": "pruefen"}[k])
        elif w == "m":
            md = {k: (t, next(iter(sorted(glob.glob(os.path.join(BASE, m)))), None)) for k, (t, m) in MD.items()}
            if os.path.isdir(os.path.join(BASE, "geschichten")):
                md["g"] = ("Geschichten …", "g")
            md["t"] = ("Tabellen …", "t")
            k = untermenue("MD öffnen …", {k: v for k, v in md.items() if v[1]})
            if k == "g":
                geschichte_oeffnen()
            elif k == "t":
                tabellen_menue()
            elif k:
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
                      ("u", "unzensiert", "ausgabe-unzensiert"), ("d", "druck", "druck"), ("g", "geschichten", "geschichten"),
                      ("t", "tabellen", "tabellen"))}
            k = untermenue("Ordner …", {k: v for k, v in ordner.items() if os.path.isdir(v[1])})
            if k:
                oeffnen(ordner[k][1])
        elif w == "g":
            k = untermenue("Geschichten …", {"e": ("schreiben …", 0), "n": ("neue Geschichte", 0),
                                             "b": ("fehlende ins Buch", 0),
                                             "a": ("alle zurückholen" if os.path.exists(ALLE) else "alle in 1 Datei", 0),
                                             "s": ("Sammel-PDF", 0), "ü": ("Übersicht", 0)})
            if k and k != "a" and os.path.exists(ALLE):
                print(SPERRE)
            elif k == "a":
                alle_in_einer_datei()
            elif k == "b":
                einordnen()
            elif k == "e":
                geschichte_oeffnen()
            elif k == "n":
                titel = frage(" Titel: ")
                vorher = {p for _, p in kuerzel().values()}
                if titel and skript("neu", titel) == 0:
                    for kz, (n, p) in kuerzel().items():
                        if p not in vorher:
                            print(f"  Kürzel {kz}: {n}  → ins Buch: g → b")
                            oeffnen(p)
            elif k == "ü":
                if skript("neu") == 0:
                    oeffnen(os.path.join(BASE, "geschichten-uebersicht.html"))
            elif k == "s":
                bauen("geschichten")
        elif w == "c":
            k = untermenue("check / gegenlesen …", {"n": ("Liste neu", 0), "c": ("check-PDF …", 0), "t": ("Textdatei", 0)})
            if k == "n":
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
            tabellen_menue()
        elif w == ">":
            terminal()
        elif w == ":":
            naechste = befehle()
        elif w == "n":
            neu = {"b": ("neues Buch", 0), "h": ("Hallo-Buch", 0), "e": ("einrichten", 0),
                   "m": ("Motor-Selbsttest", 0)} if LOKAL else {}
            k = untermenue("neu …", {**neu, "v": ("Verknüpfung", 0)})
            if k == "v":
                verknuepfung()
            elif k:
                vorher = set(os.listdir(os.path.dirname(BASE)))
                {"b": lambda: skript(os.path.join("setup", "setup"), ordner=PURESATZ),
                 "h": lambda: skript("hallo", ordner=PURESATZ),
                 "m": lambda: lauf([sys.executable, os.path.join("test", "selbsttest.py")], PURESATZ,
                                   dict(os.environ, SELBSTTEST_OHNE_VENV="1")),
                 "e": lambda: skript("START-Windows" if WIN else "START-Linux", ordner=PURESATZ,
                                     mac="START-Mac.command")}[k]()
                for d in sorted(set(os.listdir(os.path.dirname(BASE))) - vorher):
                    print(f"  Neues Buch: ../{d} – dort sh menu.sh")
        elif w in ("h", "?"):
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
