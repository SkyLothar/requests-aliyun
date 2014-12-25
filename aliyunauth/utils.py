# -*- coding:utf8 -*-

import hashlib
import os

import requests

from . import consts


def cal_md5(data):
    """

    :param data: cal md5 checksum for this piece data

    Usage::

        >>> cal_md5(io.BytesIO(b"hello world"))
        5eb63bbbe01eeed093cb22bb8f5acdc3

    """
    if data is None:
        return None
    md5sum = hashlib.md5()
    if hasattr(data, "read") and hasattr(data, "seek"):
        # file-like object or IO-like object
        data_piece = data.read(consts.MD5_CHUNK_SIZE)
        while data_piece:
            if isinstance(data_piece, requests.compat.str):
                data_piece = data_piece.encode("utf8")
            md5sum.update(data_piece)
            data_piece = data.read(consts.MD5_CHUNK_SIZE)
        data.seek(0, os.SEEK_SET)
    else:
        if isinstance(data, requests.compat.str):
            data = data.encode("utf8")
        md5sum.update(data)
    return md5sum.hexdigest()


def to_bytes(some_str, encoding="utf8"):
    if isinstance(some_str, requests.compat.str):
        some_bytes = some_str.encode(encoding)
    else:
        some_bytes = some_str
    return some_bytes


def to_str(some_bytes, encoding="utf8"):
    if isinstance(some_bytes, requests.compat.bytes):
        some_str = some_bytes.decode(encoding)
    else:
        some_str = some_bytes
    return some_str


def percent_quote(query):
    return requests.compat.quote(to_bytes(query), consts.PERCENT_SAFE)


def percent_encode(params_tuple, sort=False):
    if sort:
        params = sorted(params_tuple, key=lambda x: x[0])
    else:
        params = list(params_tuple)

    encoded = "&".join([
        "{0}={1}".format(percent_quote(opt), percent_quote(val))
        for opt, val in params
        if val is not None
    ])
    return encoded
