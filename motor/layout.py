# =====================================================================
#  LAYOUT – so sieht das Buch aus.
#  Nur die Werte ändern, die Namen links stehen lassen.
#  Farben: Name aus FARBEN (z. B. "haupt") oder direkt "#RRGGBB".
#  Grössen in Punkt (pt), Ränder und Bildbreiten in Millimetern (mm).
#  Nach einer Änderung:  sh build.sh nur-pdf   (oder sh build.sh final)
# =====================================================================

# --- Schriften ---------------------------------------------------------
# Name -> Datei. Gesucht wird zuerst im Ordner fonts/ des Buchs, dann in motor/fonts/.
# Eigene Schrift: .ttf-Dateien nach fonts/ kopieren und hier eintragen.
SCHRIFTDATEIEN = {
    "Lora":             "Lora-Regular.ttf",
    "Lora-Fett":        "Lora-Bold.ttf",
    "Lora-Kursiv":      "Lora-Italic.ttf",
    "Lora-FettKursiv":  "Lora-BoldItalic.ttf",
    "Poppins":          "Poppins-Regular.ttf",
    "Poppins-Leicht":   "Poppins-Light.ttf",
    "Poppins-Mittel":   "Poppins-Medium.ttf",
    "Poppins-Fett":     "Poppins-Bold.ttf",
}

# Welche Schrift für welche Aufgabe
SCHRIFT = dict(
    text="Lora",                    # Fliesstext
    text_fett="Lora-Fett",          # **fett** im Text
    text_kursiv="Lora-Kursiv",      # Zitate, Notizen, Untertitel
    text_fettkursiv="Lora-FettKursiv",
    titel="Poppins-Mittel",         # Überschriften
    titel_fett="Poppins-Fett",      # Buchrücken, Stempel
    titel_leicht="Poppins-Leicht",  # Kopfzeile, Seitenzahlen, kleine Zeilen
    titel_normal="Poppins",         # Autorname auf dem Umschlag
)

# --- Farben ---------------------------------------------------------------
FARBEN = dict(
    text="#2E2A26",        # Fliesstext
    leise="#6E655C",       # Notizen, Untertitel, Kopfzeile
    haupt="#1E428A",       # Überschriften, Zitate
    akzent="#B8873B",      # Linien, Jahreszahlen, Links
    papier="#FBF6EC",      # Hintergrund Umschlag und Teil-Seiten
    kasten="#EEF2F9",      # Hintergrund der Kästen (::: uz)
    linie="#E3D8C4",       # feine Linien (Zeitstrahl, Notizseiten)
    offen="#FFF4C2",       # Hintergrund «::: offen» im Entwurf
    offen_linie="#D9A800", # Rand und Kopf «::: offen»
    platzhalter="#C0392B", # «::: offen-notiz» im Entwurf
    stempel="#A8322A",     # Stempel der zweiten Ausgabe auf dem Umschlag
)

# --- Seite -------------------------------------------------------------------
# Das Format (a5, taschenbuch, sachbuch, a4, quadrat) steht oben in der Buch-MD: «format: a5».
# Ränder: None = passend zum Format. Eigene Werte in mm überschreiben das.
SEITE = dict(
    rand_innen=None, rand_aussen=None, rand_oben=None, rand_unten=None,
    hintergrund=None,      # Hintergrund normaler Seiten: None = weiss, oder Farbe
)

# --- Text --------------------------------------------------------------------
# groesse / zeilenabstand: None = passend zum Format (A5: 10.2 / 15.2 pt)
TEXT = dict(groesse=None, zeilenabstand=None, abstand_nach=6.5, farbe="text",
            blocksatz=True)
KAPITEL = dict(schrift="titel", groesse=13.5, zeilenabstand=18, farbe="haupt",   # ## Kapitel
               abstand_vor=16, abstand_nach=8)
ZWISCHENTITEL = dict(schrift="titel", groesse=11.5, zeilenabstand=15, farbe="haupt",   # ### Zwischentitel
                     abstand_vor=16, abstand_nach=6)
ZITAT = dict(schrift="text_kursiv", groesse=12, zeilenabstand=17.5, farbe="haupt")     # > Zitat
NOTIZ = dict(schrift="text_kursiv", farbe="leise")                                     # ~ Randbemerkung
KOPFZEILE = dict(schrift="titel_leicht", groesse=7.5, farbe="leise")                   # auch Seitenzahl

# --- Teil-Seiten (# Teil 1|Titel|Untertitel) --------------------------------------
TEIL = dict(
    hintergrund="papier",
    bild="verzierung-hell.png",   # Bild über dem Titel (Ordner bilder/ oder fotos/), None = keines
    bild_breite=72,               # mm
    nummer_schrift="titel_leicht", nummer_groesse=10, nummer_farbe="akzent",
    titel_schrift="titel", titel_groesse=26, titel_farbe="haupt",
    untertitel_schrift="text_kursiv", untertitel_groesse=13, untertitel_farbe="leise",
)
# Ein eigenes Bild für einen einzelnen Teil: im Manuskript als 4. Angabe,
#   # Teil 2|Titel|Untertitel|berge.jpg

# --- Verzierung (Zitate, @ZIER, Motto, Mitte-Blöcke) --------------------------------
# Eigenes Bild fürs ganze Buch: in der MD «zier: bild.png» (und «zier-hell: bild-hell.png»).
VERZIERUNG = dict(bild="verzierung.png", hell="verzierung-hell.png", linie="akzent")

# --- Umschlag ------------------------------------------------------------------------
UMSCHLAG = dict(
    hintergrund="papier",
    bild="verzierung.png", bild_breite=52,      # grosses Bild oben, None = keines
    titel_groesse=24, titel_farbe="haupt",
    untertitel_groesse=12, untertitel_farbe="leise",
    autor_groesse=12, autor_farbe="text",
)
