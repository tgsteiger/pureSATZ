#!/bin/sh
# Ganzes Buch als ZIP sichern: <buchname>_JJJJMMTTHHMMSS.zip (ohne Zwischenspeicher; von den Ausgaben nur die Bildschirm-PDFs).
# Ziele in der Variablen-Datei unter # TECHNIK: sicherung-lokal, sicherung-cloud.
#   sh sicherung.sh               an alle eingetragenen Ziele
#   sh sicherung.sh lokal         nur lokal
#   sh sicherung.sh cloud         nur in die Cloud
#   sh sicherung.sh lokal cloud   an beide
cd "$(dirname "$0")"
if [ -x .venv/bin/python3 ]; then PY=.venv/bin/python3; else PY=python3; fi
"$PY" motor/sicherung.py "$@"
