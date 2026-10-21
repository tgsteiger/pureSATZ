#!/usr/bin/env python3
"""
landingpage.py – erneuert die Webseite von pureSATZ im Ordner docs/ (GitHub Pages).

Im Ordner pureSATZ:
    python3 docs/landingpage.py          Hallo-Buch bauen, Bilder daraus, docs/index.html und docs/hilfe.html
    python3 docs/landingpage.py ohne-bilder   nur die Seiten (Bilder bleiben)

Danach:  git add docs && git commit -m "Webseite" && git push
Die Seite erscheint unter https://tgsteiger.github.io/pureSATZ/ (GitHub: Settings → Pages → main, /docs).
Inhalt der Schritte wie START.md. Version aus motor/VERSION.
"""
import html
import os
import shutil
import subprocess
import sys

DOCS = os.path.dirname(os.path.abspath(__file__))
HIER = os.path.dirname(DOCS)
HALLO = os.path.normpath(os.path.join(HIER, "..", "Hallo-Buch"))
REPO = "https://github.com/tgsteiger/pureSATZ"
ZIP = REPO + "/archive/refs/heads/main.zip"


def bilder():
    """Hallo-Buch neu bauen und drei Bilder daraus machen (läuft mit dem Python des Hallo-Buchs)."""
    import pypdfium2 as pdfium
    from PIL import Image
    pdf = os.path.join(HALLO, "ausgabe-normal", "Hallo-Buch.pdf")
    d = pdfium.PdfDocument(pdf)
    texte = [d[i].get_textpage().get_text_range() for i in range(len(d))]
    ziel = os.path.join(DOCS, "bilder")
    os.makedirs(ziel, exist_ok=True)

    def seite(i, breite):
        im = d[i].render(scale=3).to_pil().convert("RGB")
        return im.resize((breite, round(im.height * breite / im.width)), Image.LANCZOS)

    def rahmen(teile, name):
        rand, h = 18, max(t.height for t in teile)
        w = sum(t.width for t in teile) + rand * (len(teile) + 1)
        bg = Image.new("RGB", (w, h + 2 * rand), (234, 226, 210))
        x = rand
        for t in teile:
            bg.paste(t, (x, rand)); x += t.width + rand
        bg.save(os.path.join(ziel, name), optimize=True, quality=86)
        print("  bilder/" + name)

    rahmen([seite(0, 420)], "umschlag.jpg")
    i = next((k for k, t in enumerate(texte) if "aber schmaler" in t), 9)
    links = i if i % 2 == 1 else i - 1          # Doppelseite: gerade Seitenzahl links (= Index ungerade)
    rahmen([seite(links, 520), seite(links + 1, 520)], "doppelseite.jpg")
    k = next((k for k, t in enumerate(texte) if "Erster Schritt" in t), 7)
    rahmen([seite(k, 520)], "aufzaehlung.jpg")


def hilfe_kopieren():
    """hilfe.html des Ordners pureSATZ als docs/hilfe.html (mit Schriften in docs/fonts/)."""
    sys.path.insert(0, os.path.join(HIER, "motor"))
    import hilfe
    quelle = hilfe.erzeuge(HIER)
    text = open(quelle, encoding="utf-8").read().replace("url(motor/fonts/", "url(fonts/")
    with open(os.path.join(DOCS, "hilfe.html"), "w", encoding="utf-8") as f:
        f.write(text)
    os.makedirs(os.path.join(DOCS, "fonts"), exist_ok=True)
    for s in ("Lora-Regular.ttf", "Lora-Bold.ttf", "Lora-Italic.ttf", "Poppins-Regular.ttf", "Poppins-Medium.ttf",
              "SCHRIFTEN-LIZENZ.md"):
        shutil.copy2(os.path.join(HIER, "motor", "fonts", s), os.path.join(DOCS, "fonts", s))
    print("  hilfe.html, fonts/")


def code(lx, win=None):
    win = win if win is not None else lx
    k = '<button class="kopie" type="button">kopieren</button>'
    return (f'<div class="code">{k}<pre><code class="lx">{html.escape(lx)}</code>'
            f'<code class="win">{html.escape(win)}</code></pre></div>')


SCHRITTE = {
    "linux": [
        ("Herunterladen und auspacken", "ZIP laden, auspacken und den Ordner <b>pureSATZ-main</b> in <b>pureSATZ</b> "
         "umbenennen. Mit git geht auch:", "git clone https://github.com/tgsteiger/pureSATZ.git"),
        ("Terminal im Ordner öffnen", "Im Dateimanager Rechtsklick in den Ordner pureSATZ → «Im Terminal öffnen».", None),
        ("Einrichten (einmalig)", "Prüft alles und installiert, was fehlt (Python, auf Wunsch git):",
         "bash pc-einrichten/linux-einrichten.sh"),
        ("Hallo-Buch ansehen", "Legt ein Beispielbuch an, baut es und öffnet das PDF. Beim ersten Mal etwa eine Minute.",
         "sh hallo.sh"),
        ("Eigenes Buch anlegen", "Fragt Titel, Autor und Format ab und legt dein Buch neben pureSATZ an.",
         "sh setup/setup.sh"),
    ],
    "mac": [
        ("Herunterladen und auspacken", "ZIP laden (Safari packt es selbst aus) und den Ordner <b>pureSATZ-main</b> in "
         "<b>pureSATZ</b> umbenennen.", None),
        ("Terminal im Ordner öffnen", "Programme → Dienstprogramme → Terminal. <code>cd </code> tippen (mit Leerzeichen), "
         "den Ordner pureSATZ ins Fenster ziehen, Enter.", None),
        ("Einrichten (einmalig)", "Prüft alles. Fehlt Python, öffnet sich python.org: den «macOS 64-bit universal2 "
         "installer» laden, installieren und den Befehl nochmals starten.", "bash pc-einrichten/mac-einrichten.sh"),
        ("Hallo-Buch ansehen", "Legt ein Beispielbuch an, baut es und öffnet das PDF. Beim ersten Mal etwa eine Minute.",
         "sh hallo.sh"),
        ("Eigenes Buch anlegen", "Fragt Titel, Autor und Format ab und legt dein Buch neben pureSATZ an.",
         "sh setup/setup.sh"),
    ],
    "win": [
        ("Herunterladen und auspacken", "ZIP laden, Rechtsklick → «Alle extrahieren …» und den Ordner "
         "<b>pureSATZ-main</b> in <b>pureSATZ</b> umbenennen.", None),
        ("Einrichten (einmalig)", "Im Ordner <b>pc-einrichten</b> die Datei <b>win-einrichten.bat</b> doppelklicken. "
         "Fehlt Python, wird es installiert (oder python.org öffnet sich: beim Installieren «Add python.exe to PATH» "
         "anhaken). Danach das Fenster schliessen und die Datei nochmals starten.", None),
        ("Hallo-Buch ansehen", "Im Ordner pureSATZ <b>hallo.bat</b> doppelklicken. Legt ein Beispielbuch an, baut es "
         "und öffnet das PDF. Beim ersten Mal etwa eine Minute.", None),
        ("Terminal im Ordner öffnen", "Rechtsklick in den Ordner pureSATZ → «Im Terminal öffnen» (PowerShell).", None),
        ("Eigenes Buch anlegen", "Fragt Titel, Autor und Format ab und legt dein Buch neben pureSATZ an.",
         ".\\setup\\setup.bat"),
    ],
}
PYTHON = {"linux": "", "mac": "https://www.python.org/downloads/macos/",
          "win": "https://www.python.org/downloads/windows/"}

KACHELN = [
    ("Zwei Ausgaben, eine Datei", "Öffentliche Fassung und z. B. «Unzensiert» oder «Director's Cut» aus demselben Text."),
    ("Druckfertig für epubli", "Buchblock und Umschlag mit Rücken, für Hardcover und Softcover. Probedruck als Booklet."),
    ("E-Book", "EPUB mit Inhaltsverzeichnis, Bildbeschreibungen und Leseprobe – aus denselben Dateien."),
    ("Geschichten sammeln", "Jede Geschichte eine Datei, mit Stand von der Idee bis fertig und einer Übersicht."),
    ("Tabellen, Fotos, Listen", "Tabellen aus CSV, Fotos in einheitlicher Grösse, Aufzählungen, Zeitstrahl."),
    ("Hilfe und Sicherheit", "Hilfe mit Suche, automatischer Verlauf jeder Fassung, ZIP-Sicherung, auf Wunsch GitHub."),
]


def seite(version):
    tabs, panels = [], []
    for os_, name in (("linux", "Linux"), ("mac", "Mac"), ("win", "Windows")):
        tabs.append(f'<button type="button" data-os="{os_}">{name}</button>')
        items = []
        for nr, (titel, text, befehl) in enumerate(SCHRITTE[os_], 1):
            items.append(f'<li><span class="nr">{nr}</span><div><h3>{titel}</h3><p>{text}</p>'
                         + (code(befehl) if befehl else "") + "</div></li>")
        py = (f'<p class="leise">Python 3.10 oder neuer: <a href="{PYTHON[os_]}">python.org</a> · git (freiwillig): '
              f'<a href="https://git-scm.com/downloads">git-scm.com</a></p>' if PYTHON[os_] else
              '<p class="leise">Python ist auf Linux meist schon da; das Einrichten ergänzt, was fehlt.</p>')
        panels.append(f'<div class="panel" data-os="{os_}"><ol class="schritte">{"".join(items)}</ol>{py}</div>')
    kacheln = "".join(f'<div class="kachel"><h3>{t}</h3><p>{x}</p></div>' for t, x in KACHELN)
    return f"""<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>pureSATZ – in fünf Minuten zu deinem ersten Buch</title>
<meta name="description" content="pureSATZ macht aus Markdown ein druckfertiges Buch, E-Book und Umschlag für epubli. Linux, Mac und Windows, kostenlos für eigene Bücher.">
<style>
@font-face{{font-family:Poppins;src:url(fonts/Poppins-Regular.ttf)}}
@font-face{{font-family:Poppins;font-weight:500;src:url(fonts/Poppins-Medium.ttf)}}
@font-face{{font-family:Lora;src:url(fonts/Lora-Regular.ttf)}}
@font-face{{font-family:Lora;font-style:italic;src:url(fonts/Lora-Italic.ttf)}}
@font-face{{font-family:Lora;font-weight:bold;src:url(fonts/Lora-Bold.ttf)}}
:root{{--papier:#FBF6EC;--karte:#fff;--text:#2E2A26;--leise:#6E655C;--haupt:#1E428A;--akzent:#B8873B;--linie:#e7dfd0;--code:#f4efe4}}
@media (prefers-color-scheme:dark){{:root{{--papier:#1d1b19;--karte:#2a2724;--text:#ece6dc;--leise:#b4ab9f;--haupt:#9db7ec;
--akzent:#d4a65a;--linie:#3b3732;--code:#24211e}}}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--papier);color:var(--text);font:17px/1.6 Lora,Georgia,serif}}
a{{color:var(--haupt)}} .wrap{{max-width:1060px;margin:0 auto;padding:0 20px}}
header{{display:flex;justify-content:space-between;align-items:center;padding:18px 0}}
.logo{{font:500 22px Poppins,system-ui,sans-serif;color:var(--haupt);text-decoration:none}} .logo b{{color:var(--akzent);font-weight:500}}
nav a{{font:14px Poppins,system-ui,sans-serif;margin-left:18px;text-decoration:none}}
.held{{display:grid;grid-template-columns:1.1fr .9fr;gap:40px;align-items:center;padding:30px 0 50px}}
h1{{font:500 clamp(30px,5vw,46px)/1.15 Poppins,system-ui,sans-serif;color:var(--haupt);margin:0 0 16px}}
.unter{{font-size:19px;color:var(--leise);margin:0 0 26px}}
.knopf{{display:inline-block;font:500 15px Poppins,system-ui,sans-serif;padding:12px 22px;border-radius:26px;text-decoration:none;margin:0 10px 10px 0}}
.knopf.voll{{background:var(--haupt);color:#fff}} .knopf.rand{{border:1px solid var(--haupt);color:var(--haupt)}}
.held img{{width:100%;height:auto;border-radius:8px;box-shadow:0 10px 30px rgba(0,0,0,.12)}}
.klein{{font:13px Poppins,system-ui,sans-serif;color:var(--leise)}}
section{{padding:40px 0;border-top:1px solid var(--linie)}}
h2{{font:500 28px Poppins,system-ui,sans-serif;color:var(--haupt);margin:0 0 6px}} h3{{font:500 17px Poppins,system-ui,sans-serif;margin:0 0 4px;color:var(--haupt)}}
.tabs{{display:flex;gap:8px;margin:18px 0}} .tabs button{{font:500 14px Poppins,system-ui,sans-serif;padding:8px 18px;border-radius:20px;
border:1px solid var(--linie);background:var(--karte);color:var(--text);cursor:pointer}} .tabs button.aktiv{{border-color:var(--akzent);background:var(--akzent);color:#fff}}
.panel{{display:none}} .panel.aktiv{{display:block}}
ol.schritte{{list-style:none;padding:0;margin:0}} ol.schritte li{{display:flex;gap:16px;background:var(--karte);border:1px solid var(--linie);
border-radius:10px;padding:16px 18px;margin:10px 0}} ol.schritte p{{margin:2px 0 6px}}
.nr{{flex:0 0 34px;height:34px;border-radius:50%;background:var(--haupt);color:#fff;font:500 16px/34px Poppins,system-ui,sans-serif;text-align:center}}
ol.schritte li>div{{flex:1;min-width:0}}
.code{{position:relative}} pre{{background:var(--code);border-radius:8px;padding:10px 12px;margin:6px 0 0;overflow-x:auto}}
code{{font:14px ui-monospace,Menlo,Consolas,monospace}} pre code.win{{display:none}}
.kopie{{position:absolute;right:6px;top:6px;font:12px Poppins,system-ui,sans-serif;border:1px solid var(--linie);background:var(--karte);
color:var(--text);border-radius:12px;padding:3px 10px;cursor:pointer}}
.kacheln{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:18px}}
.kachel{{background:var(--karte);border:1px solid var(--linie);border-radius:10px;padding:16px 18px}} .kachel p{{margin:4px 0 0;color:var(--leise);font-size:15.5px}}
.bilder{{display:grid;grid-template-columns:1.6fr 1fr;gap:20px;margin-top:18px;align-items:start}} .bilder img{{width:100%;height:auto;border-radius:6px}}
figure{{margin:0}} figcaption{{font:13px Poppins,system-ui,sans-serif;color:var(--leise);margin-top:6px}}
details{{background:var(--karte);border:1px solid var(--linie);border-radius:10px;padding:14px 18px;margin-top:14px}}
summary{{font:500 16px Poppins,system-ui,sans-serif;color:var(--haupt);cursor:pointer}}
.leise{{color:var(--leise)}} footer{{border-top:1px solid var(--linie);padding:26px 0 40px;font:14px/1.7 Poppins,system-ui,sans-serif;color:var(--leise)}}
@media (max-width:820px){{.held,.bilder{{grid-template-columns:1fr}} .kacheln{{grid-template-columns:1fr 1fr}}}}
@media (max-width:520px){{.kacheln{{grid-template-columns:1fr}} nav a{{margin-left:12px}} body{{font-size:16px}}}}
</style></head><body>
<div class="wrap">
<header><a class="logo" href="./">pure<b>SATZ</b></a>
<nav><a href="#start">Start</a><a href="hilfe.html">Hilfe</a><a href="{REPO}">GitHub</a></nav></header>

<div class="held"><div>
<h1>In fünf Minuten zu deinem ersten Buch.</h1>
<p class="unter">Du schreibst in einfachen Textdateien (Markdown). pureSATZ macht daraus ein druckfertiges Buch,
den Umschlag und ein E-Book – für epubli oder zum Selberdrucken. Auf Linux, Mac und Windows.</p>
<a class="knopf voll" href="{ZIP}">⬇ pureSATZ herunterladen (ZIP)</a><a class="knopf rand" href="{REPO}">Auf GitHub ansehen</a>
<p class="klein">Version {html.escape(version)} · kostenlos für eigene Bücher · ohne Konto, ohne Cloud</p>
</div>
<img src="bilder/umschlag.jpg" alt="Umschlag des Hallo-Buchs, gesetzt mit pureSATZ" width="456" height="640"></div>
</div>

<section id="start"><div class="wrap">
<h2>Los geht's</h2>
<p class="leise">Dein System ist schon gewählt – sonst einfach umschalten.</p>
<div class="tabs">{"".join(tabs)}</div>
{"".join(panels)}
<p>Klappt etwas nicht? Die <a href="hilfe.html#a1">Checkliste «Start»</a> hilft weiter, mit den häufigsten Meldungen und was zu tun ist.</p>
</div></section>

<section><div class="wrap">
<h2>So sieht es aus</h2>
<p class="leise">Seiten aus dem Hallo-Buch, genau so, wie <code>sh hallo.sh</code> es baut.</p>
<div class="bilder">
<figure><img src="bilder/doppelseite.jpg" alt="Doppelseite mit Fotos und einer Tabelle" loading="lazy"><figcaption>Fotos in Hoch- und Querformat, Textfluss und eine Tabelle aus einer CSV-Datei</figcaption></figure>
<figure><img src="bilder/aufzaehlung.jpg" alt="Seite mit Liste und nummerierter Aufzählung" loading="lazy"><figcaption>Kapitel, Listen und Aufzählung</figcaption></figure>
</div></div></section>

<section><div class="wrap">
<h2>Was pureSATZ kann</h2>
<div class="kacheln">{kacheln}</div>
</div></section>

<section><div class="wrap">
<h2>Auf Wunsch mit GitHub</h2>
<p class="leise">Ohne GitHub geht alles genauso. Mit GitHub ist dein Buch privat gesichert und du schreibst auf mehreren Computern.</p>
<details><summary>In drei Schritten verbinden</summary>
<ol><li>Ein kostenloses Konto auf <a href="https://github.com/signup">github.com</a> anlegen.</li>
<li>Beim Einrichten (Schritt 3) die Frage nach GitHub mit «ja» beantworten – das Skript führt durch die Anmeldung.</li>
<li>Dein Buch als <b>privates</b> Repository anlegen. Danach im Buchordner am Anfang und am Ende: <code>sh sync.sh</code></li></ol>
<p>Genaue Anleitung mit allen Befehlen: <a href="{REPO}/blob/main/INSTALLATION.md">INSTALLATION.md</a></p>
</details>
</div></section>

<div class="wrap"><footer>
pureSATZ {html.escape(version)} · © 2026 Thomas Gsteiger · kostenlos für eigene Bücher, Quelltext einsehbar –
<a href="{REPO}/blob/main/LIZENZ.md">Lizenz</a> · Schriften Lora und Poppins (SIL Open Font License)<br>
Fragen und Fehler: <a href="{REPO}/issues">Issues auf GitHub</a> · E-Mail: <a id="mail" href="#">puresatz (at) gsteiger.ch</a><br>
Entstanden beim Schreiben von «Leben 1.0, 2.0, 3.0». Der Name erinnert an pureRACE, eine Zeitmess-Software von 1994.
</footer></div>
<script>
const p=(navigator.userAgentData&&navigator.userAgentData.platform)||navigator.platform||navigator.userAgent;
let os=/win/i.test(p)?'win':/mac|iphone|ipad/i.test(p)?'mac':'linux';
function zeige(o){{document.querySelectorAll('.tabs button').forEach(b=>b.classList.toggle('aktiv',b.dataset.os===o));
document.querySelectorAll('.panel').forEach(x=>x.classList.toggle('aktiv',x.dataset.os===o))}}
document.querySelectorAll('.tabs button').forEach(b=>b.onclick=()=>zeige(b.dataset.os));zeige(os);
document.querySelectorAll('.kopie').forEach(b=>b.onclick=()=>{{const t=b.parentNode.querySelector('code.lx').textContent;
(navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(()=>{{b.textContent='kopiert ✓';
setTimeout(()=>b.textContent='kopieren',1200)}},()=>{{}})}});
const m=document.getElementById('mail'),a=['puresatz','gsteiger.ch'].join('@');m.textContent=a;m.href='mailto:'+a;
</script></body></html>
"""


def main():
    version = open(os.path.join(HIER, "motor", "VERSION"), encoding="utf-8").read().strip()
    if "--bilder" in sys.argv:
        bilder(); return
    print("=== Webseite pureSATZ ===")
    if "ohne-bilder" not in sys.argv:
        subprocess.run([sys.executable, os.path.join(HIER, "setup", "hallo.py"), "--nicht-oeffnen"]
                       + (["--ohne-venv"] if "--ohne-venv" in sys.argv else []), cwd=HIER, check=True)
        py = os.path.join(HALLO, ".venv", "Scripts" if os.name == "nt" else "bin",
                          "python.exe" if os.name == "nt" else "python3")
        py = py if os.path.exists(py) else sys.executable
        subprocess.run([py, os.path.join("motor", "bauen.py"), "nur-pdf", "final"], cwd=HALLO, check=True,
                       stdout=subprocess.DEVNULL)              # Druckfassung: ohne Entwurfs-Kästen
        subprocess.run([py, os.path.abspath(__file__), "--bilder"], check=True)
    hilfe_kopieren()
    with open(os.path.join(DOCS, "index.html"), "w", encoding="utf-8") as f:
        f.write(seite(version))
    print(f"  index.html (Version {version})\nFertig. Ansehen: docs/index.html im Browser öffnen.")


if __name__ == "__main__":
    main()
