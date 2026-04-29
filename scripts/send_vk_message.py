#!/usr/bin/env python3
"""Send a single VK message using a user access token."""

from __future__ import annotations

import argparse
import json
import logging
import secrets
import sys
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


API_URL = "https://api.vk.com/method/messages.send"
API_VERSION = "5.199"
TIMEOUT_SECONDS = 20
LOGGER = logging.getLogger("send_vk_message")


class VkApiError(RuntimeError):
    """Raised when VK API returns a structured error response."""


@dataclass(frozen=True)
class VkError:
    code: int
    message: str


def configure_logging(verbose: bool) -> None:
    configure_stdio()
    level = logging.DEBUG if verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    LOGGER.setLevel(level)


def configure_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8", errors="replace")


def parse_recipient_id(raw_recipient_id: str) -> int:
    value = raw_recipient_id.strip()
    if value.lower().startswith("id"):
        value = value[2:]

    if not value.isdigit():
        raise ValueError(
            "recipient_id must be a numeric VK user id, for example 312038444 or id312038444"
        )

    recipient_id = int(value)
    if recipient_id <= 0:
        raise ValueError("recipient_id must be greater than zero")

    return recipient_id


def build_payload(token: str, user_id: int, message: str) -> dict[str, str | int]:
    random_id = secrets.randbelow(2_147_483_647)
    return {
        "access_token": token,
        "v": API_VERSION,
        "user_id": user_id,
        "message": message,
        "random_id": random_id,
    }


def post_vk_message(payload: dict[str, str | int]) -> int:
    body = urlencode(payload).encode("utf-8")
    request = Request(
        API_URL,
        data=body,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "onboarding-vk-message-script/1.0",
        },
        method="POST",
    )

    try:
        with urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            raw_body = response.read().decode("utf-8")
    except HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} from VK API: {details}") from exc
    except URLError as exc:
        raise RuntimeError(f"Network error while calling VK API: {exc.reason}") from exc

    LOGGER.debug("VK API raw response: %s", raw_body)
    decoded = parse_json_response(raw_body)

    if "error" in decoded:
        error = parse_vk_error(decoded["error"])
        raise VkApiError(f"VK API error {error.code}: {error.message}")

    response_value = decoded.get("response")
    if not isinstance(response_value, int):
        raise RuntimeError(f"Unexpected VK API response shape: {decoded}")

    return response_value


def parse_json_response(raw_body: str) -> dict[str, Any]:
    try:
        decoded = json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"VK API returned invalid JSON: {raw_body}") from exc

    if not isinstance(decoded, dict):
        raise RuntimeError(f"VK API returned non-object JSON: {decoded}")

    return decoded


def parse_vk_error(raw_error: Any) -> VkError:
    if not isinstance(raw_error, dict):
        return VkError(code=-1, message=str(raw_error))

    code = raw_error.get("error_code", -1)
    message = raw_error.get("error_msg", "Unknown VK API error")

    return VkError(code=int(code), message=str(message))


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Send a single VK message to a user from the account behind the access token."
    )
    parser.add_argument("token", help="Full VK user access token.")
    parser.add_argument(
        "recipient_id",
        help="VK recipient user id, for example 312038444 or id312038444.",
    )
    parser.add_argument("message", help="Message text to send.")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print extra diagnostics, including the raw VK API response.",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    configure_logging(args.verbose)

    try:
        user_id = parse_recipient_id(args.recipient_id)
        payload = build_payload(args.token, user_id, args.message)

        LOGGER.debug("Sending VK message to user_id=%s", user_id)
        message_id = post_vk_message(payload)
    except (ValueError, VkApiError, RuntimeError) as exc:
        LOGGER.error("❌ Сообщение VK не отправлено: %s", exc)
        return 1

    if args.verbose:
        LOGGER.info("VK message_id=%s", message_id)
    print("✅ Сообщение VK отправлено")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
