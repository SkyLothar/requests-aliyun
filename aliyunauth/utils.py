import purl


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
        for key, val in parsed_url.query_params()
    }
    return params
