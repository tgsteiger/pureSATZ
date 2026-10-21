#!/bin/sh
# Geschichten sammeln (pureSATZ 2.11):
#   sh neu.sh "Titel der Geschichte"   neue Geschichte in geschichten/ anlegen
#   sh neu.sh                          Übersicht aller Geschichten (auch als geschichten-uebersicht.html)
cd "$(dirname "$0")"
if [ -x .venv/bin/python3 ]; then PY=.venv/bin/python3; else python3 motor/einrichten.py; PY=.venv/bin/python3; fi
"$PY" motor/geschichten.py "$@"
