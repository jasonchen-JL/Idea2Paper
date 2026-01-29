import json
import sys
from copy import deepcopy
from difflib import unified_diff
from pathlib import Path


DROP_KEYS = {
    "run_id",
    "created_at",
    "ts",
    "duration_ms",
    "latency_ms",
    "log_dir",
    "run_dir",
}


def _normalize(obj):
    if isinstance(obj, dict):
        normalized = {}
        for k, v in obj.items():
            if k in DROP_KEYS:
                continue
            normalized[k] = _normalize(v)
        return normalized
    if isinstance(obj, list):
        return [_normalize(x) for x in obj]
    return obj


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    if len(sys.argv) != 3:
        print("Usage: python compare_pipeline_result.py <base.json> <new.json>")
        sys.exit(1)

    base_path = Path(sys.argv[1])
    new_path = Path(sys.argv[2])

    base = _normalize(load_json(base_path))
    new = _normalize(load_json(new_path))

    base_text = json.dumps(base, ensure_ascii=False, sort_keys=True, indent=2)
    new_text = json.dumps(new, ensure_ascii=False, sort_keys=True, indent=2)

    if base_text == new_text:
        print("✅ No diffs after normalization.")
        return

    print("❌ Differences found:")
    for line in unified_diff(
        base_text.splitlines(),
        new_text.splitlines(),
        fromfile=str(base_path),
        tofile=str(new_path),
        lineterm=""
    ):
        print(line)


if __name__ == "__main__":
    main()
