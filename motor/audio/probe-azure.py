#!/usr/bin/env python3
# Hörproben mit Azure – Favoriten, Sprache, Tempo und Aussprache wie das Buch (pureSATZ, über hoerbuch.py / Menü hb)
# Im Ordner audio/:  sh hb.sh probe                 probe.txt mit der eingestellten Stimme
#                    sh hb.sh probe 2 -10%          Stimme 2, Tempo −10 %   ·   alle = alle Stimmen   ·   l = Liste
#                    sh hb.sh probe probe-namen.txt  anderer Probetext (im Ordner audio/)
#                    sh hb.sh woerter               «## KLINGEN FALSCH» anhören: Original, dann Aussprache
# Ergebnis im Ordner audio/: probe-<stimme>-t<tempo>.mp3 bzw. aussprache-<stimme>-t<tempo>.mp3 (z. B. probe-ollie-t-8.mp3)
import os, re, sys, subprocess, tempfile
from xml.sax.saxutils import escape

SPRACHEN = {"fr": "fr-FR", "en": "en-GB", "es": "es-ES", "it": "it-IT", "de": "de-DE"}

def sprachen(text, haupt, rate):
    """SSML-Teil in <lang><prosody> (wie bisher). {fr: La Chaux-de-Fonds} aus der Aussprache-Liste wird ein eigener
    Teil in dieser Sprache (ab 2.72.4); lang bleibt direkt unter voice, wie Azure es verlangt."""
    teile = re.split(r"\{([a-z]{2}(?:-[A-Z]{2})?):\s*([^{}]+?)\s*\}", text)    # Text, Code, Wort, Text, …
    aus = []
    for i in range(0, len(teile), 3):
        for code, stueck in ((haupt, teile[i]),) + (((teile[i + 1], teile[i + 2]),) if i + 1 < len(teile) else ()):
            if not stueck:
                continue
            code = SPRACHEN.get(code, code) if code else ""
            p = '<prosody rate="%s">%s</prosody>' % (rate, stueck)
            aus.append('<lang xml:lang="%s">%s</lang>' % (code, p) if code else p)
    return "".join(aus)

DIR = os.path.dirname(os.path.abspath(__file__))              # Skripte (motor/audio)
DATEN = os.environ.get("AUDIO_DIR") or DIR                     # Buch: audio/

# Probetext, falls audio/probe.txt fehlt (eigene Texte gehören in audio/probe.txt – bleiben bei Updates)
TEXT = "Mein erstes Buch, gelesen von einer KI-Stimme. Im Jahr 1974 kam ich in Bern zur Welt."

conf = {}
with open(os.path.join(DATEN, "audio.conf"), encoding="utf-8") as f:
    for zeile in f:
        m = re.match(r'^([A-Z0-9_]+)="([^"]*)"', zeile.strip()) 
        if m:
            conf[m.group(1)] = m.group(2)

STIMMEN = list(dict.fromkeys([
    conf.get("AZURE_FAVORIT1", "en-GB-OllieMultilingualNeural"),
    conf.get("AZURE_FAVORIT2", "de-DE-FlorianMultilingualNeural"),
    "de-DE-Florian:DragonHDLatestNeural",
    "de-DE-ConradNeural",
    "de-DE-ChristophNeural",
    "de-CH-JanNeural",
    "de-CH-LeniNeural",
]))

args = sys.argv[1:]
hoeren = any(a in ("aussprache", "woerter") for a in args)
quelle = next((a for a in args if a.endswith(".txt")), "probe.txt")
args = [a for a in args if a not in ("aussprache", "woerter") and not a.endswith(".txt")]
if args and args[0] in ("liste", "l"):
    for i, s in enumerate(STIMMEN, 1):
        print(f"{i}  {s}" + ("   (Favorit %d)" % i if i <= 2 else ""))
    print("Aufruf: sh hb.sh probe [NUMMER|alle] [TEMPO, z. B. -10%] [probe-xy.txt]")
    sys.exit(0)

wahl = conf.get("AZURE_STIMME", "1")
if args and (args[0] == "alle" or args[0].isdigit()):
    wahl = args.pop(0)
if wahl == "alle":
    auswahl = STIMMEN
elif wahl.isdigit():
    auswahl = [STIMMEN[int(wahl) - 1]]
else:
    auswahl = [wahl]                                   # ganzer Name aus audio.conf
rate = next((a for a in args if re.match(r"^[+-]?\d+%$", a)), conf.get("AZURE_RATE", "-8%"))
sprache = conf.get("AZURE_SPRACHE", "")

import azure.cognitiveservices.speech as speechsdk
key = os.environ.get("AZURE_SPEECH_KEY")
if not key:
    print("AZURE_SPEECH_KEY fehlt (export in ~/.bashrc?)"); sys.exit(1)
speech_config = speechsdk.SpeechConfig(
    subscription=key, region=os.environ.get("AZURE_SPEECH_REGION", "switzerlandnorth"))
speech_config.set_speech_synthesis_output_format(
    speechsdk.SpeechSynthesisOutputFormat.Audio24Khz96KBitRateMonoMp3)

for stimme in auswahl:
    kurz = "-".join(stimme.split("-")[2:]).replace("MultilingualNeural", "").replace("Neural", "").replace(":", "-").lower()
    aus = f"aussprache-{kurz}.txt"                     # wie txt2mp3-azure.py
    if not os.path.exists(os.path.join(DATEN, aus)):
        aus = conf.get("AUSSPRACHE", "aussprache.txt")
    art = "aussprache" if hoeren else os.path.splitext(os.path.basename(quelle))[0]
    datei = os.path.join(DATEN, f"{art}-{kurz}-t{rate.replace('%', '').lstrip('+')}.mp3")   # wie die MP3-Ordner: t-8
    if hoeren:                                         # nur «## KLINGEN FALSCH» (bis zum nächsten ##)
        teile, drin = [], False
        for z in open(os.path.join(DATEN, aus), encoding="utf-8"):
            if z.startswith("##"):
                drin = "falsch" in z.lower()
                continue
            if drin and "=" in z and not z.lstrip().startswith("#"):
                o, e = (x.strip() for x in z.split("=", 1))
                teile.append(f'{escape(o)}<break time="600ms"/>{escape(e)}<break time="1500ms"/>')
        if not teile:
            print(f"Nichts zu hören: in {aus} fehlt «## KLINGEN FALSCH» oder ist leer."); continue
        text = "".join(teile)
    else:                                              # Probetext mit den Regeln des Buchs (# = aus, Leerzeile = Absatz)
        pfad = quelle if os.path.isabs(quelle) else os.path.join(DATEN, quelle)
        if not os.path.exists(pfad):
            if quelle != "probe.txt":
                sys.exit(f"Nicht gefunden: {quelle} (im Ordner audio/)")
            with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as t:
                t.write(TEXT + "\n")
            pfad = t.name
        zeilen = subprocess.run(["bash", os.path.join(DIR, "text-vorbereiten.sh"), pfad],
                                capture_output=True, text=True, check=True,
                                env=dict(os.environ, AUSSPRACHE_DATEI=os.environ.get("PROBE_REGELN") or aus,   # fremd.py: ohne Regeln
                                         AUDIO_DIR=DATEN)).stdout.splitlines()
        text = ('<break time="%s"/>' % conf.get("AZURE_PAUSE", "1200ms")).join(escape(z.strip()) for z in zeilen if z.strip())
        if not text:
            print(f"Nichts zu hören: {quelle} ist leer (oder alles mit # auskommentiert)."); continue
    inhalt = sprachen(text, sprache, rate)              # <lang><prosody>…, {fr: …} als eigener Teil
    ssml = ('<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="de-DE">'
            f'<voice name="{stimme}">{inhalt}</voice></speak>')
    synth = speechsdk.SpeechSynthesizer(speech_config=speech_config,
                                        audio_config=speechsdk.audio.AudioOutputConfig(filename=datei))
    r = synth.speak_ssml_async(ssml).get()
    if r.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"Fertig: {os.path.relpath(datei)}  ({stimme}, Tempo {rate}, {aus})")
        print(f"  mpv {os.path.relpath(datei)}")
    else:
        print(f"Fehler bei {stimme}:", r.cancellation_details.error_details)
