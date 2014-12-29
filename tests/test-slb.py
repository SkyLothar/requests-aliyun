# -*- coding: utf8 -*-

import mock
import nose
import requests

import aliyunauth


class TestSlb(object):
    CORRECT_URL = (
        "http://slb.example.com/"
        "?AccessKeyId=access-key"
        "&Action=Test"
        "&Foo=bar"
        "&Format=json"
        "&Signature=4SDI5sAk3SXCP5Vp3dkzBuT1xtQ%3D"
        "&SignatureMethod=HMAC-SHA1"
        "&SignatureNonce=mock-nonce"
        "&SignatureVersion=1.0"
        "&TimeStamp=mock-date"
        "&Version=2014-05-15"
    )

    def setup(self):
        req_obj = requests.Request(
            "GET",
            "http://slb.example.com/",
            params={"Action": "Test", "Foo": "bar", "Format": "json"},
            auth=aliyunauth.SlbAuth("access-key", "secret-key", "xml")
        )
        self.req = req_obj

    def test_attrs(self):
        nose.tools.eq_(aliyunauth.SlbAuth.VERSION, "2014-05-15")
        nose.tools.eq_(aliyunauth.SlbAuth.SERVICE, "slb")

    @mock.patch("time.strftime")
    @mock.patch("uuid.uuid4")
    def test_auth(self, mock_uuid, mock_time):
        fake_uuid = mock.MagicMock()
        fake_uuid.hex = "mock-nonce"
        mock_uuid.return_value = fake_uuid
        mock_time.return_value = "mock-date"

        req = self.req.prepare()
        nose.tools.eq_(req.url, self.CORRECT_URL)
