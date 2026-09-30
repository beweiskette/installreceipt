# Validation record

Checked on 2026-09-30 with Python 3.11 on Windows.

Local pytest result: `7 passed, 1 skipped in 0.10s`. Skipped cases require Windows symlink creation privileges; Linux CI exercises those cases. Editable installation, CLI help and wheel construction succeeded. Only synthetic fixtures were used.

The checked-in reports under `examples/` come from actual CLI runs against the synthetic fixtures. Browser reports may contain the temporary loopback port used for that run; adjust the reproduction URL to your running fixture server.

Source review and a staged-file pattern scan found no live credential formats, private user paths or accidentally tracked environment files. This is a scoped check, not a guarantee that every possible secret format is detectable.

Actual installation inside Windows Sandbox remains untested. PowerShell scripts were syntax-checked; Python comparisons and generated XML were tested.

See the Actions tab for independent Windows and Linux CI results.
