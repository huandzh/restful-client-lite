# -*- coding: utf-8 -*-

"""
# api clients for aliyun

Avaiable clients:

* api gateway client

**copyright** (c) 2019 by Huan Di <hd@iamhd.top>
"""

import hmac
import hashlib
import base64
import time
import uuid
from restful_client_lite import APIClient
from typing import Callable, Dict, Tuple
from functools import wraps


class AliyunApiGatewayClient(APIClient):
    """
    Dataservice api client

    Notice:

    staticmethods in this class are modified from
    project at https://github.com/aliyun/api-gateway-demo-sign
    which is under [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0)
    """

    FORMAT_RFC_2616 = "%a, %d %b %Y %X GMT"

    @staticmethod
    def sign(source: str, secret: str) -> str:
        """
        sign source with secret
        """
        h = hmac.new(secret.encode("ascii"), source.encode("ascii"), hashlib.sha256)
        signature = base64.encodebytes(h.digest()).strip()
        return signature.decode("ascii")

    @staticmethod
    def init_headers(app_id: str) -> Dict[str, str]:
        """
        init headers with app_id, add X-Ca-* headers and etc.
        """
        # using current time
        time_stamp = time.time()
        headers = dict()
        headers["X-Ca-Timestamp"] = str(int(time_stamp * 1000))
        headers["X-Ca-Nonce"] = str(uuid.uuid4())
        headers["X-Ca-Key"] = app_id
        headers["Content-Type"] = "application/json; charset=utf-8"
        headers["Date"] = time.strftime(
            AliyunApiGatewayClient.FORMAT_RFC_2616, time.localtime(time_stamp)
        )
        return headers

    @staticmethod
    def x_ca_header_strings(headers: Dict[str, str]) -> Tuple[str, str]:
        """
        compute (X-Ca-Signature-headers, X-Ca-header-String) from headers
        """
        x_ca_headers = [
            (h, headers[h]) for h in sorted(headers) if h.startswith("X-Ca-")
        ]
        return (
            ",".join([h for h, v in x_ca_headers]),
            "\n".join([h + ":" + v for h, v in x_ca_headers]),
        )

    @staticmethod
    def get_signed_headers(url: str, app_id: str, secret: str) -> Dict[str, str]:
        """
        get signed headers for url, app_id, secret
        """
        headers = AliyunApiGatewayClient.init_headers(app_id)
        # params required by source
        http_method = "GET"
        accept = "*/*"
        content_md5 = ""
        content_type = headers["Content-Type"]
        date = headers["Date"]
        x_ca_header, x_ca_header_string = AliyunApiGatewayClient.x_ca_header_strings(
            headers
        )
        source = "\n".join(
            [
                http_method,
                accept,
                content_md5,
                content_type,
                date,
                x_ca_header_string,
                url,
            ]
        )
        # sign
        signature = AliyunApiGatewayClient.sign(source, secret)
        # add X-Ca-Signature
        headers["X-Ca-Signature-headers"] = x_ca_header
        headers["X-Ca-Signature"] = signature
        return headers

    def auth_headers(self, f: Callable) -> Callable:
        @wraps(f)
        def wrapper(*args, **kwargs):
            url = kwargs.get("url", args[0])
            app_id = self.auth.get("app_id", "")
            app_secret = self.auth.get("app_secret", "")
            headers = AliyunApiGatewayClient.get_signed_headers(url, app_id, app_secret)
            kwargs["headers"] = headers
            return f(*args, **kwargs)

        return wrapper
