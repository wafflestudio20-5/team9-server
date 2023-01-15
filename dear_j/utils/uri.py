from typing import Any, Dict, Optional


def get_uri_with_extra_params(url: str, extra_params: Optional[Dict[str, Any]] = None) -> str:
    if not extra_params:
        return url

    url += "?"
    for key, value in extra_params.items():
        if not url.endswith("?"):
            url += "&"
        url += f"{key}={value}"
    return url
