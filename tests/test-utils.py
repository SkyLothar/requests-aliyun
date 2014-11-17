# -*- coding: utf8 -*-

import hashlib
import io

import nose

import aliyunauth.utils
import aliyunauth.consts


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
