# Anleitung für Claude: pureSATZ modernisieren (grosser Umbau)

Erprobt beim Umbau 3.0.1 → 3.5.1 (21.11.2026, ein Tag, alle Bücher am Schluss «Alles gleich»).
Zweck: Wenn sich wieder viel angesammelt hat (alte Schreibweisen, doppelter Code, chaotische Hilfe, Menü mit
Widersprüchen), kann Claude den Umbau mit dieser Anleitung selbst planen und durchführen.
Technik und Prüfwerkzeuge: `KI-pureSATZ.md`. Diese Datei ist öffentlich – nichts Persönliches hineinschreiben.

## Grundsätze
- **Nie im Original umbauen.** Thomas legt eine Kopie an, Claude schreibt nur dort. Am Schluss geht nur pureSATZ zurück.
- **Jeder Schritt ist eigenständig und geprüft:** Selbsttest grün, alle Bücher alt/neu «Alles gleich», Sicherung, Logbuch.
- **Bücher sehen nachher gleich aus.** Ein Unterschied ist nur erlaubt, wo er gewollt ist (und dann angesehen).
- **Alte Schreibweisen und Tasten gehen weiter** (umbenennen.py bzw. alte Taste im Menü), bis ein Buch umgestellt ist.
- KISS: vorhandenen Code wiederverwenden. Grosse Dateien (build.py) nicht aufteilen – Risiko grösser als Gewinn.
- Plan mit Kürzeln, Thomas gibt «go …». Unterwegs hinterfragen und optimieren, Zwischenschritte dürfen dazukommen.

## Ablauf

### K1 Kopie anlegen (Thomas, einmal)
```
mkdir -p ~/Dokumente/pureWORLD-umbau/buecher
cd ~/Dokumente/pureWORLD
rsync -a --exclude .git --exclude _backup pureSATZ ../pureWORLD-umbau/
rsync -a --exclude .git --exclude 'motor-alt-*' --exclude md-history buecher/Leben123 buecher/Naehrstoffe buecher/pureSATZ-Handbuch ../pureWORLD-umbau/buecher/
```
Logbuch `pureWORLD-umbau/pureSATZ/LOGBUCH-<version>.md` anlegen: Auftrag, Befund, Plan, Verlauf (Tabelle).
Während des Umbaus keine Motor-Änderung im Original (sonst im Logbuch festhalten und beim Zurückkopieren übernehmen).

### K2 Arbeitsumgebung in der Cloud
- Ganze Kopie holen (stage, Unterordner einzeln wegen der 2000er-Grenze): pureSATZ und die Bücher (MD, druck/,
  fotos/, bilder/, tabellen/, geschichten/, ausgabe-* als Vergleich «vorher»).
- Ablage: `w/orig/` (Stand vorher), `w/neu-src/pureSATZ` (Arbeitsstand). Schnappschuss je Version behalten (Referenz).
- **aufbau.sh** `<ziel> <pureSATZ>`: Umgebung mit Motor und Büchern zum Bauen:
```
Z=$1; P=$2
rm -rf $Z; mkdir -p $Z/buecher
cp -r $P $Z/pureSATZ
for b in Leben123 Naehrstoffe pureSATZ-Handbuch; do
  cp -r w/orig/buecher/$b $Z/buecher/$b
  rm -rf $Z/buecher/$b/motor; cp -r $P/motor $Z/buecher/$b/motor
  mkdir -p $Z/buecher/$b/.venv/bin; ln -s $(which python3) $Z/buecher/$b/.venv/bin/python3
done
```
- **pruefen.sh** `<name>`: aufbau, dann parallel Selbsttest, `sh build.sh final` je Buch und das Testbuch, danach
  `test/vergleich.py <referenz> <neu>` je Buch. Referenz = letzter geprüfter Stand (nicht ein zu alter!).
- Hörtexte: Buch-MD mit Platzhaltern durch `motor/audio/md2txt.sh` (Umgebung MD, ZIEL, PLATZHALTER, VERSION) → txt alt/neu vergleichen.
- Menübild: Menü in einem Pseudo-Terminal laufen lassen, ANSI-Farben in ein PNG zeichnen (für motor/bilder/menu.png).

### G0 Testbuch zuerst
`test/alle-befehle.py`: baut aus der Vorlage ein Buch mit **jedem** Befehl, jedem Bereich, jeder Fassung, Foto, QR,
Tabelle, Geschichte, Zeitstrahl, Verzeichnissen; prüft die Abdeckung gegen manuskript.py (NAMEN, FASSUNG).
Ist Teil des Selbsttests. Ohne dieses Netz keinen Umbau beginnen. Neue Fälle hier ergänzen, bevor man sie baut.

### Schritte (Muster, je eine Version)
| | Was | Worauf achten |
|---|---|---|
| G1 | Altlasten weg: alte Schreibweisen, tote Funktionen, Versionskommentare | vorher grep in allen Büchern und der Vorlage; umbenennen.py behält die Übersetzung |
| G2 | Innen auf die neue Schreibweise: ein Leser (`befehl()`) zerlegt jeden Befehl, alle Module nutzen ihn | gross, mittel Risiko – Testbuch erweitern, Fehler zeigen sich als Seitenunterschiede |
| G3 | Ein Leser für alle Ausgaben (PDF, E-Book, Prüfen, Stände, Hörbuch) | Hörbuch nur umstellen, wenn ohnehin neu aufgenommen wird (Azure-Kosten) |
| G4 | Doppelten Code zusammenführen | Seitenbild alt/neu muss gleich bleiben |
| G5 | Menü und Begriffe: Tasten = Terminal-Befehle, ein Wort pro Sache | alte Tasten weiter; Menü mit Eingaben testen; Menübild neu |
| G6 | Hilfe: jede Sache an einer Stelle, keine Versionsgeschichte, keine doppelten Listen | hilfe.html und Webseite neu erzeugen, tote Anker prüfen |
| + | Starter (build.sh usw.) nicht doppelt pflegen: Befehlsliste nur in bauen.py | update erneuert Starter ausser `# eigen` |

### Pro Schritt
1. Ändern in `neu-src`, Testbuch ergänzen.
2. Selbsttest, Testbuch, alle Bücher alt/neu vergleichen, Hörtexte wenn md2txt betroffen, Menü wenn menu.py betroffen.
3. Jeden Unterschied ansehen (pdftoppm, Seiten nebeneinander). Nur Gewolltes bleibt.
4. VERSION, CHANGELOG, Logbuch (Verlauf: Version, Schritt, Selbsttest, Vergleich).
5. Zurückschreiben in die Kopie: geänderte Dateien bestimmen (cmp gegen den zuletzt geholten Stand), aktuellen Stand
   holen und prüfen, ob Thomas etwas geändert hat, alte Dateien nach `_backup/vor-<version>/`, schreiben mit
   expectedMtimeMs, nochmals holen und vergleichen.
6. Thomas baut lokal in der Kopie (mit Silbentrennung und CMYK) und schaut an.

### K4 Zurück ins Original
1. Prüfen, ob das Original-pureSATZ seit dem Anlegen der Kopie unverändert ist (Grösse/mtime gegen die ältesten
   Sicherungen). Sonst zuerst zusammenführen.
2. Nur geänderte und neue Dateien schreiben (`.git` nie anfassen), alte nach `pureSATZ/_backup/vor-<version>-umbau/`.
3. Nochmals holen und vergleichen.
4. Das **aktuelle** Hauptbuch aus dem Original mit altem und neuem Motor bauen → «Alles gleich».
   Baut es mit keinem Motor (Thomas schreibt gerade daran), die Stelle melden und für den Test weglassen.
5. Thomas: Selbsttest, `sh release.sh`, in den Büchern `sh update.sh lokal`, bauen im Menü.
6. Danach: Wiedereinstieg `KI-pureSATZ.md` nachführen, Logbuch archivieren, Kopie `pureWORLD-umbau` löschen.

## Fallen (erlebt)
- Zahl im Befehl verwechselt (Grösse statt Höhe) → nur der Seitenvergleich findet es.
- Reihenfolge im E-Book (Randbemerkung vor ihrem Absatz) → Absatz vorher abschliessen.
- Selbsttest erwartet alte Ausgaben (z. B. Import) → Test mit anpassen, nicht den Code verbiegen.
- Alte Referenz für den Vergleich gewählt → lauter «Unterschiede». Immer gegen den letzten geprüften Stand vergleichen.
- Fassung vor einem Befehl hat schon eine Bedeutung (alles nur dort) – nie still umdeuten, sonst verschwinden oder
  erscheinen Texte. Neue Bedeutung bekommt eine neue Schreibweise (z. B. Fassung hinten).
- Bilder werden beim Übertragen neu verpackt: Pixel vergleichen, nicht Bytes.
