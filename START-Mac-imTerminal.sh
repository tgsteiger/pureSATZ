#!/bin/sh
# pureSATZ starten (Mac): Terminal öffnen (Cmd+Leertaste, «Terminal», Enter), «sh » tippen (mit Leerzeichen),
# diese Datei ins Fenster ziehen, Enter. Führt in fünf Schritten durch: Technik, Ort, Hallo-Buch, eigenes Buch, Extras.
# (Doppelklick geht nicht: der Mac sperrt heruntergeladene Startdateien.)
cd "$(dirname "$0")" && exec bash pc-einrichten/start.sh "$@"
