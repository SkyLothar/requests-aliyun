# -*- coding: utf8 -*-

import base64
import hashlib
import io

import nose
import requests

import aliyunauth.utils
import aliyunauth.consts


def test_cal_b64md5():
    s_data = b"foo"
    l_data = b"bar" * aliyunauth.consts.MD5_CHUNK_SIZE
    # normal data, None
    nose.tools.eq_(aliyunauth.utils.cal_b64md5(None), None)

    def b64md5(data):
        return base64.b64encode(hashlib.md5(data).digest()).decode("utf8")

    # normal data, small size, bytes
    nose.tools.eq_(aliyunauth.utils.cal_b64md5(s_data), b64md5(s_data))

    # normal data, small size, bytes
    nose.tools.eq_(
        aliyunauth.utils.cal_b64md5(s_data.decode("utf8")), b64md5(s_data)
    )

    # io-like, big size, bytes
    nose.tools.eq_(
        aliyunauth.utils.cal_b64md5(io.BytesIO(l_data)), b64md5(l_data)
    )
    # io-like, big size, str
    nose.tools.eq_(
        aliyunauth.utils.cal_b64md5(io.StringIO(l_data.decode("utf8"))),
        b64md5(l_data)
    )


def test_to_bytes():
    nose.tools.ok_(isinstance(
        aliyunauth.utils.to_bytes(u"foo"),
        requests.compat.bytes
    ))
    nose.tools.ok_(isinstance(
        aliyunauth.utils.to_bytes(b"foo"),
        requests.compat.bytes
    ))
    nose.tools.eq_(aliyunauth.utils.to_bytes(u"福", "gb2312"), b'\xb8\xa3')


def test_to_str():
    nose.tools.ok_(isinstance(
        aliyunauth.utils.to_str(u"bar"),
        requests.compat.str
    ), "unicode to str failed")
    nose.tools.ok_(isinstance(
        aliyunauth.utils.to_str(b"bar"),
        requests.compat.str
    ), "bytes to str failed")
    nose.tools.eq_(aliyunauth.utils.to_str(b"\xb0\xf4", "gb2312"), u"棒")


def test_percent_quote():
    nose.tools.eq_(
        aliyunauth.utils.percent_quote(u"福棒 &?/*~=+foo\""),
        "%E7%A6%8F%E6%A3%92%20%26%3F%2F%2A~%3D%2Bfoo%22"
    )


def test_percent_encode():
    nose.tools.eq_(
        aliyunauth.utils.percent_encode([("福 棒", "foo+bar")]),
        "%E7%A6%8F%20%E6%A3%92=foo%2Bbar"
    )
    nose.tools.eq_(
        aliyunauth.utils.percent_encode([("foo", "福"), ("bar", "棒")], True),
        "bar=%E6%A3%92&foo=%E7%A6%8F"
    )
