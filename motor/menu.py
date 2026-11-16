#!/usr/bin/env python3
"""
menu.py – Menü mit den häufigsten Befehlen (ab 2.50, Buchstaben 2.51). Aufruf im Buchordner: sh menu.sh (Windows: menu.bat)

Ein Buchstabe pro Befehl, m / g / t / c / w / p / o / n mit Untermenü; Geschichten mit festem Kürzel (g → e). ↑ ↓ = letzte Eingaben, Enter (oder z) = zurück (im Hauptmenü: beenden? [j/N]).
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
LINUX = sys.platform.startswith("linux")                       # Hörbuch (hb) vorerst nur unter Linux
FARBIG = not WIN and sys.stdout.isatty()                           # Farben/fett nur im echten Terminal (Linux/Mac)
FETT = (lambda t: f"\033[1;38;5;178m{t}\033[0m") if FARBIG else (lambda t: t)   # Bereich / Titel: fett, Gold
HELL = (lambda t: f"\033[1;97m{t}\033[0m") if FARBIG else (lambda t: t)          # Buchname: fett, weiss
GRAU = (lambda t: f"\033[38;5;244m{t}\033[0m") if FARBIG else (lambda t: t)      # Trennlinien: gedämpft
GRUEN = (lambda t: f"\033[38;5;108m{t}\033[0m") if FARBIG else (lambda t: t)    # ✓ nach einem Lauf (gedämpft, 2.82.3)
ROT = (lambda t: f"\033[38;5;167m{t}\033[0m") if FARBIG else (lambda t: t)      # ✗ Fehler (gedämpft, 2.82.3)
GOLDFEIN = (lambda t: f"\033[38;5;136m{t}\033[0m") if FARBIG else (lambda t: t)  # Linien um einen Lauf: fein, dunkleres Gold
SCHILD = (lambda t: f"\033[1;38;5;234;48;5;178m {t} \033[0m") if FARBIG else (lambda t: t)   # Buchname: goldenes Schild (2.69.19)
zuletzt = ""                                                                   # letzte Eingabe (für die Startlinie)
RAND = 71                                                                      # rechter Rand von Kopfzeile, Linien, «Weiteres»


class Beenden(Exception):
    """z im Hauptmenü (oder q, Strg+C): Menü ganz beenden (nach Rückfrage)."""


def beenden_frage():
    """Vor dem Beenden fragen; Enter = nein (ein z zu viel schadet nicht)."""
    try:
        a = frage(" Menü beenden? [j/N]: ").lower()
    except KeyboardInterrupt:
        return True
    return a in ("j", "ja", "q")                      # «q» kommt auch bei Eingabe-Ende (EOF)


def kurzname(n, laenge=24):
    """Buchname für die Kopfzeile, zu lange gekürzt («Mein-sehr-langer-Buchtit…»)."""
    return n if len(n) <= laenge else n[:laenge - 1] + "…"


def fenstertitel(text):
    """Titel des Terminalfensters/Tabs = Buchname (2.69.19), damit man bei mehreren Büchern das richtige findet."""
    try:
        if WIN:
            import ctypes
            ctypes.windll.kernel32.SetConsoleTitleW(text)
        elif sys.stdout.isatty():
            sys.stdout.write(f"\033]0;{text}\007"); sys.stdout.flush()
    except Exception:
        pass


def kopf(bereich="", rechts=""):
    """Kopfzeile: «══ [Leben123] · pureSATZ 2.69.19 › Hörbuch     rechts ══» (Buchname als goldenes Schild, Version grau,
    Bereich fett, ══ gold = hier beginnt das Menü)."""
    buch = next(iter(glob.glob(os.path.join(BASE, "*-buch.md"))), "Buch-buch.md")
    version = open(os.path.join(MOTOR, "VERSION"), encoding="utf-8").read().strip()
    name = kurzname(os.path.basename(buch)[:-8])
    fenstertitel(f"{name} – pureSATZ")
    links = f" {SCHILD(name)} · pureSATZ {version}" + (f" › {bereich}" if bereich else "")
    links = links.replace(SCHILD(name), f" {name} " if FARBIG else name)      # sichtbare Länge (ohne Farbcodes)
    zeile = (GOLDFEIN("══") + f" {SCHILD(name)} " + GRAU(f"· pureSATZ {version}")
             + (f" › {FETT(bereich)}" if bereich else ""))
    sichtbar = len(re.sub(r"\033\[[0-9;]*m", "", rechts))                       # rechts darf Farben haben (Klang (!))
    return zeile + " " * max(2, 66 - len(links) - sichtbar) + rechts + " " + GOLDFEIN("══")   # endet bei Spalte 71 (RAND)
EINST = os.path.join(BASE, ".menu")
sys.path.insert(0, MOTOR)
import plattform                        # noqa: E402
PURESATZ = plattform.puresatz(BASE)    # ../pureSATZ oder ../../pureSATZ (z. B. buecher/Buch)
LOKAL = os.path.isdir(os.path.join(PURESATZ, "motor"))
BEFEHLE = ("cover-stand", "schnell", "komplett", "final", "entwurf", "leseprobe", "korrektur", "nur-pdf", "nur-druck", "nur-ebook", "covers", "isbn",
           "pruefen", "personen", "stichworte", "stand", "aenderungen", "änderungen", "geschichten", "hilfe", "mockup", "sicherung")
MD = {"b": ("Buch", "*-buch.md"), "v": ("Variablen", "*-variablen.md"), "u": ("Umschlag", "*-umschlag.md"),
      "s": ("Stichworte", "stichworte-*.txt"), "h": ("meine Hilfe", "meine-hilfe.md")}
WEG = ("check_", "_Buchblock", "_Cover", "_Umschlag", "_booklet", "_Inhalt", "_Aenderungen", "_Leseprobe", "_Korrektur",
       "_tmp")
ton = True
gelaufen = False                       # hat der letzte Menüpunkt etwas ausgeführt (Meldungen stehen lassen)?
INITIAL_VERLAUF = []                   # ↑ ↓ im Initialen-Menü (2.82.16), in EINST als «in:…»


def einstellungen(speichern=False):
    global ton
    if speichern:
        n = readline.get_current_history_length() if readline else 0
        verlauf = [readline.get_history_item(i) for i in range(max(1, n - 49), n + 1)] if readline else []
        with open(EINST, "w", encoding="utf-8") as f:
            f.write("ton=" + ("ein" if ton else "aus") + "\n" + "".join(v + "\n" for v in verlauf if v)
                    + "".join("in:" + v + "\n" for v in INITIAL_VERLAUF[-20:]))
    elif os.path.exists(EINST):
        zeilen = open(EINST, encoding="utf-8").read().splitlines()
        ton = not (zeilen and zeilen[0] == "ton=aus")
        for z in zeilen[1:]:
            if z.startswith("in:"):
                INITIAL_VERLAUF.append(z[3:])
            elif readline:
                readline.add_history(z)


def frage(text, merken=False):
    """Eingabe; nur Befehle im Hauptmenü kommen in den Verlauf (↑)."""
    global zuletzt
    n = readline.get_current_history_length() if readline else 0
    if FARBIG:                                        # › gold, «Eingabe»/«Wahl» gold; \001 \002 = für readline unsichtbar
        g = lambda t: f"\001\033[1;38;5;178m\002{t}\001\033[0m\002"
        wort = next((w for w in ("Eingabe", "Wahl") if text.startswith(" " + w)), "")
        text = " " + g("›") + " " + (g(wort) + text[len(wort) + 1:] if wort else text[1:])
    try:
        e = input(text).strip()
    except EOFError:
        return "q"
    zuletzt = e or zuletzt
    if readline:
        neu = readline.get_current_history_length() > n
        merken = merken and e.lower() not in ("", "q") and (n == 0 or readline.get_history_item(n) != e)
        if neu and not merken:
            readline.remove_history_item(n)
        elif merken and not neu:
            readline.add_history(e)
    return e


def frage_verlauf(text, verlauf):
    """Eingabe mit eigenem Verlauf (↑ ↓ nur Eingaben dieses Untermenüs); danach gilt wieder der Hauptmenü-Verlauf."""
    haupt = [readline.get_history_item(i) for i in range(1, readline.get_current_history_length() + 1)] if readline else []
    if readline:
        readline.clear_history()
        for v in verlauf:
            readline.add_history(v)
    try:
        e = frage(text)
    finally:
        if readline:
            readline.clear_history()
            for v in haupt:
                readline.add_history(v)
    if e and e.lower() != "q" and (not verlauf or verlauf[-1] != e):
        verlauf.append(e)
        del verlauf[:-20]
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


def hb_stimme(args):
    """Für die Startlinie eines Hörbuch-Laufs: « · Ollie · F0» (nur wo Azure spricht)."""
    if not args or args[0] in ("texte", "paket", "hoerprobe", "liste", "pruefen", "schluessel", "stufe", "hilfe"):
        return ""
    try:
        import hoerbuch as H
        c = H.konf()
    except Exception:
        return ""
    st = c.get("AZURE_STIMME", "1")
    for a in args[1:]:
        if a.startswith("stimme="):
            st = a[7:]
        elif args[0] == "probe" and (a in ("1", "2") or a.count("-") >= 2) and not a.endswith("%"):
            st = a
    voll = c.get("AZURE_FAVORIT" + st, st) if st in ("1", "2") else st
    kurz = "-".join(voll.split("-")[2:]).replace("MultilingualNeural", "").replace("Neural", "") or voll
    return f" · {kurz} · {H.stufe_jetzt()}"


def lauf(cmd, ordner=BASE, env=None, titel=None):
    global gelaufen
    gelaufen, t = True, time.time()
    breit = min(RAND - 1, shutil.get_terminal_size((80, 24)).columns - 2)   # endet bei Spalte 71 wie Menü und Kopfzeile
    linie = lambda vorne, n: " " + GOLDFEIN("── ") + vorne + " " + GOLDFEIN("─" * max(3, breit - n))
    name = "hb " + " ".join(cmd[2:]) + hb_stimme(cmd[2:]) if cmd[1:2] and cmd[1].endswith("hoerbuch.py") else titel or zuletzt
    print(linie(FETT(name), len(name) + 4))           # Startlinie: ── sy ─────
    try:
        r = subprocess.run(cmd, cwd=ordner, env=env).returncode
    except KeyboardInterrupt:                   # Ctrl+C bricht nur den Befehl ab, nicht das Menü
        r = 1
    d = int(time.time() - t)
    zeit = f" · {d // 60} Min. {d % 60} s"
    text = (GRUEN("✓") + GOLDFEIN(" Fertig" + zeit)) if r == 0 else (ROT("✗ Fehler – siehe oben") + GOLDFEIN(zeit))
    print(linie(text, len(zeit) + (12 if r == 0 else 25)) + "\n")   # Schlusslinie, dann Leerzeile
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


def untermenue(titel, eintraege, zusatz=""):
    """eintraege: {Taste: (Text, Pfad oder None)} – gibt die gewählte Taste zurück, None = zurück.
    zusatz: z. B. "tp" – dann geht auch Taste + t / p (bt, ap …) und eine Hinweiszeile steht darunter."""
    print(f"\n {FETT(titel)}")
    raster([(k, t) for k, (t, _) in eintraege.items()] + [("↵", "zurück")])
    if zusatz:
        print("  " + GRAU("dazu: + t = Terminal dort (bt, at …) · + p = Pfad kopieren (bp, ap …)"))
    e = frage(" Wahl: ").lower()
    if zusatz and len(e) == 2 and e[0] in eintraege and e[1] in zusatz:
        return e
    if e == "q" and "q" not in eintraege:
        if beenden_frage():
            raise Beenden
        return None
    e = "ü" if e == "u" and "ü" in eintraege and "u" not in eintraege else e      # ohne ü-Taste
    return e if e in eintraege else None


def druck_dateien():
    """{Taste: (Text, Pfad)} der Druckdateien aus der Variablen-Datei («## Ausgabe: Druck …» → {druck-datei}).
    n = normal, u = unzensiert, weitere Ausgaben 1, 2, … (2.82.12)"""
    var = next(iter(glob.glob(os.path.join(BASE, "*-variablen.md"))), None)
    if not var:
        return {}
    aus, ziel = None, {}
    for z in open(var, encoding="utf-8"):
        if z.startswith("## "):
            aus = z[3:].strip() if z.lower().startswith("## ausgabe: druck") else None
        elif aus and z.startswith("{druck-datei}:"):
            name = z.split(":", 1)[1].strip()
            pfad = os.path.join(BASE, "druck", name + ".md")
            if name and os.path.isfile(pfad):
                art = aus.split("Druck", 1)[1].strip() or "normal"
                taste = "u" if "unzensiert" in art.lower() else "n" if art.lower() == "normal" else str(len(ziel) + 1)
                ziel[taste] = (f"{art} · {name}", pfad)
    return ziel


def druck_oeffnen():
    """m → d: Druckdatei öffnen – bei mehreren Fassungen (normal / unzensiert) zuerst wählen."""
    liste = druck_dateien()
    if len(liste) == 1:
        return oeffnen(next(iter(liste.values()))[1])
    k = untermenue("Druck …", liste)
    if k:
        oeffnen(liste[k][1])


def status_zeile():
    """Eine Zeile über dem Menü: Buchblock-Seiten je Fassung, letzter Bau, Cover (aus 00-UEBERSICHT.txt, 2.82.18)."""
    teile, bau = [], ""
    for f in sorted(glob.glob(os.path.join(BASE, "ausgabe-*", "00-UEBERSICHT.txt"))):
        name = os.path.basename(os.path.dirname(f))[8:]
        kurz = {"normal": "N", "unzensiert": "UZ"}.get(name, name[:3].upper())
        text = open(f, encoding="utf-8").read()
        m = re.search(r"_Buchblock\.pdf\s.*?(\d+) S\.", text)
        teile.append(f"{kurz} {m.group(1)} S." if m else f"{kurz} –")
        b = re.search(r"Letzter Bau: .*?«([^»]+)» · (\d\d\.\d\d)\.\d{4} (\d\d:\d\d)", text)
        if b and (not bau or b.group(2) + b.group(3) > bau[0]):
            bau = (b.group(2) + b.group(3), f"{b.group(1)} {b.group(2)}. {b.group(3)}")
    if not teile:
        return ""
    cover = "Cover ⚠ → co" if cover_faellig() else "Cover ✓"
    return GRAU(" " + " · ".join([os.path.basename(BASE)] + teile + ([bau[1]] if bau else []) + [cover]))


def trennstellen_menue():
    """tr: {trennstellen} der Variablen-Datei zeigen, Wort mit | ergänzen, «-wort» entfernen (2.82.18)."""
    pfad = next(iter(sorted(glob.glob(os.path.join(BASE, "*-variablen.md")))), None)
    if not pfad:
        return
    while True:
        zeilen = open(pfad, encoding="utf-8").read().split("\n")
        i = next((n for n, z in enumerate(zeilen) if z.startswith("{trennstellen}:")), None)
        liste = [w.strip() for w in zeilen[i].split(":", 1)[1].split(",") if w.strip()] if i is not None else []
        print("\n " + FETT("Trennstellen …") + GRAU(f"  {len(liste)} Wörter · | = hier darf getrennt werden"))
        zeile = " "
        for w in liste:
            if len(zeile) + len(w) + 3 > RAND:
                print(zeile); zeile = " "
            zeile += " " + w + " ·"
        print(zeile.rstrip(" ·"))
        print(GRAU("  z. B.  Re|vi|ta|ler  = ergänzen   ·   -Revitaler  = entfernen   ·   ↵ = zurück"))
        e = frage(" Wahl: ").strip()
        if not e or e == "q":
            return
        if e.startswith("-"):
            neu = [w for w in liste if w.replace("|", "") != e[1:].replace("|", "")]
        elif "|" in e:
            neu = [w for w in liste if w.replace("|", "") != e.replace("|", "")] + [e]
        else:
            print(ROT("  ✗ Mit | zeigen, wo getrennt werden darf, z. B. Re|vi|ta|ler"))
            continue
        z = "{trennstellen}: " + ", ".join(neu)
        if i is None:
            zeilen.append(z)
        else:
            zeilen[i] = z
        open(pfad, "w", encoding="utf-8").write("\n".join(zeilen))
        print(GRUEN("  ✓ gespeichert") + GRAU(" – wirkt beim nächsten Bau (s)"))


def stichworte_menue():
    """st: Vorschläge machen (und öffnen), mit [+] markierte übernehmen, Stichwortdatei öffnen."""
    k = untermenue("Stichworte …", {"v": ("Vorschläge", 0), "u": ("übernehmen [+]", 0), "o": ("Stichwortdatei öffnen", 0)})
    if k == "v":
        if bauen("stichworte") == 0:
            oeffnen(os.path.join(BASE, "stichworte-vorschlag.txt"))
    elif k == "u":
        bauen("stichworte", "uebernehmen")
    elif k == "o":
        oeffnen(next((p for p in sorted(glob.glob(os.path.join(BASE, "stichworte*.txt")))
                      if not p.endswith("stichworte-vorschlag.txt")), None))


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
    print("  ↵   zurück")
    e = frage(" Wahl: ").lower()
    if e in ks:
        oeffnen(ks[e][1])


ALLE = os.path.join(BASE, "geschichten-alle.md")
DEMO = "Dieses Demo-Kapitel zeigt alle Möglichkeiten"
SPERRE = "  ⚠ Alle Geschichten liegen in geschichten-alle.md – zuerst g → a zurückholen."


def buchdatei():
    return next(iter(glob.glob(os.path.join(BASE, "*-buch.md"))), None)


def einordnen(extra=None):
    """g → b: fehlende Geschichten (@@) und Tabellen (@#) in den Block «## Noch einordnen» (Buch-Reihenfolge bleibt).
    extra = eigene Zeilen statt Geschichten, z. B. ["@#preise"] nach t → n."""
    import geschichten as G
    buch, kopf = buchdatei(), "## Noch einordnen"
    v = G.verweise(buch)
    texte = [buch] + list(G.alle(BASE).values()) if buch else []
    drin = {x.strip()[2:].split()[0] for p in texte for x in open(p, encoding="utf-8") if x.strip().startswith("@#") and x.strip()[2:].split()}
    tab = sorted(glob.glob(os.path.join(BASE, "tabellen", "*.csv")), key=os.path.getmtime)
    fehlt = extra or (["##### @@" + n for n in G.reihe(BASE, buch) if n not in {n for _, n in v}]
                      + ["@#" + n for n in (os.path.basename(p)[:-4] for p in tab) if n not in drin and n != "muster"])
    if not buch or not fehlt:
        return print("  Alles ist im Buch (Geschichten und Tabellen).")
    z = open(buch, encoding="utf-8").read().split("\n")
    s = [x.strip() for x in z]
    neu = sum((["", x] for x in fehlt), [])
    demo = not extra and DEMO in "\n".join(z) and "## Vorwort" in s and any(x.startswith("# ") and "anhang" in x.lower() for x in s)
    if demo and frage(" Das Buch enthält noch den Demo-Inhalt. Durch deine Geschichten ersetzen? "
                      "[j/N]: ").lower() in ("j", "ja", "y"):
        bauen("sicherung")
        if "## Ein Teil mit eigenem Bild" in s:                  # Beispielkapitel im Anhang
            b = s.index("## Ein Teil mit eigenem Bild")
            del z[b:next((i for i in range(b + 1, len(s)) if s[i].startswith("#")), len(s))]
            s = [x.strip() for x in z]
        a = next(i for i, x in enumerate(s) if x.startswith("# ") and "anhang" in x.lower())
        if kopf in s:                                            # Inhalt eines vorhandenen Blocks behalten
            k = s.index(kopf)
            neu = sum((["", x] for x in s[k + 1:next((i for i in range(k + 1, len(s)) if s[i].startswith("#")
                                                      and not s[i].lstrip("# ").startswith("@@")), len(s))]
                       if x.lstrip("# ").startswith(("@@", "@#"))), []) + neu
        z[s.index("## Vorwort"):a] = ["## Vorwort", "", "Hier kommt dein Vorwort.", "", "# Teil 1|Geschichten|"] + neu + [""]
        open(buch, "w", encoding="utf-8").write("\n".join(z))
        return print("  Demo-Inhalt ersetzt durch: " + ", ".join(fehlt) + "\n  → ansehen: s schnell, dann p")
    bauen("sicherung")
    if kopf in s:                                   # Block gibt es schon: hinten anhängen
        k = s.index(kopf)
        ende = next((i for i in range(k + 1, len(s)) if s[i].startswith("#") and not s[i].lstrip("# ").startswith("@@")), len(s))
        pos = max([i + 1 for i in range(k + 1, ende) if s[i].lstrip("# ").startswith(("@@", "@#"))] or [k + 1])
    else:                                           # nach der letzten @@-Zeile, sonst vor den Anhang, sonst ans Ende
        pos = v[-1][0] if v else next((i for i, x in enumerate(s) if x.startswith("# ") and "anhang" in x.lower()), len(s))
        pos += 1 if v and pos < len(s) and s[pos] == ":::" else 0          # nicht in einen ::: nur-uz-Block
        neu = ["", kopf] + neu + ([""] if not v and pos < len(s) else [])
    z[pos:pos] = neu
    open(buch, "w", encoding="utf-8").write("\n".join(z))
    print(f"  Ins Buch (ab Zeile {pos + 2}, «{kopf}»): " + ", ".join(fehlt) + "\n  → ansehen: s schnell, dann p")


def hoerbuch_menue():
    """hb: Hörbuch mit Azure (motor/audio/hoerbuch.py, nur Linux). Einstellungen, Wörter, Probetexte in audio/."""
    sys.path.insert(0, os.path.join(MOTOR, "audio"))
    import hoerbuch as H
    audio = os.path.join(BASE, "audio")
    hb = [sys.executable, os.path.join(MOTOR, "audio", "hoerbuch.py")]
    H.anlegen()                                       # audio/ aus der Vorlage, Bestehendes bleibt
    while True:                                       # bleibt offen bis z / Enter
        try:
            if not hoerbuch_schritt(H, audio, hb):
                return
        except KeyboardInterrupt:                     # Strg+C bei einer Frage: wie q
            print()
            if beenden_frage():
                raise Beenden


def hoerbuch_schritt(H, audio, hb):
    """Ein Durchgang im Hörbuch-Menü; False = zurück ins Hauptmenü."""
    global gelaufen
    c = H.konf()
    st = c.get("AZURE_STIMME", "1")
    kurz = lambda s: "-".join(s.split("-")[2:]).replace("MultilingualNeural", "").replace("Neural", "") or s
    fav = {n: kurz(c.get("AZURE_FAVORIT" + n, "")) for n in ("1", "2")}
    andere = "1" if st == "2" else "2"                # die andere Favoritin zum Umschalten
    name = fav.get(st) or kurz(st)
    st = H.stufe_jetzt()
    gold = FETT if FARBIG else (lambda t: f"[{t}]")    # aktive Azure-Stufe: gold (ohne Farben in Klammern)
    k_ = kopf("Hörbuch", f"{name} · {c.get('AZURE_RATE', '')} · {c.get('MP3_KBIT', '128')} kbit · {st}")
    i_ = k_.rfind(f" {st} ")                          # erst nach dem Ausrichten färben (Farbcodes haben keine Breite)
    print("\n" + (k_[:i_ + 1] + FETT(st) + k_[i_ + 1 + len(st):] if FARBIG and i_ > 0 else k_))
    spalten_zeigen([("Probieren", [("p", "Probe hören (probe.txt)"), ("w", "Wörter hören (KLINGEN FALSCH)"),
                                   ("u", "Fremdwörter prüfen (Browser)")]),
                    ("Hörbuch", [("a", "alles: Texte → vertonen → Paket → Hörprobe"),
                                 ("t", "Texte aus dem Buch (zeigt Geänderte)"), ("v", "vertonen: was fehlt + geändert"),
                                 ("k", "vertonen: Kapitel auswählen …")]),
                    ("Weitergeben", [("f", "fertiges Paket: ZIP mit M4B"), ("r", "Hörprobe (verkauf/)")]),
                    ("Bearbeiten · Ordner", [("e", "Wörter · Probe · Einstellungen"), ("s", "Azure-Schlüssel eingeben"),
                                             ("x", "Azure: " + " ↔ ".join(gold(t) if t[:2] == st else t
                                                                          for t in ("F0 gratis", "S0 bezahlt"))),
                                             ("$", "Terminal in audio/"), ("o", "Ordner audio/ öffnen")])],
                   "h hilfe · c prüfen · ↵ zurück")
    k = frage(" Wahl: ").lower()
    if k in ("", "z"):
        return False
    if k == "q":
        if beenden_frage():
            raise Beenden
        return True
    gelaufen = False
    neu = lambda muster: sorted(glob.glob(os.path.join(audio, muster)), key=os.path.getmtime)
    def tempo_frage():                                # Enter = eingestellt · "" · None = zurück
        print(f" Tempo – Enter = {c.get('AZURE_RATE', '-8%')} (eingestellt) · z. B. -5% · 0% normal · z = zurück")
        t_ = frage(" Tempo: ").strip()
        return None if t_.lower() in ("z", "q") else (t_ if not t_ or t_.endswith("%") else t_ + "%")
    def abspielen(muster, seit):
        d = [p for p in neu(muster) if os.path.getmtime(p) >= seit - 1]
        if d and shutil.which("mpv"):
            subprocess.Popen(["mpv", "--force-window=yes", d[-1]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if k == "p":
        print(" Probe: liest audio/probe.txt vor und spielt sie ab (neue Datei probe-….mp3).")
        print(f" Stimme – Enter = {name} (eingestellt) · {andere} = {fav[andere]} · l = alle Stimmen zeigen · z = zurück")
        s_ = frage(" Stimme: ").strip()
        if s_ == "l":
            lauf(hb + ["probe", "l"])
            gelaufen = False
            print(f" Stimme – Nummer oder Name aus der Liste (z. B. de-CH-LeniNeural) · Enter = {name} (eingestellt) · z = zurück")
            s_ = frage(" Stimme: ").strip()
        if s_ in ("z", "q"):
            return True
        t_ = tempo_frage()
        if t_ is None:
            return True
        seit = time.time()
        r_ = lauf(hb + ["probe"] + [x for x in (s_, t_) if x])
        abspielen("*.mp3", seit)
        neu_ = H.stimme_name(s_) if s_ else ""
        if r_ == 0 and neu_ and neu_ != H.stimme_name(c.get("AZURE_STIMME", "1")) and \
                frage(f" {neu_} als Standard-Stimme? [j/N]: ").lower() in ("j", "ja", "y"):
            H.conf_setzen("AZURE_STIMME", s_ if s_ in ("1", "2") else neu_,
                          "1/2 = Favorit oder ganzer Name – hb → p → l zeigt alle")
            alt_, neu_a = (os.path.join(audio, f"aussprache-{H.kurzname(x)}.txt") for x in (H.stimme_name(c.get("AZURE_STIMME", "1")), neu_))
            if not os.path.exists(neu_a) and os.path.exists(alt_) and \
                    frage(f" Aussprache-Liste von {os.path.basename(alt_)} übernehmen? [J/n]: ").lower() not in ("n", "nein"):
                shutil.copy(alt_, neu_a)
            print(f" ✓ Stimme: {neu_} – neue MP3s kommen in einen eigenen Ordner (…-{H.kurzname(neu_)}-…)")
    elif k == "w":
        seit = time.time()
        lauf(hb + ["woerter"])
        abspielen("aussprache-*.mp3", seit)
    elif k == "t":
        print(" Texte aus dem Buch → audio/txt-md/ (nur geänderte werden ersetzt, MP3 bleiben).")
        if frage(" Weiter? [J/n]: ").lower() in ("n", "nein", "z", "q"):
            return True
        if lauf(hb + ["texte"]) == 0 and frage(f" Jetzt vertonen, was fehlt oder geändert ist (Tempo {c.get('AZURE_RATE', '-8%')})?"
                 " [J/n]: ").lower() not in ("n", "nein", "z", "q"):
            lauf(hb + ["vertonen"])
    elif k == "a":
        print(" Alles in einem: Texte aus dem Buch → vertonen (was fehlt + geändert) → Paket → Hörprobe.")
        print(" Hält beim ersten Fehler an. Am Schluss spielt die Hörprobe. Ergebnis: audio/verkauf/")
        t_ = tempo_frage()
        if t_ is not None:
            lauf(hb + ["komplett"] + ([f"tempo={t_}"] if t_ else []))
    elif k in ("v", "m"):                             # m = alte Taste
        print(" Vertonen: MP3 für Kapitel ohne MP3 oder mit geändertem Text (fertige bleiben).")
        print(" Anderes Tempo = eigener Ordner (z. B. …-t-5-k192) – so kannst du vergleichen.")
        t_ = tempo_frage()
        if t_ is not None:
            lauf(hb + ["vertonen"] + ([f"tempo={t_}"] if t_ else []))
    elif k == "f":
        print(" Paket: Kapitel-MP3s (Mono, PAKET_KBIT), M4B mit Kapiteln, Playlist, Cover → audio/verkauf/…zip")
        print(" Vorher: Texte aktuell (t) und alles vertont (v). Die Original-MP3s bleiben unverändert.")
        if frage(" Weiter? [J/n]: ").lower() not in ("n", "nein", "z", "q"):
            lauf(hb + ["paket"])
    elif k == "r":
        v = frage(" Enter = Hörprobe · v = Vergleich 96 · 128 · 192 kbit · z = zurück: ").lower()
        if v in ("z", "q"):
            return True
        seit = time.time()
        if lauf(hb + ["hoerprobe"] + (["vergleich"] if v == "v" else [])) == 0 and v != "v":
            abspielen("verkauf/hoerprobe.mp3", seit)
    elif k == "x":
        H.stufe([])
    elif k == "u":
        print(" Fremdwörter: Scan → Prüfseite im Browser. Klick = fr · en · es · it · ✎ · ✗ deutsch · ▶ hören.")
        print(" «💾 übernehmen» schreibt in die Aussprache-Liste. Danach w (anhören) und v. Zurück hierher: Ctrl+C.")
        lauf(hb + ["fremd", "server"])
    elif k == "c":
        lauf(hb + ["pruefen"])
    elif k == "k":
        lauf(hb + ["liste"])
        gelaufen = False
        print(" Kapitel vertonen: nur die gewählten, immer neu (MP3 wird ersetzt).")
        da = [re.sub(r"\D", "", os.path.basename(p).split("_", 1)[0]) for p in glob.glob(os.path.join(audio, "txt-md", "*.txt"))]
        while True:                                   # Kürzel gleich prüfen, falsche nochmals fragen
            wahl = frage(" Kapitel – z. B. 0603,0605 · 06 = Teil 6 · z = zurück: ").strip()
            falsch = [w for w in wahl.replace(" ", ",").split(",") if w and not any(d.startswith(w.replace(".", "")) for d in da)]
            if wahl.lower() in ("", "z", "q") or not falsch:
                break
            print(" " + ROT("✗ Nicht gefunden: " + ", ".join(falsch)) + GRAU(" – Kürzel aus der Liste oben"))
        if wahl and wahl.lower() not in ("z", "q"):
            t_ = tempo_frage()
            if t_ is not None:
                lauf(hb + wahl.split() + ([f"tempo={t_}"] if t_ else []))
    elif k == "e":
        datei = {"w": ("Wörter", (glob.glob(os.path.join(audio, f"aussprache-{name.lower()}.txt")) or
                                  sorted(glob.glob(os.path.join(audio, "aussprache-*.txt"))) or [""])[0]),
                 "p": ("Probe (probe.txt)", os.path.join(audio, "probe.txt")),
                 "e": ("Einstellungen (audio.conf)", os.path.join(audio, "audio.conf"))}
        e = untermenue("öffnen …", datei)
        if e:
            oeffnen(datei[e][1])
    elif k == "s":
        H.schluessel()                                # im Menü sofort gültig (os.environ)
    elif k == "$":
        terminal(audio)
        print("  Terminal im Ordner audio/ – dort:  sh hb.sh   (zeigt alle Befehle)")
    elif k == "o":
        oeffnen(audio)
    elif k == "h":
        hilfe = os.path.join(BASE, "hilfe.html")
        if not os.path.exists(hilfe):
            bauen("hilfe")
        import webbrowser
        webbrowser.open("file://" + hilfe + "#Hörbuch-Was-es-braucht")
    else:
        print(" " + ROT(f"✗ Unbekannt: {k}") + GRAU(" – h = Hilfe"))
    if gelaufen:                                      # Meldungen stehen lassen
        gelaufen = False
        a = frage(" Enter = Hörbuch-Menü · z = zurück: ").lower()
        if a == "q" and beenden_frage():
            raise Beenden
        return a != "z"
    return True


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
        print("  ↵   zurück")
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
            f.write("> Alle Geschichten in einer Datei. Text frei ändern, Steuerzeichen unverändert lassen:\n"
                    "> @@@ name (Trennzeile, nie ändern) · stand: / stichworte: / quelle: / notiz: (Kopfzeilen) ·\n"
                    "> # bis #### (Titel) · @#name (Tabelle) · #### @FOTO (Foto) · > (Zitat) · ::: … ::: (Bereiche)\n"
                    "> Antwort bitte vollständig als Markdown mit allen Steuerzeichen, zum Kopieren.\n"
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


def cover_faellig():
    """[(kuerzel, druckdatei, seiten, berechnet, grund, fassung)] aus _druckbilder/cover-*.txt (schreibt jeder Bau der
    Druckdateien, ab 2.78; Fassung normal|uz ab 2.82.3, ältere Dateien: aus dem Namen geraten)."""
    out = []
    for p in sorted(glob.glob(os.path.join(BASE, "_druckbilder", "cover-*.txt"))):
        try:
            teile = open(p, encoding="utf-8").read().strip().split("|")
            d, n, b, g = teile[:4]
        except (OSError, ValueError):
            continue
        k = os.path.basename(p)[6:-4]
        f = teile[4] if len(teile) > 4 else ("uz" if "uz" in (k + d).lower() else "normal")
        out.append((k, d, n, b, g, f))
    return out


def cover_menue():
    """cv: Druckdateien mit fälligem Coverrechner öffnen und sagen, was zu tun ist."""
    faellig = cover_faellig()
    if not faellig:
        return print("  Coverrechner: alles passt (oder noch kein «final» gebaut).")
    for k, d, n, b, g, _ in faellig:
        print(f"  {FETT(k)}: Buchblock {n} Seiten, Werte für {b} – {g}. Öffne {d} …")
        oeffnen(os.path.join(BASE, d))
    print("  Im Coverrechner der Druckerei diese Seitenzahl eingeben, den Text zuunterst unter «## Coverrechner (Rohdaten)»\n"
          "  einfügen (alten ersetzen). Dann f final: der Motor liest die Werte und baut den Umschlag neu.")


INITIAL_SCHRIFTEN = (("t", "", "Textschrift", "schlicht, wie der Text"), ("f", "fett", "fett", "kräftig"),
                     ("c", "cinzel", "Cinzel", "elegant, römisch"), ("u", "uncial", "Uncial", "keltisch, verspielt"),
                     ("r", "fraktur", "Fraktur", "alt, schwerer lesbar"))


INITIAL_FARBEN = (("g", "akzent", "gold", "Akzentfarbe, wie Zierlinien und Lotus"),
                  ("b", "haupt", "blau", "wie die Überschriften"), ("s", "text", "schwarz", "wie der Text"),
                  ("ü", "ueberschrift", "Überschrift", "jede Stufe in der Farbe ihrer Überschrift"))


INITIAL_SCHLUESSEL = ("initial", "initial-stufen", "initial-zeilen", "initial-schrift", "initial-farbe", "kapitaelchen",
                      "absatz-einzug")


def initialen_menue():
    """in (ab 2.82.8; getrennt normal/unzensiert ab 2.82.14): Initial am Kapitelanfang – wo (0–4 Zeilen im Text, ti = im
    Titel), Schrift, Farbe, Kapitälchen, Einzug. Eingabe z. B. «n ti c b k1» · «uz 0» · «e1» (ohne n/uz = beide);
    «n0» / «uz0» = alles aus; «v» = Vorschau. Sind normal und unzensiert gleich, steht eine Zeile {name}: in der
    Variablen-Datei, sonst zwei: {name-normal}: und {name-uz}: (der Motor liest beides, manuskript.Ausgabe.wert)."""
    pfad = next(iter(sorted(glob.glob(os.path.join(BASE, "*-variablen.md")))), None)
    if not pfad:
        return
    standard = {"initial": "nein", "initial-stufen": "2", "initial-zeilen": "3", "initial-schrift": "",
                "initial-farbe": "akzent", "kapitaelchen": "nein", "absatz-einzug": "nein"}
    while True:
        zeilen = open(pfad, encoding="utf-8").read().split("\n")
        roh = lambda n: next((z.split(":", 1)[1].strip() for z in zeilen if z.startswith("{" + n + "}:")), None)
        hat_uz = any(z.startswith("## Ausgabe:") and "unzensiert" in z for z in zeilen) or \
            any(re.match(r"\{[a-z0-9-]+-uz\}:", z) for z in zeilen)
        fassungen = ("normal", "uz") if hat_uz else ("normal",)

        def wert(n, f):                                # {n-f}: vor {n}: (gleich wie beim Bauen, wenn {n}: fehlt)
            w = roh(f"{n}-{f}")
            if w is None:
                w = roh(n)
            return (w if w is not None else standard[n]).lower()

        def stand(f):
            art, zahl, schrift = wert("initial", f), wert("initial-zeilen", f), wert("initial-schrift", f)
            stufen = " ".join(sorted(set(re.findall(r"[234]", wert("initial-stufen", f))))) or "2"
            farbe_ = {"blau": "haupt", "schwarz": "text", "gold": "akzent"}.get(wert("initial-farbe", f), wert("initial-farbe", f))
            aus = art not in ("ja", "j", "titel") or (art != "titel" and zahl == "0")
            name = next((n for _, w, n, _ in INITIAL_SCHRIFTEN if w == schrift), schrift or "Textschrift")
            if art == "titel" and not schrift:
                name = "Titelschrift"
            return {"wo": "aus" if aus else f"im Titel ({stufen.replace(' ', ', ')})" if art == "titel" else
                    "erhöht" if zahl == "1" else zahl + " Zeilen",
                    "schrift": "–" if aus else name,
                    "farbe": "–" if aus else next((n for _, w, n, _ in INITIAL_FARBEN if w == farbe_), "gold"),
                    "kap": "ja" if wert("kapitaelchen", f) in ("ja", "j") else "nein",
                    "einzug": "ja" if wert("absatz-einzug", f) in ("ja", "j") else "nein", "aus": aus}

        st = {f: stand(f) for f in fassungen}
        print("\n " + FETT("Initialen …".ljust(27)) + "".join(FETT(("normal" if f == "normal" else "unzensiert").ljust(17))
                                                            for f in fassungen))
        for titel, k in (("Wo", "wo"), ("Schrift", "schrift"), ("Farbe", "farbe"), ("Kapitälchen", "kap"),
                         ("Einzug", "einzug")):
            print(f"  {titel:<26}" + "".join(f"{st[f][k]:<17}" for f in fassungen))
        print(GRAU(" " + "─" * 54))
        print(f"  {FETT('Wo')}       0 aus · 1 erhöht · 2 · 3 · 4 Zeilen")
        print(f"           {FETT('ti')} im Titel · {FETT('ti3')} · {FETT('ti23')} · {FETT('ti234')} " + GRAU("(Stufen)"))
        print(f"  {FETT('Schrift')}  " + " · ".join(f"{FETT(t)} {n}" for t, _, n, _ in INITIAL_SCHRIFTEN).replace("Textschrift", "Text"))
        print(f"  {FETT('Farbe')}    " + " · ".join(f"{FETT(t)} {n}" for t, _, n, _ in INITIAL_FARBEN).replace("Überschrift", "wie Überschrift"))
        print(f"  {FETT('k1')} / {FETT('k0')}  Kapitälchen ein / aus  " + GRAU("(erste Wörter in GROSSBUCHSTABEN)"))
        print(f"  {FETT('e1')} / {FETT('e0')}  Einzug ein / aus       " + GRAU("(Absätze eingerückt statt mit Abstand)"))
        print(f"  {FETT('v')}        Vorschau " + GRAU("(schnell bauen, PDF öffnen)"))
        print(GRAU(" " + "─" * 54))
        if hat_uz:
            print(f"  {FETT('n')} … = nur normal · {FETT('uz')} … = nur unzensiert · ohne = beide")
            print(f"  {FETT('n0')} / {FETT('uz0')} = alles aus " + GRAU("(Initial, Kapitälchen, Einzug)"))
            print(GRAU("  z. B.  n ti c b k1   ·   uz 0   ·   e1   ·   ↵ = zurück"))
        else:
            print(GRAU("  z. B.  ti c b k1   ·   0   ·   e1   ·   ↵ = zurück"))
        e = frage_verlauf(" Wahl: ", INITIAL_VERLAUF).lower().split()
        if not e or e == ["q"]:
            einstellungen(speichern=True)                 # Verlauf gleich sichern
            return
        ziel = list(fassungen)
        if e[0] in ("n", "uz", "n0", "uz0") and hat_uz:
            ziel = ["normal" if e[0].startswith("n") else "uz"]
            if e[0].endswith("0"):
                e[0:1] = ["0", "k0", "e0"]
            else:
                e = e[1:]
        neu = {}
        vorschau = False
        for t in e:
            if t in ("0", "1", "2", "3", "4"):
                neu["initial"] = "ja" if t != "0" else "nein"
                if t != "0":
                    neu["initial-zeilen"] = t
            elif re.fullmatch(r"ti[234]*", t):
                neu["initial"] = "titel"
                neu["initial-stufen"] = " ".join(sorted(set(t[2:]))) or "2"
            elif t in ("k1", "k0"):
                neu["kapitaelchen"] = "ja" if t == "k1" else "nein"
            elif t in ("e1", "e0"):
                neu["absatz-einzug"] = "ja" if t == "e1" else "nein"
            elif t in ("k", "e"):
                print(ROT(f"  ✗ {t}1 = ein · {t}0 = aus"))
            elif t == "v":
                vorschau = True
            elif any(t == x[0] for x in INITIAL_SCHRIFTEN):
                neu["initial-schrift"] = next(w for x, w, _, _ in INITIAL_SCHRIFTEN if x == t)
            elif t == "ue":
                neu["initial-farbe"] = "ueberschrift"
            elif any(t == x[0] for x in INITIAL_FARBEN):
                neu["initial-farbe"] = next(w for x, w, _, _ in INITIAL_FARBEN if x == t)
            else:
                print(ROT(f"  ✗ Unbekannt: {t}"))
        if neu:
            werte = {f: {n: wert(n, f) for n in INITIAL_SCHLUESSEL} for f in fassungen}
            geaendert = set(neu)
            for f in ziel:
                if st[f]["aus"] and "initial" not in neu and ({"initial-schrift", "initial-farbe"} & set(neu)):
                    werte[f]["initial"] = "ja"            # Schrift oder Farbe gewählt, Initial war aus: einschalten
                    if werte[f]["initial-zeilen"] == "0":
                        werte[f]["initial-zeilen"] = "3"
                    geaendert |= {"initial", "initial-zeilen"}
                werte[f].update(neu)
            for n in (n for n in INITIAL_SCHLUESSEL if n in geaendert):
                gleich = len({werte[f][n] for f in fassungen}) == 1
                soll = {n: werte[fassungen[0]][n]} if gleich else {f"{n}-{f}": werte[f][n] for f in fassungen}
                alt = [i for i, x in enumerate(zeilen)
                       if any(x.startswith("{" + k + "}:") for k in [n] + [f"{n}-{f}" for f in ("normal", "uz")])]
                pos = alt[0] if alt else next((i + 1 for i, x in enumerate(zeilen) if x.startswith("{initial")),
                                              next((i + 1 for i, x in enumerate(zeilen) if x.strip() == "## Gestaltung"),
                                                   len(zeilen)))
                for i in reversed(alt):
                    del zeilen[i]
                for j, (k, w) in enumerate(soll.items()):
                    zeilen.insert(pos + j, "{" + k + "}:" + (" " + w if w else ""))
            open(pfad, "w", encoding="utf-8").write("\n".join(zeilen))
            wer = "beide" if len(ziel) > 1 else ("normal" if ziel == ["normal"] else "unzensiert")
            print(GRUEN(f"  ✓ gespeichert ({wer})") + GRAU(" – v = Vorschau"))
        if vorschau and bauen("schnell") == 0:
            liste = pdfs()
            if liste:
                oeffnen(next(iter(liste.values()))[1])


ISBN_AUSGABEN = (("Druck normal", "Druck normal"), ("Druck unzensiert", "Druck UZ"),
                 ("E-Book", "E-Book normal"), ("E-Book unzensiert", "E-Book UZ"))


def isbn_menue():
    """is (ab 2.82.7; bis 2.82.10 w → i): die ISBN aller Ausgaben ansehen und eintragen (Enter = bleibt, - = leeren). Sie stehen weiter
    in der Variablen-Datei («{isbn}:» unter «## Ausgabe: …») – nur dort, also immer gleich. Danach Prüfziffer und
    Strichcode-PNG der gedruckten Fassungen (sh build.sh isbn), die PNG öffnen sich."""
    pfad = next(iter(sorted(glob.glob(os.path.join(BASE, "*-variablen.md")))), None)
    if not pfad:
        return
    zeilen = open(pfad, encoding="utf-8").read().split("\n")

    def stelle(abschnitt):                            # (Zeile «## Ausgabe: …», Zeile «{isbn}:» oder None)
        k = next((i for i, z in enumerate(zeilen) if z.strip() == "## Ausgabe: " + abschnitt), None)
        if k is None:
            return None, None
        for i in range(k + 1, len(zeilen)):
            if zeilen[i].startswith("## "):
                break
            if zeilen[i].startswith("{isbn}:"):
                return k, i
        return k, None

    print(GRAU(" ISBN – Enter = bleibt · - = leeren · steht in ") + os.path.basename(pfad))
    geaendert = False
    for abschnitt, kurz in ISBN_AUSGABEN:
        k, i = stelle(abschnitt)
        if k is None:
            continue
        alt = zeilen[i].split(":", 1)[1].strip() if i is not None else ""
        e = frage(f"  {kurz:<14} [{alt or 'leer'}]: ").strip()
        if e.lower() == "q":
            return
        if not e or e == alt:
            continue
        z = "{isbn}:" + ("" if e == "-" else " " + e)
        if i is None:
            zeilen.insert(k + 1, z)
        else:
            zeilen[i] = z
        geaendert = True
    if geaendert:
        open(pfad, "w", encoding="utf-8").write("\n".join(zeilen))
        print(GRUEN("  ✓ gespeichert"))
    if bauen("isbn") == 0:
        try:
            for p in open(os.path.join(BASE, "_druckbilder", "isbn.txt"), encoding="utf-8").read().split():
                oeffnen(p)
        except OSError:
            pass


def pruef_stand():
    """Letzte Prüfung (bauen.py schreibt _druckbilder/pruefen.txt, ab 2.82.1): «ok», «fehler» oder "" =
    noch nie geprüft oder seither Buch, Variablen, Umschlag, Stichworte, Druckdatei, Geschichte oder Tabelle geändert."""
    p = os.path.join(BASE, "_druckbilder", "pruefen.txt")
    try:
        wert, zeit = (open(p, encoding="utf-8").read().split() or [""])[0], os.path.getmtime(p)
    except OSError:
        return ""
    muster = [m for _, m in MD.values()] + ["druck/*.md", "geschichten/*.md", "tabellen/*.csv"]
    if any(os.path.getmtime(f) > zeit for m in muster for f in glob.glob(os.path.join(BASE, m))):
        return ""
    return wert


def bp_marke():
    """«bp Buch prüfen» mit dem Stand pro Fassung (2.82.3): «✓» bzw. «N ✓  UZ ✗». ✗ (rot) = Prüfung mit Fehler oder
    Coverrechner-Warnung der Fassung, ? = noch nicht geprüft. Ist die Prüfung veraltet, prüft das Menü kurz selbst."""
    if not pruef_stand():
        try:                                          # still prüfen (ca. 1 s, nur nach Änderungen)
            subprocess.run([sys.executable, os.path.join(MOTOR, "bauen.py"), "pruefen"], cwd=BASE, timeout=120,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass
    stand = pruef_stand()
    try:
        fassungen = open(os.path.join(BASE, "_druckbilder", "pruefen.txt"), encoding="utf-8").read().split()[1:] or ["normal"]
    except OSError:
        fassungen = ["normal"]
    warn = {f for _, _, _, _, _, f in cover_faellig()}
    marke = lambda f: ROT("✗") if stand == "fehler" or f in warn else ("✓" if stand == "ok" else "?")
    if len(fassungen) < 2:
        return "Buch prüfen " + marke(fassungen[0])
    return "Buch prüfen  " + "  ".join(("N " if f == "normal" else "UZ ") + marke(f) for f in fassungen)


def zeige():
    bp = bp_marke()                                   # zuerst: prüft bei Bedarf still (Stand für die Zeile unten)
    print("\n" + kopf(rechts=f"Klang ({FETT('!')}) {'ein' if ton else 'aus'}"))
    for k, d, n, b, g, _ in cover_faellig():
        print(FETT(f" ⚠ Coverrechner {k}: {n} Seiten, eingetragen für {b}") + GRAU(f"  ({g}) → co"))
    if pruef_stand() == "fehler":
        print(ROT(" ✗ Buch prüfen: Fehler gefunden") + GRAU("  → bp"))
    status = status_zeile()                           # 2.82.18: Stand auf einen Blick (Seiten, letzter Bau, Cover)
    if status:
        print(status)
    spalten = [("1 Schreiben", [("m", "MD öffnen …"), ("g", "Geschichten …"), ("t", "Tabellen …"),   # 2.82.18:
                               ("c", "check / gegenlesen …")]),                                      # Blöcke im Buchablauf,
               ("2 Einstellen", [("in", "Initialen …"), ("tr", "Trennstellen …"), ("st", "Stichworte …"),  # Tasten gleich
                                 ("is", "ISBN …")]),
               ("3 Bauen", [("s", "schnell  (Lese-PDF)"), ("w", "weitergeben (lp + ko)"), ("k", "komplett (vor dem Druck)")]
                + ([("hb", "Hörbuch … (Linux)")] if LINUX else [])),
               ("4 Ansehen", [("p", "PDF öffnen …"), ("o", "Ordner öffnen …"), ("a", "änderungen (a|ä)"),
                              ("db", "Druckbericht")]),
               ("5 Prüfen", [("bp", bp), ("co", "Coverrechner prüfen")]),
               ("6 Weitere Ausgaben", [("lp", "Leseprobe    ko Korrektur"), ("np", "nur-pdf      ne nur E-Book")]),
               ("Abgleichen", [("sy", "sync   (GitHub)"), ("u", "update" + (" (ul lokal)" if LOKAL else ""))]),
               ("Aufräumen", [("sm", "Stand merken"), ("au", "aufräumen …")])]
    spalten_zeigen(spalten, "n neu · $ Terminal · : Befehle · h hilfe · hf finden")
    if os.path.exists(ALLE):
        print(SPERRE)


def spalten_zeigen(spalten, weiteres):
    """Gruppen paarweise in zwei Spalten (Haupt- und Hörbuch-Menü gleich) und «── Weiteres ──» mit den übrigen Tasten."""
    taste = lambda k: FETT(k) + " " * (3 - len(k))                 # Taste gold, danach auf 3 Zeichen aufgefüllt
    zweite = lambda t: re.sub(r"(\s{1,})([a-zäöü]{2}) ", lambda m: m.group(1) + FETT(m.group(2)) + " ", t, count=1) \
        if re.search(r"\s[a-z]{2} [A-ZÄÖÜa-z]", t[12:]) else t   # «Leseprobe    ko Korrektur»: zweite Taste gold
    linie = lambda t, n=30: GRAU("── ") + t + " " + GRAU("─" * (n - len(t)))
    for (t1, z1), (t2, z2) in zip(spalten[0::2], spalten[1::2]):     # Gruppen paarweise nebeneinander
        print(f" {linie(t1)}   {linie(t2, 29)}")                  # rechte Linie endet bei RAND
        for a, b in zip(z1 + [("", "")] * 3, z2 + [("", "")] * 3):
            if a[0] or b[0]:
                print((f"  {taste(a[0])}{a[1]:<33}" + (f"{taste(b[0])}{zweite(b[1])}" if b[0] else "")).rstrip())
    print(f" {GRAU('──')} Weiteres {GRAU('─' * (RAND - 13))}")       # wie die anderen Gruppen (2.82.3)
    zeile, laenge = "", 2                                              # Tasten unter den anderen Tasten, umbrechen bei RAND
    for i, t in enumerate(weiteres.split(" · ")):
        teil = (FETT(t.split(" ", 1)[0]) + " " + t.split(" ", 1)[1]) if " " in t else t
        if i and laenge + 3 + len(t) > RAND:
            print("  " + zeile); zeile, laenge = teil, 2 + len(t)
        else:
            zeile, laenge = zeile + (" · " if i else "") + teil, laenge + (3 if i else 0) + len(t)
    print("  " + zeile)


def raster(zeilen):
    b = max(16, max(len(t) for _, t in zeilen) + 2)                     # Spalten so breit wie der längste Text
    for i in range(0, len(zeilen), 4 if b <= 16 else 3):
        print(("  " + "".join(FETT(k) + " " * (3 - len(k)) + f"{t:<{b}}" for k, t in zeilen[i:i + (4 if b <= 16 else 3)])).rstrip())


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
    e = frage(" Eingabe (Enter = zurück): ", merken=True)
    return "" if e.lower() == "z" else e             # z hier = zurück, nicht beenden


def terminal(ordner=BASE):
    """Neues Terminal im Buchordner (oder einem Unterordner) öffnen; das Menü wartet nicht."""
    if WIN:
        return subprocess.Popen(["cmd"], cwd=ordner, creationflags=subprocess.CREATE_NEW_CONSOLE)
    if MAC:
        return subprocess.Popen(["open", "-a", "Terminal", ordner])
    for t in ("x-terminal-emulator", "gnome-terminal", "konsole", "xfce4-terminal", "xterm"):
        if shutil.which(t):
            return subprocess.Popen([t], cwd=ordner, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("  Kein Terminal gefunden – Rechtsklick in den Buchordner → «Im Terminal öffnen».")


def pfad_kopieren(ordner):
    """Pfad in die Zwischenablage (Linux: wl-copy, xclip oder xsel · Mac: pbcopy · Windows: clip) und anzeigen."""
    for cmd in ([["clip"]] if WIN else [["pbcopy"]] if MAC else
                [["wl-copy"], ["xclip", "-selection", "clipboard"], ["xsel", "-b", "-i"]]):
        if shutil.which(cmd[0]):
            subprocess.run(cmd, input=ordner.encode(), stderr=subprocess.DEVNULL)
            print(f"  Kopiert: {ordner}")
            return
    print(f"  {ordner}\n  (zum Kopieren markieren – für Strg+C fehlt xclip: sudo apt install xclip)")


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


def finde_hilfe(wort):
    """hf wort (hilfe finden): Abschnitte der Hilfe mit dem Wort (und verwandten: isbn → Strichcode, Barcode), Nummer öffnet dort."""
    import hilfe as Hf
    wort = wort or frage(" In der Hilfe suchen (z. B. isbn, farbe, hörbuch): ").strip()
    if not wort or wort.lower() in ("z", "q"):
        return
    tr = Hf.finden(BASE, wort)
    if tr is None:
        return print("  Noch keine Hilfe – einmal bauen (s), dann nochmals hf.")
    if not tr:
        return print(f"  Nichts gefunden zu «{wort}».")
    verwandt = [x for x in Hf.erweitern(wort)[1:]]
    print(f"\n {FETT('Hilfe')} · «{wort}»" + (GRAU(" (auch: " + ", ".join(verwandt) + ")") if verwandt else "")
          + f" · {len(tr)} Abschnitte")
    breit = max(20, shutil.get_terminal_size((80, 24)).columns - 40)
    for i, (g, t, z, n) in enumerate(tr[:20], 1):
        print(f"  {FETT(f'{i:>2}')}  {t[:32]:<33}" + GRAU(z[:breit] if z else ""))
    if len(tr) > 20:
        print(GRAU(f"  … und {len(tr) - 20} weitere – a zeigt alle in der Hilfe"))
    k = frage(" Nummer = dort öffnen · a = alle in der Hilfe · ↵ zurück: ").strip().lower()
    if k == "a":
        Hf.oeffne_suche(BASE, wort)
    elif k.isdigit() and 0 < int(k) <= len(tr):
        Hf.oeffne_suche(BASE, wort, tr[int(k) - 1][1])


def verknuepfung():
    """Starter mit Lotus, der dieses Menü öffnet: Linux .desktop (Startmenü), Windows .lnk, Mac .command."""
    name = os.path.basename(next(iter(glob.glob(os.path.join(BASE, "*-buch.md"))), "Buch-buch.md"))[:-8]
    orte = [BASE] + ([schreibtisch()] if frage(" Auch auf den Schreibtisch? [J/n]: ").lower() not in ("n", "nein")
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
    global ton, gelaufen
    if sys.argv[1:2] == ["verknuepfung"]:
        return verknuepfung()
    einstellungen()
    naechste = ""
    while True:
        try:
            if naechste:                                  # Eingabe aus «: Befehle»
                e, naechste = naechste, ""
            elif gelaufen:                                # Meldungen stehen lassen, kein neues Menü
                gelaufen = False
                e = frage(" Eingabe (Enter = Menü): ", merken=True)
                if not e:
                    continue
            else:
                zeige()
                print(" Wahl oder Befehl (z. B. final · ↑ = letzte · ↵ = beenden):")
                e = frage(" Eingabe: ", merken=True)
            w = e.lower()
            if w in ("", "z", "q"):                   # Hauptmenü: Enter / z = beenden? [j/N] – nur j schliesst
                if beenden_frage():
                    break
                continue
            seit = time.time()
            if w == "cv":                                   # Coverrechner fällig? (ab 2.78)
                cover_menue()
            elif w == "hf" or w.startswith("hf "):          # hilfe finden: hf isbn
                finde_hilfe(e[2:].strip())
            elif w == "s":
                bauen("schnell")
            elif w == "k":
                bauen("komplett")
            elif w == "f":
                bauen("final")
            elif w == "db":                                 # Druckbericht des letzten Druck-Baus (ab 2.82.11)
                oeffnen(next(iter(sorted(glob.glob(os.path.join(BASE, "*", "00-Druckbericht.pdf")))), None))
            elif w == "co":                                 # Coverrechner prüfen, ohne zu bauen (ab 2.82.11)
                bauen("cover-stand")
            elif w == "in":
                initialen_menue()
            elif w == "is":
                isbn_menue()
            elif w == "st":
                stichworte_menue()
            elif w == "tr":                                 # Trennstellen (ab 2.82.18)
                trennstellen_menue()
            elif w in ("lp", "ko", "np", "ne"):
                bauen({"lp": "leseprobe", "ko": "korrektur", "np": "nur-pdf", "ne": "nur-ebook"}[w])
            elif w == "sm":
                name = frage(" Name des Stands: ")
                bauen("stand", *([name] if name else []))
            elif w == "au":
                lauf([sys.executable, os.path.join(MOTOR, "aufraeumen.py")], titel="aufräumen")
            elif w == "w":                                  # 2.82.13: weitergeben = Leseprobe + Korrektur (ex «weitere»)
                if bauen("leseprobe") == 0:
                    bauen("korrektur")
            elif w == "m":
                md = {k: (t, next((p for p in sorted(glob.glob(os.path.join(BASE, m)))
                                      if not p.endswith("stichworte-vorschlag.txt")), None)) for k, (t, m) in MD.items()}
                if os.path.isdir(os.path.join(BASE, "geschichten")):
                    md["g"] = ("Geschichten …", "g")
                md["t"] = ("Tabellen …", "t")
                if druck_dateien():
                    md["d"] = ("Druck …", "d")                # 2.82.12: Druckdatei(en) der Ausgaben
                k = untermenue("MD öffnen …", {k: v for k, v in md.items() if v[1]})
                if k == "g":
                    geschichte_oeffnen()
                elif k == "t":
                    tabellen_menue()
                elif k == "d":
                    druck_oeffnen()
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
                          ("t", "tabellen", "tabellen"), ("a", "audio (Hörbuch)", "audio"),
                          ("p", "Pfad Buchordner kopieren", ""))}
                k = untermenue("Ordner …", {k: v for k, v in ordner.items() if os.path.isdir(v[1])}, zusatz="tp")
                k = "bp" if k == "p" else k               # p allein = Pfad des Buchordners
                if k:                                     # b = öffnen · bt = Terminal · bp = Pfad kopieren
                    {"t": terminal, "p": pfad_kopieren}.get(k[1:], oeffnen)(ordner[k[0]][1])
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
            elif w == "bp":                                 # Buch prüfen: Variablen, Druckdateien, Befehle, Fotos … (ab 2.82)
                bauen("pruefen")
            elif w in ("a", "ä"):
                seit = time.time()
                if bauen("aenderungen") == 0:
                    neu = [p for p in glob.glob(os.path.join(BASE, "ausgabe-*", "*_Aenderungen.pdf"))
                           if os.path.getmtime(p) >= seit - 1]
                    for p in neu:
                        oeffnen(p)
            elif w == "hb" and LINUX:
                hoerbuch_menue()
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
            elif w == "$":
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
                    neu_in = plattform.buecher(PURESATZ)
                    vorher = set(os.listdir(neu_in))
                    {"b": lambda: skript(os.path.join("setup", "setup"), ordner=PURESATZ),
                     "h": lambda: skript("hallo", ordner=PURESATZ),
                     "m": lambda: lauf([sys.executable, os.path.join("test", "selbsttest.py")], PURESATZ,
                                       dict(os.environ, SELBSTTEST_OHNE_VENV="1")),
                     "e": lambda: skript("START-Windows" if WIN else "START-Linux", ordner=PURESATZ,
                                         mac="START-Mac-imTerminal.sh")}[k]()
                    for d in sorted(set(os.listdir(neu_in)) - vorher):
                        print(f"  Neues Buch: {os.path.relpath(os.path.join(neu_in, d), BASE)} – dort sh menu.sh")
            elif w in ("h", "?"):
                bauen("hilfe")
            elif w.split()[0] in ("xdg-open", "open", "start"):   # wie im Terminal: Datei öffnen, ohne zu warten
                for teil in shlex.split(e, posix=not WIN)[1:]:
                    oeffnen(os.path.join(BASE, os.path.expanduser(teil.strip('"'))))
            elif w.split()[0] in BEFEHLE:          # ganzer Befehl: final · leseprobe uz 18,20 · personen Eltern
                bauen(*e.split())
            else:
                print(" " + ROT(f"✗ Unbekannt: {e}") + GRAU(" – : = Befehle · h = Hilfe"))
            neu = {k: p for k, (_, p) in pdfs().items() if os.path.getmtime(p) >= seit - 1} if gelaufen else {}
            for p in ([neu[k] for k in ("n", "u") if k in neu] if len(neu) > 2 else neu.values()):
                oeffnen(p)                                # neu gebaute Lese-PDFs gleich öffnen
            einstellungen(speichern=True)
        except Beenden:
            break
        except KeyboardInterrupt:                     # Strg+C bei einer Frage: wie q
            print()
            if beenden_frage():
                break
    einstellungen(speichern=True)


if __name__ == "__main__":
    if FARBIG:
        sys.stdout.write("\033]12;#d7af5f\007")         # Cursor gold (Terminator, GNOME, xterm; sonst ohne Wirkung)
    try:
        main()
    except KeyboardInterrupt:
        print()
    finally:
        if FARBIG:
            sys.stdout.write("\033]112\007")            # Cursorfarbe zurück
