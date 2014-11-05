import logging

import requests
import requests.packages.urllib3

from . import consts


logger = logging.getLogger(__name__)


def mk_pair(key, val):
    return '{0}={1}'.format(key, val)


class OssAuth(requests.auth.AuthBase):
    """Attach Aliyun OSS Authentication to the given request"""
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

    def __init__(
        self,
        app_key,
        secret_key,
        sub_resources=None,
        override_query=None
    ):
        self._app_key = app_key
        self._secret_key = secret_key

        self._sub_resources = sub_resources
        self._override_query = override_query

    def __call__(self, req):
        return req

    def canonicalize_oss_headers(self, headers):
        oss_headers = [
            '{0}:{1}'.format(key, val)
            for key, val in sorted(headers.lower_items(), key=lambda k: k[0])
            if key.startswith(consts.X_OSS_PREFIX)
        ]
        return '\n'.join(oss_headers)

    def canonicalize_resources(self, query):
        query_list = []
        for key, val in query.items():
            if key in self.SUB_RESOURCES:
                logger.debug('found sub resource: {0}={1}'.format(key, val))
                query_list.append(key if val is None else mk_pair(key, val))
            elif key in self.OVERRIDE_QUERIES:
                logger.debug('found override_query: {0}={1}'.format(key, val))
                query_list.append(mk_pair(key, val))

        return ''
