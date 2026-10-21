pureSATZ - Vorlage und Motor für eigene Bücher (Hilfe: hilfe.html, START.md, README.md)
=====================================================================

Ordner
  setup/          neues Buch anlegen, Motor ins Buch bringen
  pc-einrichten/  Computer einmalig einrichten (Linux, Mac, Windows)
  import/         Buch aus LibreOffice/Word anlegen (Testphase)
  motor/          das Satzsystem (nicht ändern)
  vorlage/        Vorlage für jedes neue Buch
  test/           Selbsttest

Nur schnell sehen (im Ordner pureSATZ)
  sh hallo.sh              Beispielbuch anlegen und PDF öffnen (Windows: hallo.bat doppelklicken)
  Checkliste: START.md

Erste Schritte (im Ordner pureSATZ)
  1. Computer einrichten   bash pc-einrichten/linux-einrichten.sh
                           bash pc-einrichten/mac-einrichten.sh
                           Windows: pc-einrichten\win-einrichten.bat doppelklicken
  2. Neues Buch anlegen    sh setup/setup.sh          (Windows: setup\setup.bat)
  3. Im neuen Buchordner   sh build.sh                (Windows: build.bat)

Mehr: ERSTES-BUCH.md (fünf Schritte), INSTALLATION.md, GITHUB.md
