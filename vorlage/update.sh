#!/bin/sh
# Motor-Update: prüft auf GitHub, ob es einen neueren Motor gibt, und setzt ihn ein (Buch-Dateien bleiben).
#   sh update.sh            prüfen, Neuerungen zeigen, fragen, aktualisieren
#   sh update.sh pruefen    nur prüfen
#   sh update.sh ja         ohne Rückfrage
#   sh update.sh lokal      aus dem Ordner ../pureSATZ statt von GitHub
cd "$(dirname "$0")"
python3 motor/update.py "$@"
