from __future__ import annotations

import dataclasses
from typing import Dict, List


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
class UserPKData:
    pk: int

    @classmethod
    def create_nth_user_pk_data(cls, pk: int):
        return cls(pk=pk)


@dataclasses.dataclass
class CalendarData:
    title: str
    start_at: str
    end_at: str
    description: str
    protection_level: int
    participants: List[UserPKData]

    @classmethod
    def create_nth_user_data(cls, n: int, protection_level: int, participants: List[int]) -> CalendarData:
        participants_list = []
        for pk in participants:
            participants_list.append(UserPKData.create_nth_user_pk_data(pk))
        return cls(
            title=f"Test Schedule {n}",
            start_at="2022-12-11 00:00:00",
            end_at="2022-12-12 00:00:00",
            description=f"Test Description {n}",
            protection_level=protection_level,
            participants=participants_list,
        )


@dataclasses.dataclass
class AttendenceData:
    status: int

    @classmethod
    def create_attendence_data(cls, attendence_status: int) -> AttendenceData:
        return cls(
            status=attendence_status,
        )
