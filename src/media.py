from __future__ import annotations

import base64
import mimetypes
from pathlib import Path


def file_to_data_uri(path: str) -> str:
    p = Path(path)
    data = p.read_bytes()
    mime, _ = mimetypes.guess_type(p.name)
    if mime is None:
        # vLLM accepts data URIs; default to mp4 since that's our expected format.
        mime = "video/mp4"
    b64 = base64.b64encode(data).decode("ascii")
    return f"data:{mime};base64,{b64}"


def is_probably_url(s: str) -> bool:
    return s.startswith("http://") or s.startswith("https://") or s.startswith("data:")
