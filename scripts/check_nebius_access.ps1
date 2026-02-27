param(
  [Parameter(Mandatory=$true)][string]$Ip
)

if (!$env:NEBIUS_VLLM_API_KEY) {
  Write-Error "NEBIUS_VLLM_API_KEY not set in environment. (Tip: load .env in your shell or set it manually)"
  exit 1
}

Write-Host "Checking port 8000 reachability..."
Test-NetConnection $Ip -Port 8000 | Out-Host

$h = @{ "Authorization" = "Bearer $env:NEBIUS_VLLM_API_KEY" }
$url = "http://$Ip`:8000/v1/models"
Write-Host "GET $url"
try {
  Invoke-RestMethod -Uri $url -Headers $h | ConvertTo-Json -Depth 8 | Out-Host
  Write-Host "OK: /v1/models responded with auth."
} catch {
  Write-Error $_
  exit 1
}
