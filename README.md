Aliyun using python-requests
============================
[![Build Status][travis-image]][travis-url]
[![Coverage Status][coverage-image]][coverage-url]
[![Requirements Status][req-status-image]][req-status-url]


## Aliyun authentication for the awesome requests!

- [x] OSS (api-version: 2014-08-28)
- [x] ECS (api-version: 2014-05-26)
- [ ] RDS (work in process: eta 2014-12)


## Usage:

Play with Oss
-------------
Full api document avaiable at: [OSS API][oss-api]
```python
>>> import requests
>>> from aliyunauth import OssAuth
>>> req = request.get(
...     "http://bucket-name.oss-url.com/path/to/file",
...     auth=OssAuth("bucket-name", "access-key", "secret-key")
... )
<Response [200]>
```

Play with ECS
-------------
Full api document avaiable at: [ECS API][ecs-api]
```python
>>> import requests
>>> from aliyunauth import EcsAuth
>>> req = request.get(
...     "https://ecs.aliyuncs.com",
...     params=dict(Action="DescribeInstanceTypes"),
...     auth=EcsAuth("access-key", "secret-key")
... )
<Response [200]>
```

[travis-url]: https://travis-ci.org/SkyLothar/requests-aliyun
[travis-image]: https://travis-ci.org/SkyLothar/requests-aliyun.svg?branch=master
[coverage-image]: https://coveralls.io/repos/SkyLothar/requests-aliyun/badge.png
[coverage-url]: https://coveralls.io/r/SkyLothar/requests-aliyun
[req-status-url]: https://requires.io/github/SkyLothar/requests-aliyun/requirements/?branch=master
[req-status-image]: https://requires.io/github/SkyLothar/requests-aliyun/requirements.svg?branch=master

[oss-api]: http://imgs-storage.cdn.aliyuncs.com/help/oss/oss%20api%2020140828.pdf
[ecs-api]: http://aliyunecs.oss.aliyuncs.com/ECS-API-Reference%202014-05-26.pdf
