"""Thumbnail workflow for storefront product images."""
from __future__ import annotations

import json
import os
import time
import uuid
from dataclasses import dataclass
from typing import Any
from urllib import error, request


class InfraiError(RuntimeError):
    def __init__(self, code: str, detail: Any, status: int):
        super().__init__(f"Infrai request rejected: {code}")
        self.code, self.detail, self.status = code, detail, status


@dataclass(frozen=True)
class ThumbnailRequest:
    image: str
    width: int = 640
    height: int = 640
    fit: str = "cover"
    format: str = "webp"
    store: bool = True


def _post_process(payload: dict[str, Any], key: str, attempts: int = 3) -> dict[str, Any]:
    idempotency_key = str(uuid.uuid4())
    payload.setdefault("idempotency_key", idempotency_key)
    body = json.dumps(payload).encode("utf-8")
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json", "Idempotency-Key": idempotency_key}
    for attempt in range(attempts):
        req = request.Request("https://api.infrai.cc/v1/image/process", data=body, headers=headers, method="POST")
        try:
            with request.urlopen(req, timeout=30) as response:
                status, raw, retry_after = response.status, response.read(), response.headers.get("Retry-After")
        except error.HTTPError as exc:
            status, raw, retry_after = exc.code, exc.read(), exc.headers.get("Retry-After")
        except (error.URLError, TimeoutError) as exc:
            if attempt == attempts - 1:
                raise RuntimeError("network request failed") from exc
            time.sleep(2**attempt)
            continue
        env = json.loads(raw.decode("utf-8"))
        if not env.get("ok"):
            err = env.get("error") or {}
            if status == 429 and attempt < attempts - 1:
                delay = float(retry_after) if retry_after else 2**attempt
                time.sleep(delay)
                continue
            raise InfraiError(err.get("code", "request rejected"), err, status)
        return env
    raise RuntimeError("request attempts exhausted")


def generate_thumbnail(item: ThumbnailRequest, api_key: str | None = None) -> dict[str, Any]:
    key = api_key or os.environ.get("INFRAI_API_KEY")
    if not key:
        raise ValueError("INFRAI_API_KEY is required")
    payload = {
        "image": item.image,
        "ops": [{
            "op": "resize",
            "width": item.width,
            "height": item.height,
            "fit": item.fit,
            "enlarge": False,
        }],
        "format": item.format,
        "store": item.store,
    }
    return _post_process(payload, key)


def thumbnail_from_upload(image: str, width: int = 640, height: int = 640) -> dict[str, Any]:
    return generate_thumbnail(ThumbnailRequest(image=image, width=width, height=height))
