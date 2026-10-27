#!/bin/bash
# =====================================================================
#  pureSATZ einrichten, in fünf Schritten (Linux und Mac).
#  Aufruf über START-Linux.sh (sh START-Linux.sh) bzw. START-Mac.command (Doppelklick).
#    1. Technik (Python …)   2. Ort für die Bücher   3. Hallo-Buch
#    4. Dein eigenes Buch    5. Fertig und Extras (Ghostscript, GitHub – freiwillig)
#  Die Technik und die Extras stehen in linux-einrichten.sh bzw. mac-einrichten.sh.
#  Darf beliebig oft laufen. --weiter = nach dem Kopieren an den festen Ort.
# =====================================================================
[ -n "$BASH_VERSION" ] || exec bash "$0" "$@"          # auch mit «sh …» (Linux Mint: dash)
cd "$(dirname "$0")/.." || exit 1                     # Ordner pureSATZ
HIER="$(pwd)"
OBEN="$(dirname "$HIER")"
if [ "$(uname)" = "Darwin" ]; then MAC=1; OS=mac; START="START-Mac.command"; else MAC=""; OS=linux; START="START-Linux.sh"; fi

titel() { clear; echo "=============================================================="; echo "  $1"
          echo "=============================================================="; echo; }
weiter() { echo; read -r -p "Weiter mit Enter … " _; }
oeffne() { if [ -n "$MAC" ]; then open "$1"; else xdg-open "$1" >/dev/null 2>&1 & fi; }

if [ ! -f motor/bauen.py ]; then
    echo "Das ZIP ist nicht vollständig ausgepackt. Bitte ganz auspacken und $START im"
    echo "ausgepackten Ordner nochmals starten."
    exit 1
fi

# --- Willkommen -----------------------------------------------------------
if [ "$1" != "--weiter" ]; then
    titel "pureSATZ – Willkommen"
    echo "Das passiert jetzt, in fünf Schritten:"
    echo
    echo "  1. Technik einrichten       Python, einmalig"
    echo "  2. Ort für deine Bücher     ein fester Ordner – nicht Downloads"
    echo "  3. Hallo-Buch               ein Beispielbuch zum Anschauen"
    echo "  4. Dein eigenes Buch        leer, mit deinem Titel und Namen"
    echo "  5. Fertig                   Extras wie GitHub sind freiwillig"
    echo
    echo "Bei jeder Frage nimmt Enter den Vorschlag."
    weiter
fi

# --- Schritt 1: Technik ---------------------------------------------------
titel "Schritt 1 von 5 – Technik einrichten"
echo "pureSATZ braucht Python (3.10 oder neuer). Fehlt etwas, wird es jetzt installiert."
echo
bash "pc-einrichten/$OS-einrichten.sh" --technik || exit 1
sleep 2

# --- Schritt 2: Ort ---------------------------------------------------------
if [ "$1" != "--weiter" ]; then
    titel "Schritt 2 von 5 – Ort für deine Bücher"
    if [ -d .git ]; then
        echo "pureSATZ wurde mit git geholt und bleibt, wo es ist:"
        echo "  $HIER"
    elif [ "$(basename "$OBEN")" = "Buchprojekte" ]; then
        echo "pureSATZ liegt schon am festen Ort:"
        echo "  $HIER"
    else
        ZIEL="$HOME/Buchprojekte"
        echo "pureSATZ liegt jetzt in:  $HIER"
        echo "Deine Bücher entstehen neben pureSATZ. Besser ist ein fester Ort –"
        echo "nicht Downloads, nicht Schreibtisch, nicht in einer Cloud (iCloud, OneDrive …)."
        echo
        echo "Vorschlag:  $ZIEL"
        echo
        echo "  Enter oder j  = Vorschlag übernehmen"
        echo "  anderer Pfad  = eintippen (oder Ordner ins Fenster ziehen)"
        echo "  n             = hier lassen"
        echo
        read -r -p "Deine Wahl: " ORT
        ORT="${ORT//\'/}"; ORT="${ORT//\"/}"; ORT="${ORT//\\ / }"; ORT="${ORT%"${ORT##*[![:space:]]}"}"
        case "$ORT" in
            n|nein) echo "pureSATZ bleibt hier:"; echo "  $HIER" ;;
            *)
                case "$ORT" in ""|j|ja) ;; *) ZIEL="${ORT/#\~/$HOME}" ;; esac
                if [ "$ZIEL/pureSATZ" != "$HIER" ]; then
                    mkdir -p "$ZIEL" || { echo "Ordner $ZIEL geht nicht – $START nochmals starten, anderen Ort wählen."; exit 1; }
                    NEU="$(cat motor/VERSION)"
                    if [ -f "$ZIEL/pureSATZ/motor/VERSION" ]; then
                        ALT="$(cat "$ZIEL/pureSATZ/motor/VERSION")"
                        echo
                        echo "pureSATZ $ALT ist dort schon vorhanden (diese Version: $NEU)."
                        read -r -p "Ersetzen? Die alte bleibt als pureSATZ-alt-$ALT. [Enter = ja, n = die vorhandene nehmen]: " ERS
                        case "$ERS" in
                            ""|j|ja)
                                A="$ZIEL/pureSATZ-alt-$ALT"
                                [ -e "$A" ] && A="$A-$(date +%H%M%S)"
                                mv "$ZIEL/pureSATZ" "$A" || exit 1
                                echo "OK  alte Version: $A" ;;
                            *)
                                exec bash "$ZIEL/pureSATZ/pc-einrichten/start.sh" --weiter ;;
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
                    echo "Den Ordner $HIER darfst du am Schluss löschen."
                    weiter
                    exec bash "$ZIEL/pureSATZ/pc-einrichten/start.sh" --weiter
                fi ;;
        esac
    fi
    echo "Deine Bücher entstehen daneben, in $OBEN"
    weiter
fi

# --- Schritt 3: Hallo-Buch ----------------------------------------------------
titel "Schritt 3 von 5 – Hallo-Buch"
python3 setup/hallo.py --kette             # erklärt, fragt, baut, öffnet Ordner und PDF
weiter

# --- Schritt 4: Dein eigenes Buch ---------------------------------------------
titel "Schritt 4 von 5 – Dein eigenes Buch"
python3 setup/setup.py --kette             # fragt Titel, Untertitel, Autor, Format, öffnet den Buchordner
weiter

# --- Schritt 5: Fertig und Extras ---------------------------------------------
titel "Schritt 5 von 5 – Fertig und Extras"
echo "Zwei Extras – beide freiwillig, beide gehen auch später ($START nochmals starten)."
bash "pc-einrichten/$OS-einrichten.sh" --extras
GH=$?                                       # 10 = mit GitHub

echo
echo "=============================================================="
echo "  Fertig – so sieht es jetzt aus:"
echo "=============================================================="
echo
echo "  $OBEN/"
for d in "$OBEN"/*/; do
    n="$(basename "$d")"
    case "$n" in
        "$(basename "$HIER")") t="die Werkstatt – hier nichts schreiben" ;;
        pureSATZ-alt-*)        t="alte Version – darf weg" ;;
        Hallo-Buch)            t="zum Ausprobieren – darf weg" ;;
        *) [ -f "$d/build.sh" ] || continue; t="dein Buch – hier schreibst und baust du" ;;
    esac
    printf "    %-24s %s\n" "$n/" "$t"
done
echo
echo "Geschrieben und gebaut wird im Ordner deines Buchs – nie in pureSATZ."
if [ -n "$MAC" ]; then
    echo "Im Buchordner «Terminal hier» doppelklicken, dann:"
else
    echo "Im Buchordner Rechtsklick → «Im Terminal öffnen», dann:"
fi
echo "  sh build.sh schnell     Lese-PDF ansehen, in Sekunden"
echo "  sh build.sh final       Druckfassung"
echo "  sh sicherung.sh         ZIP-Sicherung"
[ "$GH" = "10" ] && echo "  sh sync.sh              mit GitHub abgleichen (am Anfang und am Ende)"
echo "Hilfe: hilfe.html im Ordner pureSATZ öffnen, oben «Start»."
