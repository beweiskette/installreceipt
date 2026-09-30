# Validation

Checked on 2026-09-30 with Python 3.11 on Windows.

Before these repairs: 8 collected tests. After: 14 collected, 13 passed and 1 skipped. The skipped cases require Windows symlink creation privileges. Linux CI runs those cases. New bug regressions were run against the previous implementation and observed failing before their fixes; the XML test strengthens existing escaping coverage.

Tests inspect synthetic receipts, malformed inputs, generated XML with an ampersand in the host mapping and external CAB/MST packaging. PowerShell parsing succeeds. Actual MSI/CAB/MST execution in Windows Sandbox remains untested because Sandbox is unavailable on the development host.

The current wheel builds with `python -m pip wheel --no-deps .` using pip's isolated build environment. CLI help succeeds. German README validation with schreibwaechter and locale de-CH reports 0 errors and 0 warnings. Only synthetic test inputs were used.

CI results are available at [GitHub Actions](https://github.com/beweiskette/installreceipt/actions). See SECURITY.md for report contents and runtime boundaries.
