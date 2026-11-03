#!/bin/sh
# Hörbuch im Ordner audio/ – ohne Menü:  sh hb.sh   (zeigt alle Befehle)
# Beispiele: sh hb.sh probe · sh hb.sh woerter · sh hb.sh 0201 · sh hb.sh alles
cd "$(dirname "$0")/.." || exit 1
P=python3; [ -x .venv/bin/python ] && P=.venv/bin/python
exec "$P" motor/audio/hoerbuch.py "$@"
