import hashlib
import os

import purl

from . import consts


def parse_query(url):
    """parse url query part into dict

    :param url: url to parse

    Usage::

        >>> params = parse_query("http://www.example.com/?foo=bar&baz")
        {'foo': 'bar', 'baz': None}

    """
    parsed_url = purl.URL(url)
    params = {
        key: val[0] if val[0] else None
        for key, val in parsed_url.query_params().items()
    }
    return params


def cal_md5(data):
    """

    :param data: cal md5 checksum for this piece data

    Usage::

        >>> cal_md5(io.BytesIO(b"hello world"))
        5eb63bbbe01eeed093cb22bb8f5acdc3

    """
    md5sum = hashlib.md5()
    if hasattr(data, "read") and hasattr(data, "seek"):
        # file-like object or IO-like object
        data_piece = data.read(consts.MD5_CHUNK_SIZE)
        while data_piece:
            md5sum.update(data_piece)
            data_piece = data.read(consts.MD5_CHUNK_SIZE)
        data.seek(0, os.SEEK_SET)
    else:
        md5sum.update(data)
    return md5sum.hexdigest()
