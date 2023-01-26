from __future__ import annotations

import dataclasses
from typing import Dict, List, Optional


@dataclasses.dataclass
class ScheduleData:
    title: str
    start_at: str
    end_at: str
    description: str
    protection_level: int
    participants: List[Dict]
    show_content: bool = True
    is_opened: bool = True
    is_recurring: bool = False
    cron_expr: Optional[str] = None
    recurring_end_at: Optional[str] = None

    @classmethod
    def create_nth_schedule_data(cls, n: int, protection_level: int, raw_participants: List[int]) -> ScheduleData:
        participants = [{"pk": i} for i in raw_participants.copy()]

        return cls(
            title=f"Test Schedule {n}",
            start_at="2022-12-11 00:00:00",
            end_at="2022-12-12 00:00:00",
            description=f"Test Description {n}",
            protection_level=protection_level,
            participants=participants,
        )

    @classmethod
    def create_recurring_schedule_data(
        cls,
        protection_level: int,
        raw_participants: List[int],
        cron_expr: str,
        recurring_end_at: str,
    ) -> ScheduleData:
        participants = [{"pk": i} for i in raw_participants.copy()]

        return cls(
            title="Test Schedule",
            start_at="2022-12-11 00:00:00",
            end_at="2022-12-12 00:00:00",
            description="Test Description",
            protection_level=protection_level,
            participants=participants,
            is_recurring=True,
            cron_expr=cron_expr,
            recurring_end_at=recurring_end_at,
        )

    def as_dict(self) -> Dict:
        return dataclasses.asdict(self)
