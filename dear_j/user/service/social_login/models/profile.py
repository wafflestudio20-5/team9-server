import dataclasses
import datetime


@dataclasses.dataclass
class SocialProfile:
    email: str
    username: str = None
    birthdate: datetime.date = None
