#!/bin/bash
# =====================================================================
#  pureSATZ – Mac einrichten. Für Intel-Macs UND Macs mit Apple-Chip (M1, M2, M3 …), ohne Homebrew.
#  Am einfachsten: im Ordner pureSATZ  START-Mac.command  doppelklicken – führt in fünf Schritten
#  durch (Technik, Ort, Hallo-Buch, eigenes Buch, Extras) und ruft dieses Skript auf:
#    bash pc-einrichten/mac-einrichten.sh --technik   Apple-Werkzeuge (git), Python
#    bash pc-einrichten/mac-einrichten.sh --extras    GitHub (freiwillig), Ghostscript, CotEditor (empfohlen)
#  Ohne Angabe startet der ganze Ablauf (wie START-Mac.command).
#  Darf beliebig oft laufen. Hält es an (Apple-Werkzeuge, Python), danach einfach nochmals starten.
# =====================================================================
cd "$(dirname "$0")/.." || exit 1          # Ordner pureSATZ
HIER="$(pwd)"
case "$1" in
    --technik|--extras) ;;
    *) exec bash pc-einrichten/start.sh "$@" ;;
esac

if [ "$1" = "--technik" ]; then
    echo "Prozessor: $(uname -m)   (x86_64 = Intel, arm64 = Apple-Chip)"
    # --- 1. Apple-Kommandozeilenwerkzeuge (bringen git mit) ---------------
    if ! xcode-select -p >/dev/null 2>&1; then
        echo "Die Apple-Kommandozeilenwerkzeuge fehlen."
        echo "Gleich öffnet sich ein Fenster: auf «Installieren» klicken."
        echo "Wenn es fertig ist: START-Mac.command NOCHMALS doppelklicken."
        xcode-select --install 2>/dev/null
        exit 2
    fi
    echo "OK  Kommandozeilenwerkzeuge – $(git --version)"

    # --- 2. Python 3.10 oder neuer (von python.org, «universal2») ----------
    if ! python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)' 2>/dev/null; then
        echo
        echo "Es fehlt ein aktuelles Python (3.10 oder neuer)."
        echo "Gleich öffnet sich python.org: den neusten"
        echo "«macOS 64-bit universal2 installer» laden und installieren"
        echo "(läuft auf Intel und Apple-Chip)."
        echo "Danach Terminal SCHLIESSEN und START-Mac.command nochmals doppelklicken."
        open "https://www.python.org/downloads/macos/"
        exit 2
    fi
    echo "OK  $(python3 --version)  ($(command -v python3))"
    exit 0
fi

# --- Extra 1: GitHub (freiwillig) ---------------------------------------
github() {
echo
echo "GitHub (freiwillig): Sicherung und mehrere Computer."
read -r -p "Mit GitHub arbeiten? [j = ja | Enter = nein]: " GH
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
        return 1
    fi
fi

# Bücher von GitHub holen (neben diesen Ordner)
BESITZER="$(printf '%s' "$URL" | sed -E 's#.*github.com[:/]([^/]+)/.*#\1#')"
echo
read -r -p "Hast du schon ein Buch auf GitHub? [j = ja | Enter = nein]: " W
while [ "$W" = "j" ] || [ "$W" = "ja" ]; do
    read -r -p "Name des Buchs auf GitHub (z. B. mein-buch): " R
    [ -z "$R" ] && break
    case "$BESITZER" in ""|*/*|*:*) read -r -p "Dein GitHub-Benutzername: " BESITZER ;; esac
    STD="$(printf '%s' "$R" | awk '{print toupper(substr($0,1,1)) substr($0,2)}')"
    read -r -p "Ordnername [Enter = $STD]: " O
    O="${O:-$STD}"
    ZIEL="$(dirname "$HIER")/$O"
    if [ -d "$ZIEL/.git" ]; then
        echo "Schon da: $ZIEL – hole neusten Stand"
        (cd "$ZIEL" && sh sync.sh)
        bauen
    elif git clone "https://github.com/$BESITZER/$R.git" "$ZIEL"; then
        bauen
    fi
    echo
    read -r -p "Noch ein Buch holen? [j = ja | Enter = nein]: " W
done

else
    echo "OK  ohne GitHub. Gesichert wird mit  sh sicherung.sh  (ZIP)."
fi
}
bauen() {
    read -r -p "Jetzt einmal bauen (1–2 Min)? [n = nein | Enter = ja]: " B
    case "$B" in n|nein) ;; *) (cd "$ZIEL" && sh build.sh schnell) ;; esac
}
github

# --- Extra 2: Ghostscript (empfohlen, für CMYK-Druckdateien) -------------
# Gebraucht mit «{farbmodus}: cmyk» in einer Druckdatei (z. B. tredition), umgewandelt wird bei final.
echo
echo "Ghostscript (empfohlen): dann bist du bereit für CMYK-Druck."
if command -v gs >/dev/null 2>&1; then
    echo "OK  Ghostscript $(gs --version) vorhanden"
elif command -v brew >/dev/null 2>&1 || command -v port >/dev/null 2>&1; then
    read -r -p "Ghostscript installieren? [n = nein | Enter = ja]: " GS
    case "$GS" in
        n|nein) ;;
        *) if command -v brew >/dev/null 2>&1; then brew install ghostscript; else sudo port install ghostscript; fi \
               && echo "OK  Ghostscript $(gs --version)" ;;
    esac
else
    echo "Ghostscript fehlt – installieren mit:  brew install ghostscript"
fi

# --- Extra 3: CotEditor (empfohlen, Schreibprogramm für die MD-Dateien) -------
echo
echo "CotEditor (empfohlen): Schreibprogramm für die MD-Dateien – schlicht, dunkles Design, Gliederung."
if [ -d /Applications/CotEditor.app ] || [ -d "$HOME/Applications/CotEditor.app" ]; then
    echo "OK  CotEditor vorhanden"
else
    read -r -p "CotEditor installieren? [n = nein | Enter = ja]: " CE
    case "$CE" in
        n|nein) ;;
        *) if command -v brew >/dev/null 2>&1; then
               brew install --cask coteditor && echo "OK  CotEditor installiert"
           else
               open "macappstore://apps.apple.com/app/id1024640650" 2>/dev/null || open "https://coteditor.com"
               echo "Im App Store bei CotEditor auf «Laden» klicken."
               read -r -p "Weiter mit Enter … " _
           fi
           echo "    .md immer mit CotEditor: Rechtsklick auf eine .md → Informationen → Öffnen mit: CotEditor → Alle ändern" ;;
    esac
fi

[ "$GH" = "j" ] || [ "$GH" = "ja" ] && exit 10       # 10 = mit GitHub (für die Schlussseite)
exit 0
