#!/usr/bin/env python3
"""
tabellen.py – Tabellen aus CSV-Dateien ins Buch setzen (pureSATZ ab 2.12).

Eine Tabelle ist eine CSV-Datei im Ordner tabellen/ des Buchs, z. B. tabellen/behandlungen.csv:

    Behandlungen pro Jahr                   <- Zeile 1: Bezeichnung (steht über der Tabelle)
    Jahr;Emotionscode;Body Code;Total       <- Zeile 2: Spaltenüberschriften
    2018;40;12;52                           <- ab Zeile 3: Werte
    2019;65;30;95
    Quelle: eigene Praxisstatistik          <- optional: letzte Zeile «Quelle: …» steht klein darunter

Trenner ; oder , (wird erkannt), Zeichensatz UTF-8 (LibreOffice: Speichern unter → Text CSV).
Im Buch eine eigene Zeile:  @#behandlungen   (oder @# behandlungen; mit «quer» oder «hoch» am Schluss
die Ausrichtung selbst bestimmen). Neue Tabelle:  sh neu.sh tabelle "Behandlungen pro Jahr"
"""
import csv
import io
import os
import re

ORDNER = "tabellen"
VERWEIS = re.compile(r"^\s*@#\s*([A-Za-z0-9][A-Za-z0-9._-]*)(?:\s+(quer|hoch))?\s*$", re.I)
ZAHL = re.compile(r"^[-+−]?\s*(?:CHF|Fr\.|EUR|€|\$)?\s*[\d'’ .,]*\d[\d'’ .,]*\s*(?:%|CHF|Fr\.|EUR|€|h|min|kg|km|m)?$")


def ordner(basis):
    return os.path.join(basis, ORDNER)


def alle(basis):
    """{name: pfad} aller CSV-Tabellen im Ordner tabellen/ (auch Unterordner)."""
    out = {}
    o = ordner(basis)
    if not os.path.isdir(o):
        return out
    for wurzel, unter, dateien in os.walk(o):
        unter[:] = sorted(u for u in unter if not u.startswith((".", "_")))
        for f in sorted(dateien):
            if f.lower().endswith(".csv") and not f.startswith((".", "_")):
                out.setdefault(f[:-4], os.path.join(wurzel, f))
    return out


def verweis(zeile):
    """(name, ausrichtung) für eine Zeile «@#name [quer|hoch]», sonst None."""
    m = VERWEIS.match(zeile)
    return (m.group(1), (m.group(2) or "").lower()) if m else None


def lies(pfad):
    """dict(titel, kopf, zeilen, quelle, fehler) – fehler = Liste von Meldungen (leer = in Ordnung)."""
    roh = open(pfad, encoding="utf-8-sig").read()
    zeilen_txt = [z for z in roh.replace("\r\n", "\n").replace("\r", "\n").split("\n")]
    while zeilen_txt and not zeilen_txt[-1].strip(";, \t"):
        zeilen_txt.pop()
    name = os.path.basename(pfad)
    if len(zeilen_txt) < 2:
        return dict(titel="", kopf=[], zeilen=[], quelle="", fehler=[f"{name}: zu kurz – Zeile 1 Bezeichnung, "
                                                                        "Zeile 2 Spaltenüberschriften, dann Werte."])
    trenner = ";" if zeilen_txt[1].count(";") >= zeilen_txt[1].count(",") else ","
    reihen = list(csv.reader(io.StringIO("\n".join(zeilen_txt)), delimiter=trenner))
    titel = " ".join(x.strip() for x in reihen[0] if x.strip())
    kopf = [x.strip() for x in reihen[1]]
    while kopf and not kopf[-1]:
        kopf.pop()
    werte, quelle, fehler = [], "", []
    for nr, r in enumerate(reihen[2:], 3):
        r = [x.strip() for x in r]
        if not any(r):
            continue
        if r[0].lower().startswith("quelle:") and not any(r[1:]):
            quelle = r[0]
            continue
        while len(r) > len(kopf) and not r[-1]:
            r.pop()
        if len(r) > len(kopf):
            fehler.append(f"{name}, Zeile {nr}: {len(r)} Werte, aber nur {len(kopf)} Spaltenüberschriften.")
        r += [""] * (len(kopf) - len(r))
        werte.append(r[:len(kopf)])
    if not kopf:
        fehler.append(f"{name}, Zeile 2: keine Spaltenüberschriften.")
    if not werte:
        fehler.append(f"{name}: keine Werte (ab Zeile 3).")
    return dict(titel=titel, kopf=kopf, zeilen=werte, quelle=quelle, fehler=fehler)


def ist_zahl(t):
    t = t.strip().replace("**", "")
    return bool(t) and bool(ZAHL.match(t))


def pruefe(basis, zeile):
    """Meldungen für eine Zeile «@#…» (leer = in Ordnung)."""
    v = verweis(zeile)
    if not v:
        return [f"«{zeile.strip()}»: Tabelle so angeben: @#name  (optional: @#name quer  oder  @#name hoch)"]
    vorhanden = alle(basis)
    if v[0] not in vorhanden:
        import difflib
        tipp = difflib.get_close_matches(v[0], list(vorhanden), n=1)
        return [f"Tabelle «@#{v[0]}» nicht gefunden (erwartet: tabellen/{v[0]}.csv)."
                + (f" Gemeint: @#{tipp[0]}?" if tipp else "")]
    return lies(vorhanden[v[0]])["fehler"]


def name_aus_titel(titel):
    t = titel.lower()
    for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss"), ("é", "e"), ("è", "e"), ("à", "a")):
        t = t.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:60].strip("-") or "tabelle"


def neu(basis, titel):
    """Neue Tabelle mit Muster anlegen. Gibt (name, pfad) zurück."""
    o = ordner(basis)
    os.makedirs(o, exist_ok=True)
    name = stamm = name_aus_titel(titel)
    n = 2
    while os.path.exists(os.path.join(o, name + ".csv")):
        name = f"{stamm}-{n}"; n += 1
    pfad = os.path.join(o, name + ".csv")
    with open(pfad, "w", encoding="utf-8") as f:
        f.write(f"{titel}\nSpalte 1;Spalte 2;Spalte 3\nWert;12;CHF 90\nWert;7;CHF 120\nQuelle: \n")
    return name, pfad
