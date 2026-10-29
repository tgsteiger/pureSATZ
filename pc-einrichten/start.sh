#!/bin/bash
# =====================================================================
#  pureSATZ einrichten, in fünf Schritten (Linux und Mac).
#  Aufruf über START-Linux.sh (sh START-Linux.sh) bzw. START-Mac.command (Doppelklick).
#    1. Technik (Python …)   2. Ort für die Bücher   3. Hallo-Buch
#    4. Dein eigenes Buch    5. Extras (GitHub freiwillig, Ghostscript empfohlen)
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
    echo "In fünf Schritten:"
    echo
    echo "  1. Technik       Python, einmalig"
    echo "  2. Ort           fester Ordner für deine Bücher"
    echo "  3. Hallo-Buch    Beispiel zum Anschauen"
    echo "  4. Dein Buch     mit Titel und Namen"
    echo "  5. Extras        GitHub, Ghostscript"
    echo
    echo "Enter nimmt immer den Vorschlag."
    weiter
fi

# --- Schritt 1: Technik ---------------------------------------------------
titel "Schritt 1 von 5 – Technik"
echo "Python 3.10+ wird geprüft und wenn nötig installiert."
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
        echo "pureSATZ liegt in:  $HIER"
        echo "Fester Ort für deine Bücher (nicht Downloads/Schreibtisch/Cloud):"
        echo
        echo "Vorschlag:  $ZIEL"
        echo "  n     = pureSATZ hier lassen"
        echo "  Pfad  = eigenen Ort eintippen (oder Ordner ins Fenster ziehen)"
        echo
        read -r -p "Ort [Enter = Vorschlag]: " ORT
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
                        echo "Dort ist schon pureSATZ $ALT."
                        read -r -p "Durch $NEU ersetzen (alte bleibt als pureSATZ-alt-$ALT)? [n = nein | Enter = ja]: " ERS
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
                    echo
                    echo "Weiter in $ZIEL/pureSATZ."
                    echo "Den alten Ordner $HIER darfst du am Schluss löschen."
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
python3 setup/hallo.py --kette             # erklärt, fragt, baut, öffnet das PDF
weiter

# --- Schritt 4: Dein eigenes Buch ---------------------------------------------
titel "Schritt 4 von 5 – Dein eigenes Buch"
python3 setup/setup.py --kette             # fragt Titel, Untertitel, Autor, Format, öffnet den Buchordner
weiter

# --- Schritt 5: Extras (zuerst GitHub, am Schluss Ghostscript) -----------------
titel "Schritt 5 von 5 – Extras"
echo "Zwei Extras – gehen auch später."
bash "pc-einrichten/$OS-einrichten.sh" --extras
GH=$?                                       # 10 = mit GitHub

# Übersicht in 00-UEBERSICHT.txt schreiben (neben die Bücher) und hier anzeigen
uebersicht() {
    echo "Übersicht: $OBEN"
    echo "====================================================================="
    echo
    for d in "$OBEN"/*/; do
        n="$(basename "$d")"
        case "$n" in
            "$(basename "$HIER")") t="die Werkstatt – für ein neues Buch und Updates, hier nichts schreiben" ;;
            pureSATZ-alt-*)        t="alte Version – darf weg" ;;
            Hallo-Buch)            t="Beispielbuch zum Ausprobieren – darf weg" ;;
            *) [ -f "$d/build.sh" ] || continue; t="DEIN BUCH – hier schreibst und baust du" ;;
        esac
        printf "  %-16s %s\n" "$n/" "$t"
    done
    echo
    echo "Am einfachsten: Lotus «Buch Menü» auf dem Schreibtisch doppelklicken – oder"
    if [ -n "$MAC" ]; then
        echo "im Buchordner «Terminal hier» doppelklicken, dann:"
    else
        echo "im Buchordner Rechtsklick → «Im Terminal öffnen», dann:"
    fi
    echo "  sh menu.sh              Menü: alles mit einem Buchstaben (s schnell, k komplett …)"
    echo "  sh build.sh schnell     Lese-PDF ansehen, in Sekunden"
    echo "  sh build.sh final       Druckfassung"
    echo "  sh sicherung.sh         ZIP-Sicherung"
    [ "$GH" = "10" ] && echo "  sh sync.sh              mit GitHub abgleichen (am Anfang und am Ende)"
    echo
    echo "Hilfe: pureSATZ/hilfe.html öffnen, oben «Start»."
}
echo
echo "=============================================================="
echo "  Fertig – so sieht es jetzt aus (steht auch in 00-UEBERSICHT.txt):"
echo "=============================================================="
echo
uebersicht | tee "$OBEN/00-UEBERSICHT.txt"
