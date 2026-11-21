#!/bin/sh
# Buch bauen (vorher: MD sichern nach md-history/ und prüfen). Beispiele: sh build.sh · sh build.sh final · sh build.sh schnell
# Alle Befehle: sh build.sh befehle  (oder im Menü: sh menu.sh). Ganzes Buch als ZIP: sh sicherung.sh
# Beim ersten Mal wird die Python-Umgebung .venv eingerichtet (braucht Internet).
set -e
cd "$(dirname "$0")"
if [ -x .venv/bin/python3 ]; then PY=.venv/bin/python3; else python3 motor/einrichten.py; PY=.venv/bin/python3; fi
"$PY" motor/bauen.py "$@"
