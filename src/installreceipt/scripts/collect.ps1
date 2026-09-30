param([Parameter(Mandatory=$true)][string]$OutputPath)
$ErrorActionPreference = 'Stop'
$items = @{}
$issues = [System.Collections.Generic.List[string]]::new()
function Add-Fingerprint([string]$Name, [object]$Value) {
    $json = ConvertTo-Json -InputObject $Value -Compress -Depth 8
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try {
        $items[$Name] = ([BitConverter]::ToString($sha.ComputeHash([Text.Encoding]::UTF8.GetBytes($json)))).Replace('-', '').ToLowerInvariant()
    } finally { $sha.Dispose() }
}
$trees = @(
    'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall',
    'HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall',
    'HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall',
    'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run',
    'HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run'
)
foreach ($tree in $trees) {
    try {
        if (-not (Test-Path -LiteralPath $tree)) { continue }
        $keys = @((Get-Item -LiteralPath $tree)) + @(Get-ChildItem -LiteralPath $tree -Recurse -ErrorAction Stop)
        foreach ($key in $keys) {
            # Retain registry key identity, but hash names AND values together.
            # No raw value, licence key or command line is written to disk.
            $properties = [ordered]@{}
            foreach ($name in @($key.GetValueNames() | Sort-Object)) {
                $properties[$name] = $key.GetValue($name, $null, 'DoNotExpandEnvironmentNames')
            }
            Add-Fingerprint ('registry:' + $key.Name) $properties
        }
    } catch { $issues.Add('registry-incomplete') }
}
try {
    foreach ($service in Get-CimInstance Win32_Service -ErrorAction Stop) {
        Add-Fingerprint ('service:' + $service.Name) ([ordered]@{Path=$service.PathName; StartMode=$service.StartMode; Account=$service.StartName})
    }
} catch { $issues.Add('services-incomplete') }
foreach ($scope in @('Machine', 'User')) {
    try { Add-Fingerprint ('environment:PATH:' + $scope) ([Environment]::GetEnvironmentVariable('PATH', $scope)) }
    catch { $issues.Add('environment-incomplete') }
}
$result = [ordered]@{schema=1; complete=($issues.Count -eq 0); items=$items; issues=@($issues.ToArray())}
$result | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $OutputPath -Encoding UTF8
