# -*- coding: utf8 -*-

import mock
import nose
import requests

import aliyunauth


class TestRds(object):
    CORRECT_URL = (
        "http://rds.example.com/"
        "?AccessKeyId=access-key"
        "&Action=Test"
        "&Foo=bar"
        "&Format=json"
        "&Signature=q4DMNXzkcAD6uzs7eTC62uZiX%2FE%3D"
        "&SignatureMethod=HMAC-SHA1"
        "&SignatureNonce=mock-nonce"
        "&SignatureVersion=1.0"
        "&TimeStamp=mock-date"
        "&Version=2014-08-15"
    )

    def setup(self):
        req_obj = requests.Request(
            "GET",
            "http://rds.example.com/",
            params={"Action": "Test", "Foo": "bar", "Format": "json"},
            auth=aliyunauth.RdsAuth("access-key", "secret-key", "xml")
        )
        self.req = req_obj

    def test_attrs(self):
        nose.tools.eq_(aliyunauth.RdsAuth.VERSION, "2014-08-15")
        nose.tools.eq_(aliyunauth.RdsAuth.SERVICE, "rds")

    @mock.patch("time.strftime")
    @mock.patch("uuid.uuid4")
    def test_auth(self, mock_uuid, mock_time):
        fake_uuid = mock.MagicMock()
        fake_uuid.hex = "mock-nonce"
        mock_uuid.return_value = fake_uuid
        mock_time.return_value = "mock-date"

        req = self.req.prepare()
        nose.tools.eq_(req.url, self.CORRECT_URL)
