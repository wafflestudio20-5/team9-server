from __future__ import annotations

import dataclasses
from typing import Dict, List


@dataclasses.dataclass
class PostData:
    title: str
    content: str
    #schedules: List[Dict]

    @classmethod
    def create_post_data(cls, schedules_list: List[int]) -> PostData:
        schedules = [{"pk": i} for i in schedules_list.copy()]
        return cls(
            title="Test Post",
            content="Test Content",
        )
