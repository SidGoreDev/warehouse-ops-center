param([string]$OutDir = "data/videos/meva_examples_selected10")
$ErrorActionPreference = "Stop"
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$items = @(
  @{ url = "https://mevadata-public-01.s3.amazonaws.com/examples/videos/ex027-heavy-carry.mp4"; name = "ex027-heavy-carry.mp4" },
  @{ url = "https://mevadata-public-01.s3.amazonaws.com/examples/videos/ex028-heavy-carry.mp4"; name = "ex028-heavy-carry.mp4" },
  @{ url = "https://mevadata-public-01.s3.amazonaws.com/examples/videos/ex029-heavy-carry.mp4"; name = "ex029-heavy-carry.mp4" },
  @{ url = "https://mevadata-public-01.s3.amazonaws.com/examples/videos/ex033-load-vehicle.mp4"; name = "ex033-load-vehicle.mp4" },
  @{ url = "https://mevadata-public-01.s3.amazonaws.com/examples/videos/ex034-load-vehicle.mp4"; name = "ex034-load-vehicle.mp4" },
  @{ url = "https://mevadata-public-01.s3.amazonaws.com/examples/videos/ex035-load-vehicle.mp4"; name = "ex035-load-vehicle.mp4" },
  @{ url = "https://mevadata-public-01.s3.amazonaws.com/examples/videos/ex085-theft.mp4"; name = "ex085-theft.mp4" },
  @{ url = "https://mevadata-public-01.s3.amazonaws.com/examples/videos/ex086-unload-vehicle.mp4"; name = "ex086-unload-vehicle.mp4" },
  @{ url = "https://mevadata-public-01.s3.amazonaws.com/examples/videos/ex087-unload-vehicle.mp4"; name = "ex087-unload-vehicle.mp4" },
  @{ url = "https://mevadata-public-01.s3.amazonaws.com/examples/videos/ex088-unload-vehicle.mp4"; name = "ex088-unload-vehicle.mp4" },
)

foreach ($it in $items) {
  $dst = Join-Path $OutDir $it.name
  if (Test-Path $dst) { Write-Host "SKIP $($it.name)"; continue }
  Write-Host "GET  $($it.name)"
  curl.exe -L --fail --retry 5 --retry-delay 2 -o $dst $it.url
}
Write-Host "Done."
