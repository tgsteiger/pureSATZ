#!/bin/sh
# Räumt den Buchordner auf: Zwischenspeicher, _backup/, *.backup, alte Motoren, stichworte-vorschlag.txt.
# Zeigt zuerst die Liste und fragt, bevor etwas gelöscht wird. md-history/ bleibt immer.
#   sh cleanup.sh            aufräumen
#   sh cleanup.sh ausgaben   zusätzlich die Ausgabeordner, auch alte (neu erstellen mit: sh build.sh final)
cd "$(dirname "$0")"
if [ -x .venv/bin/python3 ]; then PY=.venv/bin/python3; else PY=python3; fi
"$PY" motor/aufraeumen.py "$@"
