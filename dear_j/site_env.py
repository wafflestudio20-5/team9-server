import enum
import os


class SiteEnv(enum.Enum):
    PROD = "PROD"
    DEV = "DEV"
    LOCAL = "LOCAL"


_current_site = SiteEnv[os.environ.get("SITE", "LOCAL").upper()]


def is_prod() -> bool:
    return _current_site is SiteEnv.PROD


def is_dev() -> bool:
    return _current_site is SiteEnv.DEV


def is_local() -> bool:
    return _current_site is SiteEnv.LOCAL


def is_prod_or_dev() -> bool:
    return is_prod() or is_dev()
