pureSATZ - Vorlage und Motor für eigene Bücher
=====================================================================

ZUM STARTEN   Windows: START-Windows.bat doppelklicken
              Mac:     START-Mac.command doppelklicken
                       (blockiert: Rechtsklick -> Öffnen, oder Systemeinstellungen ->
                       Datenschutz & Sicherheit -> «Dennoch öffnen»)
              Linux:   Rechtsklick in den Ordner -> «Im Terminal öffnen», dann  sh START-Linux.sh
              Fünf Schritte: Technik (Python) · Ort für die Bücher (Buchprojekte im
              Benutzerordner) · Hallo-Buch · dein eigenes Buch (Titel, Untertitel, Autor,
              Format) · Extras (GitHub, freiwillig). Enter nimmt jeweils den Vorschlag.

DANACH        Buchprojekte/
                pureSATZ/      die Werkstatt – hier nichts schreiben
                Hallo-Buch/    zum Ausprobieren, darf weg
                Mein-Buch/     dein Buch – hier schreibst und baust du
              «Terminal hier» im Buchordner doppelklicken öffnet das Befehlsfenster genau dort
              (Windows und Mac; Linux: Rechtsklick -> «Im Terminal öffnen»).

HILFE         hilfe.html doppelklicken -> oben «Start». Schritt für Schritt, mit Schalter für
              Linux/Mac oder Windows. Online: https://tgsteiger.github.io/pureSATZ/hilfe.html


Ordner
  START-Windows.bat, START-Mac.command, START-Linux.sh   der Startknopf, je Betriebssystem einer
  setup/          neues Buch anlegen, Motor ins Buch bringen
  pc-einrichten/  Computer einrichten (Linux, Mac, Windows); start.sh = gemeinsamer Ablauf Linux/Mac
  import/         Buch aus LibreOffice/Word anlegen (Testphase)
  motor/          das Satzsystem (nicht ändern)
  vorlage/        Vorlage für jedes neue Buch
  test/           Selbsttest

Start in fünf Punkten (auch in hilfe.html unter «Start»)
  1. Erstes PDF in 5 Minuten   der ganze Weg als Checkliste
  2. Computer einrichten        macht start (von Hand: siehe «Erste Schritte» unten)
  3. Hallo-PDF                  macht start (von Hand: sh hallo.sh, Windows: hallo.bat doppelklicken)
  4. Dein Buch bauen            sh setup/setup.sh, dann im Buchordner sh build.sh / sh build.sh final
                                alles inkl. Leseprobe und Korrektur: sh build.sh komplett
                                welche Datei wofür: ausgabe-normal/00-UEBERSICHT.txt
  5. Wenn etwas klemmt          hilfe.html → Start → «Wenn etwas klemmt», oder die Suche

Nur schnell sehen (im Ordner pureSATZ)
  sh hallo.sh              Beispielbuch anlegen und PDF öffnen (Windows: hallo.bat doppelklicken)
  Checkliste: START.md

Erste Schritte von Hand (im Ordner pureSATZ; start macht dasselbe)
  1. Computer einrichten   bash pc-einrichten/linux-einrichten.sh
                           bash pc-einrichten/mac-einrichten.sh
                           Windows: pc-einrichten\win-einrichten.bat doppelklicken
  2. Neues Buch anlegen    sh setup/setup.sh          (Windows: setup\setup.bat)
  3. Im neuen Buchordner   sh build.sh                (Windows: build.bat)

Druck (ab 2.19)
  Druckangaben pro Fassung in druck/<datei>.md (Muster: vorlage/druck/, epubli und BoD).
  sh build.sh final                     Druckdateien in ausgabe-normal/, ausgabe-<zweite>/
  sh build.sh final druck=<datei>       Test mit einer anderen Druckdatei -> ausgabe-test/<datei>/
  Andere Plattformen (KDP, XinXii, Lulu, Copyshop): hilfe.html, Gruppe «Andere Plattformen».

Mehr: ERSTES-BUCH.md (fünf Schritte), INSTALLATION.md, GITHUB.md
