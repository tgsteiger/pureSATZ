#!/bin/bash
# Macht aus der Buch-MD je Kapitel eine vorlesbare txt-Datei
# Aufruf über hoerbuch.py (setzt MD, ZIEL, PLATZHALTER aus dem Buch); von Hand: MD=… ZIEL=… bash md2txt.sh
MD="${MD:-../../buch.md}"                 # Quelle (hoerbuch.py: Buch-MD mit eingesetzten Geschichten)
ZIEL="${ZIEL:-./txt-md}"                  # Zielordner
VERSION="${VERSION:-normal}"              # normal | uz
TIEFE="${TIEFE:-3}"                       # bis zu dieser Ebene eine eigene Datei (3 = ###)
TABELLEN="${TABELLEN:-lesen}"             # lesen = Zeile für Zeile, kurz = nur "Tabelle."
PLATZHALTER="${PLATZHALTER:-}"            # {name}=Text;… (hoerbuch.py: Variablen des Buchs), unbekannte fallen weg

[ "$VERSION" = "unzensiert" ] && VERSION="uz"
[ -f "$MD" ] || { echo "Nicht gefunden: $MD"; exit 1; }
mkdir -p "$ZIEL"
if ls "$ZIEL"/*.txt >/dev/null 2>&1; then
  echo "$ZIEL ist nicht leer – bitte leeren oder anderen Ordner angeben"; exit 1
fi
GESAMT="${ZIEL%/}/../buch.txt"             # alles, was vorgelesen wird
ENTFERNT="${ZIEL%/}/../buch-entfernt.txt"  # alles, was weggelassen wurde

awk -v ziel="${ZIEL%/}" -v tab="$TABELLEN" -v maxt="$TIEFE" -v ver="$VERSION" \
    -v ph="$PLATZHALTER" -v gesamt="$GESAMT" -v entfernt="$ENTFERNT" '
BEGIN { n=split(ph,a,";")
        for (i=1;i<=n;i++) { q=index(a[i],"="); if (q) P[substr(a[i],1,q-1)]=substr(a[i],q+1) }
        printf "" > gesamt; printf "" > entfernt }
function out(s)   { print s > datei; print s > gesamt }
function entf(s)  { print FNR ": " s > entfernt }
function punkt(s) { return (s ~ /[.!?:;]$/ ? s : s ".") }
function ersetze(s,   m, t, k) {
  while (match(s, /\{[a-z-]+\}/)) {                    # Platzhalter
    k=substr(s,RSTART+1,RLENGTH-2)
    s=substr(s,1,RSTART-1) ((k in P) ? P[k] : "") substr(s,RSTART+RLENGTH) }
  while (match(s, /!\[[^]]*\]\([^)]*\)/)) {           # Bilder
    m=substr(s,RSTART,RLENGTH); t=m; sub(/^!\[/,"",t); sub(/\].*$/,"",t)
    s=substr(s,1,RSTART-1) (t!="" ? "Bild: " t "." : "") substr(s,RSTART+RLENGTH) }
  while (match(s, /\[[^]]*\]\([^)]*\)/)) {             # Links
    m=substr(s,RSTART,RLENGTH); t=m; sub(/^\[/,"",t); sub(/\].*$/,"",t)
    s=substr(s,1,RSTART-1) t substr(s,RSTART+RLENGTH) }
  gsub(/\[\^[^]]*\]/,"",s)                             # Fussnoten-Verweise
  gsub(/<br *\/?>/," ",s)
  gsub(/<[^>]*>/,"",s); gsub(/\*\*|__|\*|`|\\/,"",s)
  return s }
function zelle(s, a) {
  sub(/^ *\| */,"",s); sub(/ *\| *$/,"",s); return split(s,a,/ *\| */) }
function neu(L, T, N,   j, fn) {
  if (datei) close(datei)
  c[L]++; for (j=L+1;j<=9;j++) c[j]=0
  fn=sprintf("%02d",c[1]); for (j=2;j<=tief;j++) fn=fn sprintf(".%02d",c[j])
  gsub(/[\/:*?"<>|«»]/,"",N); gsub(/ +/,"-",N)
  datei=ziel "/" fn "_" N ".txt"
  out(punkt(T)); out("") }
function fotoaus() {
  if (foto && datei) { out("Bild: " punkt(ftitel) (ftxt!="" ? " " punkt(ftxt) : "")); out("") }
  foto=0; fskip=0; ftxt="" }

FNR==NR { if (/^#+ / && !/^#+ @/) { l=index($0," ")-1; if (l<=maxt && l>tief) tief=l }; next }
FNR==1 && /^---$/ { yaml=1; next }
yaml  { if (/^---$/) yaml=0; next }
/^```/ { code=!code; next }
code  { next }
kom   { if (/-->/) kom=0; next }
/<!--/ && !/-->/ { kom=1; next }
{ gsub(/<!--[^>]*-->/,"") }

# Versions-Blöcke  ::: klasse [Titel] ... :::
/^::: *$/ { if (weg) entf($0); if (d>0) d--
            weg=0; for (i=1;i<=d;i++) if (!halt[i]) weg=1; next }
/^:::/ { fotoaus(); k=$0; sub(/^::: */,"",k)
         kl=k; sub(/ .*/,"",kl); ti=k; sub(/^[^ ]+ */,"",ti)
         v=""; if (kl=="uz" || kl ~ /-uz$/) v="uz"
         else if (kl=="normal" || kl ~ /-normal$/) v="normal"
         else if (kl ~ /-ebook$/) v="ebook"
         halt[++d]=(v=="" || v==ver)
         weg=0; for (i=1;i<=d;i++) if (!halt[i]) weg=1
         if (weg) { entf($0); next }
         if (kl=="uz" && datei) { out(punkt(ti!="" ? ersetze(ti) : "Unzensiert")); out("") }
         next }
weg { entf($0); next }

# Fotos  @FOTO Titel / @FOTO-UZ Titel  mit text: ...
/^(#+ +)?@FOTO/ { fotoaus(); s=$0; sub(/^#+ +/,"",s)
                  kw=s; sub(/ .*/,"",kw); ftitel=s; sub(/^[^ ]+ */,"",ftitel)
                  fv=""; if (kw ~ /-UZ$/) fv="uz"; else if (kw ~ /-NORMAL$/) fv="normal"
                  if (fv!="" && fv!=ver) { fskip=1; entf($0) } else foto=1
                  next }
(foto || fskip) && /^[a-z]+: / { if (fskip) entf($0)
                                  else if (/^text: /) { ftxt=$0; sub(/^text: */,"",ftxt); ftxt=ersetze(ftxt) }
                                  next }
(foto || fskip) { fotoaus() }

# Überschriften
/^#+ / { l=index($0," ")-1; t=substr($0,l+2)
         if (t ~ /^@WIDMUNG/)  { atsek=0; neu(l, "Widmung", "Widmung"); next }
         if (t ~ /^@KERNSATZ/) { atsek=0; s=t; sub(/^@KERNSATZ */,"",s)
                                 if (datei && s!="") { out(punkt(ersetze(s))); out("") }; next }
         if (t ~ /^@/) { atsek=1; entf($0); next }        # @TITEL, @IMPRESSUM usw.
         atsek=0
         sub(/ *\{[#.][^}]*\} *$/,"",t); sub(/ *#+ *$/,"",t)
         t=ersetze(t); n=split(t,p,"|"); t=""; nm=""
         for (i=1;i<=n;i++) { gsub(/^ +| +$/,"",p[i])
           if (p[i]!="") { t=t (t!="" ? ". " : "") p[i]; nm=nm (nm!="" ? " " : "") p[i] } }
         intab=0
         if (l>maxt) { if (datei) { out(""); out(punkt(t)); out("") }; next }
         neu(l, t, nm); next }
atsek  { entf($0); next }
!datei { next }                                          # Text vor 1. Überschrift

# Steuerbefehle
/^@ZITAT/    { s=$0; sub(/^@ZITAT[^ ]* */,"",s); out(punkt(ersetze(s))); out(""); next }
/^@PORTRAIT/ { s=$0; sub(/^[^|]*\| */,"",s); if (s!=$0) { out("Bild: " punkt(ersetze(s))); out("") }; next }
/^@/         { entf($0); next }

/^\[\^[^]]*\]:/ { next }                                 # Fussnoten-Text weglassen
/^ *(---|\*\*\*|___) *$/ { out(""); next }

# Zeitstrahl  "1974 | Text"  wird zu  "1974: Text."
{ zi=index($0," | ") }
zi>1 && zi<=25 && !/^ *\|/ { s=$0; sub(/ *\| */,": ",s); out(punkt(ersetze(s))); out(""); next }

# Tabellen
!/^ *\|/ { intab=0 }
/^ *\|/ && /^[ |:-]+$/ { next }
/^ *\|/ {
  if (!intab) { intab=1; zelle($0,kopf); if (tab=="kurz") out("Tabelle."); next }
  if (tab=="kurz") next
  n=zelle($0,z); s=""
  for (i=1;i<=n;i++) s=s (i>1 ? ", " : "") kopf[i] " " z[i]
  out(punkt(ersetze(s))); out(""); next }

# Normaler Text, Listen, Randbemerkungen (~)
{ s=$0; sub(/^ *> ?/,"",s); sub(/^~ +/,"",s)
  if (sub(/^ *([-*+]|[0-9]+\.) +/,"",s)) { out(punkt(ersetze(s))); out(""); next }
  out(ersetze(s)) }
END { fotoaus() }
' "$MD" "$MD"

echo "Fertig: $(ls "$ZIEL"/*.txt 2>/dev/null | wc -l) Dateien in $ZIEL"
echo "Prüfen: $GESAMT und $ENTFERNT"
