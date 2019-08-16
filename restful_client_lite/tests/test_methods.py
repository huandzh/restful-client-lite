# -*- coding: utf-8 -*-

from restful_client_lite.tests import ClientTestBase, generate_random_key
import random


class MethodsTestCase(ClientTestBase):
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
