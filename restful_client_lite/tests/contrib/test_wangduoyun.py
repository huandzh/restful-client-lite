# -*- coding: utf-8 -*-
# type: ignore
"""
Put `wangduoyun.ini` at where to run tests
with the follow settings and fill in credentials:

```txt
[Api]
api_root=
graphql_root=
source_id=
user_key=
user_secret=
```

**Don't commit your config file**
"""

import unittest
from restful_client_lite.contrib.wangduoyun import (
    WangduoyunApiClient,
    WangduoyunGraphqlClient,
)
import configparser
from restful_client_lite.tests import TEST_ON_CONTRIB

CONFIG = configparser.ConfigParser()
CONFIG.read("wangduoyun.ini")

SKIPS = {"Api": {}}

for key in SKIPS:
    if TEST_ON_CONTRIB is None:
        SKIPS[key] = {"is_skipped": True, "message": "skip tests on contrib"}
    elif key not in CONFIG:
        SKIPS[key] = {"is_skipped": True, "message": "no settings for" + key}
    else:
        SKIPS[key] = {"is_skipped": False, "message": ""}


@unittest.skipIf(SKIPS["Api"]["is_skipped"], SKIPS["Api"]["message"])
class WangduoyunApiClientTestCase(unittest.TestCase):
    def test_can_post_to_api(self):
        api = WangduoyunApiClient(
            CONFIG["Api"]["api_root"],
            {
                "user_key": CONFIG["Api"]["user_key"],
                "user_secret": CONFIG["Api"]["user_secret"],
            },
        )
        res = api.post("user/node")
        # if success, field `data` should be avaiable
        res_json = res.json()
        self.assertIn("data", res_json)
        self.assertIn("node_all", res_json["data"])

    def test_can_get_graphql(self):
        query = 'source(__id:{gt:1},limit:2,sort:"asc"){data{hid},page_info{end_cursor,has_next_page}}'
        api = WangduoyunGraphqlClient(
            CONFIG["Api"]["graphql_root"],
            {
                "user_key": CONFIG["Api"]["user_key"],
                "user_secret": CONFIG["Api"]["user_secret"],
                "source_id": CONFIG["Api"]["source_id"],
            },
        )
        url = "&query={query}".format(
            query=query,
        )
        res = api.get(url)
        # if success, field `result` should be avaiable
        self.assertIn("result", res.json())
        self.assertEqual(len(res.json()["result"]), 2)
