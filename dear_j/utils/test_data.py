from __future__ import annotations

import dataclasses
from typing import Dict, List, Optional


@dataclasses.dataclass
class UserData:
    username: str
    email: str
    password: str
    birthdate: str

    @property
    def for_registration(self) -> Dict:
        return {
            "username": self.username,
            "email": self.email,
            "password1": self.password,
            "password2": self.password,
            "birthdate": self.birthdate,
        }

    @property
    def for_login(self) -> Dict:
        return {
            "email": self.email,
            "password": self.password,
        }

    @classmethod
    def create_nth_user_data(cls, n: int) -> UserData:
        return cls(
            username=f"user{n}",
            email=f"user{n}@example.com",
            password=f"password@{n}",
            birthdate="2000-01-01",
        )


@dataclasses.dataclass
class RecurringRuleData:
    cron: int
    end_date: str
    
    @classmethod
    def create_recurring_data(cls, cron: int, end_date: str) -> RecurringRuleData:
        return cls(
            cron=cron,
            end_date=end_date,
        )

@dataclasses.dataclass
class ScheduleData:
    title: str
    start_at: str
    end_at: str
    description: str
    protection_level: int
    participants: List[Dict]
    is_recurring: bool
    recurring_rule: Optional[RecurringRuleData] = None

    @classmethod
    def create_nth_calendar_data(cls, n: int, protection_level: int, raw_participants: List[int]) -> ScheduleData:
        participants = [{"pk": i} for i in raw_participants.copy()]

        return cls(
            title=f"Test Schedule {n}",
            start_at="2022-12-11 00:00:00",
            end_at="2022-12-12 00:00:00",
            description=f"Test Description {n}",
            protection_level=protection_level,
            participants=participants,
            is_recurring=False,
        )

    @classmethod
    def create_recurring_calendar_data(cls, n: int, protection_level: int, raw_participants: List[int], cron: int, end_date: str) -> ScheduleData:
        participants = [{"pk": i} for i in raw_participants.copy()]
        recurring_rule = RecurringRuleData.create_recurring_data(cron, end_date)
        return cls(
            title=f"Test Schedule {n}",
            start_at="2022-12-11 00:00:00",
            end_at="2022-12-12 00:00:00",
            description=f"Test Description {n}",
            protection_level=protection_level,
            participants=participants,
            is_recurring = True, 
            recurring_rule=recurring_rule,
        )
