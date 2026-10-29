#!/bin/sh
# Menü mit den häufigsten Befehlen: s schnell, k komplett, m MD öffnen, o PDF öffnen … (↑ = letzte Befehle)
cd "$(dirname "$0")"
if [ -x .venv/bin/python3 ]; then PY=.venv/bin/python3; else python3 motor/einrichten.py; PY=.venv/bin/python3; fi
"$PY" motor/menu.py "$@"
