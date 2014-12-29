# -*- coding:utf8 -*-

"""
aliyunauth.rds
~~~~~~~~~~~~~~

This module contains the authentication handlers for Ali Rds Service
"""

from . import sign_ver_1_0


class RdsAuth(sign_ver_1_0.AuthBase):
    """Attach Aliyun Rds Authentication to the given request

    :param access_key: the access_key of your ecs account
    :param secret_key: the secret_key of your ecs account
    :param response_format: (optional) response format [`xml`/`json`(default)]
    :param ram: (optional) resource access managment string (default None)

    Usage::

        >>> import requests
        >>> from aliyunauth import RdsAuth
        >>> req = request.get(
        ...     "https://rds.aliyuncs.com",
        ...     params=dict(Action="DescribeInstanceTypes"),
        ...     auth=EcsAuth("access-key", "secret-key")
        ... )
        <Response [200]>

    """
    SERVICE = "rds"
    VERSION = "2014-08-15"
