import base64
import hashlib
import hmac
import logging
import mimetypes
import os
import time

import requests


from . import url
from . import utils


logger = logging.getLogger(__name__)


class OssAuth(requests.auth.AuthBase):
    """Attach Aliyun OSS Authentication to the given request"""
    X_OSS_PREFIX = "x-oss-"
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

    def __init__(self, bucket, app_key, secret_key, allow_empty_md5=False):
        self._bucket = bucket
        self._app_key = app_key
        self._secret_key = secret_key
        self._allow_empty_md5 = allow_empty_md5

        self._sign_with_url = None

    def set_more_headers(self, req, **extra_headers):
        oss_url = url.URL(req.url)
        req.headers.update(extra_headers)

        # set content-type
        if req.headers.get("content-type"):
            logger.info()
        else:
            content_type, __ = mimetypes.guess_type(oss_url.path)
            req.headers["content-type"] = content_type

        # set date
        if "date" not in req.headers:
            timestamp = time.gmtime()
            date = time.strftime(self.TIME_FMT, timestamp)
            req.headers["date"] = date
            logger.debug("date is [{0}|{1}]".format(timestamp, date))

        # set content-md5
        if req.body is not None:
            content_md5 = req.headers.get("content-md5")
            if content_md5 is None and self._allow_empty_md5 is False:
                content_md5 = utils.cal_md5(req.body)
        else:
            content_md5 = ""

        req.headers["content-md5"] = content_md5

        return req

    def get_signature(self, req):
        oss_url = url.URL(req.url)

        oss_headers = [
            "{0}:{1}".format(key, val)
            for key, val in req.headers.lower_items()
            if key.startswith(self.X_OSS_PREFIX)
        ]
        canonicalized_headers = "\n".join(sorted(oss_headers))
        logger.debug(
            "canonicalized header : [{0}]".format(canonicalized_headers)
        )

        oss_url.params = {
            key: val
            for key, val in oss_url.params.items()
            if key in self.SUB_RESOURCES or key in self.OVERRIDE_QUERIES
        }

        oss_url.forge(key=lambda x: x[0])
        canonicalized_str = "{0}/{1}".format(
            canonicalized_headers, os.path.join(self._bucket + oss_url.uri)
        )

        str_to_sign = "\n".join([
            req.method,
            req.headers["content-md5"],
            req.headers["content-type"],
            req.headers["date"],
            canonicalized_str
        ])
        logger.debug(
            "signature str is \n{0}\n{1}\n{0}\n".format("#" * 20, str_to_sign)
        )

        signature_bin = hmac.new(self._secret_key, str_to_sign, hashlib.sha1)
        signature = base64.b64encode(signature_bin.digest())
        logger.debug("signature is [{0}]".format(signature))
        return signature

    def __call__(self, req):
        req = self.set_more_headers(req)
        signature = self.get_signature(req)

        req.headers["authorization"] = "OSS {0}:{1}".format(
            self._app_key, signature
        )
        return req

    def sign_with_url(self, req, expires=None):
        # set expires
        req.headers["date"] = expires

        req = self.set_more_headers(req)
        signature = self.get_signature(req)

        oss_url = req.URL(req.url)
        oss_url.append_params(dict(
            Expire=expires,
            OSSAccessKeyId=self._app_key,
            Signature=signature
        ))

        url = oss_url.forge(key=lambda x: x[0])
        return url
