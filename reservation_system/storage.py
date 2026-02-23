"""JSON storage helpers for loading and saving lists of dictionaries."""
import json
from pathlib import Path
from typing import Any


def ensure_json_file(path: Path) -> None:
    """Create JSON file with empty list if it does not exist."""
    path.parent.mkdir(parents=True, exist_ok=True)

    if not path.exists():
        path.write_text("[]", encoding="utf-8")


def load_list(path: Path) -> list[dict[str, Any]]:
    """
    Load list from JSON file.

    Requirements handled:
    - File missing - create automatically
    - Empty file - return []
    - Invalid JSON - print error and continue
    """
    ensure_json_file(path)

    try:
        content = path.read_text(encoding="utf-8").strip()

        if not content:
            return []

        data = json.loads(content)

        if isinstance(data, list):
            return [item for item in data if isinstance(item, dict)]

        print(f"ERROR: Expected list in {path}")
        return []

    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR reading {path}: {exc}")
        return []


def save_list(path: Path, items: list[dict[str, Any]]) -> None:
    """Save list of dictionaries to JSON."""
    ensure_json_file(path)

    path.write_text(
        json.dumps(items, indent=2),
        encoding="utf-8",
    )
