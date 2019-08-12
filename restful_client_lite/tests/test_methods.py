# -*- coding: utf-8 -*-

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

    def test_can_post(self):
        doc = {"name": generate_random_key(6), "score": random.randint(60, 100)}
        res = self.api.post("/scores", data=doc)
        self.assertEqual(res.status_code, 201)

    def test_can_get(self):
        for i in range(3):
            doc = {"name": generate_random_key(6), "score": random.randint(60, 100)}
            res = self.api.post("/scores", data=doc)
        res = self.api.get("/scores")
        self.assertEqual(res.status_code, 200)

    def test_can_delete_auto_etag(self):
        score = random.randint(60, 100)
        doc = {"name": generate_random_key(6), "score": score}
        res = self.api.post("/scores", data=doc)
        _id = res.json()["_id"]
        url = "/scores/" + _id
        res = self.api.delete_auto_etag(url)
        self.assertEqual(res.status_code, 204)

    def test_can_delete_with_etag(self):
        score = random.randint(60, 100)
        doc = {"name": generate_random_key(6), "score": score}
        res = self.api.post("/scores", data=doc)
        _id = res.json()["_id"]
        _etag = res.json()["_etag"]
        url = "/scores/" + _id
        res = self.api.delete(url, etag=_etag)
        self.assertEqual(res.status_code, 204)

    def test_can_patch_auto_etag(self):
        score = random.randint(60, 100)
        doc = {"name": generate_random_key(6), "score": score}
        res = self.api.post("/scores", data=doc)
        _id = res.json()["_id"]
        url = "/scores/" + _id
        patch_doc = {"score": score - 5}
        res = self.api.patch_auto_etag(url, data=patch_doc)
        self.assertEqual(res.status_code, 200)
        res = self.api.get(url)
        self.assertEqual(res.json()["score"], score - 5)

    def test_can_patch_with_etag(self):
        score = random.randint(60, 100)
        doc = {"name": generate_random_key(6), "score": score}
        res = self.api.post("/scores", data=doc)
        _id = res.json()["_id"]
        _etag = res.json()["_etag"]
        url = "/scores/" + _id
        patch_doc = {"score": score - 5}
        res = self.api.patch(url, etag=_etag, data=patch_doc)
        self.assertEqual(res.status_code, 200)
        res = self.api.get(url)
        self.assertEqual(res.json()["score"], score - 5)
