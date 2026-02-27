param(
  [Parameter(Mandatory=$true)][string]$Manifest
)

if (!(Test-Path "lessons_learned.md")) {
  Write-Error "lessons_learned.md not found in repo root. Aborting."
  exit 1
}

if (!$env:NEBIUS_VLLM_BASE_URL -or !$env:NEBIUS_VLLM_API_KEY) {
  Write-Error "NEBIUS_VLLM_BASE_URL / NEBIUS_VLLM_API_KEY not set. Aborting."
  exit 1
}

python -m src.cli batch --manifest $Manifest
