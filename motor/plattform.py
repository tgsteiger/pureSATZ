"""
plattform.py – auf Windows zeigen Meldungen die Windows-Befehle (pureSATZ ab 2.17.1).

Alle Skripte schreiben Hinweise wie «sh build.sh final». Auf Windows wird daraus beim Ausgeben
automatisch «.\\build.bat final» (ebenso setup, import, pc-einrichten und «python3 motor/…» → «py motor\\…»).
Auf Linux und Mac ändert sich nichts.
"""
import os
import re
import sys

_REGELN = [
    (re.compile(r"\bsh setup/setup\.sh\b"), r".\\setup\\setup.bat"),
    (re.compile(r"\bsh import/import-text\.sh\b"), r".\\import\\import-text.bat"),
    (re.compile(r"\bbash pc-einrichten/\w+-einrichten\.sh\b"), r".\\pc-einrichten\\win-einrichten.bat"),
    (re.compile(r"\bsh ([\w-]+)\.sh\b"), r".\\\1.bat"),
    (re.compile(r"\bpython3 (motor|setup|docs|test)/([\w-]+\.py)\b"), r"py \1\\\2"),
]


def windows(text):
    for muster, ersatz in _REGELN:
        text = muster.sub(ersatz, text)
    return text


class _Strom:
    def __init__(self, strom):
        self._strom = strom

    def write(self, text):
        return self._strom.write(windows(text) if isinstance(text, str) else text)

    def __getattr__(self, name):
        return getattr(self._strom, name)


def windows_befehle():
    """Auf Windows stdout/stderr so umleiten, dass Befehle in Meldungen als .bat erscheinen."""
    if os.name != "nt" and os.environ.get("PURESATZ_WINDOWS") != "1":
        return
    for name in ("stdout", "stderr"):
        s = getattr(sys, name)
        if s is not None and not isinstance(s, _Strom):
            setattr(sys, name, _Strom(s))
