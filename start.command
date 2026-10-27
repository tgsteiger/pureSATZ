#!/bin/sh
# pureSATZ starten (Mac): Doppelklick. Ort, Einrichten, Hallo-Buch, eigenes Buch – siehe start.sh.
# Blockiert der Mac es: Rechtsklick → Öffnen, oder Systemeinstellungen → Datenschutz & Sicherheit → «Dennoch öffnen».
cd "$(dirname "$0")" && exec bash start.sh "$@"
