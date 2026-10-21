@echo off
rem LibreOffice- oder Word-Dokument (.odt / .docx) als neues Buch anlegen (Windows, Testphase)
rem   import\import-text.bat manuskript.odt
where py >nul 2>nul && (py "%~dp0import-text.py" %*) || (python "%~dp0import-text.py" %*)
