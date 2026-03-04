param(
  [Parameter(Mandatory=$true)][string]$InDir,
  [Parameter(Mandatory=$true)][string]$OutDir,
  [int]$Seconds = 20,
  [string]$Start = "00:00:00",
  [switch]$Copy
)

$ErrorActionPreference = "Stop"

if (!(Test-Path $InDir)) { throw "InDir not found: $InDir" }
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$inputs = Get-ChildItem -Path $InDir -Recurse -File | Where-Object {
  $_.Extension -in @(".avi", ".mp4", ".mov", ".mkv")
}

if ($inputs.Count -eq 0) {
  Write-Host "No videos found under $InDir"
  exit 0
}

foreach ($f in $inputs) {
  $base = [IO.Path]::GetFileNameWithoutExtension($f.Name)
  $out = Join-Path $OutDir ($base + "_trim" + $Seconds + "s.mp4")
  if (Test-Path $out) {
    Write-Host "SKIP $($f.Name)"
    continue
  }

  Write-Host "TRIM $($f.Name) -> $(Split-Path -Leaf $out)"

  if ($Copy) {
    # Best-quality quick trim: stream copy (no re-encode).
    ffmpeg -y -hide_banner -loglevel error `
      -ss $Start -i $f.FullName -t $Seconds `
      -c copy -an -movflags +faststart `
      $out
  } else {
    # Re-encode fallback. We use h264_mf because the Windows ffmpeg in this environment doesn't ship libx264.
    ffmpeg -y -hide_banner -loglevel error `
      -ss $Start -i $f.FullName -t $Seconds `
      -c:v h264_mf -pix_fmt yuv420p -an `
      $out
  }
}

Write-Host "Done."
