# -*- coding: utf-8 -*-

import unittest
from restful_client_lite import APIClient
import os


class ClientTestBase(unittest.TestCase):
    def setUp(self):
        self.api_root = os.environ.get("API_ROOT", "http://127.0.0.1:5000")
        self.token = os.environ.get("TOKEN_AUTHOR", "")
        self.auth = {"token": self.token}
        self.api = APIClient(self.api_root, self.auth)

    def test_get_401_without_token(self):
        api = APIClient(self.api_root, {"token": ""})
        res = api.get("")
        self.assertEqual(res.status_code, 401)
