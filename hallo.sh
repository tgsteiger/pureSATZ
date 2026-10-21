#!/bin/sh
# Hallo-Buch: Beispielbuch anlegen, bauen und das PDF öffnen – der erste Blick auf pureSATZ (siehe START.md).
#   sh hallo.sh            im Ordner pureSATZ
cd "$(dirname "$0")"
if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 fehlt. Zuerst einrichten: bash pc-einrichten/linux-einrichten.sh (Mac: mac-einrichten.sh) – siehe START.md"
  exit 1
fi
python3 setup/hallo.py "$@"
