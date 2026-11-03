# Umbau 1: Hörbuch-Skripte von awk/sed nach Python

Stand: 3.11.2026 · pureSATZ 2.68.0 · **Entscheid: vorerst nicht umbauen** (Thomas bleibt bei Linux, alles läuft).

## Worum es geht

Zwei Skripte in `motor/audio/` sind Shell, der Rest ist Python:

| Skript | Sprache | Aufgabe |
|---|---|---|
| `md2txt.sh` | bash + awk (~150 Zeilen) | Buch-MD → ein Text pro Kapitel in `audio/txt-md/` (Überschriften, Fotos, Blöcke, Tabellen, Zeitstrahl, Platzhalter, normal/uz) |
| `text-vorbereiten.sh` | bash + sed (~20 Zeilen) | Absätze zu Zeilen, Satzpunkt, Aussprache-Regeln (`Original = Aussprache` → sed-Befehle), Jahreszahlen, Gedankenstrich |

`hoerbuch.py`, `txt2mp3-azure.py` und `probe-azure.py` rufen sie mit `bash` auf.

## Wann umbauen (Auslöser)

- Hörbuch soll auf **Mac oder Windows** laufen (Mac: BSD-sed kennt `\b` und `I` nicht; Windows: kein bash).
- Die Eigenheiten der Aussprache-Regeln stören öfter (siehe unten).
- Ein neues Buch zeigt Fälle, die awk schlecht kann (z. B. verschachtelte Blöcke, neue Befehle).

## Vorteile Python

- Eine Sprache wie der ganze Motor – leichter lesen und ändern (auch für eine andere KI).
- Aussprache-Regeln ohne sed-Trick: Punkt am Ende (`Dipl.`) und Sonderzeichen (`$`, `.`, `(`) gehen sauber.
- Klare Fehlermeldungen (z. B. «aussprache-ollie.txt, Zeile 12: kein =»).
- Kein «Keine Berechtigung» bei `./md2txt.sh`.
- `md2txt` könnte mehr vom Motor nutzen (`manuskript.zeilen()`: Fotos, Blöcke, Platzhalter) statt einer eigenen Nachbildung.
- Mac/Windows fast gratis dabei.

## Vorteile awk/sed (warum es bleibt)

- Erprobt: Leben123 ganz gehört, Ergebnis gut.
- Kurz und durchschaubar: `bash text-vorbereiten.sh datei.txt` zeigt sofort, was die Stimme bekommt.
- Unter Linux immer da, schnell.

## Eigenheiten heute (Workarounds)

| Eigenheit | Workaround |
|---|---|
| Punkt am Ende des Originals greift nicht (`Dipl. = …`) | mit dem nächsten Wort: `Dipl. Techniker = Diplomierter Techniker` – oder ohne Punkt `Dipl = Diplomierter` (der Punkt bleibt stehen, kurze Pause) |
| Zeichen am Zeilenanfang (`$Füsse`) machen die Regel unwirksam | Zeile ohne Sonderzeichen beginnen |
| `.` im Original passt auf jedes Zeichen | harmlos bei Web-Adressen (`www.thomasgsteiger.ch`) |
| Reihenfolge: erste passende Regel gewinnt | lange/besondere Regeln vor kurzen/allgemeinen |

## Vorgehen, wenn es so weit ist

1. `text-vorbereiten.py` und `md2txt.py` in `motor/audio/` schreiben, gleiche Ein- und Ausgaben, gleiche
   Umgebungsvariablen (`AUDIO_DIR`, `AUSSPRACHE_DATEI`, `MD`, `ZIEL`, `PLATZHALTER`, `VERSION`).
2. **Prüfstein Leben123:** `audio/txt-md/` und `audio/buch.txt` vorher/nachher Zeichen für Zeichen vergleichen
   (`diff -r`), dazu die Ausgabe von text-vorbereiten für alle Kapitel. Erst bei 0 Unterschieden umstellen.
3. Aufrufe in `hoerbuch.py`, `txt2mp3-azure.py`, `probe-azure.py` von `bash …sh` auf Python umstellen;
   `.sh` nach `delete/`.
4. Aussprache-Regeln: Original wörtlich (re.escape), ganze Wörter mit eigener Grenze statt `\b`
   (damit `Dipl.` greift); Reihenfolge wie bisher (erste gewinnt).
5. Hilfe «Hörbuch: Aussprache verfeinern» anpassen (Punkt-Regel streichen), CHANGELOG.

Aufwand: etwa ein halber Tag (Claude), Test mit Leben123 ca. 30 Minuten. Mac/Windows danach: siehe
Chat 3.11. (ffmpeg freiwillig, MP3 von Azure direkt + mutagen für Tags/Cover, Standard-Player statt mpv).
