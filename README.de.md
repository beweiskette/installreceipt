# InstallReceipt

Bereitet einen MSI-Lauf in Windows Sandbox vor und vergleicht Installationsänderungen sowie Deinstallationsreste anhand gehashter Bestandsaufnahmen.

Erste nutzbare Version 0.1.0. Python ab 3.11, MIT-Lizenz. Vollständige Schnittstellen und Beispiele stehen in der [englischen README](README.md).

## Installation

Im geklonten Repo eine virtuelle Umgebung anlegen:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[test]"
```

## Beispiel

```sh
installreceipt compare examples/before.json examples/installed.json examples/removed.json --out outputs/check
installreceipt prepare ./installer.msi --out outputs/sandbox-package
```

Berichte entstehen als `report.json` und `report.html` im gewählten Ausgabeordner. Rückgabecode 0 bedeutet bestanden, 1 bedeutet Befunde, 2 einen Eingabe- oder Laufzeitfehler. Die Beispieldaten sind künstlich.

Windows Sandbox ist auf dem Entwicklungsrechner nicht verfügbar. Vergleiche, Paketerstellung, XML-Schutzvorgaben und PowerShell-Syntax wurden geprüft; die tatsächliche MSI-Installation bleibt ungetestet. Erfasst werden ausgewählte Registry-Bäume, Dienste und PATH. Dateien, weitere Registry-Bereiche und Zustände nach einem Neustart fehlen. Schlüsselpfade und Dienstnamen bleiben im Bericht sichtbar.

Tests: `python -m pytest -q`. Für Docker- und Browsertests gelten die zusätzlichen Voraussetzungen in der englischen README. Das Werkzeug lädt keine Berichte hoch und ruft keine Modell-API auf.
