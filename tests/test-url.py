# -*- coding: utf8 -*-

import nose

import aliyunauth.url


class TestURL(object):
    def test_full_parts(self):
        url = aliyunauth.url.URL(
            "https://usr:pwd@example.com:99/path0/path1/path2"
            "?q0=foo&q1=bar&flag#frag"
        )
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
        url.forge(key=lambda x: x[0])
        nose.tools.eq_(url.uri, "/path0/path1/path2?flag&q0=foo&q1=bar#frag")

    def test_forge(self):
        url = aliyunauth.url.URL("http://example.com")
        url.path = "/path0/path1"
        nose.tools.eq_("http://example.com/path0/path1", str(url))

        url.params = {"foo": "bar", "hello": "world", "a": None}
        nose.tools.eq_(
            "http://example.com/path0/path1?hello=world&foo=bar&a",
            url.forge(key=lambda x: x[0], reverse=True)
        )

        url.params = [("z", "last"), ("a", None)]
        nose.tools.eq_(
            "http://example.com/path0/path1?a&z=last",
            url.forge(key=lambda x: x[0])
        )

        url.append_params({"a": "b"})
        nose.tools.eq_({"a": "b", "z": "last"}, url.params)

        url.append_params([("z", None)])
        nose.tools.eq_({"a": "b", "z": None}, url.params)

        nose.tools.eq_(
            aliyunauth.url.parse_qs(url.query, True),
            dict(a=["b"], z=[""])
        )
