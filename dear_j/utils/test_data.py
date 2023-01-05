from __future__ import annotations

import dataclasses
from typing import Dict


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
