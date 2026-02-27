# Lessons Learned — Cosmos Cookoff (SafeFloor)

Portable reference for any new project using Nebius cloud + Cosmos Reason2 + vLLM.
Written so a fresh agent in a fresh repo can hit the ground running.

---

## 1. Nebius Cloud Setup (From Scratch)

### What Nebius Is
Nebius AI Cloud provides GPU VM instances (H100, etc.) in the `eu-north1` region. For the Cosmos Cookoff, NVIDIA provided credits on Nebius to run vLLM serving Cosmos Reason2.

### Instance Provisioning
- **Console URL**: https://console.nebius.com
- **Instance type used**: 1x NVIDIA H100 NVLink 80GB, 16 vCPUs, 200 GiB RAM, 256 GiB SSD
- **OS**: Ubuntu 24.04 LTS, CUDA 12
- **Deployment mode**: "Container over VM" preset — vLLM + Jupyter pre-installed
- **Budget awareness**: H100 at ~$2.95/hr. Stop the VM when not in use. Credits deplete fast if left running overnight.

### SSH Access Setup
1. **Generate an SSH key locally** (if you don't have one):
   ```powershell
   ssh-keygen -t ed25519 -f $env:USERPROFILE\.ssh\id_ed25519
   ```
2. **Register the public key** in the Nebius Console under VM Access / cloud-init settings.
3. **Choose a canonical SSH username** and register it alongside the key. We used `sgdev`. Document this in your project docs — the username must match what cloud-init provisions on the VM.
4. **Connect**:
   ```powershell
   ssh -i $env:USERPROFILE\.ssh\id_ed25519 sgdev@<public_ip> "hostname && whoami"
   ```

### Critical: Public IP Is Volatile
- Nebius VMs get a **dynamic public IP**. Every time the VM restarts, the IP can change.
- **Before every session**, check the current public IP in the Nebius Console. Do not trust stale values from prior sessions or docs.
- If the IP changes, your local `known_hosts` will reject the new host key. Remove the old entry:
  ```powershell
  ssh-keygen -R <old_ip>
  ```
- **Recommendation**: If Nebius supports static IP allocation in your project/region, pin one. We never did this and it cost us hours of debugging.

### Environment Variables
Create a `.env` file in the repo root (gitignored). The pipeline reads it automatically.

```bash
NEBIUS_VLLM_BASE_URL=http://<current_public_ip>:8000
NEBIUS_VLLM_API_KEY=<your_vllm_api_key>
NEBIUS_VLLM_MODEL=nvidia/Cosmos-Reason2-8B
NEBIUS_VLLM_TIMEOUT_S=120
NEBIUS_VLLM_TOP_P=0.95
```

Legacy env var names (`COSMOS_API_BASE`, `COSMOS_API_KEY`, `COSMOS_MODEL`) also work as fallbacks.

---

## 2. Nebius CLI Usage

### Installation
The Nebius CLI (`nebius`) is a **Linux-only binary**. On Windows, run it from WSL.

```bash
# Inside WSL
nebius auth login --profile <your_profile_name>
```

This opens a browser-based OAuth flow. If copy-pasting the auth URL from the terminal is difficult, write it to a file and open from there:
```bash
nebius auth login --profile codex2 2>&1 | tee /tmp/nebius_auth.txt
# Then open the URL from the file in your browser
```

### CLI vs Console
In practice, we used the **Nebius web console** far more than the CLI for:
- Checking the current public IP
- Starting/stopping VMs
- Updating Access/cloud-init SSH keys and usernames

The CLI is useful for scripted automation, but for a hackathon project the console is faster for ad-hoc checks.

---

## 3. vLLM Endpoint Access

### How It Works
Nebius runs vLLM as a containerized service on the GPU VM. It exposes an **OpenAI-compatible API** at `http://<public_ip>:8000`.

### Verifying the Endpoint
```powershell
# 1. Check network reachability
Test-NetConnection <public_ip> -Port 8000

# 2. Check model availability (expects 200 with API key, 401 without)
$headers = @{"Authorization" = "Bearer $env:NEBIUS_VLLM_API_KEY"}
Invoke-RestMethod -Uri "http://<public_ip>:8000/v1/models" -Headers $headers

# 3. Quick chat completion test
$body = @{
    model = "nvidia/Cosmos-Reason2-8B"
    messages = @(@{role = "user"; content = "What is 2+2?"})
    max_tokens = 50
} | ConvertTo-Json -Depth 5
Invoke-RestMethod -Method Post -Uri "http://<public_ip>:8000/v1/chat/completions" -Headers $headers -Body $body -ContentType "application/json"
```

### API Key vs IAM Auth
- The **vLLM API key** authenticates to the model endpoint (`/v1/chat/completions`). It's set when deploying the vLLM container.
- **Nebius IAM auth** (`nebius auth login`) authenticates to the Nebius control plane (managing VMs, not calling the model).
- These are **completely separate credentials**. Don't mix them up. We did, multiple times.

---

## 4. Access Failures — What Went Wrong and How to Avoid It

This was the single biggest time sink. Here's every failure mode we hit.

### Failure: SSH Connection Refused
- **Cause**: VM was stopped, or the public IP had changed.
- **Fix**: Check the console for the current IP. Start the VM if stopped.

### Failure: SSH Host Key Mismatch
- **Cause**: IP changed but old `known_hosts` entry remained.
- **Fix**: `ssh-keygen -R <old_ip>` then reconnect.

### Failure: SSH Permission Denied
- **Cause**: Wrong username, or the SSH key wasn't registered in cloud-init.
- **Fix**: Verify the username matches the cloud-init config (ours was `sgdev`). Re-register the public key in the Nebius Console under VM Access if needed. You may need to restart the VM for cloud-init changes to take effect.

### Failure: SSH Works but Wrong Shell Context
- **Cause**: Logged into a minimal container shell instead of the host VM shell. Commands like `ss`, `systemctl`, `ssh-keygen` are missing.
- **Fix**: Make sure you're SSH'ing into the **host VM**, not exec'ing into a container. If basic Linux tools are missing, you're in the wrong context.

### Failure: vLLM Endpoint Connection Refused
- **Cause**: VM just restarted and vLLM hasn't started yet, or wrong IP.
- **Fix**: Wait 1-2 minutes after VM start for vLLM to initialize. Verify IP. Check port 8000 with `Test-NetConnection`.

### Failure: vLLM Returns 401
- **Cause**: Missing or wrong API key.
- **Fix**: This is actually a **good sign** — the endpoint is reachable. Just fix the `Authorization: Bearer` header.

### Failure: `reasoning_content` Is Null
- **Cause**: vLLM wasn't started with `--reasoning-parser qwen3`. Without this flag, the server won't extract `<think>` blocks into `reasoning_content`.
- **Fix**: If you control the vLLM startup, add the flag:
  ```bash
  python3 -m vllm.entrypoints.openai.api_server \
    --model nvidia/Cosmos-Reason2-8B \
    --host 0.0.0.0 --port 8000 \
    --reasoning-parser qwen3
  ```
  If using a managed Nebius template that doesn't expose startup args, you may not be able to fix this. Our workaround was to not depend on native `reasoning_content` — the prompt requires explicit JSON planning fields instead, and the pipeline derives reasoning traces from those.

---

## 5. Session-Start SOP (Do This Every Time)

```
1. Open Nebius Console → confirm VM is running → note the current public IP.
2. Update .env with the current IP:
     NEBIUS_VLLM_BASE_URL=http://<current_ip>:8000
3. Verify SSH:
     ssh -i $env:USERPROFILE\.ssh\id_ed25519 sgdev@<current_ip> "hostname && whoami"
4. Verify endpoint:
     Test-NetConnection <current_ip> -Port 8000
     Invoke-RestMethod -Uri "http://<current_ip>:8000/v1/models" -Headers @{"Authorization"="Bearer $env:NEBIUS_VLLM_API_KEY"}
5. If SSH fails → check username/key in console → re-register if needed → restart VM.
6. If endpoint fails → wait for vLLM to start → re-check in 60s.
```

---

## 6. Cosmos Reason2 — Model Behavior Notes

### What It Is
`nvidia/Cosmos-Reason2-8B` is a Qwen3-VL-based vision-language model post-trained on physical common sense and embodied reasoning data. It takes video + text and produces structured chain-of-thought reasoning about physical world state.

### Prompting Tips
- **Request structured JSON output explicitly.** The model can produce it reliably if you specify the exact schema in the prompt.
- **Use explicit planning fields** (`observe`, `diagnose`, `plan`, `next`) rather than relying on free-form chain-of-thought. This makes the output deterministic and parseable.
- **Keep temperature low** (0.2) and **use a fixed seed** (e.g., 7) for reproducibility.
- **max_tokens=800** was sufficient for our safety critique output schema.
- **Video input**: The model accepts video via URL or base64 data URI. Local files are converted to `data:video/mp4;base64,...` before sending.

### JSON Parsing Robustness
The model sometimes produces slightly malformed JSON (e.g., missing commas between adjacent string keys). Build a JSON repair layer:
- Strip markdown code fences if present
- Find the first `{...}` block in the response
- Attempt repair for common issues (missing commas, trailing commas)
- Retry up to 2 times on parse failure

### Verdict Calibration
Raw model verdicts need post-processing calibration. The model tends to over-escalate (calling things "fail" that are really "at_risk"). We built heuristic escalation/de-escalation rules based on severity scores and compliance sub-scores to align with ground truth labels.

---

## 7. Project Architecture Lessons

### Zero External Dependencies
Our entire CLI (`safefloor`) runs on Python 3.11+ stdlib only. No pip install of torch, transformers, etc. for the core pipeline. This made it trivially reproducible for judges.

### Config Precedence
`CLI args → .env file → environment variables → defaults`. Use a `CriticConfig` dataclass that loads from all sources.

### Separate Concerns
- **client.py**: Thin HTTP wrapper to `/v1/chat/completions` (nothing else)
- **pipeline.py**: Prompt building, response parsing, calibration
- **schema.py**: Output validation
- **cli.py**: Argument parsing and dispatch

### Test Everything Offline
All 153 tests run without a live endpoint. Mock the HTTP layer. This saved us when the VM was down.

---

## 8. What We'd Do Differently

1. **Pin a static IP on day one.** The volatile IP caused more wasted hours than any other issue.
2. **Write the session-start SOP on day one** and run it mechanically every session. We wrote it on day 3 after losing time twice.
3. **Don't fight the reasoning parser.** If the managed deployment doesn't expose `--reasoning-parser`, design around it immediately. We spent hours trying to get native `reasoning_content` working when the JSON-field workaround was always available.
4. **Budget tracking.** We never hit a credit limit, but we also never tracked burn rate systematically. At $2.95/hr an H100 left running overnight costs $70.
5. **Cache model responses aggressively.** During prompt iteration, re-running the same clips through the endpoint is slow and wasteful. Save raw responses to disk and replay them locally.
6. **Keep credentials out of chat/logs.** We accidentally pasted API keys in debug output twice. Rotate immediately if this happens.

---

## 9. Key File Patterns for a New Project

If building a similar Cosmos Reason2 project from scratch, you'll want:

```
.env.example          # Template with all env vars (no secrets)
.env                  # Actual secrets (gitignored)
docs/RUNBOOK.md       # Session-start SOP + full execution commands
docs/SETUP_NEBIUS_CLI.md  # SSH/CLI setup instructions
docs/STATUS.md        # Living doc: access evidence, eval evidence, blockers
scripts/check_nebius_access.ps1  # Automated SSH + endpoint + GPU check
src/<pkg>/config.py   # CriticConfig with .env + env var + CLI arg loading
src/<pkg>/client.py   # Thin OpenAI-compatible HTTP client
```

---

## 10. Useful Commands Reference

### PowerShell (Local Windows)
```powershell
# SSH to Nebius VM
ssh -i $env:USERPROFILE\.ssh\id_ed25519 sgdev@<ip> "hostname && whoami"

# Check GPU on remote
ssh -i $env:USERPROFILE\.ssh\id_ed25519 sgdev@<ip> "nvidia-smi --query-gpu=name,memory.total --format=csv,noheader"

# Test endpoint reachability
Test-NetConnection <ip> -Port 8000

# List models
$h = @{"Authorization" = "Bearer $env:NEBIUS_VLLM_API_KEY"}
Invoke-RestMethod -Uri "http://<ip>:8000/v1/models" -Headers $h

# Quick chat completion
$body = @{model="nvidia/Cosmos-Reason2-8B"; messages=@(@{role="user"; content="Describe this scene."}); max_tokens=100} | ConvertTo-Json -Depth 5
Invoke-RestMethod -Method Post -Uri "http://<ip>:8000/v1/chat/completions" -Headers $h -Body $body -ContentType "application/json"
```

### WSL / Linux
```bash
# Nebius CLI auth
nebius auth login --profile <profile_name>

# vLLM startup with reasoning parser (if you control the server)
python3 -m vllm.entrypoints.openai.api_server \
  --model nvidia/Cosmos-Reason2-8B \
  --host 0.0.0.0 --port 8000 \
  --reasoning-parser qwen3
```

---

## 11. Links & References

| Resource | URL |
|----------|-----|
| Nebius Console | https://console.nebius.com |
| Cosmos Reason2 repo | https://github.com/nvidia-cosmos/cosmos-reason2 |
| Cosmos Cookbook | https://nvidia-cosmos.github.io/cosmos-cookbook/recipes/all_recipes.html |
| Cookoff submission template | https://github.com/nvidia-cosmos/cosmos-cookbook/issues |
| Competition discussion | https://github.com/orgs/nvidia-cosmos/discussions/4 |
| vLLM docs (reasoning parsers) | https://docs.vllm.ai |
| SmartSpaces dataset (HuggingFace) | nvidia/PhysicalAI-SmartSpaces on HF |
