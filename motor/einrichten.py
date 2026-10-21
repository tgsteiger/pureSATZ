#!/usr/bin/env python3
"""
einrichten.py – richtet im Buchordner die Python-Umgebung .venv ein (einmalig, braucht Internet).
Aufruf (im Buchordner):  python3 motor/einrichten.py
Läuft unter Linux, macOS und Windows.
"""
import os
import shutil
import subprocess
import sys

MOTOR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(MOTOR)
PAKETE = ["reportlab==5.0.1", "pillow", "pypdf", "pypdfium2"]


def venv_python(base=BASE):
    if os.name == "nt":
        return os.path.join(base, ".venv", "Scripts", "python.exe")
    return os.path.join(base, ".venv", "bin", "python3")


def bereit(py):
    if not os.path.exists(py):
        return False
    r = subprocess.run([py, "-c", "import reportlab, PIL, pypdf, pypdfium2, sys; sys.exit(reportlab.Version != '5.0.1')"],
                       capture_output=True)
    return r.returncode == 0


def einrichten(base=BASE):
    py = venv_python(base)
    if bereit(py):
        print("Python-Umgebung ist bereit (.venv).")
    else:
        print("=== Python-Umgebung einrichten (.venv, einmalig, ca. 1 Minute) ===")
        shutil.rmtree(os.path.join(base, ".venv"), ignore_errors=True)
        try:
            subprocess.run([sys.executable, "-m", "venv", os.path.join(base, ".venv")], check=True)
        except subprocess.CalledProcessError:
            print("\nFEHLER: venv fehlt. Linux: sudo apt install python3-venv")
            sys.exit(1)
        try:
            subprocess.run([py, "-m", "pip", "install", "--quiet", "--upgrade", "pip"], check=True)
            subprocess.run([py, "-m", "pip", "install", "--quiet"] + PAKETE, check=True)
        except subprocess.CalledProcessError:
            shutil.rmtree(os.path.join(base, ".venv"), ignore_errors=True)
            print("\nFEHLER: Pakete konnten nicht installiert werden (Internet?). Später nochmals versuchen.")
            sys.exit(1)
        print("Umgebung bereit.")
    return py


if __name__ == "__main__":
    einrichten()
