# MEVA KF1 — Minimal Download Strategy (No 300GB)

This repo uses a *curated subset* of MEVA KF1 (5-minute clips) and trims them locally into short MP4s for CR2 inference.

We avoid `aws s3 sync` entirely. Instead we:
1. List hour-level keys via the public S3 ListObjectsV2 API (no AWS CLI needed).
2. Select `N` clips per camera for an hour prefix.
3. Download only those files via `curl.exe`.

## 0) Browse Prefixes

List top-level facilities:

```powershell
python scripts/meva_s3.py ls --s3-uri s3://mevadata-public-01/drops-123-r13/ --delimiter --max-keys 200
```

Then drill down (repeat with the prefix you find):

```powershell
python scripts/meva_s3.py ls --s3-uri s3://mevadata-public-01/drops-123-r13/<facility>/ --delimiter --max-keys 200
python scripts/meva_s3.py ls --s3-uri s3://mevadata-public-01/drops-123-r13/<facility>/<date>/ --delimiter --max-keys 200
python scripts/meva_s3.py ls --s3-uri s3://mevadata-public-01/drops-123-r13/<facility>/<date>/<hour>/ --max-keys 200
```

You want an *hour prefix* that returns a list of `.avi` clip objects.

## 1) Generate a Small Download Plan

Pick 2-4 camera IDs you want for a multi-camera scenario (example: `G328,G329,G330`), and select 2-6 clips per camera.

```powershell
python scripts/meva_s3.py plan `
  --hour-prefix-s3 s3://mevadata-public-01/drops-123-r13/<facility>/<date>/<hour>/ `
  --cameras G328,G329,G330 `
  --per-camera 3
```

This writes:
- `data/meva/meva_selected_keys.txt` (selected S3 keys)
- `scripts/download_meva_selected.ps1` (downloads those keys to `data/meva/raw/`)

## 2) Download

```powershell
powershell -File scripts/download_meva_selected.ps1 -OutDir data\\meva\\raw
```

## 3) Trim/Transcode To Short MP4s (Recommended)

Trim the first 20 seconds of each downloaded clip into `data/videos/`:

```powershell
powershell -File scripts/meva_quick_trim.ps1 -InDir data\\meva\\raw -OutDir data\\videos -Seconds 20
```

Then run inference via:

```powershell
python -m src.cli analyze --mode timeline --video data\\videos\\<trimmed>.mp4 --force
```

