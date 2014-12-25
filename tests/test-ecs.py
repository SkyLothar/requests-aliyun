# -*- coding: utf8 -*-

import base64
import hashlib
import hmac

import mock
import nose
import requests

import aliyunauth


CORRECT_URL = (
    "http://ecs.example.bucket/"
    "?AccessKeyId=access-key"
    "&Action=Test"
    "&Foo=bar"
    "&Format=json"
    "&Signature=Excuc%2FHHj8tbhnmwuxjiGwAf4d8%3D"
    "&SignatureMethod=HMAC-SHA1"
    "&SignatureNonce=mock-nonce"
    "&SignatureVersion=1.0"
    "&TimeStamp=mock-date"
    "&Version=2014-05-26"
)


class TestEcs(object):
    def setup(self):
        req_obj = requests.Request(
            "GET",
            "http://ecs.example.bucket/",
            params={"Action": "Test", "Foo": "bar", "Format": "json"},
            auth=aliyunauth.EcsAuth("access-key", "secret-key", "xml")
        )
        self.req = req_obj

    def test_sign(self):
        auth_signature = self.req.auth.sign("METHOD", {})
        correct_sig = hmac.new(b"secret-key&", b"METHOD&%2F&", hashlib.sha1)

        nose.tools.eq_(
            auth_signature,
            base64.b64encode(correct_sig.digest())
        )

    @mock.patch("time.strftime")
    @mock.patch("uuid.uuid4")
    def test_overide_common_params(self, mock_uuid, mock_time):
        fake_uuid = mock.MagicMock()
        fake_uuid.hex = "mock-nonce"
        mock_uuid.return_value = fake_uuid
        mock_time.return_value = "mock-date"

        params = self.req.auth.set_common_params(dict(
            Format="format",
            Signature="signature",
            Version="version",
            TimeStamp="timestamp",
            SignatureMethod="sig-method",
            SignatureVersion="sig-version",
            SignatureNonce="sig-nonce"
        ))
        nose.tools.eq_(
            params,
            dict(
                AccessKeyId="access-key",
                Format="format",
                SignatureMethod=self.req.auth.SIG_METHOD,
                SignatureVersion=self.req.auth.SIG_VERSION,
                SignatureNonce="mock-nonce",
                TimeStamp="mock-date",
                Version=self.req.auth.VERSION
            )
        )

    @mock.patch("time.strftime")
    @mock.patch("uuid.uuid4")
    def test_set_common_params(self, mock_uuid, mock_time):
        fake_uuid = mock.MagicMock()
        fake_uuid.hex = "mock-nonce"
        mock_uuid.return_value = fake_uuid
        mock_time.return_value = "mock-date"

        self.req.auth._ram = "ram"

        params = self.req.auth.set_common_params(dict())

        nose.tools.eq_(
            params,
            dict(
                AccessKeyId="access-key",
                Format="xml",
                ResourceOwnerAccount="ram",
                SignatureMethod=self.req.auth.SIG_METHOD,
                SignatureVersion=self.req.auth.SIG_VERSION,
                SignatureNonce="mock-nonce",
                TimeStamp="mock-date",
                Version=self.req.auth.VERSION
            )
        )

    @mock.patch("time.strftime")
    @mock.patch("uuid.uuid4")
    def test_auth(self, mock_uuid, mock_time):
        fake_uuid = mock.MagicMock()
        fake_uuid.hex = "mock-nonce"
        mock_uuid.return_value = fake_uuid
        mock_time.return_value = "mock-date"

        req = self.req.prepare()
        nose.tools.eq_(req.url, CORRECT_URL)
