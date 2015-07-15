# -*- coding:utf8 -*-

"""
aliyunauth.sign_ver_1_0
~~~~~~~~~~~~~~

This module contains the authentication handlers for Ali Sign Version 1.0
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


class AuthBase(requests.auth.AuthBase):
    """Attach Aliyun Ecs Authentication to the given request

    :param access_key: the access_key of your ecs account
    :param secret_key: the secret_key of your ecs account
    :param response_format: (optional) response format [`xml`/`json`(default)]
    :param ram: (optional) resource access managment string (default None)
    """
    DEFAULT_FORMAT = "json"
    SERVICE = None
    VERSION = None
    SIG = "Signature"
    SIG_METHOD = "HMAC-SHA1"
    SIG_VERSION = "1.0"
    TIME_FMT = "%Y-%m-%dT%XZ"
    PARAMS_MAP = {}

    def __init__(
        self,
        access_key, secret_key,
        response_format=None, ram=None
    ):
        if self.VERSION is None or self.SERVICE is None:
            raise NotImplementedError(
                "{0} {1}@{2} lack of necessary field".format(
                    self, self.SERVICE, self.VERSION
                )
            )

        self._access_key = access_key
        self._secret_key = secret_key
        self._format = response_format or self.DEFAULT_FORMAT
        self._ram = None

    def set_common_params(self, params):
        payload = params.copy()

        if self.SIG in payload:
            del payload[self.SIG]
        payload.setdefault("Format", self._format)
        payload[self.getkey("Version")] = self.VERSION
        payload[self.getkey("AccessKeyId")] = self._access_key
        payload[self.getkey("TimeStamp")] = \
            time.strftime(self.TIME_FMT, time.gmtime())
        payload[self.getkey("SignatureMethod")] = self.SIG_METHOD
        payload[self.getkey("SignatureVersion")] = self.SIG_VERSION
        payload[self.getkey("SignatureNonce")] = uuid.uuid4().hex

        if self._ram is not None:
            payload["ResourceOwnerAccount"] = self._ram

        return payload

    def getkey(self, key):
        return self.PARAMS_MAP.get(key, key)

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
        sign_url = url.URL(req.url)

        params = self.set_common_params(sign_url.params)
        logger.debug("compelete params are {0}".format(params))

        signature = self.sign(req.method, params)
        params[self.SIG] = signature

        logger.debug("signature of this request is {0}".format(signature))

        sign_url.params = params
        req.url = sign_url.forge(key=lambda x: x[0])

        return req
