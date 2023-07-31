from typing import Dict
from settings import SiteSettings

import requests


def _make_request(method: str, url: str, headers: Dict, params: Dict, success=200):
    response = requests.request(
        method,
        url,
        headers=headers,
        params=params,
    )
    status_code = response.status_code

    if status_code == success:
        return response

    return status_code


def _get_test(method: str, url: str, headers: Dict, querystring: Dict, func=_make_request):
    response = func(method, url, headers=headers, params=querystring)

    return response


class SiteApiInterface:
    @staticmethod
    def get_test():
        return _get_test
