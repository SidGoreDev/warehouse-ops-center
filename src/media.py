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


def video_arg_to_video_url(video: str, *, embed: bool) -> str:
    """
    Convert a CLI `--video` argument into a `video_url` payload.

    If `embed=False` and `video` is a local path, return a placeholder data URI
    to avoid dumping multi-MB base64 into terminals/logs.
    """
    if is_probably_url(video):
        return video
    if embed:
        return file_to_data_uri(video)
    return "data:video/mp4;base64,<omitted>"
