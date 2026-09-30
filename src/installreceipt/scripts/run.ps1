$ErrorActionPreference = 'Stop'
$status = [ordered]@{schema=1; status='incomplete'; install_exit=$null; uninstall_exit=$null}
try {
    $options = Get-Content -LiteralPath C:\ReceiptInput\install-options.json -Raw | ConvertFrom-Json
    $arguments = @('/i', 'C:\ReceiptInput\installer.msi', '/qn', '/norestart')
    if ($options.transforms.Count -gt 0) {
        $paths = @($options.transforms | ForEach-Object { Join-Path 'C:\ReceiptInput' $_ })
        $arguments += ('TRANSFORMS="' + ($paths -join ';') + '"')
    }
    & C:\ReceiptInput\collect.ps1 -OutputPath C:\ReceiptOutput\before.json
    $install = Start-Process msiexec.exe -ArgumentList $arguments -Wait -PassThru -WindowStyle Hidden
    $status.install_exit = $install.ExitCode
    if ($install.ExitCode -notin @(0, 3010)) { throw 'Installation failed' }
    & C:\ReceiptInput\collect.ps1 -OutputPath C:\ReceiptOutput\installed.json
    $uninstall = Start-Process msiexec.exe -ArgumentList @('/x', 'C:\ReceiptInput\installer.msi', '/qn', '/norestart') -Wait -PassThru -WindowStyle Hidden
    $status.uninstall_exit = $uninstall.ExitCode
    if ($uninstall.ExitCode -notin @(0, 3010)) { throw 'Uninstallation failed' }
    & C:\ReceiptInput\collect.ps1 -OutputPath C:\ReceiptOutput\removed.json
    $status.status = 'complete'
} catch { $status.status = 'failed' }
$status | ConvertTo-Json | Set-Content -LiteralPath C:\ReceiptOutput\run-status.json -Encoding UTF8
Write-Host 'Receipt collection finished. Inspect run-status.json and the snapshots in the mapped output folder.'
