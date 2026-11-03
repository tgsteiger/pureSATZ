#!/bin/sh
# Hörbuch im Ordner audio/ – ohne Menü:  sh hb.sh   (zeigt alle Befehle)
# Beispiele: sh hb.sh probe · sh hb.sh texte · sh hb.sh vertonen · sh hb.sh 0201 tempo=-5%
cd "$(dirname "$0")/.." || exit 1
P=python3; [ -x .venv/bin/python ] && P=.venv/bin/python
exec "$P" motor/audio/hoerbuch.py "$@"
