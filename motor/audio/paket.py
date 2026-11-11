#!/usr/bin/env python3
"""
paket.py – Hörbuch weitergeben (pureSATZ ab 2.72): Paket und Hörprobe in audio/verkauf/.
Aufruf über hoerbuch.py:  sh hb.sh paket [mp3-ordner]  ·  sh hb.sh hoerprobe [kapitel] [minuten]

Paket = ZIP mit Kapitel-MP3s (Mono, PAKET_KBIT, alle Tags + Cover), playlist.m3u, einer M4B mit Kapitelmarken,
cover.jpg und LIESMICH.txt. Die Original-MP3s bleiben unverändert.
Hörprobe = Ansage + die ersten Minuten eines Kapitels, am Schluss ausgeblendet (HOERPROBE in audio.conf).
"""
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from datetime import datetime

DATEN = os.environ.get("AUDIO_DIR") or os.getcwd()
ZIEL = os.path.join(DATEN, "verkauf")


def konf():
    conf = {}
    for z in open(os.path.join(DATEN, "audio.conf"), encoding="utf-8"):
        m = re.match(r'^([A-Z0-9_]+)="([^"]*)"', z.strip())
        if m:
            conf[m.group(1)] = m.group(2)
    return conf


def ffmpeg(*args):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args], check=True)


def dauer(datei):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", datei],
                       capture_output=True, text=True)
    return float(r.stdout.strip() or 0)


def quelle(arg=None):
    """MP3-Ordner: angegeben oder der zuletzt geänderte mp3-md-azure-…"""
    if arg:
        d = arg if os.path.isabs(arg) else os.path.join(DATEN, arg.rstrip("/"))
    else:
        alle = [d for d in glob.glob(os.path.join(DATEN, "mp3-md-azure-*")) if glob.glob(os.path.join(d, "*.mp3"))]
        d = max(alle, key=os.path.getmtime) if alle else ""
    if not d or not glob.glob(os.path.join(d, "*.mp3")):
        sys.exit("Kein MP3-Ordner gefunden – zuerst vertonen (hb → v).")
    return d


def titel(datei):
    """Kapitelname: erste Zeile des Textes in txt-md/ («Rennrad, Pfadi und House-Musik»), sonst aus dem Dateinamen."""
    stamm = os.path.splitext(os.path.basename(datei))[0]
    name = stamm.split("_", 1)[-1]
    txt = os.path.join(DATEN, "txt-md", stamm + ".txt")
    if name not in ("Ansage", "Abspann") and os.path.exists(txt):
        erste = open(txt, encoding="utf-8").readline().strip().rstrip(".").strip()
        if 0 < len(erste) <= 120:
            return erste
    return re.sub(r"\s+", " ", name.replace("-", " ")).strip()


def cover(conf):
    """COVER_QUADRAT (audio/…) vor dem Umschlag vorne (HB_COVER); sonst keins."""
    c = conf.get("COVER_QUADRAT", "")
    c = os.path.join(DATEN, c) if c and not os.path.isabs(c) else c
    for p in (c, os.environ.get("HB_COVER", "")):
        if p and os.path.exists(p):
            return p
    return ""


def angaben(conf):
    album = conf.get("ALBUM") or os.environ.get("HB_TITEL", "") or "Hörbuch"
    return dict(album=album, artist=conf.get("ARTIST") or os.environ.get("HB_AUTOR", ""),
                jahr=os.environ.get("HB_JAHR", "") or str(datetime.now().year))


def bild_args(bild, nr):
    return (["-i", bild, "-map", "0:a", "-map", f"{nr}:v", "-c:v", "mjpeg", "-disposition:v", "attached_pic"]
            if bild else ["-map", "0:a"])


def paket(arg=None):
    conf, src = konf(), quelle(arg)
    a, bild = angaben(conf), cover(konf())
    kbit = conf.get("PAKET_KBIT", "96")
    mp3s = sorted(glob.glob(os.path.join(src, "*.mp3")))
    texte = sorted(glob.glob(os.path.join(DATEN, "txt-md", "*.txt")))
    if texte:                                              # nur Kapitel, die es im Buch noch gibt – und alle davon
        stamm = lambda f: os.path.splitext(os.path.basename(f))[0]
        da = {stamm(f): f for f in mp3s}
        fehlt = [stamm(t) for t in texte if stamm(t) not in da]
        if fehlt:
            sys.exit(f"Noch nicht vertont ({len(fehlt)}): " + ", ".join(fehlt[:5]) + (" …" if len(fehlt) > 5 else "") +
                     " – zuerst vertonen (hb → v).")
        alt = [stamm(t) for t in texte if os.path.getmtime(t) > os.path.getmtime(da[stamm(t)])]
        if alt:
            print(f"Achtung: {len(alt)} Text(e) neuer als die MP3 (z. B. {alt[0]}) – vertonen (hb → v) bringt sie nach.")
        mp3s = [da[stamm(t)] for t in texte]
    n = len(mp3s)
    tmp = tempfile.mkdtemp(prefix="_paket-", dir=DATEN)
    try:
        klein = ""
        if bild:                                           # in jedem MP3 nur ein kleines Bild (600 px) – spart Platz
            klein = os.path.join(tmp, "_cover-600.jpg")
            ffmpeg("-i", bild, "-vf", "scale='min(600,iw)':-2", "-q:v", "3", klein)
        os.makedirs(os.path.join(tmp, "MP3"))
        m3u, kapitel, t0 = ["#EXTM3U"], [], 0
        print(f"Paket aus {os.path.basename(src)}/ – {n} Kapitel, MP3 {kbit} kbit Mono" + (", mit Cover" if bild else ", ohne Cover"))
        for i, f in enumerate(mp3s, 1):
            t = titel(f)
            name = f"{i:02d} {re.sub(r'[/:*?<>|\"]', '', t)}.mp3"
            ffmpeg("-i", f, *bild_args(klein, 1), "-ac", "1", "-ar", "44100", "-b:a", f"{kbit}k", "-id3v2_version", "3",
                   "-metadata", f"title={t}", "-metadata", f"track={i}/{n}", "-metadata", f"album={a['album']}",
                   "-metadata", f"artist={a['artist']}", "-metadata", f"album_artist={a['artist']}",
                   "-metadata", "genre=Hörbuch", "-metadata", f"date={a['jahr']}",
                   "-metadata", "comment=Gelesen von einer KI-Stimme", os.path.join(tmp, "MP3", name))
            d = dauer(f)
            m3u += [f"#EXTINF:{round(d)},{a['artist']} – {t}", f"MP3/{name}"]
            kapitel.append((t0, t0 + d, t)); t0 += d
            print(f"\r  {i}/{n}", end="", flush=True)
        print()
        open(os.path.join(tmp, "playlist.m3u"), "w", encoding="utf-8").write("\n".join(m3u) + "\n")
        # M4B: alle Original-MP3s hintereinander, Kapitelmarken aus den Dateinamen, AAC 64 kbit Mono
        liste = os.path.join(tmp, "_liste.txt")
        open(liste, "w", encoding="utf-8").write("".join("file '%s'\n" % f.replace("'", "'\\''") for f in mp3s))
        meta = os.path.join(tmp, "_kapitel.txt")
        esc = lambda s: re.sub(r"([=;#\\\n])", r"\\\1", s)
        with open(meta, "w", encoding="utf-8") as m:
            m.write(f";FFMETADATA1\ntitle={esc(a['album'])}\nartist={esc(a['artist'])}\nalbum={esc(a['album'])}\n"
                    f"genre=Hörbuch\ndate={a['jahr']}\ncomment=Gelesen von einer KI-Stimme\n")
            for s, e, t in kapitel:
                m.write(f"[CHAPTER]\nTIMEBASE=1/1000\nSTART={int(s * 1000)}\nEND={int(e * 1000)}\ntitle={esc(t)}\n")
        m4b = os.path.join(tmp, f"{a['album']}.m4b".replace("/", "-"))
        print("  M4B mit Kapitelmarken …")
        ffmpeg("-f", "concat", "-safe", "0", "-i", liste, "-i", meta, *(["-i", bild] if bild else []),
               "-map", "0:a", *(["-map", "2:v", "-c:v", "mjpeg", "-disposition:v", "attached_pic"] if bild else []),
               "-map_metadata", "1", "-map_chapters", "1", "-c:a", "aac", "-b:a", "64k", "-ac", "1", "-f", "mp4", m4b)
        if bild:
            shutil.copy(bild, os.path.join(tmp, "cover.jpg"))
        lang = f"{int(t0 // 3600)} Std. {int(t0 % 3600 // 60)} Min."
        open(os.path.join(tmp, "LIESMICH.txt"), "w", encoding="utf-8").write(
            f"{a['album']} – Hörbuch\nVon {a['artist']} · {a['jahr']} · {n} Kapitel · {lang}\n\n"
            f"Inhalt\n  {os.path.basename(m4b)}   das ganze Hörbuch in einer Datei, mit Kapiteln (Handy, Hörbuch-App)\n"
            "  MP3/            jedes Kapitel einzeln, für jeden Player\n"
            "  playlist.m3u    alle Kapitel in der richtigen Reihenfolge\n\n"
            "Gelesen von einer KI-Stimme.\n"
            f"© {a['jahr']} {a['artist']}. Nur für den eigenen Gebrauch – bitte nicht weitergeben. Danke!\n")
        os.makedirs(ZIEL, exist_ok=True)
        zipname = os.path.join(ZIEL, f"{os.path.basename(os.path.dirname(DATEN))}-Hoerbuch_{datetime.now():%Y%m%d-%H%M}.zip")
        with zipfile.ZipFile(zipname, "w", zipfile.ZIP_STORED) as z:          # MP3/M4B sind schon gepackt
            for p in sorted(glob.glob(os.path.join(tmp, "**"), recursive=True)):
                if os.path.isfile(p) and not os.path.basename(p).startswith("_"):
                    z.write(p, os.path.relpath(p, tmp))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"Fertig: verkauf/{os.path.basename(zipname)}  ({os.path.getsize(zipname) / 1e6:.0f} MB, {lang})")
    print(f"  Inhalt ansehen:  unzip -l verkauf/{os.path.basename(zipname)}")
    return 0


def hoerprobe(rest):
    conf = konf()
    w = (rest[0] if rest else conf.get("HOERPROBE", "0002 3").split()[0]).replace(".", "")
    minuten = float(rest[1] if len(rest) > 1 else (conf.get("HOERPROBE", "0002 3").split() + ["3"])[1])
    src = quelle(None)
    kap = [f for f in sorted(glob.glob(os.path.join(src, "*.mp3")))
           if os.path.basename(f).split("_")[0].replace(".", "").startswith(w)]
    if not kap:
        sys.exit(f"Kapitel {w} nicht gefunden – Kürzel wie in «sh hb.sh liste», z. B. 0002 = Vorwort.")
    ansage = glob.glob(os.path.join(src, "00.00.00_*.mp3"))
    a, bild = angaben(conf), cover(conf)
    os.makedirs(ZIEL, exist_ok=True)
    ziel = os.path.join(ZIEL, "hoerprobe.mp3")
    s = minuten * 60
    eingaenge = ([("-i", ansage[0])] if ansage else []) + [("-t", str(s), "-i", kap[0])]
    flach = [x for e in eingaenge for x in e]
    k = len(eingaenge)
    filt = (f"[{k - 1}:a]afade=t=out:st={max(0, s - 4)}:d=4[b];" +
            ("[0:a][b]concat=n=2:v=0:a=1[a]" if ansage else "[b]anull[a]"))
    ffmpeg(*flach, *(["-i", bild] if bild else []), "-filter_complex", filt, "-map", "[a]",
           *(["-map", f"{k}:v", "-c:v", "mjpeg", "-disposition:v", "attached_pic"] if bild else []),
           "-ac", "1", "-b:a", "128k", "-id3v2_version", "3", "-metadata", f"title=Hörprobe: {titel(kap[0])}",
           "-metadata", f"album={a['album']}", "-metadata", f"artist={a['artist']}",
           "-metadata", "comment=Gelesen von einer KI-Stimme", ziel)
    print(f"Fertig: verkauf/hoerprobe.mp3 – {'Ansage + ' if ansage else ''}{titel(kap[0])}, "
          f"{dauer(ziel) / 60:.1f} Min.   Anhören:  mpv verkauf/hoerprobe.mp3")
    return 0


if __name__ == "__main__":
    a = sys.argv[1:] or ["paket"]
    sys.exit(paket(a[1] if len(a) > 1 else None) if a[0] == "paket" else hoerprobe(a[1:]))
