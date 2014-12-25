# -*- coding: utf8 -*-

import hashlib
import io

import nose
import requests

import aliyunauth.utils
import aliyunauth.consts


def test_cal_md5():
    s_data = b"foo"
    l_data = b"bar" * aliyunauth.consts.MD5_CHUNK_SIZE
    # normal data, None
    nose.tools.eq_(aliyunauth.utils.cal_md5(None), None)

    # normal data, small size, bytes
    nose.tools.eq_(
        aliyunauth.utils.cal_md5(s_data),
        hashlib.md5(s_data).hexdigest()
    )
    # normal data, small size, bytes
    nose.tools.eq_(
        aliyunauth.utils.cal_md5(s_data.decode("utf8")),
        hashlib.md5(s_data).hexdigest()
    )

    # io-like, big size, bytes
    nose.tools.eq_(
        aliyunauth.utils.cal_md5(io.BytesIO(l_data)),
        hashlib.md5(l_data).hexdigest()
    )
    # io-like, big size, str
    nose.tools.eq_(
        aliyunauth.utils.cal_md5(io.StringIO(l_data.decode("utf8"))),
        hashlib.md5(l_data).hexdigest()
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
