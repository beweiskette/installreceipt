# Design

Compare MSI installation changes and uninstall residue from Windows Sandbox snapshots.

Use `--cab ./data.cab` for each external cabinet stored beside the MSI and `--transform ./custom.mst` for each transform. These options can be repeated. Files are copied using their original basenames, and transforms are applied in the specified order. Companion names must be unique ignoring case. Cabinets required in nested source folders and installers that fetch missing components from the network are outside this version; sandbox networking stays disabled.

Malformed JSON, unsupported snapshots and malformed release receipts produce a reason and exit 2 without a Python traceback. Package tests use dummy bytes and inspect the generated XML, companion files and PowerShell arguments. They do not validate an actual CAB/MST installation. The XML escaping test places an ampersand in the mapped host folder and checks both the escaped XML and the parsed path.

## Scope

The sandbox maps one input folder read-only and one newly created output folder writable. Networking, clipboard, printers, audio/video input and vGPU are disabled. Never put unrelated host data in the output folder. The installer can modify receipts inside its sandbox, so these are observations for trusted software testing, not tamper-proof forensic evidence.

Collection covers selected machine/user uninstall and startup registry trees, service configuration and machine/user PATH. Values and registry value names are hashed before any output is written. Registry key paths and service names remain visible and may be sensitive. Hashes are fingerprints, not encryption; low-entropy values can be guessed. File changes, scheduled tasks, drivers, all other registry trees and post-reboot state are outside this version.

Snapshots with collection errors or non-hash values are refused. MSI exit codes 0 and 3010 are accepted and recorded; 3010 means a reboot is still required, and this tool does not perform it.

Current verification: Python comparisons, package generation, XML restrictions and PowerShell syntax were checked. **Actual MSI installation inside Windows Sandbox has not been tested on the development host because Windows Sandbox is unavailable there.** Treat the runner as experimental until verified on your own Sandbox host.
