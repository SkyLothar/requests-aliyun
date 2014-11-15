# -*- coding: utf8 -*-

import hashlib
import io

import nose

import aliyunauth.utils
import aliyunauth.consts


def test_parse_query():
    test_query = "?foo=bar&baz=%e4%bd%a0%e5%a5%bd+%e4%b8%96%e7%95%8c&flag"
    params = aliyunauth.utils.parse_query(test_query)
    nose.tools.eq_(params, dict(foo="bar", baz=u"你好 世界", flag=None))


def test_cal_md5():
    s_data = b"hello world"
    l_data = b"big" * aliyunauth.consts.MD5_CHUNK_SIZE
    # normal data, small size
    nose.tools.eq_(
        aliyunauth.utils.cal_md5(s_data),
        hashlib.md5(s_data).hexdigest()
    )
    # io-like, big size
    nose.tools.eq_(
        aliyunauth.utils.cal_md5(io.BytesIO(l_data)),
        hashlib.md5(l_data).hexdigest()
    )
