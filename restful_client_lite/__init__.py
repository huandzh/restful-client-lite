# -*- coding: utf-8 -*-

"""
    restful_client_lite
    ~~~~~~~~~~~~~~~~~

    Provides a simple client for RESTFUL APIs, with limited features.
"""
from typing import Dict, List, Callable, Union
from urllib.parse import urljoin
import requests
import json

from functools import wraps


class NoneEtag(IOError):
    """None etag from api"""

    pass


class APIClient(object):
    """
    A dmicros api connection
    ====
    Provides api functions
    """

    def __init__(self, api_root: str, auth: Dict[str, str]) -> None:
        self.api_root = api_root
        self.auth = auth

    def get_authorization_header(self) -> str:
        """
        get authorization header from property
        """
        return self.auth.get("token", "")

    def auth_headers(f: Callable) -> Callable:
        @wraps(f)
        def wrapper(self, *args, **kwargs):
            headers = kwargs.get("headers", {}).copy()
            headers.update({"Authorization": self.get_authorization_header()})
            kwargs["headers"] = headers
            return f(self, *args, **kwargs)

        return wrapper

    def abs_url(f: Callable) -> Callable:
        @wraps(f)
        def wrapper(self, url, *args, **kwargs):
            return f(self, urljoin(self.api_root, url), *args, **kwargs)

        return wrapper

    def encode_data(f: Callable) -> Callable:
        @wraps(f)
        def wrapper(self, *args, **kwargs):
            data = json.dumps(kwargs.get("data", {}))
            kwargs["data"] = data
            headers = kwargs.get("headers", {}).copy()
            headers.update({"Content-Type": "application/json; charset=utf-8"})
            kwargs["headers"] = headers
            return f(self, *args, **kwargs)

        return wrapper

    @abs_url
    @auth_headers
    def get(self, url: str, headers: Dict = {}) -> requests.Response:
        """method GET"""
        return requests.get(url, headers=headers)

    @abs_url
    @auth_headers
    @encode_data
    def post(
        self, url: str, data: Union[List, Dict] = {}, headers: Dict = {}
    ) -> requests.Response:
        """method POST"""
        return requests.post(url, data=data, headers=headers)

    @abs_url
    @auth_headers
    @encode_data
    def method_with_etag(
        self, url: str, etag: str, data: Union[List, Dict], headers: Dict, method: str
    ) -> requests.Response:
        """method using etag"""
        headers["If-Match"] = etag
        return requests.__getattribute__(method)(url, data=data, headers=headers)

    def method_auto_etag(
        self, url: str, data: Union[List, Dict], headers: Dict, method: str
    ) -> requests.Response:
        """method using etag, retrieve etag automatically in advance"""
        res = self.get(url, headers=headers)
        if res.status_code != 200:
            raise NoneEtag("Fail to get from url")
        try:
            etag = res.json()["_etag"]
        except KeyError:
            raise NoneEtag("None etag in response")
        return self.method_with_etag(
            url, etag, data=data, headers=headers, method=method
        )

    def patch(
        self, url: str, etag: str, data: Union[List, Dict] = {}, headers: Dict = {}
    ) -> requests.Response:
        """method patch"""
        return self.method_with_etag(
            url, etag, data=data, headers=headers, method="patch"
        )

    def patch_auto_etag(
        self, url: str, data: Union[List, Dict] = {}, headers: Dict = {}
    ) -> requests.Response:
        """method patch, auto handle etag"""
        return self.method_auto_etag(url, data=data, headers=headers, method="patch")

    def delete(
        self, url: str, etag: str, data: Union[List, Dict] = {}, headers: Dict = {}
    ) -> requests.Response:
        """method delete"""
        return self.method_with_etag(
            url, etag, data=data, headers=headers, method="delete"
        )

    def delete_auto_etag(
        self, url: str, data: Union[List, Dict] = {}, headers: Dict = {}
    ) -> requests.Response:
        """method delete, auto handle etag"""
        return self.method_auto_etag(url, data=data, headers=headers, method="delete")
