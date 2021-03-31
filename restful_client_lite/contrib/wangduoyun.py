# -*- coding: utf-8 -*-

"""
# api clients for wangduoyun

**copyright** (c) 2021 by Huan Di <hd@iamhd.top>
"""
import hashlib
import datetime
from functools import wraps
import urllib.parse
from typing import Callable, Dict, Tuple
from restful_client_lite import APIClient


class WangduoyunApiClient(APIClient):
    """
    WangDuoYun api client

    Notice:

    See docs at https://docs.wangduoyun.com/develop/overview/aboutus.html
    """

    def __init__(self, api_root: str, auth: Dict[str, str]) -> None:
        """
        auth : {user_key, user_secret}
        """
        super(WangduoyunApiClient, self).__init__(api_root, auth)
        # apply wrappers without decorater sugar
        self.get = self.abs_url(self.get_inner)
        self.post = self.set_default_data(self.abs_url(self.post_inner))

    def get_sign(self) -> Tuple[str, int]:
        """
        get authorized sign and its timestamp
        """
        md5 = hashlib.md5()
        timestamp = int(datetime.datetime.now().timestamp())
        md5.update(
            (self.auth["user_key"] + str(timestamp) + self.auth["user_secret"]).encode(
                "utf-8"
            )
        )
        sign = md5.hexdigest()
        return sign, timestamp

    def set_default_data(self, f: Callable) -> Callable:
        @wraps(f)
        def wrapper(*args, **kwargs):
            data = kwargs.get("data", {})
            sign, timestamp = self.get_sign()
            data.update(
                {
                    "user_key": self.auth["user_key"],
                    "timestamp": timestamp,
                    "sign": sign,
                }
            )
            kwargs["data"] = data
            return f(*args, **kwargs)

        return wrapper

    def abs_url(self, f: Callable) -> Callable:
        @wraps(f)
        def wrapper(url, *args, **kwargs):
            return f(urllib.parse.urljoin(self.api_root, url), *args, **kwargs)

        return wrapper


class WangduoyunGraphqlClient(WangduoyunApiClient):
    """
    WangDuoYun api client

    Notice:

    See docs at https://docs.wangduoyun.com/develop/overview/aboutus.html
    """

    def __init__(self, api_root: str, auth: Dict[str, str]) -> None:
        """
        auth : {user_key, user_secret}
        """
        super(WangduoyunApiClient, self).__init__(api_root, auth)
        # apply wrappers without decorater sugar
        self.get = self.abs_auth_url(self.get_inner)
        self.post = self.set_default_data(self.abs_url(self.post_inner))

    def get_sign(self) -> Tuple[str, int]:
        """
        get authorized sign and its timestamp
        """
        md5 = hashlib.md5()
        timestamp = int(datetime.datetime.now().timestamp())
        md5.update(
            (self.auth["user_key"] + str(timestamp) + self.auth["user_secret"]).encode(
                "utf-8"
            )
        )
        sign = md5.hexdigest()
        return sign, timestamp

    def set_default_data(self, f: Callable) -> Callable:
        @wraps(f)
        def wrapper(*args, **kwargs):
            data = kwargs.get("data", {})
            sign, timestamp = self.get_sign()
            data.update(
                {
                    "user_key": self.auth["user_key"],
                    "timestamp": timestamp,
                    "sign": sign,
                }
            )
            kwargs["data"] = data
            return f(*args, **kwargs)

        return wrapper

    def abs_auth_url(self, f: Callable) -> Callable:
        @wraps(f)
        def wrapper(url, *args, **kwargs):
            sign, timestamp = self.get_sign()
            auth_part = "?user_key={user_key}&timestamp={timestamp}&sign={sign}&source_id={source_id}".format(
                user_key=self.auth["user_key"],
                source_id=self.auth["source_id"],
                sign=sign,
                timestamp=timestamp,
            )
            return f(
                urllib.parse.urljoin(self.api_root, auth_part + url), *args, **kwargs
            )

        return wrapper
