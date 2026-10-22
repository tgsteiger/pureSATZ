#!/usr/bin/env python3
"""
epub2.py – «epub2-light»: macht aus dem fertigen EPUB 3 eine zusätzliche EPUB-2-Datei (pureSATZ 2.20).

Für Shops und Prüfprogramme, die nur EPUB 2 annehmen (z. B. epubli). Das EPUB 3 bleibt unverändert.
Was geändert wird:
  - content.opf: Version 2.0, Metadaten in EPUB-2-Form (Barrierefreiheit als <meta name>), Titelbild per <meta name="cover">,
    nav.xhtml bleibt als normale Inhaltsseite, Inhaltsverzeichnis für das Lesegerät ist toc.ncx
  - Seiten: XHTML 1.1 – section, nav, aside, figure … werden zu div; epub:type, role, aria-*, lang entfernt
Ein- und ausschalten: Variable «ebook-epub2: ja» (Standard nein) – dann entsteht <datei>_EPUB2.epub.
Von Hand:  python3 motor/epub2.py ausgabe-normal/Buch.epub   (schreibt ausgabe-normal/Buch_EPUB2.epub)
"""
import re
import sys
import zipfile

DOCTYPE = ('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" '
           '"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">')
HTML5 = ("section", "nav", "aside", "figure", "figcaption", "header", "footer", "main", "article")


def _ol_start(t):
    """<ol start="3"> gibt es in XHTML 1.1 nicht: Nummern ausschreiben (3. 4. …), Liste ohne eigene Zählung."""
    aus, pos = [], 0
    for m in re.finditer(r'<ol\b([^>]*?)\s+start="(\d+)"([^>]*)>', t):
        if m.start() < pos:
            continue
        aus.append(t[pos:m.start()])
        aus.append(f'<ol{m.group(1)}{m.group(3)} style="list-style-type:none">')
        nr, tiefe, i = int(m.group(2)), 0, m.end()
        for k in re.finditer(r"<(/?)(ol|ul|li)\b[^>]*>", t[m.end():]):
            j = m.end() + k.start()
            if k.group(2) in ("ol", "ul"):
                if k.group(1):
                    if tiefe == 0:                       # Ende dieser Liste
                        aus.append(t[i:j]); i = j; break
                    tiefe -= 1
                else:
                    tiefe += 1
            elif k.group(2) == "li" and not k.group(1) and tiefe == 0:
                ende = m.end() + k.end()
                aus.append(t[i:ende] + f"{nr}. "); i = ende; nr += 1
        pos = i
    aus.append(t[pos:])
    return "".join(aus)


def _seite(t):
    """Eine XHTML-Seite von EPUB 3 (XHTML5) auf XHTML 1.1."""
    t = _ol_start(t)
    t = re.sub(r"<(nav|section|div)\b[^>]*\bhidden=\"[^\"]*\"[^>]*>.*?</\1>\n?", "", t, flags=re.S)  # z. B. Landmarks
    t = re.sub(r"<!DOCTYPE[^>]*>", DOCTYPE, t, count=1)
    t = t.replace("<style>", '<style type="text/css">')
    t = re.sub(r"(<body[^>]*>)\s*(<img\b[^>]*/>)\s*(</body>)", r"\1<div>\2</div>\3", t)    # Titelbild
    t = re.sub(r'\s+xmlns:epub="[^"]*"', "", t)
    t = re.sub(r'\s+(epub:type|role|aria-[a-z]+|lang|hidden)="[^"]*"', "", t)
    t = t.replace('<meta charset="utf-8"/>', '<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>')
    for tag in HTML5:
        t = re.sub(rf"<{tag}(\s[^>]*)?>", lambda m: "<div" + (m.group(1) or "") + ">", t)
        t = t.replace(f"</{tag}>", "</div>")
    return t


def _opf(t):
    """content.opf von Version 3.0 auf 2.0."""
    t = re.sub(r'<package\b[^>]*>',
               '<package xmlns="http://www.idpf.org/2007/opf" version="2.0" unique-identifier="bookid">', t, count=1)
    t = t.replace('<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">',
                  '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">')
    # Barrierefreiheit (schema.org) bleibt erhalten – in EPUB 2 als <meta name="…" content="…"/> (Ace by DAISY)
    t = re.sub(r'<meta property="(schema:[^"]+)">(.*?)</meta>',
               lambda m: f'<meta name="{m.group(1)}" content="{m.group(2)}"/>', t, flags=re.S)
    t = re.sub(r"<meta property=[^>]*>.*?</meta>\n?", "", t, flags=re.S)        # dcterms:modified u. ä.
    t = re.sub(r'\s+properties="[^"]*"', "", t)                                  # nav, cover-image
    t = t.replace('media-type="font/ttf"', 'media-type="application/vnd.ms-opentype"')
    t = t.replace("</spine>", "</spine>\n<guide>\n<reference type=\"cover\" title=\"Titelbild\" href=\"cover.xhtml\"/>\n"
                              "<reference type=\"toc\" title=\"Inhalt\" href=\"nav.xhtml\"/>\n</guide>", 1)
    return t


def wandle(quelle, ziel):
    """EPUB 3 (quelle) → EPUB 2 (ziel). Gibt den Zielpfad zurück."""
    with zipfile.ZipFile(quelle) as q, zipfile.ZipFile(ziel, "w") as z:
        z.writestr(zipfile.ZipInfo("mimetype"), "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        for info in q.infolist():
            if info.filename == "mimetype":
                continue
            daten = q.read(info.filename)
            if info.filename.endswith(".xhtml"):
                daten = _seite(daten.decode("utf-8")).encode("utf-8")
            elif info.filename.endswith(".opf"):
                daten = _opf(daten.decode("utf-8")).encode("utf-8")
            z.writestr(info.filename, daten, compress_type=zipfile.ZIP_DEFLATED)
    return ziel


if __name__ == "__main__":
    if len(sys.argv) < 2 or not sys.argv[1].endswith(".epub"):
        sys.exit("Aufruf: python3 motor/epub2.py <datei>.epub")
    print("Fertig:", wandle(sys.argv[1], sys.argv[1][:-5] + "_EPUB2.epub"))
