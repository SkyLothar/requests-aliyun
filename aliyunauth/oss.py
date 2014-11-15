import base64
import hashlib
import hmac
import logging
import time

import requests
import requests.packages.urllib3

from . import consts
from . import utils


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

    def __init__(self, app_key, secret_key):
        self._app_key = app_key
        self._secret_key = secret_key

    def __call__(self, req):
        content_md5 = req.headers.get("content-md5", "")
        content_type = req.headers.get("content-type", "")

        params = utils.parse_query(req.url)
        expire = params.get("Expires")
        if "Expires" in params:
            date = params["Expires"]
            params["OSSAccessKeyId"] = self._app_key
            params["Signature"] = signature
        else:
            date = time.strftime(self.TIME_FMT, time.gmtime())
            headers["date"] = date
            headers["authorization"] = "OSS {0}:{1}".format(self._app_key, signature)

        # headers
        canonicalized_header_str = self.canonicalize_oss_headers(req.headers)
        canonicalized_url = self.canonicalize_url(req.url)
        canonicalized_str = "{0}{1}".format(
            canonicalized_header, canonicalized_res
        )

        str_to_sign = "\n".join([
            req.method, content_md5, content_type, date, canonicalized_str
        ])
        signature = hmac.new(self._secret_key, str_to_sign, hashlib.sha1)
        b64_signature = base64.b64encode(signature.digest())

        # res url
        if path:
            url = "/{0}".format()
        if query:

        return req

    def canonicalize_oss_headers(self, headers):
        oss_headers = [
            "{0}:{1}".format(key, val)
            for key, val in sorted(headers.lower_items(), key=lambda k: k[0])
            if key.startswith(consts.X_OSS_PREFIX)
        ]
        return "\n".join(oss_headers)

    def canonicalize_resources(self, url):
        """
        returns new path of url
        canonicalize resources
        """
        query_list = []
        for key, val in params.items():
            if key in self.SUB_RESOURCES:
                logger.debug("found sub resource: {0}={1}".format(key, val))
                query_list.append(key if val is None else mk_pair(key, val))
            elif key in self.OVERRIDE_QUERIES:
                logger.debug("found override_query: {0}={1}".format(key, val))
                query_list.append(mk_pair(key, val))
            else:
                logger.info("unrecognized params: {0}={1}".format(key, val))
        canonicalized_resources = "&".join(query_list)
        return canonicalized_resources
