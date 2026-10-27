#!/bin/sh
# pureSATZ starten (Mac): Doppelklick. Führt in fünf Schritten durch: Technik, Ort, Hallo-Buch, eigenes Buch, Extras.
# Blockiert der Mac es: Rechtsklick → Öffnen, oder Systemeinstellungen → Datenschutz & Sicherheit → «Dennoch öffnen».
cd "$(dirname "$0")" && exec bash pc-einrichten/start.sh "$@"
