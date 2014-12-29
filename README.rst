Aliyun using python-requests
============================

.. image:: https://travis-ci.org/SkyLothar/requests-aliyun.svg?branch=master
    :target: https://travis-ci.org/SkyLothar/requests-aliyun

.. image:: https://coveralls.io/repos/SkyLothar/requests-aliyun/badge.png
    :target: https://coveralls.io/r/SkyLothar/requests-aliyun

.. image:: https://requires.io/github/SkyLothar/requests-aliyun/requirements.svg?branch=master
    :target: https://requires.io/github/SkyLothar/requests-aliyun/requirements/?branch=master

.. image:: https://pypip.in/py_versions/requests-aliyun/badge.svg?style=flat
    :target: https://pypi.python.org/pypi/requests-aliyun/
    :alt: Supported Python versions

.. image:: https://pypip.in/license/requests-aliyun/badge.svg?style=flat
    :target: https://pypi.python.org/pypi/requests-aliyun/
    :alt: License

Aliyun authentication for the awesome requests!
-----------------------------------------------

- [x] OSS (api-version: 2014-08-28)
- [x] ECS (api-version: 2014-05-26)
- [x] RDS (api-version: eta 2014-08-15)


Play with Oss
-------------
Full api document avaiable at: `OSS API`_

.. code-block:: python

    >>> import requests
    >>> from aliyunauth import OssAuth
    >>> req = request.get(
    ...     "http://bucket-name.oss-url.com/path/to/file",
    ...     auth=OssAuth("bucket-name", "access-key", "secret-key")
    ... )
    <Response [200]>

Play with ECS
-------------
Full api document avaiable at: `ECS API`_

.. code-block:: python

    >>> import requests
    >>> from aliyunauth import EcsAuth
    >>> req = request.get(
    ...     "https://ecs.aliyuncs.com",
    ...     params=dict(Action="DescribeInstanceTypes"),
    ...     auth=EcsAuth("access-key", "secret-key")
    ... )
    <Response [200]>

Play with RDS
-------------
Full api document avaiable at: `RDS API`_

.. code-block:: python

    >>> import requests
    >>> from aliyunauth import RdsAuth
    >>> req = request.get(
    ...     "https://rds.aliyuncs.com",
    ...     params=dict(Action="DescribeDBInstances", RegionId="cn-hangzhou")
    ...     auth=RdsAuth("access-key", "secret-key")
    ... )
    <Response [200]>

.. _OSS API: http://imgs-storage.cdn.aliyuncs.com/help/oss/oss%20api%2020140828.pdf
.. _ECS API: http://aliyunecs.oss.aliyuncs.com/ECS-API-Reference%202014-05-26.pdf
.. _RDS API: http://imgs-storage.cdn.aliyuncs.com/help/rds/RDS-API-Reference.pdf
