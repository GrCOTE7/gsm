from dataclasses import dataclass, field
from datetime import date


@dataclass
class Habit:
    name: str
    frequency: str = "daily"  # "daily" | "weekly"
    id: int | None = None
    created_at: date = field(default_factory=date.today)
    checkins: list[date] = field(default_factory=list)

    def is_done_today(self) -> bool:
        return date.today() in self.checkins
