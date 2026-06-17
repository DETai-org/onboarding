from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


FORBIDDEN_PATTERNS: tuple[tuple[str, str], ...] = (
    ("browser_runtime", r"\bbrowser_runtime\b"),
    ("codex_iab", r"\bcodex_iab\b"),
    ("web_warming", r"\bweb_warming\b"),
    ("friend_warming", r"\bfriend_warming\b"),
    ("warming_import", r"(?:from|import)\s+.*\bwarming\b"),
    ("warming_state", r"\bWarmingStateStore\b|\bWarmup"),
    ("browser_action", r"\bBrowserAction\b|\bexecute_safe_browser_action\b"),
    ("browser_await", r"\bawaiting_browser_runtime\b"),
    ("story_api", r"\bstories\.get\b|\bstory_bonus\b|\blike_story\b|\bview_story\b|\bactive_stories\b"),
    ("runtime_ai_generation", r"\bActivityAIConnector\b|\bPromptLayer\b|\bAI follow-up\b|\[activity\.ai\]"),
    (
        "template_message_runner",
        r"\bgenerate_message_plan\b|\bHelloy\.json\b|\bmessage_engine\b|from\s+\.*activity\.core\.runner|python\s+-m\s+VK\.auto_funnel\.activity\.core\.runner",
    ),
)

SKIP_DIRS = {
    ".git",
    ".pytest_cache",
    "__pycache__",
    "state",
    "logs",
    "statistics",
    ".venv",
    "node_modules",
}
TEXT_SUFFIXES = {
    ".py",
    ".toml",
    ".md",
    ".txt",
    ".json",
    ".jsonl",
    ".yaml",
    ".yml",
    ".mjs",
    ".js",
    ".sh",
}


def iter_text_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        yield path


def scan(project_root: Path) -> dict[str, object]:
    root = project_root.resolve()
    findings: list[dict[str, object]] = []
    compiled = [(name, re.compile(pattern)) for name, pattern in FORBIDDEN_PATTERNS]
    for path in iter_text_files(root):
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        for line_no, line in enumerate(lines, start=1):
            for name, pattern in compiled:
                if pattern.search(line):
                    findings.append(
                        {
                            "kind": name,
                            "path": str(path.relative_to(root)),
                            "line": line_no,
                            "text": line.strip()[:240],
                        }
                    )
    return {
        "project_root": str(root),
        "passed": not findings,
        "finding_count": len(findings),
        "findings": findings,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = scan(Path(args.project_root))
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(
            f"api_direct_dead_path_scan passed={result['passed']} "
            f"findings={result['finding_count']}"
        )
        for item in result["findings"]:
            print(f"{item['path']}:{item['line']} [{item['kind']}] {item['text']}")
    if not result["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
