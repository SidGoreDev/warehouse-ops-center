from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests

from .config import AppConfig


@dataclass(frozen=True)
class ChatResponse:
    content_text: str
    raw: Dict[str, Any]


class NebiusVllmClient:
    def __init__(self, cfg: AppConfig) -> None:
        self._cfg = cfg
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Authorization": f"Bearer {cfg.api_key}",
                "Content-Type": "application/json",
            }
        )

    def list_models(self) -> Dict[str, Any]:
        url = f"{self._cfg.base_url}/v1/models"
        r = self._session.get(url, timeout=self._cfg.timeout_s)
        r.raise_for_status()
        return r.json()

    def mm_processor_kwargs(self) -> Dict[str, Any]:
        return {"fps": self._cfg.mm_fps, "do_sample_frames": self._cfg.mm_do_sample_frames}

    def chat_completions(
        self,
        *,
        messages: List[Dict[str, Any]],
        max_tokens: Optional[int] = None,
        extra_body: Optional[Dict[str, Any]] = None,
    ) -> ChatResponse:
        url = f"{self._cfg.base_url}/v1/chat/completions"

        body: Dict[str, Any] = {
            "model": self._cfg.model,
            "messages": messages,
            "temperature": self._cfg.temperature,
            "top_p": self._cfg.top_p,
            "top_k": self._cfg.top_k,
            "presence_penalty": self._cfg.presence_penalty,
            "repetition_penalty": self._cfg.repetition_penalty,
            "max_tokens": max_tokens if max_tokens is not None else self._cfg.max_tokens,
        }
        if extra_body:
            body.update(extra_body)
        if self._cfg.seed is not None:
            body["seed"] = self._cfg.seed

        r = self._session.post(url, json=body, timeout=self._cfg.timeout_s)
        r.raise_for_status()
        raw = r.json()

        # vLLM OpenAI-compatible responses typically return a string in message.content
        try:
            content = raw["choices"][0]["message"]["content"]
        except Exception as e:  # noqa: BLE001
            raise RuntimeError(f"Unexpected vLLM response shape: {raw}") from e

        if not isinstance(content, str):
            # Some APIs return structured content; we only support string for now.
            content = str(content)

        return ChatResponse(content_text=content, raw=raw)


def build_messages_for_video(*, prompt_text: str, video_url: str) -> List[Dict[str, Any]]:
    # Matches NVIDIA reason guide: media-first ordering in user.content.
    return [
        {
            "role": "system",
            "content": "You are a helpful assistant.",
        },
        {
            "role": "user",
            "content": [
                {"type": "video_url", "video_url": {"url": video_url}},
                {"type": "text", "text": prompt_text},
            ],
        },
    ]


def build_messages_text_only(*, prompt_text: str) -> List[Dict[str, Any]]:
    return [
        {
            "role": "system",
            "content": "You are a helpful assistant.",
        },
        {
            "role": "user",
            "content": prompt_text,
        },
    ]
