from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Optional

from dotenv import load_dotenv


def _get_env(name: str, default: Optional[str] = None) -> Optional[str]:
    v = os.getenv(name)
    if v is None or v == "":
        return default
    return v


def _get_float(name: str, default: float) -> float:
    v = _get_env(name)
    if v is None:
        return default
    return float(v)


def _get_int(name: str, default: int) -> int:
    v = _get_env(name)
    if v is None:
        return default
    return int(v)


@dataclass(frozen=True)
class AppConfig:
    # Endpoint + auth
    base_url: str
    api_key: str
    model: str
    timeout_s: int

    # Sampling (NVIDIA reason guide defaults for reasoning-on)
    temperature: float = 0.6
    top_p: float = 0.95
    top_k: int = 20
    presence_penalty: float = 0.0
    repetition_penalty: float = 1.0
    max_tokens: int = 800

    # Optional
    seed: Optional[int] = None

    # Multimodal processor kwargs (per NVIDIA reason guide examples)
    mm_fps: int = 4
    mm_do_sample_frames: bool = True

    @staticmethod
    def load() -> "AppConfig":
        # CLI args are handled in cli.py. Here we implement env + .env.
        load_dotenv(override=False)

        base_url = (
            _get_env("NEBIUS_VLLM_BASE_URL")
            or _get_env("COSMOS_API_BASE")
            or ""
        )
        api_key = (
            _get_env("NEBIUS_VLLM_API_KEY")
            or _get_env("COSMOS_API_KEY")
            or ""
        )
        model = (
            _get_env("NEBIUS_VLLM_MODEL")
            or _get_env("COSMOS_MODEL")
            or "nvidia/Cosmos-Reason2-8B"
        )
        timeout_s = _get_int("NEBIUS_VLLM_TIMEOUT_S", 120)

        temperature = _get_float("NEBIUS_VLLM_TEMPERATURE", 0.6)
        top_p = _get_float("NEBIUS_VLLM_TOP_P", 0.95)
        top_k = _get_int("NEBIUS_VLLM_TOP_K", 20)
        presence_penalty = _get_float("NEBIUS_VLLM_PRESENCE_PENALTY", 0.0)
        repetition_penalty = _get_float("NEBIUS_VLLM_REPETITION_PENALTY", 1.0)
        max_tokens = _get_int("NEBIUS_VLLM_MAX_TOKENS", 800)

        seed_env = _get_env("NEBIUS_VLLM_SEED")
        seed = int(seed_env) if seed_env not in (None, "") else None

        mm_fps = _get_int("NEBIUS_VLLM_MM_FPS", 4)
        mm_do_sample_frames_env = (_get_env("NEBIUS_VLLM_DO_SAMPLE_FRAMES", "true") or "true").strip().lower()
        mm_do_sample_frames = mm_do_sample_frames_env in ("1", "true", "yes", "y", "on")

        if not base_url:
            raise RuntimeError("Missing NEBIUS_VLLM_BASE_URL (or COSMOS_API_BASE).")
        if not api_key:
            raise RuntimeError("Missing NEBIUS_VLLM_API_KEY (or COSMOS_API_KEY).")

        return AppConfig(
            base_url=base_url.rstrip("/"),
            api_key=api_key,
            model=model,
            timeout_s=timeout_s,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            presence_penalty=presence_penalty,
            repetition_penalty=repetition_penalty,
            max_tokens=max_tokens,
            seed=seed,
            mm_fps=mm_fps,
            mm_do_sample_frames=mm_do_sample_frames,
        )
