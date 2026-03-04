param(
  [string]$EnvPath = ".env"
)

$ErrorActionPreference = "Stop"

if (!(Test-Path $EnvPath)) {
  return
}

$lines = Get-Content $EnvPath
foreach ($line in $lines) {
  $t = $line.Trim()
  if ($t.Length -eq 0) { continue }
  if ($t.StartsWith("#")) { continue }
  $eq = $t.IndexOf("=")
  if ($eq -le 0) { continue }

  $key = $t.Substring(0, $eq).Trim()
  $val = $t.Substring($eq + 1).Trim()

  # Strip surrounding quotes if present
  if (($val.StartsWith('"') -and $val.EndsWith('"')) -or ($val.StartsWith("'") -and $val.EndsWith("'"))) {
    $val = $val.Substring(1, $val.Length - 2)
  }

  if ($key) {
    Set-Item -Path "Env:$key" -Value $val
  }
}
