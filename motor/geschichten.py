#!/usr/bin/env python3
"""
geschichten.py – einzelne Geschichten sammeln und ins Buch einbinden (pureSATZ ab 2.11).

Jede Geschichte ist eine eigene Datei im Ordner geschichten/ des Buchs, z. B. geschichten/schutzschild-hoch.md:

    ## Schutzschild hoch!
    stand: entwurf
    stichworte: Emotionscode, Schutz
    quelle: Praxis 2018

    Der Text der Geschichte …

Kopfzeilen (stand, stichworte, quelle, notiz) sind freiwillig und werden nicht gedruckt; notiz darf mehrfach stehen.
stand: idee · entwurf · ueberarbeiten · fertig  (nur für die Übersicht, wirkt nicht auf den Druck).
Im Buch bindet eine eigene Zeile «@@schutzschild-hoch» die Geschichte ein (Name = Dateiname ohne .md).

Aufruf über neu.sh / neu.bat im Buchordner:
    sh neu.sh "Schutzschild hoch!"    neue Geschichte anlegen
    sh neu.sh                         Übersicht zeigen (und geschichten-uebersicht.html schreiben)
    sh neu.sh tabelle "Titel"         neue Tabelle in tabellen/ anlegen
Ohne Ordner geschichten/ ändert sich nichts: ein Buch aus einer einzigen Buchdatei läuft wie bisher.
"""
import html
import os
import re
import sys
from datetime import datetime
try:                                            # Windows: «sh build.sh» in Meldungen als «.\build.bat»
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "."))
    import plattform
    plattform.windows_befehle()
except ImportError:
    pass

ORDNER = "geschichten"
STAENDE = ("idee", "entwurf", "ueberarbeiten", "fertig")
STAND_TEXT = {"idee": "Idee", "entwurf": "Entwurf", "ueberarbeiten": "überarbeiten", "fertig": "fertig"}
KOPF = re.compile(r"^\s*(?:-\s*)?(stand|stichworte|quelle|notiz)\s*:\s*(.*?)\s*$", re.I)   # «- » freiwillig
VERWEIS = re.compile(r"^\s*(?:#{1,6}\s+)?@@([A-Za-z0-9][A-Za-z0-9._-]*)\s*$")   # auch «##### @@name» (Gliederung im Editor)
NICHT = {"liesmich", "readme", "uebersicht"}            # Hilfedateien im Ordner sind keine Geschichten


def ordner(basis):
    return os.path.join(basis, ORDNER)


def alle(basis):
    """{name: pfad} aller Geschichten (auch in Unterordnern). Gleicher Name zweimal = Fehler."""
    o = ordner(basis)
    gefunden = {}
    if not os.path.isdir(o):
        return gefunden
    for wurzel, unter, dateien in os.walk(o):
        unter[:] = sorted(u for u in unter if not u.startswith((".", "_")))
        for f in sorted(dateien):
            if not f.lower().endswith(".md") or f.startswith((".", "_")):
                continue
            name = f[:-3]
            if name.lower() in NICHT:
                continue
            p = os.path.join(wurzel, f)
            if name in gefunden:
                raise SystemExit(f"Zwei Geschichten heissen «{name}»: {os.path.relpath(gefunden[name], basis)} und "
                                 f"{os.path.relpath(p, basis)}. Bitte eine umbenennen.")
            gefunden[name] = p
    return gefunden


def lies(pfad):
    """(titel, kopf, [(nr, zeile)]) – Kopfzeilen direkt unter dem Titel werden herausgenommen."""
    roh = open(pfad, encoding="utf-8").read().split("\n")
    titel, kopf, text, im_kopf = "", {}, [], False
    for i, z in enumerate(roh, 1):
        s = z.strip()
        if not titel and s.startswith("## "):
            titel, im_kopf = s[3:].strip(), True
            text.append((i, z))
            continue
        if im_kopf:
            m = KOPF.match(z)
            if m:
                kopf[m.group(1).lower()] = m.group(2)
                continue
            im_kopf = False
        text.append((i, z))
    if not titel:
        titel = os.path.splitext(os.path.basename(pfad))[0].replace("-", " ")
    return titel, kopf, text


def stand(kopf):
    s = (kopf.get("stand") or "").strip().lower().replace("ü", "ue")
    return s if s in STAENDE else ""


def stichworte(basis):
    """Stichwörter aus den Köpfen aller Geschichten (für das Stichwortverzeichnis)."""
    out = []
    for p in alle(basis).values():
        for w in lies(p)[1].get("stichworte", "").split(","):
            if w.strip() and w.strip() not in out:
                out.append(w.strip())
    return out


def name_aus_titel(titel):
    t = titel.lower()
    for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss"), ("é", "e"), ("è", "e"), ("à", "a")):
        t = t.replace(a, b)
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return t[:60].strip("-") or "geschichte"


def verweise(buchdatei):
    """[(zeilennummer, name)] aller @@-Zeilen in der Buchdatei (alle Fassungen)."""
    if not buchdatei or not os.path.exists(buchdatei):
        return []
    out = []
    for i, z in enumerate(open(buchdatei, encoding="utf-8").read().split("\n"), 1):
        m = VERWEIS.match(z)
        if m:
            out.append((i, m.group(1)))
    return out


def reihe(basis, buchdatei):
    """Namen aller Geschichten: zuerst wie im Buch (@@), dann wie angelegt (geschichten/kuerzel.txt), dann nach Datum."""
    a = alle(basis)
    k = os.path.join(ordner(basis), "kuerzel.txt")
    angelegt = [z.split(None, 1)[1].strip() for z in open(k, encoding="utf-8").read().splitlines()
                if not z.startswith("#") and len(z.split(None, 1)) == 2] if os.path.exists(k) else []
    out = []
    for n in [n for _, n in verweise(buchdatei)] + angelegt + sorted(a, key=lambda n: os.path.getmtime(a[n])):
        if n in a and n not in out:
            out.append(n)
    return out


def teile_der_verweise(buchdatei):
    """{name: «Teil …»} – in welchem Teil des Buchs eine Geschichte eingebunden ist."""
    out, teil = {}, ""
    if not buchdatei or not os.path.exists(buchdatei):
        return out
    for z in open(buchdatei, encoding="utf-8").read().split("\n"):
        s = z.strip()
        if s.startswith("# "):
            stuecke = s[2:].split("|")
            teil = (stuecke[0].strip() + (" · " + stuecke[1].strip() if len(stuecke) > 1 else ""))
        m = VERWEIS.match(z)
        if m:
            out.setdefault(m.group(1), teil or "Buch")
    return out


def neu(basis, titel):
    """Neue Geschichte anlegen. Gibt (name, pfad) zurück."""
    o = ordner(basis)
    os.makedirs(o, exist_ok=True)
    vorhanden = alle(basis)
    name = basis_name = name_aus_titel(titel)
    n = 2
    while name in vorhanden or os.path.exists(os.path.join(o, name + ".md")):
        name = f"{basis_name}-{n}"; n += 1
    pfad = os.path.join(o, name + ".md")
    with open(pfad, "w", encoding="utf-8") as f:
        f.write(f"## {titel}\nstand: idee\nstichworte:\nquelle:\nnotiz: stand = idee · entwurf · ueberarbeiten · fertig – "
                "Kopfzeilen werden nicht gedruckt\n\nHier beginnt die Geschichte …\n")
    return name, pfad


def daten(basis, buchdatei):
    """Eine Zeile pro Geschichte: dict(name, titel, stand, woerter, teil, geaendert, pfad)."""
    teile = teile_der_verweise(buchdatei)
    zeilen = []
    for name, p in alle(basis).items():
        titel, kopf, text = lies(p)
        rumpf = " ".join(z for _, z in text[1:] if not z.strip().startswith((":::", "@", "- datei:", "datei:")))
        rumpf = re.sub(r"<[^>]+>|\{[^}]*\}|\[([^\]]*)\]\([^)]*\)", r"\1", rumpf)
        zeilen.append(dict(name=name, titel=titel, stand=stand(kopf), woerter=len(re.findall(r"\w+", rumpf)),
                           teil=teile.get(name, ""), geaendert=datetime.fromtimestamp(os.path.getmtime(p)),
                           pfad=os.path.relpath(p, basis).replace(os.sep, "/")))
    rang = {s: i for i, s in enumerate(STAENDE)}
    zeilen.sort(key=lambda d: (rang.get(d["stand"], len(STAENDE)), d["titel"].lower()))
    return zeilen


def zahl(n):
    return f"{n:,}".replace(",", "'")


def zusammenfassung(zeilen):
    teile = [f"{len(zeilen)} Geschichten"]
    for s in reversed(STAENDE):
        k = sum(1 for d in zeilen if d["stand"] == s)
        if k:
            teile.append(f"{k} {STAND_TEXT[s]}")
    ohne = sum(1 for d in zeilen if not d["stand"])
    if ohne:
        teile.append(f"{ohne} ohne Stand")
    teile.append(f"{zahl(sum(d['woerter'] for d in zeilen))} Wörter")
    frei = sum(1 for d in zeilen if not d["teil"])
    if frei:
        teile.append(f"{frei} noch nicht im Buch")
    return " · ".join(teile)


def schreibe_md(basis, zeilen, buchtitel):
    z = [f"# Geschichten – {buchtitel}", "", f"Stand {datetime.now():%d.%m.%Y %H:%M} · "
         + zusammenfassung(zeilen), "", "Automatisch erstellt von pureSATZ (sh neu.sh, sh build.sh) – nicht von Hand ändern.", "",
         "| Geschichte | Stand | Wörter | Im Buch | Geändert | Datei |", "|---|---|---|---|---|---|"]
    for d in zeilen:
        z.append(f"| {d['titel']} | {STAND_TEXT.get(d['stand'], '–')} | {zahl(d['woerter'])} | {d['teil'] or '–'} | "
                 f"{d['geaendert']:%d.%m.%Y} | {d['pfad']} |")
    with open(os.path.join(ordner(basis), "UEBERSICHT.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(z) + "\n")


def schreibe_html(basis, zeilen, buchtitel, farben):
    karten = {s: [] for s in STAENDE + ("",)}
    reihen = []
    for d in zeilen:
        st = d["stand"] or "ohne"
        link = html.escape(d["pfad"])
        t = html.escape(d["titel"])
        reihen.append(
            f'<tr data-stand="{st}"><td><a href="{link}">{t}</a></td>'
            f'<td data-wert="{STAENDE.index(d["stand"]) if d["stand"] else -1}"><span class="st st-{st}">'
            f'{html.escape(STAND_TEXT.get(d["stand"], "–"))}</span></td>'
            f'<td class="zahl" data-wert="{d["woerter"]}">{zahl(d["woerter"])}</td>'
            f'<td>{html.escape(d["teil"]) or "–"}</td>'
            f'<td data-wert="{d["geaendert"]:%Y%m%d%H%M}">{d["geaendert"]:%d.%m.%Y}</td></tr>')
        karten[d["stand"]].append(
            f'<a class="karte" href="{link}"><b>{t}</b><span>{zahl(d["woerter"])} Wörter'
            f'{" · " + html.escape(d["teil"]) if d["teil"] else " · noch nicht im Buch"}</span></a>')
    gesamt = max(1, len(zeilen))
    balken = "".join(f'<i class="b-{s}" style="width:{100 * sum(1 for d in zeilen if d["stand"] == s) / gesamt:.1f}%" '
                     f'title="{STAND_TEXT[s]}"></i>' for s in STAENDE)
    spalten = "".join(f'<div class="spalte"><h3><span class="st st-{s}">{STAND_TEXT[s]}</span> '
                      f'<small>{len(karten[s])}</small></h3>{"".join(karten[s]) or "<p class=leer>–</p>"}</div>'
                      for s in STAENDE)
    if karten[""]:
        spalten += (f'<div class="spalte"><h3><span class="st st-ohne">ohne Stand</span> <small>{len(karten[""])}</small>'
                    f'</h3>{"".join(karten[""])}</div>')
    knoepfe = "".join(f'<button data-filter="{s}">{STAND_TEXT[s]}</button>' for s in STAENDE)
    f = farben
    seite = f"""<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Geschichten – {html.escape(buchtitel)}</title>
<style>
@font-face{{font-family:Poppins;src:url(motor/fonts/Poppins-Regular.ttf)}}
@font-face{{font-family:Poppins;font-weight:500;src:url(motor/fonts/Poppins-Medium.ttf)}}
@font-face{{font-family:Lora;src:url(motor/fonts/Lora-Regular.ttf)}}
:root{{--papier:{f['papier']};--text:{f['text']};--leise:{f['leise']};--haupt:{f['haupt']};--akzent:{f['akzent']};
--karte:#ffffff;--linie:#e7dfd0;--s-idee:#c9c2b8;--s-entwurf:#e6c487;--s-ueberarbeiten:#9fb6dc;--s-fertig:#8fbf9a}}
@media (prefers-color-scheme:dark){{:root{{--papier:#1d1b19;--text:#ece6dc;--leise:#b4ab9f;--haupt:#9db7ec;
--karte:#2a2724;--linie:#3b3732}}}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--papier);color:var(--text);
font:16px/1.5 Lora,Georgia,serif;padding:24px 16px 48px}}
main{{max-width:1000px;margin:0 auto}} h1,h2,h3,button,th,.st,.karte b{{font-family:Poppins,system-ui,sans-serif}}
h1{{color:var(--haupt);font-weight:500;margin:0 0 4px}} .sub{{color:var(--leise);margin:0 0 18px}}
.balken{{display:flex;height:12px;border-radius:6px;overflow:hidden;background:var(--linie);margin:0 0 18px}}
.balken i{{display:block;height:100%}} .b-idee{{background:var(--s-idee)}} .b-entwurf{{background:var(--s-entwurf)}}
.b-ueberarbeiten{{background:var(--s-ueberarbeiten)}} .b-fertig{{background:var(--s-fertig)}}
.leiste{{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 14px}}
button{{border:1px solid var(--linie);background:var(--karte);color:var(--text);border-radius:16px;padding:5px 12px;
cursor:pointer;font-size:14px}} button.aktiv{{border-color:var(--akzent);color:var(--akzent)}}
.ansicht{{margin-left:auto}} table{{width:100%;border-collapse:collapse;background:var(--karte);border-radius:8px;overflow:hidden}}
th,td{{text-align:left;padding:9px 12px;border-bottom:1px solid var(--linie)}} th{{font-weight:500;font-size:14px;
color:var(--leise);cursor:pointer;user-select:none}} th:hover{{color:var(--akzent)}} .zahl{{text-align:right}}
a{{color:var(--haupt);text-decoration:none}} a:hover{{text-decoration:underline}}
.st{{display:inline-block;font-size:12px;padding:2px 9px;border-radius:10px;color:#2a2622}}
.st-idee{{background:var(--s-idee)}} .st-entwurf{{background:var(--s-entwurf)}} .st-ueberarbeiten{{background:var(--s-ueberarbeiten)}}
.st-fertig{{background:var(--s-fertig)}} .st-ohne{{background:var(--linie);color:var(--leise)}}
.kanban{{display:none;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px}}
.spalte h3{{font-size:15px;font-weight:500;margin:0 0 8px}} .spalte small{{color:var(--leise)}}
.karte{{display:block;background:var(--karte);border:1px solid var(--linie);border-radius:8px;padding:9px 11px;margin:0 0 8px}}
.karte b{{display:block;font-weight:500;font-size:14px;color:var(--text)}} .karte span{{font-size:13px;color:var(--leise)}}
.leer{{color:var(--leise)}} footer{{color:var(--leise);font-size:13px;margin-top:20px}}
.tabelle-wrap{{overflow-x:auto}}
</style></head><body><main>
<h1>Geschichten – {html.escape(buchtitel)}</h1>
<p class="sub">{html.escape(zusammenfassung(zeilen))}</p>
<div class="balken">{balken}</div>
<div class="leiste"><button data-filter="alle" class="aktiv">alle</button>{knoepfe}
<button class="ansicht" id="ansicht">Kanban-Ansicht</button></div>
<div class="tabelle-wrap"><table id="tabelle"><thead><tr><th>Geschichte</th><th>Stand</th><th class="zahl">Wörter</th>
<th>Im Buch</th><th>Geändert</th></tr></thead><tbody>{"".join(reihen)}</tbody></table></div>
<div class="kanban" id="kanban">{spalten}</div>
<footer>Erstellt {datetime.now():%d.%m.%Y %H:%M} von pureSATZ · neu erstellen mit «sh neu.sh» oder «sh build.sh» ·
Klick auf eine Geschichte öffnet die MD-Datei.</footer>
</main><script>
const knoepfe=document.querySelectorAll('[data-filter]');
knoepfe.forEach(b=>b.onclick=()=>{{knoepfe.forEach(x=>x.classList.remove('aktiv'));b.classList.add('aktiv');
const f=b.dataset.filter;document.querySelectorAll('#tabelle tbody tr').forEach(r=>{{
r.style.display=(f==='alle'||r.dataset.stand===f)?'':'none'}});}});
const ansicht=document.getElementById('ansicht'),tab=document.querySelector('.tabelle-wrap'),kan=document.getElementById('kanban');
ansicht.onclick=()=>{{const k=kan.style.display==='grid';kan.style.display=k?'none':'grid';tab.style.display=k?'':'none';
ansicht.textContent=k?'Kanban-Ansicht':'Tabellen-Ansicht';}};
document.querySelectorAll('#tabelle th').forEach((th,i)=>{{let auf=true;th.onclick=()=>{{
const tb=document.querySelector('#tabelle tbody');const r=[...tb.rows];r.sort((a,b)=>{{
const x=a.cells[i].dataset.wert??a.cells[i].textContent.toLowerCase(),y=b.cells[i].dataset.wert??b.cells[i].textContent.toLowerCase();
const n=!isNaN(x)&&!isNaN(y);const c=n?(x-y):x.localeCompare(y,'de');return auf?c:-c;}});auf=!auf;r.forEach(z=>tb.appendChild(z));}};}});
</script></body></html>
"""
    with open(os.path.join(basis, "geschichten-uebersicht.html"), "w", encoding="utf-8") as fh:
        fh.write(seite)


def uebersicht(basis, buchdatei, buchtitel="Buch", farben=None, zeigen=False):
    """UEBERSICHT.md und geschichten-uebersicht.html schreiben (nur wenn es den Ordner geschichten/ gibt)."""
    if not os.path.isdir(ordner(basis)):
        return None
    zeilen = daten(basis, buchdatei)
    farben = dict(dict(papier="#FBF6EC", text="#2E2A26", leise="#6E655C", haupt="#1E428A", akzent="#B8873B"),
                  **(farben or {}))
    schreibe_md(basis, zeilen, buchtitel)
    schreibe_html(basis, zeilen, buchtitel, farben)
    if zeigen:
        print(f"\nGeschichten – {buchtitel}:  {zusammenfassung(zeilen)}\n")
        for d in zeilen:
            print(f"  {STAND_TEXT.get(d['stand'], '–'):14} {zahl(d['woerter']):>6} W.  "
                  f"{(d['teil'] or '– noch nicht im Buch')[:24]:24}  {d['titel']}  (@@{d['name']})")
        print("\nÜbersicht im Browser: geschichten-uebersicht.html   ·   Tabelle: geschichten/UEBERSICHT.md")
        print('Neue Geschichte: sh neu.sh "Titel"   ·   neue Tabelle: sh neu.sh tabelle "Titel"')
    return zeilen


# Hilfsdateien für Bücher, die vom älteren Motor aktualisiert wurden (update.py ≤ 2.10 kannte neu.sh noch nicht)
NEU_SH = '#!/bin/sh\n# Geschichten sammeln (pureSATZ 2.11):\n#   sh neu.sh "Titel der Geschichte"   neue Geschichte in geschichten/ anlegen\n#   sh neu.sh                          Übersicht aller Geschichten (auch als geschichten-uebersicht.html)\ncd "$(dirname "$0")"\nif [ -x .venv/bin/python3 ]; then PY=.venv/bin/python3; else python3 motor/einrichten.py; PY=.venv/bin/python3; fi\n"$PY" motor/geschichten.py "$@"\n'
NEU_BAT = '@echo off\r\nrem Geschichten sammeln (Windows): neu.bat "Titel der Geschichte" / neu.bat = Uebersicht\r\ncd /d "%~dp0"\r\nif not exist ".venv\\Scripts\\python.exe" (\r\n  where py >nul 2>nul && (py motor\\einrichten.py) || (python motor\\einrichten.py)\r\n)\r\n".venv\\Scripts\\python.exe" motor\\geschichten.py %*\r\n'
IGNORIEREN = ("geschichten-uebersicht.html", "geschichten/UEBERSICHT.md", "_geschichten-sammlung.md", "hilfe.html")


def hilfsdateien(basis):
    """neu.sh / neu.bat anlegen und .gitignore ergänzen, falls es fehlt. Ändert nie Bestehendes."""
    for f, inhalt in (("neu.sh", NEU_SH), ("neu.bat", NEU_BAT)):
        p = os.path.join(basis, f)
        if not os.path.exists(p):
            with open(p, "w", encoding="utf-8", newline="") as fh:
                fh.write(inhalt)
            print(f"Neu im Buch: {f} (Geschichten sammeln)")
    gi = os.path.join(basis, ".gitignore")
    if os.path.exists(gi):
        alt = open(gi, encoding="utf-8").read()
        fehlt = [x for x in IGNORIEREN if x not in alt.split("\n")]
        if fehlt:
            with open(gi, "a", encoding="utf-8") as fh:
                fh.write(("" if alt.endswith("\n") else "\n") + "# Geschichten-Übersicht (wird bei jedem Bau neu erzeugt)\n"
                         + "\n".join(fehlt) + "\n")


def main():
    motor = os.path.dirname(os.path.abspath(__file__))
    basis = os.path.dirname(motor)
    sys.path.insert(0, motor)
    import build as bk
    buch = os.path.join(basis, bk.TEXT)
    if sys.argv[1:2] and sys.argv[1].lower() == "tabelle":          # sh neu.sh tabelle "Titel"
        import tabellen
        titel = " ".join(sys.argv[2:]).strip()
        if not titel:
            print('Neue Tabelle:  sh neu.sh tabelle "Titel der Tabelle"   (Windows: neu.bat tabelle "…")')
            vorhanden = tabellen.alle(basis)
            if vorhanden:
                print("Vorhandene Tabellen: " + ", ".join("@#" + n for n in vorhanden))
            return
        name, pfad = tabellen.neu(basis, titel)
        print(f"Neue Tabelle: {os.path.relpath(pfad, basis)}  (mit LibreOffice öffnen, als «Text CSV» speichern)")
        print(f"Im Buch einbinden mit dieser Zeile:\n\n    @#{name}\n")
        return
    titel = " ".join(sys.argv[1:]).strip()
    farben = {n: bk.hexfarbe(n) for n in ("papier", "text", "leise", "haupt", "akzent")}
    if titel:
        name, pfad = neu(basis, titel)
        print(f"Neue Geschichte: {os.path.relpath(pfad, basis)}")
        print(f"Im Buch einbinden mit dieser Zeile (eigene Zeile, z. B. unter einem Teil):\n\n    @@{name}\n")
    elif not os.path.isdir(ordner(basis)):
        print("Noch keine Geschichten. Neue Geschichte anlegen:  sh neu.sh \"Titel der Geschichte\"")
        return
    uebersicht(basis, buch, bk.V("titel") or "Buch", farben, zeigen=not titel)


if __name__ == "__main__":
    main()
