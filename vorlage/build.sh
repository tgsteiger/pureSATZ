#!/bin/sh
# Buch bauen. Vorher werden die MD-Dateien gesichert (md-history/) und geprüft.
#   sh build.sh                 alles als Entwurf: Bildschirm-PDF, Druckdateien, E-Book
#   sh build.sh final           alles als Druckfassung (für epubli)
#   sh build.sh komplett        final + Leseprobe + Korrektur in einem Durchgang
#   sh build.sh schnell         nur Lese-PDFs, so schnell wie möglich (beim Schreiben, ca. halbe Zeit)
#   sh build.sh nur-pdf         nur Bildschirm-PDFs mit Booklet und Statistik
#   sh build.sh nur-pdf final   nur Bildschirm-PDFs als Druckfassung + Booklets zum Selberdrucken
#   sh build.sh leseprobe       Leseprobe: Umschlag, Titelei, erste Kapitel (Variable «leseprobe»)
#   sh build.sh leseprobe uz 18,20,23   einmalig diese Seiten, nur diese Fassung
#   sh build.sh personen [Name]  Personen mit Seiten (personen-seiten.txt) · mit Name: check_Name_Gegenlesen.pdf
#   sh build.sh stand "Name"  Stand festhalten · sh build.sh aenderungen  was seither geändert ist (PDF)
#   sh build.sh korrektur       Korrekturfassung: A4, Zeilennummern, Rand für Notizen
#   sh build.sh nur-druck [final] / nur-ebook [final] / pruefen / sicherung (nur MD nach md-history/)
# Ganzes Buch als ZIP sichern: sh sicherung.sh
# Beim ersten Mal wird die Python-Umgebung .venv eingerichtet (braucht Internet).
set -e
cd "$(dirname "$0")"
if [ -x .venv/bin/python3 ]; then PY=.venv/bin/python3; else python3 motor/einrichten.py; PY=.venv/bin/python3; fi
"$PY" motor/bauen.py "$@"
