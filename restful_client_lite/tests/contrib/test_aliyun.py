# -*- coding: utf-8 -*-
# type: ignore
"""
Put `aliyun.ini` at where to run tests
with the follow settings and fill in credentials:

```txt
[ApiGateway]
api_root=
app_id=
app_secret=
url=
```

**Don't commit your config file**
"""

import unittest
from restful_client_lite.contrib.aliyun import AliyunApiGatewayClient
import configparser
from restful_client_lite.tests import TEST_ON_CONTRIB

CONFIG = configparser.ConfigParser()
CONFIG.read("aliyun.ini")

SKIPS = {"ApiGateway": {}}

for key in SKIPS:
    if TEST_ON_CONTRIB is None:
        SKIPS[key] = {"is_skipped": True, "message": "skip tests on contrib"}
    elif key not in CONFIG:
        SKIPS[key] = {"is_skipped": True, "message": "no settings for" + key}
    else:
        SKIPS[key] = {"is_skipped": False, "message": ""}


@unittest.skipIf(SKIPS["ApiGateway"]["is_skipped"], SKIPS["ApiGateway"]["message"])
class AliyunApiGatewayClientTestCase(unittest.TestCase):
    def test_can_get_from_api(self):
        api = AliyunApiGatewayClient(
            CONFIG["ApiGateway"]["api_root"],
            {
                "app_id": CONFIG["ApiGateway"]["app_id"],
                "app_secret": CONFIG["ApiGateway"]["app_secret"],
            },
        )
        res = api.get(CONFIG["ApiGateway"]["url"])
        # if success, field `data` should be avaiable
        self.assertIn("data", res.json())
