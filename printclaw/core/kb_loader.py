from pathlib import Path
from typing import Any

import yaml

from printclaw.core.paths import KB_DIR


class KnowledgebaseLoader:
    def __init__(self, kb_dir: Path = KB_DIR):
        self.kb_dir = kb_dir

    def load_all(self) -> dict[str, Any]:
        data: dict[str, Any] = {}
        for path in sorted(self.kb_dir.rglob("*.yaml")):
            data[str(path.relative_to(self.kb_dir))] = yaml.safe_load(path.read_text())
        return data

    def search(self, query: str) -> list[dict[str, Any]]:
        query_l = query.lower()
        matches: list[dict[str, Any]] = []
        for rel_path, payload in self.load_all().items():
            entries = payload.get("entries", []) if isinstance(payload, dict) else []
            for entry in entries:
                haystack = " ".join(str(v) for v in entry.values()).lower()
                if query_l in haystack:
                    matches.append({"file": rel_path, "entry": entry})
        return matches
