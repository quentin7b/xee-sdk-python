#!/usr/bin/env python
# coding: utf8
import unittest

import responses

import xee.utils as xee_utils
from xee.exceptions import APIException

class TestBearerGetRequest(unittest.TestCase):

    def do_bearer_get_request_code(self, code):
        responses.add(responses.GET, "https://toto.com", json=[{
            "type": "json",
            "message": "msg",
            "tip": "tip"
        }],status=code)
        try:
            response = xee_utils.do_bearer_get_request("https://toto.com", ":)")
        except APIException as err:
            self.assertIsNotNone(err)

    @responses.activate
    def test_bearer_get_request_code_200(self):
        responses.add(responses.GET, "https://toto.com", json=[{
            "some":"json"
        }],status=200)
        response = xee_utils.do_bearer_get_request("https://toto.com", ":)")
        self.assertIsNotNone(response)
    
    @responses.activate
    def test_bearer_get_request_code_400(self):
        self.do_bearer_get_request_code(400)
    
    @responses.activate
    def test_bearer_get_request_code_401(self):
        self.do_bearer_get_request_code(401)

    @responses.activate
    def test_bearer_get_request_code_403(self):
        self.do_bearer_get_request_code(403)
    
    @responses.activate
    def test_bearer_get_request_code_404(self):
        self.do_bearer_get_request_code(404)

    @responses.activate
    def test_bearer_get_request_code_416(self):
        self.do_bearer_get_request_code(416)

    @responses.activate
    def test_bearer_get_request_code_500(self):
        responses.add(responses.GET, "https://toto.com", json=[{
            "some":"json"
        }],status=500)
        try:
            response = xee_utils.do_bearer_get_request("https://toto.com", ":)")
        except Exception as err:
            self.assertIsNotNone(err)

class TestBasicGetRequest(unittest.TestCase):

    def do_basic_get_request_code(self, code):
        responses.add(responses.GET, "https://toto.com", json=[{
            "type": "json",
            "message": "msg",
            "tip": "tip"
        }],status=code)
        try:
            response = xee_utils.do_basic_get_request("https://toto.com", ":)", ":()")
            self.assertTrue(False)
        except APIException as err:
            self.assertIsNotNone(err)

    @responses.activate
    def test_basic_get_request_code_200(self):
        responses.add(responses.GET, "https://toto.com", json=[{
            "some":"json"
        }],status=200)
        response = xee_utils.do_basic_get_request("https://toto.com", ":)", ":()")
        self.assertIsNotNone(response)
    
    @responses.activate
    def test_basic_get_request_code_400(self):
        self.do_basic_get_request_code(400)
    
    @responses.activate
    def test_basic_get_request_code_401(self):
        self.do_basic_get_request_code(401)

    @responses.activate
    def test_basic_get_request_code_403(self):
        self.do_basic_get_request_code(403)
    
    @responses.activate
    def test_basic_get_request_code_404(self):
        self.do_basic_get_request_code(404)

    @responses.activate
    def test_basic_get_request_code_416(self):
        self.do_basic_get_request_code(416)

    @responses.activate
    def test_basic_get_request_code_500(self):
        responses.add(responses.GET, "https://toto.com", json=[{
            "some":"json"
        }],status=500)
        try:
            response = xee_utils.do_basic_get_request("https://toto.com", ":)", ":()")
            self.assertTrue(False)
        except Exception as err:
            self.assertIsNotNone(err)