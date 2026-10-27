#!/bin/sh
# pureSATZ starten (Linux): Rechtsklick in den Ordner pureSATZ → «Im Terminal öffnen», dann:  sh START-Linux.sh
# Führt in fünf Schritten durch: Technik, Ort, Hallo-Buch, eigenes Buch, Extras (siehe pc-einrichten/start.sh).
cd "$(dirname "$0")" && exec bash pc-einrichten/start.sh "$@"
