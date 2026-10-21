#!/bin/sh
# Buchdaten mit GitHub abgleichen (am Anfang und am Ende der Arbeit): eigene Änderungen hochladen, fremde holen.
# Einmalig einrichten: siehe motor/sync.py oben (git init, gh repo create … --private).
cd "$(dirname "$0")"
if [ -x .venv/bin/python3 ]; then PY=.venv/bin/python3; else PY=python3; fi
"$PY" motor/sync.py "$@"
