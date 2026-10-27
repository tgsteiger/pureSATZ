#!/bin/sh
# Hallo-Buch: Beispielbuch anlegen, bauen und das PDF öffnen – der erste Blick auf pureSATZ (siehe START.md).
#   sh hallo.sh            im Ordner pureSATZ
cd "$(dirname "$0")"
if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 fehlt. Zuerst einrichten: sh START-Linux.sh (Mac: START-Mac.command doppelklicken) – siehe START.md"
  exit 1
fi
python3 setup/hallo.py "$@"
