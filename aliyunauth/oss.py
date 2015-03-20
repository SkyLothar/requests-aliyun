# -*- coding:utf8 -*-

"""
aliyunauth.oss
~~~~~~~~~~~~~~

This module contains the authentication handlers for Ali Oss Service
"""

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
    """Attach Aliyun Oss Authentication to the given request

    :param bucket: the bucket name of this request
    :param access_key: the access_key of your oss account
    :param secret_key: the secret_key of your oss account
    :param expires: (optional) the request will expire after the given epoch
    :param expires_in: (optional) the request will expires in x `seconds`,
        this option will cause the *url sign method*
    :param allow_empty_md5: (optional) don't calculate md5. Default is `False`,
        calculate md5 when content-md5 not appears in the headers

    Usage::

        >>> import requests
        >>> from aliyunauth import OssAuth
        >>> req = request.get(
        ...     "http://bucket-name.oss-url.com/path/to/file",
        ...     auth=OssAuth("bucket-name", "access-key", "secret-key")
        ... )
        <Response [200]>

    """
    X_OSS_PREFIX = "x-oss-"
    DEFAULT_TYPE = "application/octstream"
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

    def __init__(
        self,
        bucket,
        access_key, secret_key,
        expires=None, expires_in=None,
        allow_empty_md5=False
    ):
        self._bucket = bucket
        self._access_key = access_key

        if isinstance(secret_key, requests.compat.str):
            secret_key = secret_key.encode("utf8")

        self._secret_key = secret_key
        self._allow_empty_md5 = allow_empty_md5

        if isinstance(expires, (int, float)):
            self._expires = str(int(expires))
        elif isinstance(expires_in, (int, float)):
            self._expires = str(int(time.time() + expires_in))
        else:
            self._expires = None

    def set_more_headers(self, req, extra_headers=None):
        """Set content-type, content-md5, date to the request
        Returns a new `PreparedRequest`

        :param req: the origin unsigned request
        :param extra_headers: extra headers you want to set, pass as dict
        """
        oss_url = url.URL(req.url)
        req.headers.update(extra_headers or {})

        # set content-type
        content_type = req.headers.get("content-type")
        if content_type is None:
            content_type, __ = mimetypes.guess_type(oss_url.path)
        req.headers["content-type"] = content_type or self.DEFAULT_TYPE
        logger.info("set content-type to: {0}".format(content_type))

        # set date
        if self._expires is None:
            req.headers.setdefault(
                "date",
                time.strftime(self.TIME_FMT, time.gmtime())
            )
        else:
            req.headers["date"] = self._expires

        logger.info("set date to: {0}".format(req.headers["date"]))

        # set content-md5
        if req.body is not None:
            content_md5 = req.headers.get("content-md5", "")
            if not content_md5 and self._allow_empty_md5 is False:
                content_md5 = utils.cal_b64md5(req.body)
        else:
            content_md5 = ""
        req.headers["content-md5"] = content_md5
        logger.info("content-md5 to: [{0}]".format(content_md5))

        return req

    def get_signature(self, req):
        """calculate the signature of the oss request
        Returns the signatue
        """
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
        if isinstance(str_to_sign, requests.compat.str):
            str_to_sign = str_to_sign.encode("utf8")

        signature_bin = hmac.new(self._secret_key, str_to_sign, hashlib.sha1)
        signature = base64.b64encode(signature_bin.digest()).decode("utf8")
        logger.debug("signature is [{0}]".format(signature))
        return signature

    def __call__(self, req):
        """sign the request"""
        req = self.set_more_headers(req)
        signature = self.get_signature(req)

        if self._expires is None:
            # auth with headers
            req.headers["authorization"] = "OSS {0}:{1}".format(
                self._access_key, signature
            )
        else:
            # auth with url
            oss_url = url.URL(req.url)
            oss_url.append_params(dict(
                Expire=self._expires,
                OSSAccessKeyId=self._access_key,
                Signature=signature
            ))
            req.url = oss_url.forge(key=lambda x: x[0])
        return req
