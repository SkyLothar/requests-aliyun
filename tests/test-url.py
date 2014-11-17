# -*- coding: utf8 -*-

import nose

import aliyunauth.url


TEST_URL = (
    "https://usr:pwd@example.com:99/path0/path1/path2"
    "?q0=foo&q1=bar&flag#frag"
)


def test_full_parts():
    url = aliyunauth.url.URL(TEST_URL)
    # basic
    nose.tools.eq_(url.scheme, "https")
    nose.tools.eq_(url.username, "usr")
    nose.tools.eq_(url.password, "pwd")
    nose.tools.eq_(url.host, "example.com")
    nose.tools.eq_(url.port, 99)
    nose.tools.eq_(url.path, "/path0/path1/path2")
    nose.tools.eq_(url.params, {"q0": "foo", "q1": "bar", "flag": None})
    nose.tools.eq_(url.fragment, "frag")
    # complex
    nose.tools.eq_(url.netloc, "usr:pwd@example.com:99")
    nose.tools.eq_(
        aliyunauth.url.parse_qs(url.query, True),
        dict(q0=["foo"], q1=["bar"], flag=[""])
    )
