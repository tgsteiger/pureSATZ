#!/bin/sh
# Neue Motor-Version freigeben: Änderungen zeigen, Selbsttest, GitHub, alle Bücher aktualisieren.
#   sh release.sh
cd "$(dirname "$0")"
python3 setup/release.py "$@"
