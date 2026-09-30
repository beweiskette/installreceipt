# InstallReceipt

Prepare a restricted Windows Sandbox run for an MSI installer, then compare installation changes and uninstall residue using hashed snapshots.

Version 0.1.0. [Deutsch](README.de.md). Python 3.11 or newer. MIT licence.

## Install

From a clone of this repository:

```sh
python -m venv .venv
# Linux/macOS:
. .venv/bin/activate
# Windows PowerShell instead:
# .\.venv\Scripts\Activate.ps1
python -m pip install -e ".[test]"
```

## Run

```sh
installreceipt compare examples/before.json examples/installed.json examples/removed.json --out outputs/check
installreceipt prepare ./installer.msi --out outputs/sandbox-package
```

The synthetic comparison reports a new service, changed PATH and a service left behind after uninstall. `prepare` copies the installer and collection scripts, then writes `run.wsb`. It never starts an installer on the host.

Open `run.wsb` manually on a Windows edition with Windows Sandbox installed and enabled. The sandbox installs and uninstalls the copied MSI silently with `/norestart`. Inspect `output/run-status.json`; only after a completed run, compare `output/before.json`, `output/installed.json` and `output/removed.json` with the `compare` command.

Compare two resulting `report.json` files with `installreceipt releases receipt-a.json receipt-b.json --out outputs/releases`. Use the same clean Windows baseline for meaningful release comparisons.

Reports are local JSON and self-contained HTML. Exit status is 0 for a pass, 1 for findings, and 2 for an input or runtime setup error. Commands do not publish reports or contact a model API.

## Boundaries

The sandbox maps one input folder read-only and one newly created output folder writable. Networking, clipboard, printers, audio/video input and vGPU are disabled. Never put unrelated host data in the output folder. The installer can modify receipts inside its sandbox, so these are observations for trusted software testing, not tamper-proof forensic evidence.

Collection covers selected machine/user uninstall and startup registry trees, service configuration and machine/user PATH. Values and registry value names are hashed before any output is written. Registry key paths and service names remain visible and may be sensitive. Hashes are fingerprints, not encryption; low-entropy values can be guessed. File changes, scheduled tasks, drivers, all other registry trees and post-reboot state are outside this version.

Snapshots with collection errors or non-hash values are refused. MSI exit codes 0 and 3010 are accepted and recorded; 3010 means a reboot is still required, and this tool does not perform it.

Current verification: Python comparisons, package generation, XML restrictions and PowerShell syntax were checked. **Actual MSI installation inside Windows Sandbox has not been tested on the development host because Windows Sandbox is unavailable there.** Treat the runner as experimental until verified on your own Sandbox host.

## Verify

```sh
python -m pytest -q
```

Tests use synthetic snapshots and a non-executable dummy MSI byte sequence. They verify comparison results, incomplete-input rejection, XML escaping, disabled network/clipboard and fresh output-folder requirements. They do not launch Windows Sandbox.

GitHub Actions runs tests on Windows and Linux. Integration jobs use synthetic local fixtures. No deployment or package publication workflow is configured. Dependency installation and browser/image downloads are explicit setup steps that contact their respective package providers.

See [DESIGN.md](DESIGN.md) for the scope decisions and [SECURITY.md](SECURITY.md) for data handling.
