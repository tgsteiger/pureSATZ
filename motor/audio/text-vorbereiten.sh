#!/bin/bash
# Bereitet einen Text zum Vorlesen auf – gleich für alle Stimmen
# Aufruf: ./text-vorbereiten.sh datei.txt   (Ausgabe auf den Bildschirm)
DIR="$(cd "$(dirname "$0")" && pwd)"
DATEN="${AUDIO_DIR:-$DIR}"                     # Buch: audio/ (audio.conf, Aussprache)
source "$DATEN/audio.conf"
regeln="$DATEN/${AUSSPRACHE_DATEI:-$AUSSPRACHE}"; touch "$regeln"   # AUSSPRACHE_DATEI setzt txt2mp3-azure.py
jahr=1; grep -qiE '^# *jahreszahlen *: *aus' "$regeln" && jahr=0    # «# jahreszahlen: aus» = Stimme kann es selbst

# Absätze zu je einer Zeile, Satzpunkt am Ende
sed '/^ *#/d' "$1" | awk 'BEGIN{RS=""} {gsub(/\n/," "); if ($0 !~ /[.!?:;…"»«)]$/) $0=$0 "."; print}' \
  | sed -f <(sed -nE '/^[^#].*=/ s/^ *(.*[^ ]) *= *(.*[^ ]) *$/s|\\b\1\\b|\2|gI/p' "$regeln") \
  | { [ "$jahr" = 1 ] || { cat; exit; }; sed -E 's/\b(1[1-9])00\b/\1 hundert/g
            s/\b(1[1-9])0([1-9])\b/\1 hundert \2/g
            s/\b(1[1-9])([1-9][0-9])\b/\1 hundert \2/g
            s/\b2000\b/zweitausend/g
            s/\b200([1-9])\b/zweitausend \1/g
            s/\b20([1-9][0-9])\b/zweitausend \1/g'; } \
  | sed -E 's/ [–—] /, /g'
