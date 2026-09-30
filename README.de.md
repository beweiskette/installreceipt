# InstallReceipt

Bereitet einen MSI-Lauf in Windows Sandbox vor und vergleicht InstallationsÃ¤nderungen sowie Deinstallationsreste anhand gehashter Bestandsaufnahmen.

Erste nutzbare Version 0.1.0. Python ab 3.11, MIT-Lizenz. VollstÃ¤ndige Schnittstellen und Beispiele stehen in der [englischen README](README.md).

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

Berichte entstehen als `report.json` und `report.html` im gewÃ¤hlten Ausgabeordner. RÃ¼ckgabecode 0 bedeutet bestanden, 1 bedeutet Befunde, 2 einen Eingabe- oder Laufzeitfehler. Die Beispieldaten sind kÃ¼nstlich.

Windows Sandbox ist auf dem Entwicklungsrechner nicht verfÃ¼gbar. Vergleiche, Paketerstellung, XML-Schutzvorgaben und PowerShell-Syntax wurden geprÃ¼ft; die tatsÃ¤chliche MSI-Installation bleibt ungetestet. Erfasst werden ausgewÃ¤hlte Registry-BÃ¤ume, Dienste und PATH. Dateien, weitere Registry-Bereiche und ZustÃ¤nde nach einem Neustart fehlen. SchlÃ¼sselpfade und Dienstnamen bleiben im Bericht sichtbar.

Tests: `python -m pytest -q`. FÃ¼r Docker- und Browsertests gelten die zusÃ¤tzlichen Voraussetzungen in der englischen README. Das Werkzeug lÃ¤dt keine Berichte hoch und ruft keine Modell-API auf.

Externe CAB-Dateien werden mit `--cab` hinzugefügt, Transformationen mit `--transform`. Beide Optionen sind wiederholbar. Die Dateien werden neben das MSI kopiert. Verschachtelte Quellordner werden derzeit nicht unterstützt. Fehlerhafte Eingaben ergeben eine verständliche Meldung und Rückgabecode 2. Die Installation mit diesen Begleitdateien muss noch auf einem Rechner mit Windows Sandbox geprüft werden.
