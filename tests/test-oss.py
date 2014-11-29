# -*- coding: utf8 -*-

import mock
import nose
import requests

import aliyunauth


TEST_BODY_MD5 = "31568d94c1ff0505d173ca6b5cc3cf49"


class TestOss(object):
    def setup(self):
        req_obj = requests.Request(
            "GET",
            "http://oss.example.bucket/test.sh?logging&acl=acl",
            data=b"some-data",
            params={"response-cache-control": "cache-control", "na": "na"},
            auth=aliyunauth.OssAuth("access-key", "secret-key", "bucket")
        )
        self.req = req_obj

    def test_no_md5(self):
        self.req.headers["date"] = "date"
        self.req.url = "http://oss.some.bucket/"
        self.req.auth = aliyunauth.OssAuth(
            "bucket",
            "access-key",
            "secret-key",
            allow_empty_md5=True
        )
        req = self.req.prepare()

        nose.tools.eq_(req.headers["date"], "date")
        nose.tools.eq_(req.headers["content-md5"], "")
        nose.tools.eq_(
            req.headers["content-type"],
            aliyunauth.OssAuth.DEFAULT_TYPE
        )
        nose.tools.eq_(
            req.headers["authorization"],
            "OSS access-key:6iu+Sn+U/6tz5xmJF7sXBc44lmA="
        )

    @mock.patch("time.strftime")
    def test_header_with_md5(self, mock_time):
        mock_time.return_value = "mock-date"
        req = self.req.prepare()

        nose.tools.eq_(req.headers["date"], "mock-date")
        nose.tools.eq_(req.headers["content-md5"], TEST_BODY_MD5)
        nose.tools.eq_(req.headers["content-type"], "text/x-sh")
        nose.tools.eq_(
            req.headers["authorization"],
            "OSS secret-key:oQ8oI+PxLugJnUfjmYDHufqkVUc="
        )

    def test_header_with_expires(self):
        self.req.auth = aliyunauth.OssAuth(
            "bucket",
            "access-key",
            "secret-key",
            expires=42
        )
        req = self.req.prepare()

        nose.tools.eq_(
            req.url,
            "http://oss.example.bucket/test.sh?"
            "Expire=42"
            "&OSSAccessKeyId=access-key"
            "&Signature=DxN01UTNHFf0qa8MLx4jgu%2FGpBo%3D"
            "&acl=acl&logging&na=na&response-cache-control=cache-control"
        )

    @mock.patch("time.time")
    def test_header_with_expires_in(self, mock_time):
        mock_time.return_value = 20

        self.req.auth = aliyunauth.OssAuth(
            "bucket",
            "access-key",
            "secret-key",
            expires_in=22
        )
        req = self.req.prepare()

        nose.tools.eq_(
            req.url,
            "http://oss.example.bucket/test.sh?"
            "Expire=42"
            "&OSSAccessKeyId=access-key"
            "&Signature=DxN01UTNHFf0qa8MLx4jgu%2FGpBo%3D"
            "&acl=acl&logging&na=na&response-cache-control=cache-control"
        )
