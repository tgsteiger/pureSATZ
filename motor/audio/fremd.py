#!/usr/bin/env python3
"""
fremd.py – Fremdwörter fürs Hörbuch finden und entscheiden (pureSATZ ab 2.73).
Im Ordner audio/:
  sh hb.sh fremd          Scan + Prüfseite fremdwoerter.html – Entscheide kopieren, in die Aussprache-Liste einfügen
  sh hb.sh fremd server   dasselbe mit kleinem Server: «💾 übernehmen» schreibt direkt, ▶ hört ein Wort (Menü hb → u)
Scan: Wörter, die das deutsche Wörterbuch nicht kennt, ein fremdes aber schon (hunspell, wie LibreOffice).
Entscheide landen in aussprache-<stimme>.txt: «Wort = {fr: Wort}», «Wort = Aussprache» oder «# deutsch: Wort».
"""
import glob
import html
import json
import os
import re
import shutil
import subprocess
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
DATEN = os.environ.get("AUDIO_DIR") or os.getcwd()
PORT = 8766
# Sprache: Wörterbücher (erstes vorhandenes), Name, Farbe
SPRACHEN = {"fr": (("fr_CH", "fr_FR", "fr"), "französisch", "#2f6fb5"),
            "en": (("en_GB", "en_US", "en"), "englisch", "#2e8b57"),
            "es": (("es_ES", "es"), "spanisch", "#c0392b"),
            "it": (("it_IT", "it_CH", "it"), "italienisch", "#8e44ad")}
DEUTSCH = ("de_CH", "de_CH_frami", "de_DE", "de_DE_frami", "de_AT", "de")
ORTE = ("/usr/share/hunspell", "/usr/share/myspell", "/usr/share/myspell/dicts", "/Library/Spelling",
        os.path.expanduser("~/Library/Spelling"))
WORT = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿŒœ]+(?:['’-][A-Za-zÀ-ÖØ-öø-ÿŒœ]+)*")
INSTALL = "sudo apt install hunspell hunspell-de-ch hunspell-fr hunspell-es hunspell-it hunspell-en-gb"


def konf():
    conf = {}
    for z in open(os.path.join(DATEN, "audio.conf"), encoding="utf-8"):
        m = re.match(r'^([A-Z0-9_]+)="([^"]*)"', z.strip())
        if m:
            conf[m.group(1)] = m.group(2)
    return conf


def aussprache_datei():
    """Wie txt2mp3-azure.py: aussprache-<stimme>.txt, sonst AUSSPRACHE aus audio.conf."""
    c = konf()
    wahl = c.get("AZURE_STIMME", "1")
    stimme = c.get("AZURE_FAVORIT" + wahl, wahl) if wahl in ("1", "2") else wahl
    kurz = "-".join(stimme.split("-")[2:]).replace("MultilingualNeural", "").replace("Neural", "").replace(":", "-").lower()
    n = f"aussprache-{kurz}.txt"
    return os.path.join(DATEN, n if os.path.exists(os.path.join(DATEN, n)) else c.get("AUSSPRACHE", "aussprache.txt"))


def regeln_lesen():
    """{original klein: zeile} der bestehenden Regeln und {wort klein} aus «# deutsch: Wort»."""
    regeln, deutsch, p = {}, set(), aussprache_datei()
    if os.path.exists(p):
        for z in open(p, encoding="utf-8"):
            m = re.match(r"^\s*#\s*deutsch\s*:\s*(.+?)\s*$", z, re.I)
            if m:
                deutsch.add(m.group(1).lower())
                continue
            m = re.match(r"^ *([^#].*[^ ]) *= *(.*[^ ]) *$", z.rstrip("\n"))
            if m:
                regeln[m.group(1).lower()] = z.strip()
    return regeln, deutsch


def woerterbuch(namen):
    for n in namen:
        for o in ORTE:
            if os.path.exists(os.path.join(o, n + ".dic")):
                return os.path.join(o, n)
    return None


def unbekannt(woerter, dic):
    """Wörter, die hunspell mit diesem Wörterbuch nicht kennt."""
    if not woerter:
        return set()
    r = subprocess.run(["hunspell", "-d", dic, "-l", "-i", "UTF-8"], input="\n".join(woerter),
                       capture_output=True, text=True, encoding="utf-8")
    return set(r.stdout.split())


def texte():
    dateien = sorted(glob.glob(os.path.join(DATEN, "txt-md", "*.txt")))
    if not dateien:
        sys.exit("Noch keine Texte – zuerst:  sh hb.sh texte   (Menü hb → t)")
    return [(os.path.splitext(os.path.basename(f))[0], open(f, encoding="utf-8").read()) for f in dateien]


def scan(kapitel, regeln, deutsch):
    """{wort oder wortgruppe: sprache} – vermutete Fremdwörter (ohne schon geregelte und «deutsch lassen»).
    Benachbarte Fremdwörter derselben Sprache werden eine Gruppe («Trance Healing», «La Chaux-de-Fonds»)."""
    woerter = sorted({w for _, t in kapitel for w in WORT.findall(t) if len(w) >= 2})
    teile = sorted({x for w in woerter if "-" in w for x in w.split("-") if len(x) >= 2})
    de = woerterbuch(DEUTSCH)
    hinweis, sprache = "", {}
    if not shutil.which("hunspell") or not de:
        hinweis = "Wörterbücher fehlen – Scan nur nach Akzenten (é, ñ …). Für den ganzen Scan einmal: " + INSTALL
        for w in woerter:
            if re.search(r"[ñ¿¡]", w, re.I):
                sprache[w] = "es"
            elif re.search(r"[àâçéèêëîïôûùÿœ]", w, re.I):
                sprache[w] = "fr"
    else:
        alle = sorted(set(woerter) | set(teile))
        un_de = unbekannt(alle, de)
        kennt_de = lambda w: w not in un_de or ("-" in w and all(x not in un_de for x in w.split("-") if len(x) >= 2))
        fremd = [w for w in alle if not kennt_de(w)]
        fehlen = []
        for l in ("fr", "es", "it", "en"):                 # Reihenfolge = Vorrang bei Wörtern, die mehrere kennen
            dic = woerterbuch(SPRACHEN[l][0])
            if not dic:
                fehlen.append(l)
                continue
            un = unbekannt(fremd, dic)
            for w in fremd:
                if w not in un or ("-" in w and all(x not in un for x in w.split("-") if len(x) >= 2)):
                    sprache.setdefault(w, l)
        for w in list(sprache):                            # Akzente sind eindeutiger als das Wörterbuch
            if re.search(r"[ñ¿¡]", w, re.I):
                sprache[w] = "es"
        if fehlen:
            hinweis = "Ohne Wörterbuch: " + ", ".join(SPRACHEN[l][1] for l in fehlen) + " – installieren: " + INSTALL
    # Gruppen: Fremdwörter derselben Sprache direkt hintereinander (nur Leerzeichen dazwischen)
    kand, in_gruppe, einzeln = {}, {}, {}
    for _, t in kapitel:
        treffer = list(WORT.finditer(t))
        i = 0
        while i < len(treffer):
            w = treffer[i].group(0); l = sprache.get(w)
            j = i
            while l and j + 1 < len(treffer) and sprache.get(treffer[j + 1].group(0)) == l \
                    and t[treffer[j].end():treffer[j + 1].start()] == " ":
                j += 1
            if l and j > i:
                g = t[treffer[i].start():treffer[j].end()]
                kand[g] = l
                for k in range(i, j + 1):
                    in_gruppe[treffer[k].group(0)] = in_gruppe.get(treffer[k].group(0), 0) + 1
            elif l:
                einzeln[w] = einzeln.get(w, 0) + 1
            i = j + 1
    for w, n in einzeln.items():                           # einzeln nur, wenn es auch allein vorkommt
        if len(w) >= 3:
            kand[w] = sprache[w]
    kand = {w: l for w, l in kand.items() if w.lower() not in regeln and w.lower() not in deutsch}
    return kand, hinweis


def seite(kapitel, kand, regeln, deutsch, hinweis, server):
    wl = {x: l for g, l in kand.items() for x in WORT.findall(g)}      # Wörter in Kandidaten (auch in Gruppen)
    in_regel = {x.lower(): z for o, z in regeln.items() if " " in o for x in WORT.findall(o)}   # «Trance Healing = …»
    def markieren(text):
        def span(m):
            w = m.group(0); k = w.lower()
            if k in regeln or k in in_regel:
                titel = regeln.get(k) or in_regel[k]
                return f'<span class="w r" title="{html.escape(titel)}">{html.escape(w)}</span>'
            if k in deutsch:
                return f'<span class="w d" title="deutsch lassen">{html.escape(w)}</span>'
            if w in wl:
                return f'<span class="w c {wl[w]}">{html.escape(w)}</span>'
            return f'<span class="w">{html.escape(w)}</span>'
        teile, pos = [], 0
        for m in WORT.finditer(text):
            teile += [html.escape(text[pos:m.start()]), span(m)]
            pos = m.end()
        return "".join(teile + [html.escape(text[pos:])]).replace("\n", "<br>")
    zaehl = {g: sum(len(re.findall(r"(?<!\w)%s(?!\w)" % re.escape(g), t)) for _, t in kapitel) for g in kand}
    zeilen = "".join(
        f'<tr data-o="{html.escape(w)}"><td><span class="w c {l}">{html.escape(w)}</span></td>'
        f'<td>{SPRACHEN[l][1]}</td><td>{zaehl.get(w, 0)}×</td><td class="knoepfe"></td></tr>'
        for w, l in sorted(kand.items(), key=lambda x: (x[1], x[0].lower())))
    buch = "".join(f'<h3>{html.escape(n)}</h3><p>{markieren(t)}</p>' for n, t in kapitel)
    farben = "".join(f".{l}{{background:{c}22;border-bottom:2px solid {c}}} .b-{l}{{border-color:{c};color:{c}}}"
                     for l, (_, _, c) in SPRACHEN.items())
    legende = " ".join(f'<span class="w c {l}">{n}</span>' for l, (_, n, _) in SPRACHEN.items())
    bestehend = "".join(f"<li><code>{html.escape(z)}</code></li>" for z in sorted(regeln.values(), key=str.lower))
    return SEITE.replace("{{FARBEN}}", farben).replace("{{LEGENDE}}", legende).replace("{{HINWEIS}}", html.escape(hinweis)) \
        .replace("{{ZEILEN}}", zeilen or '<tr><td colspan="4">Keine neuen Kandidaten – im Text unten jedes Wort anklickbar.</td></tr>') \
        .replace("{{BUCH}}", buch).replace("{{BESTEHEND}}", bestehend).replace("{{DATEI}}", html.escape(os.path.basename(aussprache_datei()))) \
        .replace("{{SERVER}}", "true" if server else "false").replace("{{ANZAHL}}", str(len(kand)))


def bauen(server=False):
    regeln, deutsch = regeln_lesen()
    kapitel = texte()
    kand, hinweis = scan(kapitel, regeln, deutsch)
    print(f"Fremdwörter: {len(kand)} Kandidaten in {len(kapitel)} Kapiteln" + (f"  ({hinweis})" if hinweis else ""))
    return seite(kapitel, kand, regeln, deutsch, hinweis, server)


def speichern(eintraege):
    """Entscheide in die Aussprache-Liste: gleiche Originale ersetzen, neue unter «## KLINGEN FALSCH»."""
    p = aussprache_datei()
    zeilen = open(p, encoding="utf-8").read().splitlines() if os.path.exists(p) else ["## KLINGEN FALSCH", "## KLINGEN GUT"]
    if os.path.exists(p):
        shutil.copy(p, p + ".bak")
    weg = {e["o"].strip().lower() for e in eintraege}
    def original(z):
        m = re.match(r"^\s*#\s*deutsch\s*:\s*(.+?)\s*$", z, re.I) or re.match(r"^ *([^#].*[^ ]) *= *(.*[^ ]) *$", z)
        return m.group(1).lower() if m else None
    zeilen = [z for z in zeilen if original(z) not in weg]
    regel = [e["zeile"] for e in eintraege if not e["zeile"].startswith("#")]
    deutsch = [e["zeile"] for e in eintraege if e["zeile"].startswith("#")]
    i = next((k for k, z in enumerate(zeilen) if z.strip().upper().startswith("## KLINGEN FALSCH")), None)
    if i is None:
        zeilen += ["## KLINGEN FALSCH"]; i = len(zeilen) - 1
    zeilen[i + 1:i + 1] = regel
    if deutsch:
        if "# --- deutsch lassen (Fremdwörter-Scan) ---" not in zeilen:
            zeilen.append("# --- deutsch lassen (Fremdwörter-Scan) ---")
        zeilen += deutsch
    open(p, "w", encoding="utf-8").write("\n".join(zeilen) + "\n")
    return f"{len(regel)} Regel(n) unter «KLINGEN FALSCH», {len(deutsch)}× deutsch lassen → {os.path.basename(p)} (Sicherung .bak)"


def hoeren(o, zeile):
    """Original und Entscheid nacheinander sprechen (ohne die Aussprache-Liste) → MP3-Bytes."""
    m = re.match(r"^ *(.*[^ ]) *= *(.*[^ ]) *$", zeile)
    ersatz = m.group(2) if m else o
    open(os.path.join(DATEN, "_fremd-hoeren.txt"), "w", encoding="utf-8").write(f"{o}\n\n{ersatz}\n")
    open(os.path.join(DATEN, "_fremd-leer.txt"), "w", encoding="utf-8").write("")
    for alt in glob.glob(os.path.join(DATEN, "_fremd-hoeren-*.mp3")):
        os.remove(alt)
    r = subprocess.run([sys.executable, os.path.join(DIR, "probe-azure.py"), "_fremd-hoeren.txt"], cwd=DATEN,
                       capture_output=True, text=True, env=dict(os.environ, PROBE_REGELN="_fremd-leer.txt", AUDIO_DIR=DATEN))
    mp3 = glob.glob(os.path.join(DATEN, "_fremd-hoeren-*.mp3"))
    if not mp3:
        aus = r.stdout + r.stderr
        raise RuntimeError("Azure-Paket fehlt – im Menü hb → c" if "No module named 'azure" in aus else
                           "Azure-Schlüssel fehlt – hb → s" if "AZURE_SPEECH_KEY fehlt" in aus else aus.strip()[-300:] or "keine MP3")
    daten = open(mp3[0], "rb").read()
    for f in mp3 + [os.path.join(DATEN, "_fremd-hoeren.txt"), os.path.join(DATEN, "_fremd-leer.txt")]:
        os.remove(f)
    return daten


def server():
    import http.server
    import webbrowser

    class H(http.server.BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def senden(self, body, typ="text/html; charset=utf-8", code=200):
            b = body if isinstance(body, bytes) else body.encode("utf-8")
            self.send_response(code); self.send_header("Content-Type", typ)
            self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)

        def do_GET(self):
            if self.path.split("?")[0] == "/":
                return self.senden(bauen(server=True))
            self.senden("nicht gefunden", "text/plain; charset=utf-8", 404)

        def do_POST(self):
            daten = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
            try:
                if self.path == "/speichern":
                    return self.senden(json.dumps({"ok": speichern(daten.get("eintraege", []))}), "application/json")
                if self.path == "/hoeren":
                    return self.senden(hoeren(daten["o"], daten["zeile"]), "audio/mpeg")
            except Exception as e:                                     # Meldung zur Seite, Server läuft weiter
                return self.senden(json.dumps({"fehler": str(e)}), "application/json", 500)
            self.senden("nicht gefunden", "text/plain; charset=utf-8", 404)

    try:
        srv = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), H)
    except OSError:
        sys.exit(f"Port {PORT} belegt – läuft die Prüfseite schon? http://localhost:{PORT}")
    print(f"Prüfseite: http://localhost:{PORT}   (beenden: Ctrl+C)")
    if os.environ.get("BROWSER") != "true":
        webbrowser.open(f"http://localhost:{PORT}")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nPrüfseite beendet.")
    return 0


def main():
    a = sys.argv[1:]
    if a[:1] == ["server"]:
        return server()
    ziel = os.path.join(DATEN, "fremdwoerter.html")
    open(ziel, "w", encoding="utf-8").write(bauen(server=False))
    print(f"Prüfseite: {os.path.relpath(ziel)}   (mit Speichern und ▶ hören: sh hb.sh fremd server · Menü hb → u)")
    if "--nicht-oeffnen" not in a and shutil.which("xdg-open"):
        subprocess.Popen(["xdg-open", ziel], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return 0


SEITE = r"""<!doctype html><html lang="de"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Fremdwörter – Hörbuch</title>
<style>
:root{--gold:#b98b2e;--bg:#fafaf7;--fg:#222;--line:#d0d0c8;--box:#fff}
@media (prefers-color-scheme:dark){:root{--bg:#1c1c1e;--fg:#e8e8e8;--line:#444;--box:#2a2a2d}}
body{margin:0;padding:16px 16px 140px;background:var(--bg);color:var(--fg);font:15px/1.6 -apple-system,system-ui,sans-serif;max-width:1000px}
h1{color:var(--gold);font-size:20px;margin:0 0 4px} h2{font-size:16px;margin:22px 0 6px;color:var(--gold)} h3{font-size:14px;margin:18px 0 4px;opacity:.7}
small,.hinweis{opacity:.75;font-size:13px} .hinweis{color:#c0392b}
table{border-collapse:collapse;width:100%} td{padding:3px 6px;border-bottom:1px solid var(--line);font-size:14px}
button{font:inherit;font-size:13px;padding:3px 8px;margin:1px;border:1px solid var(--line);border-radius:6px;background:var(--box);color:var(--fg);cursor:pointer}
button.an{background:var(--gold);color:#fff;border-color:var(--gold)}
.w{cursor:pointer;border-radius:3px} .w:hover{outline:1px dashed var(--gold)}
.r{border-bottom:2px dotted #888} .d{opacity:.55;text-decoration:line-through dotted}
.entschieden{outline:2px solid var(--gold);outline-offset:1px}
{{FARBEN}}
#pop{position:absolute;display:none;z-index:9;background:var(--box);border:1px solid var(--line);border-radius:8px;box-shadow:0 4px 14px #0003;padding:8px;max-width:360px}
#pop b{display:block;margin-bottom:4px}
#leiste{position:fixed;left:0;right:0;bottom:0;background:var(--box);border-top:3px solid var(--gold);padding:8px 16px;box-shadow:0 -4px 12px #0003}
#leiste pre{margin:4px 0;max-height:70px;overflow:auto;font-size:12px}
.buch p{margin:0 0 6px}
</style></head><body>
<h1>Fremdwörter fürs Hörbuch</h1>
<small>Entscheide kommen in <b>{{DATEI}}</b> unter «KLINGEN FALSCH» – danach anhören mit <b>hb → w</b>, die guten nach «KLINGEN GUT» schieben.
Legende: {{LEGENDE}} · <span class="w r">schon geregelt</span> · <span class="w d">deutsch lassen</span></small>
<div class="hinweis">{{HINWEIS}}</div>
<h2>Kandidaten ({{ANZAHL}})</h2>
<table id="kand">{{ZEILEN}}</table>
<h2>Im Text – jedes Wort anklickbar, mehrere Wörter: mit der Maus markieren</h2>
<div class="buch">{{BUCH}}</div>
<h2>Schon in der Aussprache-Liste</h2><ul>{{BESTEHEND}}</ul>
<div id="pop"></div>
<div id="leiste"><span id="zahl">Noch nichts entschieden.</span>
<button onclick="kopieren()">📋 kopieren</button><button id="sp" onclick="speichern()" style="display:none">💾 in Aussprache-Liste übernehmen</button>
<span id="meldung"></span><pre id="zeilen"></pre></div>
<script>
const SERVER={{SERVER}},L={fr:'fr',en:'en',es:'es',it:'it'},ent={};
function zeile(o,a,p){return a==='d'?'# deutsch: '+o:a==='p'?o+' = '+p:o+' = {'+a+': '+o+'}'}
function knoepfe(o){const k=['fr','en','es','it'].map(l=>`<button class="b-${l}" data-a="${l}">${l}</button>`).join('')
 +'<button data-a="p" title="eigene Aussprache">✎</button><button data-a="d" title="deutsch lassen">✗ deutsch</button>'
 +(SERVER?'<button data-a="h" title="Original und Entscheid anhören">▶</button>':'')+'<button data-a="x" title="Entscheid entfernen">–</button>';
 return k}
document.querySelectorAll('#kand tr[data-o]').forEach(tr=>{tr.querySelector('.knoepfe').innerHTML=knoepfe(tr.dataset.o)});
function setzen(o,a){if(a==='x'){delete ent[o]}else if(a==='p'){const p=prompt('Aussprache für «'+o+'» (z. B. Scha-le):',ent[o]&&ent[o].a==='p'?ent[o].p:o);if(!p)return;ent[o]={a,p}}else ent[o]={a};zeigen()}
function zeigen(){const z=Object.entries(ent).map(([o,e])=>zeile(o,e.a,e.p));document.getElementById('zeilen').textContent=z.join('\n');
 document.getElementById('zahl').textContent=z.length?z.length+' entschieden':'Noch nichts entschieden.';document.getElementById('sp').style.display=SERVER&&z.length?'':'none';
 document.querySelectorAll('.w').forEach(s=>s.classList.toggle('entschieden',!!ent[s.textContent]));
 document.querySelectorAll('#kand tr[data-o]').forEach(tr=>tr.querySelectorAll('button[data-a]').forEach(b=>b.classList.toggle('an',!!ent[tr.dataset.o]&&ent[tr.dataset.o].a===b.dataset.a)))}
async function hoeren(o){const e=ent[o]||{a:'d'},m=document.getElementById('meldung');m.textContent=' ⏳ '+o+' …';
 try{const r=await fetch('/hoeren',{method:'POST',body:JSON.stringify({o,zeile:zeile(o,e.a,e.p)})});
 if(!r.ok){m.textContent=' ✖ '+((await r.json()).fehler||r.status);return}new Audio(URL.createObjectURL(await r.blob())).play();m.textContent=' ▶ '+o}catch(x){m.textContent=' ✖ '+x}}
document.addEventListener('click',e=>{const b=e.target.closest('button[data-a]');if(!b)return;const o=b.closest('[data-o]').dataset.o;
 if(b.dataset.a==='h')hoeren(o);else{setzen(o,b.dataset.a);if(b.closest('#pop'))pop.style.display='none'}});
const pop=document.getElementById('pop');
function oeffnen(o,x,y){pop.dataset.o=o;pop.innerHTML='<b>'+o.replace(/</g,'&lt;')+'</b>'+knoepfe(o);pop.style.left=Math.min(x,innerWidth-370)+'px';pop.style.top=(y+14)+'px';pop.style.display='block'}
document.querySelector('.buch').addEventListener('mouseup',e=>{const s=getSelection().toString().trim().replace(/\s+/g,' ');
 if(s&&s.includes(' ')){oeffnen(s,e.pageX,e.pageY);return}const w=e.target.closest('.w');if(w)oeffnen(w.textContent,e.pageX,e.pageY)});
document.addEventListener('mousedown',e=>{if(!e.target.closest('#pop')&&!e.target.closest('.buch'))pop.style.display='none'});
document.addEventListener('keydown',e=>{if(e.key==='Escape')pop.style.display='none'});
function kopieren(){const t=document.getElementById('zeilen').textContent;if(!t)return;const ok=()=>document.getElementById('meldung').textContent=' ✓ kopiert – in die Aussprache-Liste unter «KLINGEN FALSCH» einfügen (gleiche Wörter dort vorher löschen)';
 if(navigator.clipboard&&window.isSecureContext)navigator.clipboard.writeText(t).then(ok);else{const a=document.createElement('textarea');a.value=t;document.body.appendChild(a);a.select();document.execCommand('copy');a.remove();ok()}}
async function speichern(){const eintraege=Object.entries(ent).map(([o,e])=>({o,zeile:zeile(o,e.a,e.p)}));
 const r=await fetch('/speichern',{method:'POST',body:JSON.stringify({eintraege})}),j=await r.json();
 if(j.ok){alert('✓ '+j.ok+'\n\nWeiter: Menü hb → w (anhören), dann v (vertonen – geänderte Wörter werden erkannt).');location.reload()}else alert('✖ '+j.fehler)}
</script></body></html>"""

if __name__ == "__main__":
    sys.exit(main())
