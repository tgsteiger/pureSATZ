#!/bin/bash
# =====================================================================
#  pureSATZ starten (Linux und Mac), im Ordner pureSATZ:   sh start.sh
#  Mac: start.command doppelklicken (blockiert der Mac es: Rechtsklick → Öffnen,
#  oder Systemeinstellungen → Datenschutz & Sicherheit → «Dennoch öffnen»).
#  1. Ort: schlägt ~/Buchprojekte vor und kopiert pureSATZ dorthin
#  2. Computer einrichten (pc-einrichten/…)
#  3. Hallo-Buch ansehen, eigenes Buch anlegen, GitHub (freiwillig)
#  Darf beliebig oft laufen. Mit git geholt oder schon in Buchprojekte: kein Kopieren.
# =====================================================================
[ -n "$BASH_VERSION" ] || exec bash "$0" "$@"          # «sh start.sh» auch auf Linux Mint (dash)
cd "$(dirname "$0")" || exit 1
HIER="$(pwd)"
MAC=""; [ "$(uname)" = "Darwin" ] && MAC=1

echo "=== pureSATZ ==="
echo

if [ ! -f motor/bauen.py ]; then
    echo "Das ZIP ist nicht vollständig ausgepackt. Bitte ganz auspacken und"
    echo "start.sh im ausgepackten Ordner nochmals starten."
    exit 1
fi

oeffne() { if [ -n "$MAC" ]; then open "$1"; else xdg-open "$1" >/dev/null 2>&1 & fi; }

# --- 1. Ort für die Buchprojekte ----------------------------------------
if [ "$1" != "--hier" ] && [ ! -d .git ] && [ "$(basename "$(dirname "$HIER")")" != "Buchprojekte" ]; then
    ZIEL="$HOME/Buchprojekte"
    echo "pureSATZ liegt in:  $HIER"
    echo "Deine Bücher entstehen neben pureSATZ. Empfohlen ist ein fester Ort –"
    echo "nicht Downloads oder Schreibtisch und nicht in einer Cloud (iCloud, OneDrive …)."
    echo
    read -r -p "Ort für Buchprojekte [$ZIEL], n = hier bleiben: " ORT
    case "$ORT" in
        n|nein) ;;
        *)
            [ -n "$ORT" ] && ZIEL="${ORT/#\~/$HOME}"
            if [ "$ZIEL/pureSATZ" != "$HIER" ]; then
                mkdir -p "$ZIEL" || { echo "Ordner $ZIEL geht nicht – anderen Ort wählen."; exit 1; }
                NEU="$(cat motor/VERSION)"
                if [ -f "$ZIEL/pureSATZ/motor/VERSION" ]; then
                    ALT="$(cat "$ZIEL/pureSATZ/motor/VERSION")"
                    echo
                    echo "pureSATZ $ALT ist dort schon vorhanden (diese Version: $NEU)."
                    read -r -p "Ersetzen? Die alte bleibt als pureSATZ-alt-$ALT. [j/n] (j): " ERS
                    case "$ERS" in
                        ""|j|ja)
                            A="$ZIEL/pureSATZ-alt-$ALT"
                            [ -e "$A" ] && A="$A-$(date +%H%M%S)"
                            mv "$ZIEL/pureSATZ" "$A" || exit 1
                            echo "OK  alte Version: $A" ;;
                        *)
                            exec bash "$ZIEL/pureSATZ/start.sh" --hier ;;
                    esac
                fi
                echo "pureSATZ wird nach $ZIEL/pureSATZ kopiert …"
                cp -R "$HIER" "$ZIEL/pureSATZ" || { echo "Kopieren ging nicht."; exit 1; }
                rm -rf "$ZIEL/pureSATZ/.venv"
                echo "OK  kopiert."
                # Mac: «Terminal hier» – Doppelklick öffnet das Terminal in diesem Ordner
                if [ -n "$MAC" ] && [ ! -e "$ZIEL/Terminal hier.command" ]; then
                    printf '#!/bin/sh\ncd "$(dirname "$0")" && exec "${SHELL:-/bin/zsh}" -l\n' > "$ZIEL/Terminal hier.command"
                    chmod +x "$ZIEL/Terminal hier.command"
                fi
                oeffne "$ZIEL"
                echo
                echo "Ab jetzt geht es in $ZIEL/pureSATZ weiter."
                echo "Den Ordner $HIER darfst du nach dem Einrichten löschen."
                echo
                exec bash "$ZIEL/pureSATZ/start.sh" --hier
            fi ;;
    esac
fi

# --- 2. Computer einrichten, Hallo-Buch, eigenes Buch ---------------------
if [ -n "$MAC" ]; then
    exec bash pc-einrichten/mac-einrichten.sh
else
    exec bash pc-einrichten/linux-einrichten.sh
fi
