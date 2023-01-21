import dataclasses
import enum
from typing import List

import site_env


@dataclasses.dataclass
class HostInfo:
    domain: str
    name: str = None
    ip: str = None
    port: int = None
    is_https: bool = False

    def get_name(self) -> str:
        if self.name:
            return self.name
        return self.domain

    @property
    def url(self) -> str:
        url = f"https://{self.domain}" if self.is_https else f"http://{self.domain}"
        if self.port and self.port != 80:
            url = f"{url}:{self.port}"
        return url

    @property
    def ALLOWED_HOSTS(self) -> List:
        if site_env.is_local():
            return [self.domain, self.ip]
        if site_env.is_dev():
            return [self.ip, "0.0.0.0"]
        return [self.domain]


class BackendHost(enum.Enum):
    PROD_HOST = HostInfo(domain="api-dearj-wafflestudio.site", ip="43.201.9.194", port=80)
    STAGE_HOST = HostInfo(domain="api-staging-dearj-wafflestudio.site", ip="13.124.64.149", port=80)
    DEV_HOST = HostInfo(domain="0.0.0.0", ip="0.0.0.0", port=8000)
    LOCAL_HOST = HostInfo(domain="localhost", ip="127.0.0.1", port=8000)

    @classmethod
    def get_host_info(cls) -> HostInfo:
        if site_env.is_prod():
            return cls.PROD_HOST.value
        if site_env.is_stage():
            return cls.STAGE_HOST.value
        if site_env.is_dev():
            return cls.DEV_HOST.value
        return cls.LOCAL_HOST.value


class FrontendHost(enum.Enum):
    PROD_HOST = HostInfo(domain="dearj-wafflestudio.com")
    LOCAL_HOST = HostInfo(domain="localhost", ip="127.0.0.1", port=3000)

    @classmethod
    def get_host_info(cls) -> HostInfo:
        if site_env.is_prod():
            return cls.PROD_HOST.value
        return cls.LOCAL_HOST.value


BACKEND_HOST = BackendHost.get_host_info()
FRONTEND_HOST = FrontendHost.get_host_info()
