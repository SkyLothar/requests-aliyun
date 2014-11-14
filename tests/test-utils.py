# -*- coding: utf8 -*-

import aliyunauth.utils


TEST_QUERY = "foo=bar&baz=%e4%bd%a0%e5%a5%bd+%e4%b8%96%e7%95%8c"

def test_parse_query():
    aliyunauth.utils.parse_query(TEST_QUERY)
