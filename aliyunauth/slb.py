# -*- coding:utf8 -*-

"""
aliyunauth.slb
~~~~~~~~~~~~~~

This module contains the authentication handlers for Ali Slb Service
"""

from . import sign_ver_1_0


class SlbAuth(sign_ver_1_0.AuthBase):
    """Attach Aliyun Slb Authentication to the given request

    :param access_key: the access_key of your slb account
    :param secret_key: the secret_key of your slb account
    :param response_format: (optional) response format [`xml`/`json`(default)]
    :param ram: (optional) resource access managment string (default None)

    Usage::

        >>> import requests
        >>> from aliyunauth import SlbAuth
        >>> req = request.get(
        ...     "https://slb.aliyuncs.com",
        ...     params=dict(Action="DescribeRegions"),
        ...     auth=EcsAuth("access-key", "secret-key")
        ... )
        <Response [200]>

    """
    SERVICE = "slb"
    VERSION = "2014-05-15"
