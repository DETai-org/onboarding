from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping


REQUIRED_FIELDS = {
    "cycle_id",
    "based_on_run_id",
    "accounts",
    "config_changes",
    "plan_changes",
    "prepared_message_count",
    "prepared_inbound_reply_count",
    "planned_first_message_count",
    "profile_kpis",
    "candidate_replenishment",
    "cross_profile_dedup",
    "social_life_changes",
    "generated_social_assets",
    "community_discovery",
    "api_call_ledger",
    "account_safety_actions",
    "skipped_repeat_count",
    "strongest_next_ideas",
    "trust_progression_note",
}


def _load_payload(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, Mapping):
        raise SystemExit("payload must be a JSON object")
    normalized = dict(payload)
    missing = sorted(field for field in REQUIRED_FIELDS if field not in normalized)
    if missing:
        raise SystemExit(f"payload missing required fields: {', '.join(missing)}")
    return normalized


def _safe_date(value: object) -> str:
    if isinstance(value, str) and value.strip():
        token = value.strip()
        try:
            return datetime.fromisoformat(token).date().isoformat()
        except ValueError:
            return token[:10]
    return datetime.now(timezone.utc).date().isoformat()


def record_change(project_root: Path, payload: Mapping[str, Any]) -> dict[str, str]:
    root = project_root.resolve()
    target_root = root / "state" / "continuous_improvement" / "autofunnel-api-director"
    changes_dir = target_root / "changes"
    changes_dir.mkdir(parents=True, exist_ok=True)

    normalized = dict(payload)
    normalized.setdefault("changed_at", datetime.now(timezone.utc).isoformat())
    normalized.setdefault("code_cleanup", [])
    normalized.setdefault("skill_self_updates", [])
    normalized.setdefault("verification", [])
    normalized.setdefault("dead_path_notes", [])
    normalized.setdefault("candidate_replenishment", [])
    normalized.setdefault("cross_profile_dedup", {"checked": False})
    normalized.setdefault("social_life_changes", [])
    normalized.setdefault("generated_social_assets", [])
    normalized.setdefault("community_discovery", [])
    normalized.setdefault("api_call_ledger", {})
    normalized.setdefault("account_safety_actions", [])
    date_key = _safe_date(normalized.get("changed_at"))

    changes_path = changes_dir / f"{date_key}.jsonl"
    with changes_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(normalized, ensure_ascii=False, sort_keys=True) + "\n")

    latest_path = target_root / "latest.json"
    latest_path.write_text(
        json.dumps(normalized, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return {
        "changes_path": str(changes_path),
        "latest_path": str(latest_path),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--payload", required=True)
    args = parser.parse_args()

    result = record_change(Path(args.project_root), _load_payload(Path(args.payload)))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
