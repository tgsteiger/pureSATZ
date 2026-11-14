#!/usr/bin/env python3
"""Test für motor/rohdaten2cover.py (ab 2.82): Rohdaten verschiedener Druckereien lesen, Werte prüfen, Ablauf.
Aufruf im Ordner pureSATZ: python3 test/rohdaten2cover-test.py  → «ROHDATEN2COVER IN ORDNUNG»"""
import datetime
import difflib
import os
import re
import sys
import tempfile

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HIER, "..", "motor"))
import rohdaten2cover as R  # noqa: E402

VORL = open(os.path.join(HIER, "..", "vorlage", "druck", "tredition-a5-hardcover.md"), encoding="utf-8").read()
EPUB = open(os.path.join(HIER, "..", "vorlage", "druck", "epubli-a5.md"), encoding="utf-8").read()
K = "\n## Coverrechner (Rohdaten)"
TRED_ROH = """DruckvorgabeHardcover
Innen unbedruckt, Veredelung Matt
Gesamtformat: 34,74 x 25,00cm
Format des Buches festlegen
In diesem Format enthalten sind: 1,70cm Beschnitt.
Dieser Beschnitt wird während der Produktion von uns entfernt. Bitte lege Hintergründe immer bis an den Rand
deines Gesamtformats an, um weiße Seitenränder zu vermeiden.
Vorder- und Rückseite
Diese Seiten sind in den Maßen identisch.
Ohne Beschnittrand beträgt die Größe: 31,34 x 21,60cm
Gesamtbreite: 34,74cm
inkl. 1,70cm Beschnitt
Rückseite
15,30cm
Vorderseite
15,30cm
Buchrücken
0,74cm
Falz 0,80cm
Falz 0,80cm
Beschnittrand 1,70cm
Gesamthöhe: 25,00cm
inkl. 1,70cm Beschnitt"""
EPUB_ROH = """Covermaße für folgende Ausstattung

Format: DIN A5 hoch
Bindung: Hardcover
Papier: 140-150 g weiß, matt
Seitenzahl: 84
Gesamthöhe: 250 mm
Gesamtbreite: 345 mm

Ihr
Buch
11 mm
157 mm
9 mm
157 mm
11 mm
11 mm
228 mm
11 mm

Gesamtbreite: 345mm | Gesamthöhe: 250mm | Beschnitt: 11mm | Rücken: 9mm
Details zum Beschnitt können Sie in unserem Hilfebereich nachlesen."""
A5 = (148, 210)
J = datetime.datetime(2026, 11, 14, 10, 42)
ERLAUBT = {"ruecken-hardcover", "ruecken-softcover", "beschnitt-hardcover", "beschnitt-softcover", "deckel-hardcover",
           "neu-berechnen", "neu-berechnet", "berechnet-fuer-seiten", "berechnet-am", "papier"}
ORD = tempfile.mkdtemp(prefix="r2c-")
os.makedirs(os.path.join(ORD, "druck"))
fehler = 0


def mit(basis, roh, **kopf):
    t = basis.split(K)[0] + K + "\n> Hinweis\n" + roh + "\n\n## Notizen\n> x\n"
    for k, v in kopf.items():
        k = k.replace("_", "-")
        t = re.sub(rf"^\{{{k}\}}:.*$", f"{{{k}}}: {v}", t, flags=re.M)
    return t


def g(t, k):
    m = re.search(rf"^\{{{k}\}}:[ \t]*(.*)$", t, re.M)
    return m.group(1) if m else None


def datei(name, text):
    p = os.path.join(ORD, "druck", name + ".md")
    open(p, "w", encoding="utf-8").write(text)
    return p


def lauf(name, pfad, n, soll, pruef=None, seite=A5):
    global fehler
    vor = open(pfad, encoding="utf-8").read()
    stufe, msg = R.auto(pfad, n, seite, jetzt=J)
    nach = open(pfad, encoding="utf-8").read()
    d = [z for z in difflib.unified_diff(vor.split("\n"), nach.split("\n"), n=0, lineterm="")
         if z[:1] in "+-" and z[:3] not in ("+++", "---")]
    namen = {m.group(1) for z in d for m in [re.match(r"[+-]\{([a-z-]+)\}", z)] if m}
    gut = stufe == soll and namen <= ERLAUBT and all(re.match(r"[+-](\{|>|$)", z) for z in d)
    gut = gut and g(nach, "neu-berechnet") == ("nein" if soll == "warnung" else "ja") and g(nach, "neu-berechnen") is None
    if pruef:
        gut = gut and pruef(nach)
    fehler += not gut
    print(("OK   " if gut else "FEHL ") + f"{name:44} [{stufe}] {msg}")


# Ablauf wie beim Probedruck: alte Datei (bis 2.81) mit Rohdaten für 68 Seiten, Buchblock jetzt 70
p = datei("ablauf", mit(VORL, TRED_ROH, neu_berechnen="ja", berechnet_fuer_seiten="68", ruecken_hardcover="7.4",
                        beschnitt_hardcover="17", deckel_hardcover="153x216"))
lauf("1 alte Datei, alte Rohdaten (68), Buchblock 70", p, 70, "warnung",
     lambda t: g(t, "berechnet-fuer-seiten") == "68" and g(t, "ruecken-hardcover") == "7.4" and "#" in g(t, "berechnet-am")
     and "«Coverwerte übernehmen»" not in t)
lauf("2 nochmals, nichts geändert", p, 70, "warnung", lambda t: g(t, "berechnet-fuer-seiten") == "68")
t = open(p, encoding="utf-8").read()
open(p, "w", encoding="utf-8").write(t.split(K)[0] + K + "\n" + TRED_ROH.replace("34,74", "34,76").replace("0,74cm", "0,76cm"))
lauf("3 neue Rohdaten (Rücken 7,6)", p, 70, "neu",
     lambda t: g(t, "berechnet-fuer-seiten") == "70" and g(t, "ruecken-hardcover") == "7.6" and g(t, "deckel-hardcover") == "153x216")
lauf("4 nochmals bauen", p, 70, "passt")
lauf("5 Buchblock wächst auf 72", p, 72, "warnung", lambda t: g(t, "berechnet-fuer-seiten") == "70")
t = open(p, encoding="utf-8").read()
open(p, "w", encoding="utf-8").write(re.sub(r"^\{berechnet-fuer-seiten\}:.*$", "{berechnet-fuer-seiten}: 72", t, flags=re.M))
lauf("6 gleicher Text, Seiten von Hand auf 72", p, 72, "passt")
# Druckereien und Fälle
lauf("7 Vorlage, erstes Mal (68)", datei("v", mit(VORL, TRED_ROH)), 68, "neu",
     lambda t: (g(t, "ruecken-hardcover"), g(t, "beschnitt-hardcover"), g(t, "deckel-hardcover")) == ("7.4", "17", "153x216"))
lauf("8 tredition 220 Seiten", datei("t220", mit(VORL, TRED_ROH.replace("34,74", "36,30").replace("0,74cm", "2,30cm"))), 220, "neu",
     lambda t: g(t, "ruecken-hardcover") == "23")
lauf("9 tredition andere Wörter", datei("tw", mit(VORL, "Rückenbreite: 1,12 cm\nGesamtbreite 35,12 cm\nGesamthöhe 25 cm\nBeschnitt 1,7 cm")),
     104, "neu", lambda t: g(t, "ruecken-hardcover") == "11.2" and g(t, "deckel-hardcover") == "153x216")
lauf("10 tredition in mm mit Punkt", datei("tmm", mit(VORL, "Gesamtformat: 351.4 x 250.0 mm\nBuchrücken: 11.4 mm\nBeschnittrand: 17 mm\nVorderseite: 153 mm")),
     120, "neu", lambda t: g(t, "ruecken-hardcover") == "11.4")
lauf("11 epubli 84 (mit Papier)", datei("e84", mit(EPUB, EPUB_ROH)), 84, "neu",
     lambda t: (g(t, "ruecken-hardcover"), g(t, "beschnitt-hardcover"), g(t, "deckel-hardcover")) == ("9", "11", "157x228")
     and g(t, "papier").startswith("140-150"))
lauf("12 epubli 84, Buchblock 86", datei("e86", mit(EPUB, EPUB_ROH)), 86, "warnung", lambda t: g(t, "ruecken-hardcover") == "")
lauf("13 epubli 240", datei("e240", mit(EPUB, EPUB_ROH.replace("84", "240").replace("345", "362").replace("Rücken: 9mm", "Rücken: 26mm"))),
     240, "neu", lambda t: g(t, "ruecken-hardcover") == "26")
lauf("14 epubli Softcover", datei("es", mit(EPUB, "Seitenzahl: 210\nGesamtbreite: 315mm | Gesamthöhe: 216mm | Beschnitt: 3mm | Rücken: 13mm",
                                          bindung="softcover")), 210, "neu", lambda t: g(t, "ruecken-softcover") == "13")
lauf("15 BoD-Stil", datei("bod", mit(VORL, "Umschlag gesamt 348,7 x 250 mm\nRückenbreite 8,7 mm\nEinschlag 17 mm", plattform="bod")),
     80, "neu", lambda t: g(t, "ruecken-hardcover") == "8.7")
lauf("16 KDP englisch, Zoll, 6x9", datei("kdp", mit(VORL, "Page count: 240\nSpine width: 0.535 in\nFull cover width: 12.785 in\n"
                                                    "Full cover height: 9.25 in\nBleed: 0.125 in", bindung="softcover")),
     240, "neu", lambda t: g(t, "ruecken-softcover") == "13.6", seite=(152.4, 228.6))
lauf("17 Rohdaten A5, Buch Taschenbuch", datei("tb", mit(VORL, TRED_ROH)), 68, "warnung", seite=(120, 190))
lauf("18 nur Notizen", datei("notiz", mit(VORL, "wie normale Fassung (Deckel 15,30 x 21,60 cm, 1,70 cm Beschnitt); Rücken nachsehen")),
     86, "warnung")
lauf("19 Unsinn", datei("x", mit(VORL, "Bitte Datei hochladen. Preis 24,90 EUR")), 70, "warnung")
lauf("20 Vorderseite widerspricht", datei("vw", mit(VORL, TRED_ROH.replace("Vorderseite\n15,30cm", "Vorderseite\n14,80cm"))), 68, "warnung")
lauf("21 keine Rohdaten, Werte von Hand passen", datei("hand", mit(VORL, "", berechnet_fuer_seiten="68", neu_berechnen="nein")), 68, "passt")
lauf("22 Datei ohne Kopfzeilen", datei("ohne", re.sub(r"^\{(neu-berechnen|berechnet-fuer-seiten)\}:.*\n", "", mit(VORL, TRED_ROH), flags=re.M)),
     68, "neu", lambda t: g(t, "berechnet-am") and g(t, "berechnet-fuer-seiten") == "68")
p = datei("test", mit(VORL, TRED_ROH))
vor = open(p, encoding="utf-8").read()
R.auto(p, 68, A5, schreiben=False)
ok = open(p, encoding="utf-8").read() == vor
fehler += not ok
print(("OK   " if ok else "FEHL ") + "23 Testlauf (schreiben=False) ändert nichts")
hist = os.path.join(ORD, "md-history", "druck")
ok = os.path.isdir(hist) and any(f.startswith("ablauf_") for f in os.listdir(hist))
fehler += not ok
print(("OK   " if ok else "FEHL ") + "24 Sicherung in md-history/druck/")
print("\nROHDATEN2COVER IN ORDNUNG" if not fehler else f"\n{fehler} FEHLER")
sys.exit(1 if fehler else 0)
