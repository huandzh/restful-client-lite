import unittest
from restful_client_lite import APIClient
import os
import random


def generate_random_key(l):
    return ("%0" + str(l) + "x") % random.randrange(16 ** l)


STANDARD_ROLES = {
    "roles": [
        {"resources": ["tokens"], "role": "user"},
        {"resources": ["scores"], "role": "author"},
    ]
}


class ClientTestBase(unittest.TestCase):
    def setUp(self):
        self.api_root = os.environ.get("API_ROOT", "http://127.0.0.1:5000")
        self.token_author = os.environ.get("TOKEN_AUTHOR", "")
        self.manager = APIClient(self.api_root, {"token": self.token_author})
        self.auth = {
            "name": generate_random_key(6),
            "token": generate_random_key(16),
            "roles": STANDARD_ROLES["roles"],
        }
        res_post_json = self.manager.post("/tokens", data=self.auth).json()
        self.auth.update(res_post_json)
        self.api = APIClient(self.api_root, {"token": self.auth["token"]})

    def tearDown(self):
        self.api.delete("/scores", etag="")
        self.manager.delete(
            "/tokens/" + self.auth["_id"], etag=self.auth["_etag"], data={}
        )
