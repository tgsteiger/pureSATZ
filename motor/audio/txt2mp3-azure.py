#!/usr/bin/env python3
# Hörbuch: liest mit einer Azure-Stimme vor (pureSATZ, nur Linux, Testphase). Meist über hoerbuch.py / Menü «hb».
# Aufruf: python3 txt2mp3-azure.py [pdf|md]                 alle, fertige werden übersprungen
#         python3 txt2mp3-azure.py [pdf|md] liste           Kapitel mit Kürzel und Zeichen anzeigen
#         python3 txt2mp3-azure.py [pdf|md] 050208,0406     nur diese (Kürzel), immer neu
#         python3 txt2mp3-azure.py [pdf|md] datei.txt ...   nur diese Dateien, immer neu
#         … stimme=2 …   einmalig andere Stimme (1, 2 oder ganzer Name), sonst AZURE_STIMME aus audio.conf
# Ausgabe pro Stimme: audio/mp3-<md|pdf>-azure-<stimme>/  (z. B. mp3-md-azure-ollie)
# Jeder Lauf wird in einstellungen.txt angehängt (Zeit, Aufruf, Einstellungen, Aussprache-Liste).
# Ganzes Buch (ohne Auswahl): ZIP mit Textordner, Aussprache-Liste und audio.conf in audio/
# Braucht: AZURE_SPEECH_KEY und AZURE_SPEECH_REGION (z.B. in ~/.bashrc)
import os, sys, glob, re, subprocess, zipfile, datetime
from xml.sax.saxutils import escape

DIR = os.path.dirname(os.path.abspath(__file__))              # Skripte (motor/audio)
DATEN = os.environ.get("AUDIO_DIR") or DIR                     # Buch: audio/ (audio.conf, Aussprache, Texte, MP3)
MAX_ZEICHEN = 4000              # pro Anfrage, sicher unter dem 10-Minuten-Limit von Azure
SATZPAUSE_MIN, SATZPAUSE_MAX = 600, 1500
ABKUERZUNGEN = {"dr", "z", "b", "ca", "bzw", "usw", "nr", "st", "s", "u", "a", "d", "h"}

# Einstellungen aus audio.conf
conf = {}
with open(os.path.join(DATEN, "audio.conf"), encoding="utf-8") as f:
    for zeile in f:
        m = re.match(r'^([A-Z0-9_]+)="([^"]*)"', zeile.strip())
        if m:
            conf[m.group(1)] = os.path.expandvars(m.group(2))

sprache   = conf.get("AZURE_SPRACHE", "de-CH")
rate      = conf.get("AZURE_RATE", "-15%")
pause     = conf.get("AZURE_PAUSE", "600ms")
titelpause = conf.get("AZURE_TITELPAUSE", "")
kbit      = int(conf.get("MP3_KBIT", "128") or 128)
album     = conf.get("ALBUM") or os.environ.get("HB_TITEL", "")          # leer = {titel} des Buchs (hoerbuch.py)
artist    = conf.get("ARTIST") or os.environ.get("HB_AUTOR", "")         # leer = {autor}
cover     = conf.get("COVER") or os.environ.get("HB_COVER", "")          # leer = Umschlag vorne, falls gebaut
if cover and not os.path.isabs(cover):
    cover = os.path.join(DATEN, cover)
cover     = cover if cover and os.path.exists(cover) else ""
hoch      = kbit >= 192                         # Produktion: verlustfrei von Azure, 44,1 kHz, Lautstärke angeglichen
satzpause = int(conf.get("AZURE_SATZPAUSE", "0") or 0)   # 0 = aus, wie bisher

# Aufruf auswerten
args = sys.argv[1:]
wahl = conf.get("AZURE_STIMME", "1")
for a in list(args):
    if a.startswith("stimme="):
        wahl = a.split("=", 1)[1]
        args.remove(a)
stimme = conf.get("AZURE_FAVORIT" + wahl, wahl) if wahl in ("1", "2") else wahl   # 1/2 = Favorit
kurz = "-".join(stimme.split("-")[2:]).replace("MultilingualNeural", "").replace("Neural", "").replace(":", "-").lower()
quelle = "md"
if args and args[0] in ("pdf", "md"):
    quelle = args.pop(0)
txt_dir = os.path.join(DATEN, "txt-" + quelle)
mp3_dir = os.path.join(DATEN, "mp3-" + quelle + "-azure-" + kurz + ("" if kbit == 128 else "-%d" % kbit))
aussprache = "aussprache-%s.txt" % kurz                    # eigene Liste pro Stimme, sonst die gemeinsame
if not os.path.exists(os.path.join(DATEN, aussprache)):
    aussprache = conf.get("AUSSPRACHE", "aussprache.txt")
alle_dateien = sorted(glob.glob(os.path.join(txt_dir, "*.txt")))

def kuerzel(datei):
    # "04.06.01_Seelen-aus…" → "040601"
    return re.sub(r"\D", "", os.path.basename(datei).split("_", 1)[0])

if args and args[0] in ("liste", "l"):
    total = 0
    for t in alle_dateien:
        with open(t, encoding="utf-8") as f:
            z = len(f.read())
        total += z
        print("%s  %-50s %6d Zeichen" % (kuerzel(t), os.path.basename(t), z))
    print("Total: %d Dateien, %d Zeichen" % (len(alle_dateien), total))
    sys.exit(0)

nur = []
for a in args:
    if os.path.isfile(a):
        nur.append(a)
        continue
    for code in a.split(","):
        code = code.replace(".", "").strip()
        if not code:
            continue
        treffer = [t for t in alle_dateien if kuerzel(t).startswith(code)]
        if not treffer:
            print("Nicht gefunden:", code)
        nur += treffer
nur = list(dict.fromkeys(nur))          # doppelte entfernen, Reihenfolge behalten
if args and not nur:
    print("Nichts ausgewählt. Kürzel anzeigen: python3 txt2mp3-azure.py %s liste" % quelle)
    sys.exit(1)

# ab hier wird gesprochen
import azure.cognitiveservices.speech as speechsdk
key = os.environ.get("AZURE_SPEECH_KEY")
if not key:
    print("AZURE_SPEECH_KEY fehlt (export in ~/.bashrc?)"); sys.exit(1)
region = os.environ.get("AZURE_SPEECH_REGION", "switzerlandnorth")

os.makedirs(mp3_dir, exist_ok=True)
print("Stimme: %s · %s → %s" % (stimme, aussprache, os.path.relpath(mp3_dir)), flush=True)
jetzt = datetime.datetime.now()
aus_pfad = os.path.join(DATEN, aussprache)
zipname = ""
if not nur:                                     # ganzes Buch: verwendete Texte sichern
    zipname = "%s_%s_%s.zip" % (os.path.basename(txt_dir), kurz, jetzt.strftime("%Y%m%d%H%M%S"))
    with zipfile.ZipFile(os.path.join(DATEN, zipname), "w", zipfile.ZIP_DEFLATED) as z:
        for t in alle_dateien:
            z.write(t, os.path.join(os.path.basename(txt_dir), os.path.basename(t)))
        for n in (aussprache, "audio.conf"):
            if os.path.exists(os.path.join(DATEN, n)):
                z.write(os.path.join(DATEN, n), n)
    print("Gesichert:", os.path.relpath(os.path.join(DATEN, zipname)), flush=True)
with open(os.path.join(mp3_dir, "einstellungen.txt"), "a", encoding="utf-8") as f:
    f.write("\n=== %s ===\nAUFRUF=python3 txt2mp3-azure.py %s\nTEXTORDNER=%s\nZIP=%s\n"
            % (jetzt.strftime("%d.%m.%Y %H:%M"), " ".join(sys.argv[1:]), os.path.basename(txt_dir), zipname or "-"))
    f.write("STIMME=%s\nSPRACHE=%s\nRATE=%s\nPAUSE=%s\nSATZPAUSE=%s\nTITELPAUSE=%s\nAUSSPRACHE=%s\nKBIT=%s\nCOVER=%s\n"
            % (stimme, sprache, rate, pause, satzpause, titelpause, aussprache, kbit, os.path.basename(cover) or "-"))
    if os.path.exists(aus_pfad):
        f.write("--- %s ---\n%s\n" % (aussprache, open(aus_pfad, encoding="utf-8").read().rstrip()))

speech_config = speechsdk.SpeechConfig(subscription=key, region=region)
speech_config.set_speech_synthesis_output_format(
    speechsdk.SpeechSynthesisOutputFormat.Riff48Khz16BitMonoPcm if hoch
    else speechsdk.SpeechSynthesisOutputFormat.Audio24Khz96KBitRateMonoMp3)

def saetze_teilen(absatz):
    # trennt nach . ! ? … wenn danach ein Grossbuchstabe, « oder eine Zahl kommt
    # und das Wort davor keine Abkürzung ist (Dr., z. B., ca. …)
    saetze, start = [], 0
    for m in re.finditer(r'[.!?…]+\s+(?=[A-ZÄÖÜ«"\d])', absatz):
        davor = absatz[start:m.start()].split()
        if davor and davor[-1].lower().rstrip(".") in ABKUERZUNGEN:
            continue
        saetze.append(absatz[start:m.end()].strip())
        start = m.end()
    rest = absatz[start:].strip()
    if rest:
        saetze.append(rest)
    return saetze

def pause_fuer(satz):
    ms = round(satzpause * len(satz.split()) / 15)
    return max(SATZPAUSE_MIN, min(SATZPAUSE_MAX, ms))

def absatz_ssml(absatz):
    if satzpause <= 0:
        return escape(absatz)                       # wie bisher
    saetze = saetze_teilen(absatz)
    teile = []
    for i, s in enumerate(saetze):
        teile.append(escape(s))
        if i < len(saetze) - 1:                     # nach dem letzten Satz gilt die Absatzpause
            teile.append('<break time="%dms"/>' % pause_fuer(s))
    return " ".join(teile)

def ssml(absaetze, titel=False):
    teile = [absatz_ssml(a) for a in absaetze]
    inhalt = ('<break time="%s"/>' % pause).join(teile[1:] if titel else teile)
    if titel:                                       # erster Absatz = Kapitelname, längere Pause davor und danach
        tp = '<break time="%s"/>' % titelpause
        inhalt = tp + teile[0] + tp + inhalt
    inhalt = '<prosody rate="%s">%s</prosody>' % (rate, inhalt)
    if sprache:
        inhalt = '<lang xml:lang="%s">%s</lang>' % (sprache, inhalt)
    return ('<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="de-DE">'
            '<voice name="%s">%s</voice></speak>' % (stimme, inhalt))

def stuecke(absaetze):
    # Absätze zu Stücken bis MAX_ZEICHEN bündeln
    teil, laenge = [], 0
    for a in absaetze:
        if teil and laenge + len(a) > MAX_ZEICHEN:
            yield teil
            teil, laenge = [], 0
        teil.append(a); laenge += len(a)
    if teil:
        yield teil

def sprechen(absaetze, datei, titel=False):
    audio = speechsdk.audio.AudioOutputConfig(filename=datei)
    synth = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio)
    r = synth.speak_ssml_async(ssml(absaetze, titel)).get()
    if r.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        raise RuntimeError(r.cancellation_details.error_details)

erzeugt = []
for t in (nur or alle_dateien):
    name = os.path.splitext(os.path.basename(t))[0]
    mp3 = os.path.join(mp3_dir, name + ".mp3")
    if not nur and os.path.exists(mp3):
        continue                      # fertige überspringen
    text = subprocess.run(["bash", os.path.join(DIR, "text-vorbereiten.sh"), t],
                          capture_output=True, text=True, check=True,
                          env=dict(os.environ, AUSSPRACHE_DATEI=aussprache, AUDIO_DIR=DATEN)).stdout
    absaetze = [z.strip() for z in text.splitlines() if z.strip()]
    if not absaetze:
        continue
    print("Lese:", name, flush=True)

    teile = []
    try:
        for i, st in enumerate(stuecke(absaetze)):
            tmp = "/tmp/tts-azure-%03d.%s" % (i, "wav" if hoch else "mp3")
            sprechen(st, tmp, titel=(i == 0 and bool(titelpause)))
            teile.append(tmp)
    except RuntimeError as e:
        print("  Fehler:", e)
        continue

    with open("/tmp/tts-azure-liste.txt", "w") as f:
        for p in teile:
            f.write("file '%s'\n" % p)
    nr = alle_dateien.index(t) + 1 if t in alle_dateien else 0      # Tracknummer: Reihenfolge im Textordner
    bild = ["-i", cover, "-map", "0:a", "-map", "1:v", "-c:v", "mjpeg", "-disposition:v", "attached_pic",
            "-metadata:s:v", "comment=Cover (front)"] if cover else []
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error",
                    "-f", "concat", "-safe", "0", "-i", "/tmp/tts-azure-liste.txt", *bild,
                    *(["-ar", "44100", "-af", "loudnorm=I=-19:TP=-3:LRA=11"] if hoch else []),
                    "-b:a", "%dk" % kbit, "-id3v2_version", "3",
                    "-metadata", "title=" + name,
                    *(["-metadata", "track=%d/%d" % (nr, len(alle_dateien))] if nr else []),
                    "-metadata", "album=" + album,
                    "-metadata", "artist=" + artist, mp3], check=True)
    for p in teile:
        os.remove(p)
    erzeugt.append(os.path.basename(mp3))
ziel = os.path.relpath(mp3_dir)
print("Fertig: %d neue Datei(en) in %s" % (len(erzeugt), ziel))
for n in erzeugt[:10]:
    print("  mpv %s/%s" % (ziel, n.replace(" ", "\\ ")))
if len(erzeugt) > 10:
    print("  … und %d weitere" % (len(erzeugt) - 10))
