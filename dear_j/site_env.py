import enum
import os


class SiteEnv(enum.Enum):
    DEV = 1
    PROD = 2


_current_site = SiteEnv[os.environ["SITE"].upper()]


def is_dev():
    return _current_site is SiteEnv.DEV


def is_prod():
    return _current_site is SiteEnv.PROD
