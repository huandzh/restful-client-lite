# -*- coding: utf-8 -*-
from restful_client_lite import APIClient
from restful_client_lite.tests import ClientTestBase
from typing import Dict, Callable
import requests
from urllib.parse import urljoin
from functools import wraps


class CustomAPIClient(APIClient):
    """custom api client"""

    def __init__(self, api_root, auth: Dict[str, str]) -> None:
        super(CustomAPIClient, self).__init__(api_root, auth)
        # store side effects by custom methods
        self.custom = {}
        # change wrapper sequence
        self.get = self.abs_url(self.auth_headers(self.get_inner))

    def abs_url(self, f: Callable) -> Callable:
        @wraps(f)
        def wrapper(url, *args, **kwargs):
            self.custom["abs_url"] = "custom"
            return f(urljoin(self.api_root, url), *args, **kwargs)

        return wrapper

    def auth_headers(self, f: Callable) -> Callable:
        @wraps(f)
        def wrapper(*args, **kwargs):
            self.custom["url"] = args[0]
            self.custom["auth_headers"] = "custom"
            headers = kwargs.get("headers", {}).copy()
            headers.update({"Authorization": self.get_authorization_header()})
            kwargs["headers"] = headers
            return f(*args, **kwargs)

        return wrapper

    def get_inner(self, url: str, headers: Dict = {}) -> requests.Response:
        """method GET"""
        self.custom["get"] = "custom"
        return requests.get(url, headers=headers)


class InheritageTestCase(ClientTestBase):
    def test_custom_client(self):
        # use custom api
        self.api = CustomAPIClient(self.api_root, {"token": self.auth["token"]})
        url = "/scores"
        # check custom wrapper and method applied
        self.api.get("/scores")
        for i in ["get", "abs_url", "auth_headers"]:
            self.assertEqual(self.api.custom.get(i), "custom")
        self.assertNotEqual(self.api.custom.get("url"), url)
