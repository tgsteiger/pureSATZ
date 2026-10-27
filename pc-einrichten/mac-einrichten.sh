#!/bin/bash
# =====================================================================
#  pureSATZ – Mac einrichten (einmalig)
#  Für Intel-Macs UND Macs mit Apple-Chip (M1, M2, M3 …), ohne Homebrew.
#  (Homebrew läuft auf Intel-Macs nicht mehr.)
#
#  Am einfachsten: start.command im Ordner pureSATZ doppelklicken (ruft dieses Skript auf).
#  Auch direkt im Ordner pureSATZ:   bash pc-einrichten/mac-einrichten.sh
#  Das Skript darf beliebig oft laufen – Erledigtes wird übersprungen.
#  Hält es an (Schritt 1 oder 2), danach einfach nochmals starten.
#  GitHub ist freiwillig und kommt am Schluss: Ohne GitHub geht Schreiben und Bauen genauso.
# =====================================================================
cd "$(dirname "$0")/.." || exit 1          # Ordner pureSATZ
HIER="$(pwd)"

echo "=== pureSATZ: Mac einrichten ==="
echo "Prozessor: $(uname -m)   (x86_64 = Intel, arm64 = Apple-Chip)"
echo

# --- 1. Apple-Kommandozeilenwerkzeuge (bringen git mit) ---------------
if ! xcode-select -p >/dev/null 2>&1; then
    echo "Schritt 1: Apple-Kommandozeilenwerkzeuge fehlen."
    echo "Gleich öffnet sich ein Fenster: auf «Installieren» klicken."
    echo "Wenn es fertig ist: dieses Skript NOCHMALS starten."
    xcode-select --install 2>/dev/null
    exit 0
fi
echo "OK  Kommandozeilenwerkzeuge – $(git --version)"

# --- 2. Python 3.10 oder neuer (von python.org, «universal2») ----------
if ! python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)' 2>/dev/null; then
    echo
    echo "Schritt 2: Es fehlt ein aktuelles Python (3.10 oder neuer)."
    echo "Gleich öffnet sich python.org: den neusten"
    echo "«macOS 64-bit universal2 installer» laden und installieren"
    echo "(läuft auf Intel und Apple-Chip)."
    echo "Danach Terminal SCHLIESSEN und start.command nochmals doppelklicken."
    open "https://www.python.org/downloads/macos/"
    exit 0
fi
echo "OK  $(python3 --version)  ($(command -v python3))"

# --- 3. Ghostscript (freiwillig, für CMYK-Druckdateien) ---------------
# Braucht es nur mit «{farbmodus}: cmyk» in einer Druckdatei (z. B. tredition), umgewandelt wird bei final.
if command -v gs >/dev/null 2>&1; then
    echo "OK  Ghostscript $(gs --version) (für {farbmodus}: cmyk)"
elif command -v brew >/dev/null 2>&1; then
    read -r -p "Ghostscript für CMYK-Druckdateien (z. B. tredition) installieren? [j/n] (j): " GS
    if [ -z "$GS" ] || [ "$GS" = "j" ] || [ "$GS" = "ja" ]; then
        brew install ghostscript && echo "OK  Ghostscript $(gs --version)"
    fi
elif command -v port >/dev/null 2>&1; then
    read -r -p "Ghostscript für CMYK-Druckdateien (z. B. tredition) installieren? [j/n] (j): " GS
    if [ -z "$GS" ] || [ "$GS" = "j" ] || [ "$GS" = "ja" ]; then
        sudo port install ghostscript && echo "OK  Ghostscript $(gs --version)"
    fi
else
    echo "Hinweis: Ghostscript fehlt – nur nötig für {farbmodus}: cmyk (z. B. tredition)."
    echo "         Installieren mit Homebrew (brew install ghostscript) oder MacPorts (sudo port install ghostscript)."
    echo "         Ohne Ghostscript bleiben die Druckdateien RGB, alles andere läuft normal."
fi

# --- 4. Hallo-Buch und eigenes Buch ----------------------------------
echo
read -r -p "Hallo-Buch jetzt ansehen (Beispielbuch, das PDF öffnet sich)? [j/n] (j): " HB
if [ -z "$HB" ] || [ "$HB" = "j" ] || [ "$HB" = "ja" ]; then
    python3 setup/hallo.py                  # fragt am Schluss selbst nach dem eigenen Buch
else
    read -r -p "Jetzt dein eigenes Buch anlegen? [j/n] (j): " NB
    if [ -z "$NB" ] || [ "$NB" = "j" ] || [ "$NB" = "ja" ]; then
        python3 setup/setup.py
    fi
fi

# --- 5. GitHub (freiwillig, geht auch jederzeit später) ---------------
echo
echo "GitHub ist freiwillig und geht auch später (dieses Skript nochmals starten, siehe GITHUB.md):"
echo "private Sicherung und dasselbe Buch auf mehreren Computern (sh sync.sh)."
read -r -p "Mit GitHub arbeiten? [j/n] (n): " GH
if [ "$GH" = "j" ] || [ "$GH" = "ja" ]; then

# Name und Mail für git
if [ -z "$(git config --global user.name)" ]; then
    read -r -p "Dein Name für git (z. B. Vorname Nachname): " N
    [ -n "$N" ] && git config --global user.name "$N"
fi
if [ -z "$(git config --global user.email)" ]; then
    echo "Mail für git: am besten die geschützte GitHub-Adresse"
    echo "(GitHub → Settings → Emails → «Keep my email addresses private»)."
    read -r -p "Mail: " M
    [ -n "$M" ] && git config --global user.email "$M"
fi
# Mac merkt sich den GitHub-Token im Schlüsselbund
git config --global credential.helper osxkeychain
echo "OK  git: $(git config --global user.name) <$(git config --global user.email)>"

# Zugang zu GitHub prüfen
URL="$(git remote get-url origin 2>/dev/null)"
if [ -n "$URL" ]; then
    if git ls-remote "$URL" >/dev/null 2>&1; then
        echo "OK  GitHub-Zugang ($URL)"
    else
        cat <<'TXT'

GitHub-Zugang klappt nicht. So geht es (einmalig):
  1. github.com/settings/tokens → «Generate new token» → «Generate new token (classic)»
  2. Note: z. B. «Mac Buchmotor» · Expiration: «No expiration» (gelbe Warnung ignorieren)
  3. NUR den obersten Haken «repo» setzen (die Unterpunkte kommen automatisch mit)
  4. «Generate token» → Token (ghp_…) kopieren – wird nur einmal angezeigt!
  5. Alten falschen Versuch vergessen:
       printf "protocol=https\nhost=github.com\n\n" | git credential reject
  6. Dieses Skript nochmals starten. Bei «Username»: GitHub-Benutzer,
     bei «Password»: den Token mit Cmd+V einfügen – es erscheint NICHTS, dann Enter.
     (Geht Einfügen nicht: anderes Terminal nehmen, z. B. das Terminal von Apple.)
  Fehler 403 «Write access … not granted» = Haken «repo» fehlt → neuen Token machen.
  Token nie in Chats oder Dateien weitergeben.
TXT
        exit 1
    fi
fi

# Bücher von GitHub holen (neben diesen Ordner)
BESITZER="$(printf '%s' "$URL" | sed -E 's#.*github.com[:/]([^/]+)/.*#\1#')"
while true; do
    echo
    read -r -p "Buch von GitHub holen? Repository-Name (z. B. mein-buch), leer = fertig: " R
    [ -z "$R" ] && break
    case "$BESITZER" in ""|*/*|*:*) read -r -p "Dein GitHub-Benutzername: " BESITZER ;; esac
    STD="$(printf '%s' "$R" | awk '{print toupper(substr($0,1,1)) substr($0,2)}')"
    read -r -p "Ordnername [$STD]: " O
    O="${O:-$STD}"
    ZIEL="$(dirname "$HIER")/$O"
    if [ -d "$ZIEL/.git" ]; then
        echo "Schon da: $ZIEL – hole neusten Stand"
        (cd "$ZIEL" && sh sync.sh)
    else
        git clone "https://github.com/$BESITZER/$R.git" "$ZIEL" || continue
    fi
    read -r -p "Jetzt einmal bauen (richtet beim ersten Mal Python ein, ca. 1–2 Min)? [j/n] " B
    [ "$B" = "j" ] && (cd "$ZIEL" && sh build.sh schnell)
done

else
    echo "OK  ohne GitHub. Gesichert wird mit  sh sicherung.sh  (ZIP)."
fi

echo
echo "=== Fertig ==="
echo "Deine Bücher liegen neben pureSATZ in $(dirname "$HIER")"
echo "pureSATZ ist die Werkstatt – dort nichts schreiben."
echo "Im Buchordner:     «Terminal hier» doppelklicken, dann  sh build.sh schnell  ·  sh build.sh final  ·  sh sicherung.sh"
echo "Neues Buch:        sh setup/setup.sh        (im Ordner pureSATZ)"
[ "$GH" = "j" ] || [ "$GH" = "ja" ] && echo "Mit GitHub:        sh sync.sh  ·  sh update.sh"
echo "Hilfe:             hilfe.html öffnen, oben «Start»"
