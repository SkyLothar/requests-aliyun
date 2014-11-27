import mock
import nose

import aliyunauth


def test_headers_no_md5():
    req = mock.MagicMock()
    req.url = "http://example.com/"
    req.body = "some-data"
    req.headers = {}

    auth = aliyunauth.OssAuth("access-key", "secret-key", "bucket", True)
    auth.set_more_headers(req, {"date": "date", "content-type": "type"})

    nose.tools.eq_(
        req.headers,
        {"date": "date", "content-type": "type", "content-md5": ""}
    )


@mock.patch("time.strftime")
def test_header_with_md5(mock_time):
    req = mock.MagicMock()
    req.url = "http://example.com/"
    req.body = "some-data"
    req.headers = {}
    mock_time.return_value = "mock-date"

    auth = aliyunauth.OssAuth("access-key", "secret-key", "bucket")
    auth.set_more_headers(req)
    nose.tools.eq_(
        req.headers,
        {
            "date": "mock-date",
            "content-type": "application/x-sh",
            "content-md5": ""
        }
    )
