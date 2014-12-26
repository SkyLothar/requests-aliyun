# -*- coding:utf8 -*-

"""
aliyunauth.ecs
~~~~~~~~~~~~~~

This module contains the authentication handlers for Ali Ecs Service
"""

import base64
import hashlib
import hmac
import logging
import time
import uuid

import requests

from . import url
from . import utils


logger = logging.getLogger(__name__)


class EcsAuth(requests.auth.AuthBase):
    """Attach Aliyun Ecs Authentication to the given request

    :param access_key: the access_key of your ecs account
    :param secret_key: the secret_key of your ecs account
    :param response_format: (optional) response format [`xml`/`json`(default)]
    :param ram: (optional) resource access managment string (default None)

    Usage::

        >>> import requests
        >>> from aliyunauth import EcsAuth
        >>> req = request.get(
        ...     "https://ecs.aliyuncs.com",
        ...     params=dict(Action="DescribeInstanceTypes"),
        ...     auth=EcsAuth("access-key", "secret-key")
        ... )
        <Response [200]>

    """
    DEFAULT_FORMAT = "json"
    VERSION = "2014-05-26"
    SIG = "Signature"
    SIG_METHOD = "HMAC-SHA1"
    SIG_VERSION = "1.0"
    TIME_FMT = "%Y-%m-%dT%XZ"

    def __init__(
        self,
        access_key, secret_key,
        response_format=None, ram=None
    ):
        self._access_key = access_key
        self._secret_key = secret_key
        self._format = response_format or self.DEFAULT_FORMAT
        self._ram = None

    def set_common_params(self, params):
        payload = params.copy()

        if self.SIG in payload:
            del payload[self.SIG]
        payload.setdefault("Format", self._format)
        payload["Version"] = self.VERSION
        payload["AccessKeyId"] = self._access_key
        payload["TimeStamp"] = time.strftime(self.TIME_FMT, time.gmtime())
        payload["SignatureMethod"] = self.SIG_METHOD
        payload["SignatureVersion"] = self.SIG_VERSION
        payload["SignatureNonce"] = uuid.uuid4().hex

        if self._ram is not None:
            payload["ResourceOwnerAccount"] = self._ram

        return payload

    def sign(self, method, params):
        """Calculate signature with the SIG_METHOD(HMAC-SHA1)
        Returns a base64 encoeded string of the hex signature

        :param method: the http verb
        :param params: the params needs calculate
        """
        query_str = utils.percent_encode(params.items(), True)

        str_to_sign = "{0}&%2F&{1}".format(
            method, utils.percent_quote(query_str)
        )

        sig = hmac.new(
            utils.to_bytes(self._secret_key + "&"),
            utils.to_bytes(str_to_sign),
            hashlib.sha1
        )
        return base64.b64encode(sig.digest())

    def __call__(self, req):
        """Sign the request"""
        ecs_url = url.URL(req.url)

        params = self.set_common_params(ecs_url.params)
        logger.debug("compelete params are {0}".format(params))

        signature = self.sign(req.method, params)
        params[self.SIG] = signature

        logger.debug("signature of this request is {0}".format(signature))

        ecs_url.params = params
        req.url = ecs_url.forge(key=lambda x: x[0])

        return req
