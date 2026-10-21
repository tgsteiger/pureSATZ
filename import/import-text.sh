#!/bin/sh
# LibreOffice- oder Word-Dokument (.odt / .docx) als neues Buch anlegen – neben dem Ordner pureSATZ (Testphase).
#   sh import/import-text.sh manuskript.odt
#   sh import/import-text.sh ~/Dokumente/manuskript.docx --autor "Vorname Nachname" --name Mein-Buch
python3 "$(dirname "$0")/import-text.py" "$@"
