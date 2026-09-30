# Data handling

InstallReceipt has no telemetry, update checks, cloud account or model API integration. Reports are written only to the chosen local output directory. HTML uses no remote scripts, fonts or images.

The sandbox maps one input folder read-only and one newly created output folder writable. Networking, clipboard, printers, audio/video input and vGPU are disabled. Never put unrelated host data in the output folder. The installer can modify receipts inside its sandbox, so these are observations for trusted software testing, not tamper-proof forensic evidence.

Collection covers selected machine/user uninstall and startup registry trees, service configuration and machine/user PATH. Values and registry value names are hashed before any output is written. Registry key paths and service names remain visible and may be sensitive. Hashes are fingerprints, not encryption; low-entropy values can be guessed. File changes, scheduled tasks, drivers, all other registry trees and post-reboot state are outside this version.

Snapshots with collection errors or non-hash values are refused. MSI exit codes 0 and 3010 are accepted and recorded; 3010 means a reboot is still required, and this tool does not perform it.

Current verification: Python comparisons, package generation, XML restrictions and PowerShell syntax were checked. **Actual MSI installation inside Windows Sandbox has not been tested on the development host because Windows Sandbox is unavailable there.** Treat the runner as experimental until verified on your own Sandbox host.

Dependencies are installed separately from package providers. GitHub Actions checks out the source and runs the test suite on GitHub-hosted runners. Workflows receive read-only repository permissions and publish no artifacts. Review inputs and reports before sharing them. Keep synthetic examples in this repository; do not commit real credentials, exports or receipts.

If you find a security issue, report it privately to the repository owner without including live credentials or personal data.
