from __future__ import annotations
import json
import os
from pathlib import Path
from typing import List
from .models import Task

DEFAULT_DIR = Path(os.path.expanduser("~/.planq"))
DEFAULT_DB = DEFAULT_DIR / "tasks.json"
DB_ENV = "PLANQ_DB"

class Storage:
    def __init__(self, db_path: Path | None = None):
        env = os.getenv(DB_ENV)
        self.db_path = Path(env) if env else (db_path or DEFAULT_DB)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.db_path.exists():
            self._write([])

    def _read(self) -> List[Task]:
        with self.db_path.open("r", encoding="utf-8") as f:
            raw = json.load(f)
        return [Task.from_dict(x) for x in raw]

    def _write(self, tasks: List[Task]) -> None:
        with self.db_path.open("w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in tasks], f, ensure_ascii=False, indent=2)

    def all(self) -> List[Task]:
        return self._read()

    def save_all(self, tasks: List[Task]) -> None:
        self._write(tasks)

    def next_id(self) -> int:
        tasks = self._read()
        return (max((t.id for t in tasks), default=0) + 1)
