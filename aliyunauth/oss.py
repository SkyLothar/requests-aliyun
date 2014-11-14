import hashlib
import logging
import time

import requests
import requests.packages.urllib3

from . import consts


logger = logging.getLogger(__name__)


def mk_pair(key, val):
    return '{0}={1}'.format(key, val)


class OssAuth(requests.auth.AuthBase):
    """Attach Aliyun OSS Authentication to the given request"""
    TIME_FMT = "%a, %d %b %Y %H:%M:%S GMT"
    SUB_RESOURCES = (
        "acl",
        "group",
        "uploadId",
        "partNumber",
        "uploads",
        "logging"
    )
    OVERRIDE_QUERIES = (
        "response-content-type",
        "response-content-language",
        "response-expires",
        "response-cache-control",
        "response-content-disposition",
        "response-content-encoding"
    )

    REGIONS = {
    }

    def __init__(
        self,
        app_key,
        secret_key,
        sub_resources=None,
        override_query=None
    ):
        self._app_key = app_key
        self._secret_key = secret_key

        self._sub_resources = sub_resources
        self._override_query = override_query

    def __call__(self, req):
        # cal md5
        content_md5 = req.headers.get("content-md5", "")
        content_type = req.headers.get("content-type", "")

        # headers
        canonicalized_header = self.canonicalize_oss_headers(req.headers)
        canonicalized_res = self.canonicalize_resources(params)
        canonicalized_str = "{0}{1}".format(
            canonicalized_header, canonicalized_res
        )

        str_to_sign = "\n".join([
            req.method, content_md5, content_type, date, canonicalized_str
        ])
        signature = hmac.new(self._secret_key, str_to_sign, hashlib.sha1)
        b64_signature = base64.b64encode(signature.digest())

        # cal md5
        # can-str
        # can-res
        # expire
        # str-to-sign
        # b64encode
        # set expire
        # res url
        # send url
        return req

    def sign_url(self, headers, params):
        sign_date = params["Expires"]
        params["OSSAccessKeyId"] = self._app_key
        params["Signature"] = signature

    def sign_header(self, headers, params):
        headers["date"] = time.strftime(self.TIME_FMT, time.gmtime())
        req.headers["authorization"] = "OSS {0}:{1}".format(
            self._app_key, signature
        )

    def canonicalize_oss_headers(self, headers):
        oss_headers = [
            "{0}:{1}".format(key, val)
            for key, val in sorted(headers.lower_items(), key=lambda k: k[0])
            if key.startswith(consts.X_OSS_PREFIX)
        ]
        return "\n".join(oss_headers)

    def canonicalize_resources(self, query):
        query_list = []
        for key, val in query.items():
            if key in self.SUB_RESOURCES:
                logger.debug("found sub resource: {0}={1}".format(key, val))
                query_list.append(key if val is None else mk_pair(key, val))
            elif key in self.OVERRIDE_QUERIES:
                logger.debug("found override_query: {0}={1}".format(key, val))
                query_list.append(mk_pair(key, val))

        return ''
