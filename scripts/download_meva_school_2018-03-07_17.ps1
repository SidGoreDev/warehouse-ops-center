param(
  [string]$OutDir = "data\\meva\\raw"
)
$ErrorActionPreference = 'Stop'
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$bucket = "mevadata-public-01"
$base = "https://mevadata-public-01.s3.amazonaws.com/"

# Keys selected from MEVA public S3 via list-type=2; download with curl.exe
$keys = @(
  "drops-123-r13/2018-03-07/17/2018-03-07.16-55-01.17-00-01.school.G328.r13.avi",
  "drops-123-r13/2018-03-07/17/2018-03-07.16-55-06.17-00-06.school.G300.r13.avi",
  "drops-123-r13/2018-03-07/17/2018-03-07.16-55-06.17-00-06.school.G336.r13.avi",
  "drops-123-r13/2018-03-07/17/2018-03-07.16-55-06.17-00-06.school.G339.r13.avi",
  "drops-123-r13/2018-03-07/17/2018-03-07.16-55-06.17-00-06.school.G424.r13.avi",
  "drops-123-r13/2018-03-07/17/2018-03-07.17-00-01.17-05-01.school.G328.r13.avi",
  "drops-123-r13/2018-03-07/17/2018-03-07.17-00-06.17-05-00.school.G336.r13.avi",
  "drops-123-r13/2018-03-07/17/2018-03-07.17-00-06.17-05-06.school.G300.r13.avi",
  "drops-123-r13/2018-03-07/17/2018-03-07.17-00-06.17-05-06.school.G339.r13.avi",
  "drops-123-r13/2018-03-07/17/2018-03-07.17-00-06.17-05-06.school.G424.r13.avi"
)

foreach ($k in $keys) {
  $rel = $k -replace '^.*/', ''
  $out = Join-Path $OutDir $rel
  if (Test-Path $out) { Write-Host "SKIP $rel"; continue }
  $url = $base + [uri]::EscapeUriString($k)
  Write-Host "GET $rel"
  curl.exe -L --fail --retry 3 --retry-delay 2 -o $out $url
}
Write-Host "Done."
