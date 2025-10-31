from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import date, datetime
from typing import Optional, Literal

Prio = Literal["low", "med", "high"]

@dataclass
class Task:
    id: int
    title: str
    done: bool = False
    prio: Prio = "med"
    due: Optional[date] = None
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["created_at"] = self.created_at.isoformat()
        d["due"] = self.due.isoformat() if self.due else None
        return d

    @staticmethod
    def from_dict(d: dict) -> "Task":
        return Task(
            id=int(d["id"]),
            title=d["title"],
            done=bool(d.get("done", False)),
            prio=d.get("prio", "med"),
            due=date.fromisoformat(d["due"]) if d.get("due") else None,
            created_at=datetime.fromisoformat(d["created_at"]) if d.get("created_at") else datetime.utcnow(),
        )
