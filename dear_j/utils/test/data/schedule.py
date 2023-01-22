from __future__ import annotations

import dataclasses
from typing import Dict, List


@dataclasses.dataclass
class ScheduleData:
    title: str
    start_at: str
    end_at: str
    description: str
    protection_level: int
    participants: List[Dict]

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
