# Stufe 2 – Aufräum-Version 3.0 des Motors

> Auftrag zum Starten: «go stufe 2» und diese Datei angeben. Erstellt 23.10.2026, Stand pureSATZ 2.31.1.
> Geplant für das neue Jahr, nach der Vernissage (9.1.2027) – bis dahin Funktionsstopp am Motor.
> Zeilennummern unten gelten für 2.31.1; vor dem Start mit `grep -n` neu suchen.

## Ziel

Der Motor liest heute noch viele alte Schreibweisen, die kein Buch mehr verwendet (es gibt nur Leben123 und die Vorlage).
Jede ist ein zusätzlicher Weg, an den man bei jeder Änderung denken muss. Stufe 2 entfernt sie und führt doppelten
Code zusammen – **ohne dass sich an einem gebauten Buch etwas ändert** (Pixel für Pixel gleich).

## Übersicht

| Schritt | Was | Zeit | Risiko | Gewinn |
|---|---|---|---|---|
| 1 | Alte Schreibweisen entfernen (Liste unten) | 2–3 h | mittel: eine übersehene Stelle bricht den Bau ab – darum zuerst Suchlauf, danach vergleich.py | etwa 150–250 Zeilen weniger, weniger Fehlerquellen, schnellere Änderungen |
| 2 | Doppelten Code zusammenführen | 1 h | klein: vergleich.py zeigt jede Abweichung | eine Änderung wirkt überall, keine Stelle wird vergessen |
| 3 | Hilfe und readme4ki.txt kürzen, wo sie Ausnahmen/alte Formen erklären | 30 min | keins | kürzere, klarere Anleitung, auch für andere KIs |
| 4 | Prüfen | 30 min | – | Gewissheit: Leben123 Pixel für Pixel gleich |

Gesamt etwa ein halber Tag, in einer Runde. Version danach: **3.0.0**.

## Schritt 0 – Vorbereitung (vor jeder Änderung)

1. Thomas: `cd ../Leben123 && sh build.sh sicherung && sh sync.sh` (MD-Stand gesichert, GitHub aktuell).
2. Claude: aktuelle Dateien vom Computer holen (pureSATZ und Leben123), md-history-Regel beachten (siehe CLAUDE-WIEDEREINSTIEG.md).
3. Suchlauf: Leben123 (Buch, Variablen, Umschlag, druck/, geschichten/ falls vorhanden) und vorlage/ nach jeder alten
   Form unten durchsuchen. Kommt eine noch vor: zuerst die Datei auf die neue Form umstellen (mit md-history), dann erst
   den Motor ändern.

## Schritt 1 – Alte Schreibweisen entfernen

| Alte Form | Neue Form | Wo im Motor (2.31.1) |
|---|---|---|
| Variablenblock zwischen `---` ganz oben in der Buch-MD | `<buch>-variablen.md` | manuskript.py `lies()`, Zweig `roh[0].strip() == "---"` |
| `- name: wert` (mit Strich) in Einstellungs-Dateien | `{name}: wert` | manuskript.py `VARIABLE`, hilfe.py `variablen_html()` und `formate_html()`, build-epub.py `_umschlag_medium`, geschichten.py `KOPF` |
| Block `::: foto Titel … :::` | `#### @FOTO Titel` | manuskript.py `ARTEN["foto"]`, `_art()`; build.py / build-epub.py Behandlung von «FOTO»-Blöcken prüfen (wird auch von `#### @FOTO` genutzt – nur den `:::`-Weg entfernen) |
| Endungen `-v2`, `-offiziell` | `-normal` | manuskript.py `ALT` |
| Endung/Block `-dc`, `::: dc` | `-uz`, `::: uz` | manuskript.py `ALT`, `ARTEN["dc"]`, `zeilen()` (`art in ("uz","dc")`), `Ausgabe.wert()`; build.py `_ueberlagern()`, `_fassung_aus_aufruf()`, `waehle()` (Aufruf-Wörter «dc», «b», «v3uz», «directors-cut» – «uz» und «unzensiert» behalten) |
| `{isbn-buch}`, `{isbn-ebook}` | `{isbn}` unter `## Ausgabe: …` | manuskript.py `Ausgabe.wert()` (isbn-Sonderfall); build.py `DRUCK_NAMEN` |
| `{druck-normal}`, `{druck-uz}`, `{ebook}` | `{druck-datei}` unter `## Ausgabe: …` | build.py `druck_datei()`, `ebook_datei()` (zweite Zeile mit `("druck")` / `("ebook")`) |
| `{preis-buch}`, `{preis-ebook}` | `{preis}` unter `## Ausgabe: …` | bauen.py `shop_angaben()` |
| `{seite}` | `{format}: 150 x 215` | build.py `format_angaben()`, `FORMAT, FMT = …`, `DRUCK_NAMEN`; bauen.py `druck_pruefen()`, `shop_angaben()` |
| `{ruecken}` (ohne -hardcover/-softcover) | `{ruecken-hardcover}`, `{ruecken-softcover}` | build-broschuere.py `RUECKEN_SOFT`, `RUECKEN_HART`; build.py `DRUCK_NAMEN` |
| `{projekt-normal}`, `{projekt-uz}` in der Variablen-Datei | `{projekt}` in der Plattform-Datei | (läuft über -normal/-uz; nur Doku) |
| `@LOTUS`, `@LOTUS-UNTEN`, `@LOTUS-TRENNER` | `@ZIER…` | build.py Befehls-Schleife (`startswith(("@LOTUS-…", "@ZIER-…"))`); manuskript.py `BEFEHLE`; hilfe.py `BEFEHL_VERSTECKT` |
| `@ANHANG` | `# Titel` | manuskript.py `BEFEHLE`; hilfe.py `BEFEHL_VERSTECKT`; mit `grep -n ANHANG motor/*.py` prüfen, wo der Bau es sonst noch behandelt |
| Umgebungsvariable `LR_FINAL` | `BUCH_FINAL` | build.py `ENTWURF = …` |
| Alte Namen `E.TITEL`, `E.JAHR` … (Klasse `_Einstellungen`), `je()`, `AUSGABE` «A»/«B» | `V("titel")`, Fassung «normal»/«uz» | build.py `_Einstellungen`, `je()`, `AUSGABE`; alle `E.`-Aufrufe in build.py (12), build-epub.py (6), build-broschuere.py (3) – **grösster Teil, sorgfältig ersetzen** |
| Impressum `{impressum-herstellung-druck}` usw. | Werte unter `## Ausgabe: …` | läuft über `name-medium`; nur Doku |

**Nicht entfernen** (wird gebraucht): `> Satz` im Buchtext, `~ Satz`, `::: nur-…`, `-normal`/`-uz`, `-druck`/`-ebook`/`-bildschirm`,
`::: offen`, `::: offen-notiz`, `::: platzhalter` (prüfen, ob Leben123 es nutzt), `\` am Zeilenende, `---` als Umbruch.

## Schritt 2 – Doppelten Code zusammenführen

- **Zitat mit Verzierung** wird an 4 Stellen gesetzt: build.py Hauptschleife (`elif s.startswith("> ")`), build.py
  Block-Inhalt (`if t.startswith("> ")` in der Funktion für `::: zusammen`/`mitte`), build-epub.py zweimal
  (Block-Inhalt und Hauptschleife). Je eine Hilfsfunktion pro Datei (PDF: `zitat_mit_zier(text)`, E-Book: `zitat_html(text)`).
- **`druck_datei()` und `ebook_datei()`** in build.py: eine gemeinsame Funktion `plattform_datei(medium, fassung)`.
- Danach prüfen, ob `mit_druckangaben()` / `mit_ebookangaben()` noch beide nötig sind (E-Book hat meist keine Plattform-Datei mehr).

## Schritt 3 – Doku kürzen

- motor/HILFE.md: Sätze zu alten Formen und Ausnahmen streichen (z. B. «Ohne `{farbschema}` gelten …» bleibt; Hinweise auf
  `seite`, `isbn-buch`, `::: foto`, `- name:` entfernen, falls noch vorhanden).
- vorlage/readme4ki.txt und Leben123/readme4ki.txt: «Erlaubte Namen» an die bereinigte Liste anpassen.
- manuskript.py Kopf-Docstring und `lies()`-Docstring («Alte Form …») kürzen.
- CHANGELOG 3.0.0: Liste der entfernten Schreibweisen mit der neuen Form daneben.

## Schritt 4 – Prüfen (Pflicht)

1. Zwei Kopien von Leben123: eine mit dem Motor 2.31.x, eine mit dem neuen. In beiden `sh build.sh final`,
   `sh build.sh leseprobe`. Dann:
   `python3 pureSATZ/test/vergleich.py <alt> <neu> --text` → «Alles gleich.» (nur das Korrektur-PDF hat Datum/Uhrzeit).
2. Selbsttest: `SELBSTTEST_OHNE_VENV=1 python3 test/selbsttest.py` → «SELBSTTEST IN ORDNUNG».
   Der Selbsttest ändert in einer Testkopie Werte mit Text-Ersetzungen – falls er Schreibweisen nutzt, die entfernt
   wurden (z. B. `- leseprobe-seiten-uz`), dort auf die neue Form umstellen.
3. Hallo-Buch: `sh hallo.sh` (läuft im Selbsttest mit).
4. `python3 motor/hilfe.py` und `python3 docs/landingpage.py ohne-bilder`; Hilfe kurz durchsehen.
5. Fehlermeldung bei alter Form: Statt stillem Ignorieren soll der Bau eine alte Form mit klarem Hinweis melden,
   z. B. «Zeile 12: «- name:» wird nicht mehr gelesen – bitte «{name}:» schreiben.» (in `pruefen()`).

## Danach (Befehle für Thomas)

```
cd ~/Dokumente/"02 Nebenerwerb"/Buchprojekt-TGS/pureSATZ
git add . && git commit -m "3.0.0 Aufräumen: alte Schreibweisen entfernt" && git push
cd ../Leben123
sh update.sh lokal
sh build.sh final
sh sync.sh
```

## Bewusst nicht in Stufe 2

- build.py (knapp 2500 Zeilen) nicht in Module aufteilen – viel Arbeit, hohes Risiko, wenig Gewinn.
- Keine neuen Funktionen in derselben Runde (sonst ist «alles gleich» nicht mehr prüfbar).
- Abgelehnte Ideen bleiben abgelehnt: `>~`, `>*`, `@OBEN`, `@SATZ-…`, eigenes CMYK im Motor.
