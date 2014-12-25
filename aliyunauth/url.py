import requests


__all__ = ["URL"]


if requests.compat.is_py2:
    from urlparse import parse_qs
elif requests.compat.is_py3:
    from urllib.parse import parse_qs

from . import utils


class URL(object):
    def __init__(self, url_str):
        """parse url query part into dict

        :param url: url to parse

        Usage::

            >>> params = parse_query("http://www.example.com/?foo=bar&baz")
            {'foo': 'bar', 'baz': None}

        """
        parsed_url = requests.compat.urlparse(utils.to_str(url_str))
        netloc_parts = parsed_url.netloc.split("@")
        if len(netloc_parts) == 1:
            username = password = None
            host_str = netloc_parts[0]
        else:
            username, password = netloc_parts[0].split(":")
            host_str = netloc_parts[1]

        host_parts = host_str.split(":")
        host = host_parts[0]

        if len(host_parts) == 1:
            port = 80
        else:
            port = int(host_parts[1])

        params = [
            (key, val[0] if val[0] else None)
            for key, val in parse_qs(parsed_url.query, True).items()
        ]

        self._info = dict(
            scheme=parsed_url.scheme or "http",
            username=username,
            password=password,
            host=host,
            port=port,
            path=parsed_url.path or "/",
            params=params,
            fragment=parsed_url.fragment
        )
        self._url = None

    def forge(self, **kwargs):
        if kwargs:
            self._info["params"].sort(**kwargs)

        parts = [
            "{0}://".format(self.scheme),
            self.netloc,
            self.uri
        ]
        self._url = utils.to_str("".join(parts))
        return self._url

    def __str__(self):
        if self._url is None:
            self.forge()
        return self._url

    @property
    def scheme(self):
        return self._info["scheme"]

    @property
    def netloc(self):
        if self.username is None or self.password is None:
            netloc = self.host
        else:
            netloc = "{0}:{1}@{2}".format(
                self.username,
                self.password,
                self.host
            )
        if self.port != 80:
            netloc = "{0}:{1}".format(netloc, self.port)
        return netloc

    @property
    def username(self):
        return self._info["username"]

    @property
    def password(self):
        return self._info["password"]

    @property
    def host(self):
        return self._info["host"]

    @property
    def port(self):
        return self._info["port"]

    @property
    def path(self):
        return self._info["path"]

    @path.setter
    def path(self, new_val):
        self._info["path"] = new_val
        return new_val

    @property
    def params(self):
        return dict(self._info["params"])

    @params.setter
    def params(self, new_params):
        if isinstance(new_params, dict):
            self._info["params"] = list(new_params.items())
        else:
            self._info["params"] = list(new_params)
        return new_params

    @property
    def query(self):
        query = []
        for key, val in self._info["params"]:
            if val is None:
                query.append(requests.compat.quote(utils.to_bytes(key)))
            else:
                param = {utils.to_bytes(key): utils.to_bytes(val)}
                query.append(requests.compat.urlencode(param))
        return "&".join(query)

    @property
    def uri(self):
        query = self.query
        fragment = self.fragment
        return "".join([
            self.path,
            "?{0}".format(query) if query else "",
            "#{0}".format(fragment) if fragment else ""
        ])

    def append_params(self, new_params):
        params = dict(self.params, **dict(new_params))
        self.params = params
        return self.params

    @property
    def fragment(self):
        return self._info["fragment"]
