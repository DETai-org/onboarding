"""Sender-scoped, best-effort DETai Runtime first-/start telemetry.

The authenticated Runtime credential defines bot_id. A real Telegram /start
records contact and bot_started; no opt-in, redirects or separate contact DB.
"""
from __future__ import annotations

import asyncio
from datetime import timezone
import json
import logging
import os
import re
from urllib.parse import urlparse
from urllib.request import Request, ProxyHandler, HTTPRedirectHandler, build_opener
from uuid import NAMESPACE_URL, uuid5

_LOG = logging.getLogger(__name__)
_LANGUAGES = frozenset({"ru", "en", "de", "fi", "zh"})


def normalize_locale(value: str | None) -> str:
    first = (value or "").lower().replace("_", "-").split("-")[0]
    return first if first in _LANGUAGES else "en"


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def _post(route: str, payload: dict[str, object]) -> dict[str, object]:
    base = os.getenv("ECOSYSTEM_NOTIFICATIONS_URL", "").rstrip("/")
    token = os.getenv("ECOSYSTEM_NOTIFICATIONS_TOKEN", "")
    if not base or not token:
        raise RuntimeError("notifications_unconfigured")
    parsed = urlparse(base)
    if parsed.scheme != "https" and not (
        parsed.scheme == "http" and parsed.hostname in {"127.0.0.1", "::1", "localhost"}
    ):
        raise ValueError("Runtime Notifications requires HTTPS or loopback HTTP")
    if parsed.query or parsed.fragment or parsed.username or parsed.password:
        raise ValueError("Invalid Runtime Notifications endpoint")
    request = Request(
        base + "/v1/notifications/" + route,
        method="POST",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"},
    )
    with build_opener(ProxyHandler({}), _NoRedirect()).open(request, timeout=3) as response:
        result = json.load(response)
    if not isinstance(result, dict) or result.get("contractVersion") != "detai.engagement/v1":
        raise ValueError("Unexpected Runtime Notifications response")
    return result


async def _record_event(message, bot_id: str, locale: str) -> None:
    user = message.from_user
    if user is None:
        return
    when = message.date
    when = when.replace(tzinfo=timezone.utc) if when.tzinfo is None else when
    payload = {
        "contractVersion": "detai.engagement/v1",
        "id": str(uuid5(NAMESPACE_URL, f"{bot_id}:bot_started:{user.id}:{message.message_id}")),
        "kind": "bot_started",
        "telegramUserId": str(user.id),
        "locale": locale,
        "occurredAt": when.astimezone(timezone.utc).isoformat(),
    }
    try:
        result = await asyncio.to_thread(_post, "events", payload)
        if result.get("accepted") is not True:
            raise ValueError("Runtime refused bot_started")
    except Exception as exc:
        _LOG.warning("First-start observation failed for %s (%s)", bot_id, type(exc).__name__)


async def observe_start(message, bot_id: str) -> str:
    """Observe only a private /start; the caller controls greeting and ACL.

    Return Hub-preferred locale when available, otherwise Telegram locale.
    Telemetry transport failures must never prevent a visitor's greeting.
    """
    user = message.from_user
    fallback = normalize_locale(user.language_code if user else None)
    if (user is None or message.chat.type != "private" or
            not os.getenv("ECOSYSTEM_NOTIFICATIONS_URL") or
            not os.getenv("ECOSYSTEM_NOTIFICATIONS_TOKEN")):
        return fallback
    username = user.username if user.username and re.fullmatch(r"[A-Za-z0-9_]{1,32}", user.username) else None
    name = "".join(c for c in (user.first_name or "") if ord(c) >= 32 and ord(c) != 127)[:120] or None
    contact = {
        "contractVersion": "detai.engagement/v1",
        "telegramUserId": str(user.id),
        "locale": fallback,
        "interaction": True,
        "telegramUsername": username,
        "telegramFirstName": name,
    }
    locale = fallback
    try:
        response = await asyncio.to_thread(_post, "contact", contact)
        locale = normalize_locale(response.get("locale") or fallback)
    except Exception as exc:
        _LOG.warning("Contact observation failed for %s (%s)", bot_id, type(exc).__name__)
    asyncio.create_task(_record_event(message, bot_id, locale))
    return locale
