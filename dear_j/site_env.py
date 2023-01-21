import enum
import os


class SiteEnv(enum.Enum):
    PROD = "PROD"
    STAGE = "STAGE"
    DEV = "DEV"
    LOCAL = "LOCAL"


_site = os.environ.get("SITE", "LOCAL").upper()
if not _site:
    _site = "LOCAL"

_current_site = SiteEnv[_site]


def is_prod() -> bool:
    return _current_site is SiteEnv.PROD


def is_stage() -> bool:
    return _current_site is SiteEnv.STAGE


def is_dev() -> bool:
    return _current_site is SiteEnv.DEV


def is_local() -> bool:
    return _current_site is SiteEnv.LOCAL


def is_prod_or_stage() -> bool:
    return is_prod() or is_stage()
