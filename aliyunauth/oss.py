import base64
import hashlib
import hmac
import logging
import mimetypes
import time

import requests


from . import consts
from . import url
from . import utils


logger = logging.getLogger(__name__)


def mk_pair(key, val):
    return '{0}={1}'.format(key, val)


class OssAuth(requests.auth.AuthBase):
    """Attach Aliyun OSS Authentication to the given request"""
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

    def __init__(self, app_key, secret_key, allow_empty_md5=False):
        self._app_key = app_key
        self._secret_key = secret_key
        self._allow_empty_md5 = allow_empty_md5

        self._url = None
        self._path = None
        self._params = None
        self._content_md5 = None
        self._content_type = None

    def analysis_request(self, req):
        parsed_url = url.URL(req.url)

        # remove all query
        self._url = parsed_url.query_params({})

        # get params dict including flags
        self._params = {
            key: val[0] if val[0] else None
            for key, val in parsed_url.query_params().items()
        }

        # cal content-md5
        content_md5 = req.headers.get("content-md5", "")
        if not content_md5 and self._allow_empty_md5 is False:
            content_md5 = utils.cal_md5(req.body)

        # guess content-type
        content_type, encoding = mimetypes.guess_type(self._url)
        self._content_type = content_type or "application/octet-stream"

    def __call__(self, req):
        self.analysis_request(req)

        expire = self._params.get("Expires")

        if expire is None:
            date = expire
        else:
            date = time.strftime(self.TIME_FMT, time.gmtime())

        # canonicalize resources
        canonicalized_header_str = self.canonicalize_oss_headers(req.headers)
        req.url = canonicalized_uri = self.canonicalize_uri(
            self._url.path(),
            self._params
        )
        canonicalized_str = canonicalized_header_str + canonicalized_uri

        # sign this request
        str_to_sign = "\n".join([
            req.method,
            self._content_md5,
            self._content_type,
            date,
            canonicalized_str
        ])
        signature = hmac.new(self._secret_key, str_to_sign, hashlib.sha1)
        b64_signature = base64.b64encode(signature.digest())

        if expire:
            # expire can only be signed with url
            req.url = "?".format(canonicalize_uri)

            date = params["Expires"]
            params["OSSAccessKeyId"] = self._app_key
            params["Signature"] = signature
        else:
            # normaly we sign with header
            self._headers["date"] = date
            self._headers["authorization"] = "OSS {0}:{1}".format(
                self._app_key, signature
            )

        return req

    def canonicalize_oss_headers(self, headers):
        oss_headers = [
            "{0}:{1}".format(key, val)
            for key, val in sorted(headers.lower_items(), key=lambda k: k[0])
            if key.startswith(consts.X_OSS_PREFIX)
        ]
        return "\n".join(oss_headers)

    def canonicalize_uri(self,  path, params):
        """
        returns new path of url
        canonicalize resources
        """
        query_list = []
        for key, val in params.items():
            if key in self.SUB_RESOURCES:
                logger.debug("found sub resource: {0}={1}".format(key, val))
                query_list.append(key if val is None else mk_pair(key, val))
            elif key in self.OVERRIDE_QUERIES:
                logger.debug("found override_query: {0}={1}".format(key, val))
                query_list.append(mk_pair(key, val))
            else:
                logger.info("unrecognized params: {0}={1}".format(key, val))

        uri = "{0}?{1}".format(path, "&".join(sorted(query_list)))
        return uri
