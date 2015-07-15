# -*- coding: utf8 -*-

import mock
import nose
import requests

import aliyunauth


class TestCms(object):
    CORRECT_URL = (
        "http://cms.example.com/"
        "?AccessKeyId=access-key"
        "&Action=Test"
        "&Foo=bar"
        "&Format=xml"
        "&Signature=gImfTlPa1OZQwF0%2F%2BB2WyYjeRdE%3D"
        "&SignatureMethod=HMAC-SHA1"
        "&SignatureNonce=mock-nonce"
        "&SignatureVersion=1.0"
        "&Timestamp=mock-date"
        "&Version=2015-04-20"
    )

    def setup(self):
        req_obj = requests.Request(
            "GET",
            "http://cms.example.com/",
            params={"Action": "Test", "Foo": "bar"},
            auth=aliyunauth.CmsAuth("access-key", "secret-key", "xml")
        )
        self.req = req_obj

    def test_attrs(self):
        nose.tools.eq_(aliyunauth.CmsAuth.VERSION, "2015-04-20")
        nose.tools.eq_(aliyunauth.CmsAuth.SERVICE, "cms")

    @mock.patch("time.strftime")
    @mock.patch("uuid.uuid4")
    def test_auth(self, mock_uuid, mock_time):
        fake_uuid = mock.MagicMock()
        fake_uuid.hex = "mock-nonce"
        mock_uuid.return_value = fake_uuid
        mock_time.return_value = "mock-date"

        req = self.req.prepare()
        nose.tools.eq_(req.url, self.CORRECT_URL)
