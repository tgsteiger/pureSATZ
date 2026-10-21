#!/bin/sh
# Neues Buch anlegen oder Motor aktualisieren – siehe setup.py (im Ordner pureSATZ aufrufen)
#   sh setup/setup.sh                     fragt alles ab
#   sh setup/setup.sh start.txt           Werte aus start.txt
#   sh setup/setup.sh motor ../Buch       nur den Motor eines Buchs aktualisieren
python3 "$(dirname "$0")/setup.py" "$@"
