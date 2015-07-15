# -*- coding:utf8 -*-

"""
aliyunauth.cms
~~~~~~~~~~~~~~

This module contains the authentication handlers for Ali Cms Service
"""

from . import sign_ver_1_0


class CmsAuth(sign_ver_1_0.AuthBase):
    """Attach Aliyun Rds Authentication to the given request

    :param access_key: the access_key of your ecs account
    :param secret_key: the secret_key of your ecs account
    :param response_format: (optional) response format [`xml`/`json`(default)]
    :param ram: (optional) resource access managment string (default None)

    Usage::

        >>> import requests
        >>> from aliyunauth import CmsAuth
        >>> req = requests.get(
        ...     "https://metrics.aliyuncs.com",
        ...     params=dict(
        ...         Action="DescribeMetricDatum",
        ...         Namespace="acs/ecs",
        ...         MetricName="vm.MemoryUtilization",
        ...         StartTime="2015-05-15T00:00:00Z",
        ...         Dimensions=json.dumps(dict(instanceId="instance-id"))
        ...     ),
        ...     auth=CmsAuth("access-key", "secret-key")
        ... )
        <Response [200]>

    """
    PARAMS_MAP = dict(TimeStamp="Timestamp")
    SERVICE = "cms"
    VERSION = "2015-04-20"
