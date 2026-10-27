#!/bin/bash
# =====================================================================
#  pureSATZ – Linux einrichten (Linux Mint, Ubuntu, Debian mit apt; andere Linux: Hinweise unten)
#  Am einfachsten: im Ordner pureSATZ  sh START-Linux.sh  – führt in fünf Schritten durch
#  (Technik, Ort, Hallo-Buch, eigenes Buch, Extras) und ruft dieses Skript auf:
#    bash pc-einrichten/linux-einrichten.sh --technik   Python, venv, git
#    bash pc-einrichten/linux-einrichten.sh --extras    Ghostscript und GitHub (freiwillig)
#  Ohne Angabe startet der ganze Ablauf (wie START-Linux.sh).
#  Darf beliebig oft laufen – Erledigtes wird übersprungen.
# =====================================================================
cd "$(dirname "$0")/.." || exit 1          # Ordner pureSATZ
HIER="$(pwd)"
case "$1" in
    --technik|--extras) ;;
    *) exec bash pc-einrichten/start.sh "$@" ;;
esac

if [ "$1" = "--technik" ]; then
    # --- 1. Python 3.10+, venv und git ------------------------------------
    FEHLT=""
    if ! python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)' 2>/dev/null; then
        FEHLT="$FEHLT python3"
    fi
    T="$(mktemp -d)"
    if ! python3 -m venv "$T/v" >/dev/null 2>&1; then
        FEHLT="$FEHLT python3-venv"
    fi
    rm -rf "$T"
    command -v git >/dev/null 2>&1 || FEHLT="$FEHLT git"

    if [ -n "$FEHLT" ]; then
        echo "Es fehlen Programme:$FEHLT"
        if command -v apt >/dev/null 2>&1; then
            echo "Sie werden jetzt installiert (dein Passwort wird gefragt; beim Tippen erscheint nichts)."
            sudo apt update && sudo apt install -y $FEHLT || { echo "Installation ging nicht – Internet?"; exit 1; }
        else
            echo "Bitte mit der Paketverwaltung installieren, z. B.:"
            echo "  Fedora:  sudo dnf install python3 git"
            echo "  Arch:    sudo pacman -S python git"
            echo "Danach dieses Skript nochmals starten."
            exit 1
        fi
    fi
    echo "OK  $(python3 --version), venv, $(git --version)"
    exit 0
fi

# --- Extras ---------------------------------------------------------------
echo
echo "Ghostscript braucht es nur, wenn eine Druckerei CMYK verlangt (z. B. tredition)."
# --- Extra 1: Ghostscript (freiwillig, für CMYK-Druckdateien) --------
# Braucht es nur mit «{farbmodus}: cmyk» in einer Druckdatei (z. B. tredition), umgewandelt wird bei final.
if command -v gs >/dev/null 2>&1; then
    echo "OK  Ghostscript $(gs --version) vorhanden"
elif command -v apt >/dev/null 2>&1; then
    read -r -p "Ghostscript installieren? [j = ja, Enter = nein]: " GS
    if [ "$GS" = "j" ] || [ "$GS" = "ja" ]; then
        sudo apt install -y ghostscript && echo "OK  Ghostscript $(gs --version)"
    fi
else
    echo "Hinweis: Für {farbmodus}: cmyk Ghostscript installieren (Paket «ghostscript»)."
fi

# --- Extra 2: GitHub (freiwillig) ---------------------------------------
echo
echo "GitHub: private Sicherung und dasselbe Buch auf mehreren Computern (sh sync.sh)."
read -r -p "Mit GitHub arbeiten? [j = ja, Enter = nein]: " GH
if [ "$GH" = "j" ] || [ "$GH" = "ja" ]; then
    if ! command -v gh >/dev/null 2>&1; then
        echo "GitHub-Programm «gh» wird installiert …"
        sudo apt install -y gh || { echo "gh liess sich nicht installieren. Hilfe: cli.github.com"; exit 1; }
    fi
    if [ -z "$(git config --global user.name)" ]; then
        read -r -p "Dein Name für git (z. B. Anna Muster): " N
        [ -n "$N" ] && git config --global user.name "$N"
    fi
    if [ -z "$(git config --global user.email)" ]; then
        echo "Mail für git: am besten die geschützte GitHub-Adresse"
        echo "(GitHub → Settings → Emails → «Keep my email addresses private»)."
        read -r -p "Mail: " M
        [ -n "$M" ] && git config --global user.email "$M"
    fi
    echo "OK  git: $(git config --global user.name) <$(git config --global user.email)>"

    if ! gh auth status >/dev/null 2>&1; then
        echo
        echo "Jetzt bei GitHub anmelden. Antworten: GitHub.com → HTTPS → Yes → Login with a web browser"
        gh auth login || { echo "Anmeldung abgebrochen – Skript später nochmals starten."; exit 1; }
    fi
    gh auth setup-git >/dev/null 2>&1          # git (auch sync.sh, update.sh) nutzt die gh-Anmeldung
    BESITZER="$(gh api user --jq .login 2>/dev/null)"
    echo "OK  bei GitHub angemeldet als $BESITZER"

    # Bücher holen (neben diesen Ordner)
    while true; do
        echo
        read -r -p "Eigenes Buch von GitHub holen? Repository-Name (z. B. mein-buch), Enter = weiter: " R
        [ -z "$R" ] && break
        case "$R" in */*) QUELLE="$R" ;; *) QUELLE="$BESITZER/$R" ;; esac
        STD="$(basename "$R" | awk '{print toupper(substr($0,1,1)) substr($0,2)}')"
        read -r -p "Ordnername [$STD]: " O
        O="${O:-$STD}"
        ZIEL="$(dirname "$HIER")/$O"
        if [ -d "$ZIEL/.git" ]; then
            echo "Schon da: $ZIEL – hole neusten Stand"
            (cd "$ZIEL" && sh sync.sh)
        else
            gh repo clone "$QUELLE" "$ZIEL" || continue
        fi
        read -r -p "Jetzt einmal bauen (richtet beim ersten Mal Python ein, ca. 1–2 Min)? [j/n] " B
        [ "$B" = "j" ] && (cd "$ZIEL" && sh build.sh schnell)
    done
else
    echo "OK  ohne GitHub. Gesichert wird mit  sh sicherung.sh  (ZIP)."
fi

[ "$GH" = "j" ] || [ "$GH" = "ja" ] && exit 10       # 10 = mit GitHub (für die Schlussseite)
exit 0
