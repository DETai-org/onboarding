#!/usr/bin/env python3
"""Send one Telegram message from a Pyrogram user session.

Usage:
    python3 send_telegram_message.py <session_name> <recipient_id> <message>

The script is intended to live in:
    /home/psy-ru/DETai-org/onboarding/scripts

It finds Telegram sessions in the sibling projects repository:
    /home/psy-ru/DETai-org/projects/Telegram/UserControl/session_file
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import sqlite3
import sys
from pathlib import Path
from typing import Any

TIMEOUT_SECONDS = 30
SESSION_RELATIVE_DIR = Path("Telegram") / "UserControl" / "session_file"
LOGGER = logging.getLogger("send_telegram_message")


class TelegramMessageError(RuntimeError):
    """Raised when a message cannot be sent."""


def configure_logging(verbose: bool) -> None:
    configure_stdio()
    level = logging.INFO if verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    LOGGER.setLevel(level)

    # Pyrogram is very chatty when root logging is DEBUG/INFO. Keep Make output
    # compact and reserve transport details for explicit debugging in code.
    for logger_name in (
        "pyrogram",
        "pyrogram.connection",
        "pyrogram.session",
        "pyrogram.dispatcher",
    ):
        logging.getLogger(logger_name).setLevel(logging.ERROR)


def configure_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8", errors="replace")


def detect_projects_root() -> Path:
    # scripts/ -> onboarding/ -> DETai-org/ -> projects/
    return Path(__file__).resolve().parents[2] / "projects"


def normalize_session_name(raw_name: str) -> str:
    name = raw_name.strip()
    if not name:
        raise ValueError("session_name must not be empty")
    if name.endswith(".session"):
        name = name[: -len(".session")]
    if any(separator in name for separator in ("/", "\\")):
        raise ValueError("session_name must be a file name, not a path")
    return name


def unique_paths(paths: list[Path]) -> list[Path]:
    seen: set[str] = set()
    result: list[Path] = []
    for path in paths:
        try:
            key = str(path.expanduser().resolve())
        except OSError:
            key = str(path.expanduser())
        if key not in seen:
            seen.add(key)
            result.append(path.expanduser())
    return result


def candidate_session_dirs(projects_root: Path, explicit_session_dir: Path | None) -> list[Path]:
    script_path = Path(__file__).resolve()
    onboarding_root = script_path.parents[1]
    org_root = script_path.parents[2]

    paths: list[Path] = []
    if explicit_session_dir is not None:
        paths.append(explicit_session_dir)

    env_session_dir = os.getenv("TELEGRAM_SESSION_DIR")
    if env_session_dir:
        paths.append(Path(env_session_dir))

    paths.extend(
        [
            projects_root / SESSION_RELATIVE_DIR,
            org_root / "projects" / SESSION_RELATIVE_DIR,
            onboarding_root / "projects" / SESSION_RELATIVE_DIR,
            onboarding_root / SESSION_RELATIVE_DIR,
            Path.cwd() / SESSION_RELATIVE_DIR,
        ]
    )
    return unique_paths(paths)


def list_sessions(session_dir: Path) -> list[str]:
    try:
        return sorted(path.name for path in session_dir.glob("*.session"))
    except OSError:
        return []


def find_case_insensitive(session_dir: Path, session_name: str) -> Path | None:
    wanted = f"{session_name}.session".lower()
    for path in session_dir.glob("*.session"):
        if path.name.lower() == wanted:
            return path
    return None


def search_session_file(search_root: Path, session_name: str) -> Path | None:
    if not search_root.exists():
        return None

    wanted = f"{session_name}.session"
    wanted_lower = wanted.lower()
    try:
        for path in search_root.rglob("*.session"):
            if path.name == wanted or path.name.lower() == wanted_lower:
                if path.parent.name == "session_file":
                    return path
    except OSError:
        return None
    return None


def read_session_api_id(session_file: Path) -> int | None:
    try:
        with sqlite3.connect(session_file) as connection:
            row = connection.execute("SELECT api_id FROM sessions LIMIT 1").fetchone()
    except sqlite3.Error:
        return None

    if not row or row[0] in (None, 0):
        return None
    try:
        return int(row[0])
    except (TypeError, ValueError):
        return None


def load_env_api_credentials() -> dict[str, int | str]:
    api_id = os.getenv("TG_API_ID") or os.getenv("API_ID")
    api_hash = os.getenv("TG_API_HASH") or os.getenv("API_HASH")
    if not api_id and not api_hash:
        return {}
    if not api_id or not api_hash:
        raise TelegramMessageError(
            "Both TG_API_ID and TG_API_HASH must be set when API credentials are provided."
        )
    return {"api_id": int(api_id), "api_hash": api_hash}


def resolve_session_file(
    session_name: str,
    projects_root: Path,
    explicit_session_dir: Path | None,
) -> Path:
    attempted: list[str] = []
    for session_dir in candidate_session_dirs(projects_root, explicit_session_dir):
        session_dir = session_dir.resolve()
        session_file = session_dir / f"{session_name}.session"
        sessions = list_sessions(session_dir) if session_dir.exists() else []
        attempted.append(
            f"- {session_dir} | exists={session_dir.exists()} | sessions={sessions[:20]}"
        )

        if session_file.exists():
            return session_file

        if session_dir.exists():
            case_match = find_case_insensitive(session_dir, session_name)
            if case_match is not None:
                LOGGER.info("Using case-insensitive session match: %s", case_match)
                return case_match

    script_path = Path(__file__).resolve()
    search_roots = unique_paths(
        [
            projects_root,
            script_path.parents[2],
            script_path.parents[1],
            Path.cwd(),
        ]
    )
    for root in search_roots:
        found = search_session_file(root.resolve(), session_name)
        if found is not None:
            LOGGER.info("Found session by fallback search: %s", found)
            return found

    details = "\n".join(attempted)
    raise TelegramMessageError(
        "Session file was not found.\n"
        f"Expected session name: {session_name}.session\n"
        "Checked session directories:\n"
        f"{details}\n"
        "You can force the directory with --session-dir /path/to/session_file "
        "or TELEGRAM_SESSION_DIR=/path/to/session_file."
    )


def parse_recipient(raw_recipient: str) -> int | str:
    value = raw_recipient.strip()
    if not value:
        raise ValueError("recipient_id must not be empty")

    signless = value[1:] if value.startswith("-") else value
    if signless.isdigit():
        return int(value)

    # Pyrogram also accepts @username strings. This keeps the script usable when
    # Telegram exposes a username instead of a numeric user id.
    return value


def phone_candidates(raw_recipient: str) -> list[str]:
    digits = "".join(ch for ch in raw_recipient if ch.isdigit())
    if len(digits) < 10:
        return []

    candidates: list[str] = []
    if raw_recipient.strip().startswith("+"):
        candidates.append("+" + digits)
    else:
        candidates.extend([digits, "+" + digits])

    if len(digits) == 10:
        candidates.append("+7" + digits)
    elif len(digits) == 11 and digits.startswith("8"):
        candidates.append("+7" + digits[1:])

    seen: set[str] = set()
    result: list[str] = []
    for candidate in candidates:
        if candidate not in seen:
            seen.add(candidate)
            result.append(candidate)
    return result


async def try_send_by_imported_phone(
    client: Any,
    raw_recipient: str,
    message: str,
) -> Any | None:
    try:
        from pyrogram.types import InputPhoneContact
    except ModuleNotFoundError:
        return None

    candidates = phone_candidates(raw_recipient)
    if not candidates:
        return None

    for phone in candidates:
        LOGGER.info("Trying recipient as phone contact: %s", phone)
        try:
            imported_users = await asyncio.wait_for(
                client.import_contacts(
                    [InputPhoneContact(phone=phone, first_name="Telegram", last_name="User")]
                ),
                timeout=TIMEOUT_SECONDS,
            )
        except Exception as exc:
            LOGGER.info("Contact import failed for %s: %s", phone, exc)
            continue

        if not imported_users:
            LOGGER.info("Telegram returned no imported user for phone %s", phone)
            continue

        user = imported_users[0]
        LOGGER.info(
            "Imported contact resolved to user_id=%s username=%s",
            getattr(user, "id", None),
            getattr(user, "username", None),
        )
        return await asyncio.wait_for(
            client.send_message(user.id, message),
            timeout=TIMEOUT_SECONDS,
        )

    return None


async def send_with_fallbacks(
    client: Any,
    recipient: int | str,
    raw_recipient: str,
    message: str,
) -> Any:
    try:
        return await asyncio.wait_for(
            client.send_message(recipient, message),
            timeout=TIMEOUT_SECONDS,
        )
    except Exception as exc:
        error_text = str(exc)
        if "PEER_ID_INVALID" not in error_text:
            raise

        LOGGER.info(
            "Telegram does not know peer_id=%s for this session. "
            "Trying phone-contact fallback.",
            raw_recipient,
        )
        sent = await try_send_by_imported_phone(client, raw_recipient, message)
        if sent is not None:
            return sent
        raise TelegramMessageError(
            "Telegram cannot resolve this recipient for the selected session. "
            "Use @username, a phone number visible/importable by this account, "
            "or make this account open a dialog with the user first. "
            f"Original error: {exc}"
        ) from exc


async def send_telegram_message(
    *,
    session_name: str,
    recipient: int | str,
    raw_recipient: str,
    message: str,
    projects_root: Path,
    explicit_session_dir: Path | None,
) -> None:
    session_file = resolve_session_file(
        session_name=session_name,
        projects_root=projects_root,
        explicit_session_dir=explicit_session_dir,
    )
    session_dir = session_file.parent

    LOGGER.info("Using session file: %s", session_file)
    session_api_id = read_session_api_id(session_file)
    if session_api_id is not None:
        LOGGER.info("Session DB contains api_id=%s", session_api_id)
    LOGGER.info("Sending Telegram message to recipient=%s", recipient)

    try:
        from pyrogram import Client
    except ModuleNotFoundError as exc:
        raise TelegramMessageError(
            "Pyrogram is not installed. Install project dependencies on the server before sending."
        ) from exc

    client_kwargs = load_env_api_credentials()
    if client_kwargs:
        LOGGER.info("Using API credentials from environment variables")

    client = Client(name=session_file.stem, workdir=str(session_dir), **client_kwargs)

    try:
        await asyncio.wait_for(client.start(), timeout=TIMEOUT_SECONDS)
        me = await asyncio.wait_for(client.get_me(), timeout=TIMEOUT_SECONDS)
        LOGGER.info("Sending from Telegram account: %s", me.username or me.first_name)
        sent = await send_with_fallbacks(
            client=client,
            recipient=recipient,
            raw_recipient=raw_recipient,
            message=message,
        )
        LOGGER.info("Message sent successfully, message_id=%s", sent.id)
    except Exception as exc:
        raise TelegramMessageError(f"Failed to send Telegram message: {exc}") from exc
    finally:
        try:
            await asyncio.wait_for(client.stop(), timeout=TIMEOUT_SECONDS)
        except Exception:
            LOGGER.debug("Failed to stop Telegram client cleanly", exc_info=True)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Send a single Telegram message from an existing Pyrogram session."
    )
    parser.add_argument(
        "session_name",
        help="Session file name from Telegram/UserControl/session_file, with or without .session.",
    )
    parser.add_argument(
        "recipient_id",
        help="Telegram recipient user id. @username is also accepted by Pyrogram.",
    )
    parser.add_argument("message", help="Message text to send.")
    parser.add_argument(
        "--projects-root",
        type=Path,
        default=detect_projects_root(),
        help="Path to the projects repository. Defaults to ../projects from DETai-org.",
    )
    parser.add_argument(
        "--session-dir",
        type=Path,
        default=None,
        help="Explicit path to Telegram/UserControl/session_file.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print extra diagnostics.",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    configure_logging(args.verbose)

    try:
        session_name = normalize_session_name(args.session_name)
        recipient = parse_recipient(args.recipient_id)
        projects_root = args.projects_root.expanduser().resolve()
        explicit_session_dir = (
            args.session_dir.expanduser().resolve() if args.session_dir else None
        )
        asyncio.run(
            send_telegram_message(
                session_name=session_name,
                recipient=recipient,
                raw_recipient=args.recipient_id,
                message=args.message,
                projects_root=projects_root,
                explicit_session_dir=explicit_session_dir,
            )
        )
    except (ValueError, TelegramMessageError) as exc:
        LOGGER.error("❌ Сообщение не отправлено: %s", exc)
        return 1

    print("✅ Сообщение отправлено")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
