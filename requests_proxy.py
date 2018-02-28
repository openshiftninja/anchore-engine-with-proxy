import requests
import json
import logging

from urllib import quote

proxy_root_url = "http://anchore-proxy:5000"
proxy_get_url = proxy_root_url + "/get?target={}&headers={}"
proxy_post_url = proxy_root_url + "/post?target={}&headers={}"
logger = logging.getLogger(__name__)


def get(url, **kwargs):
    if str(url).startswith("https://ancho.re"):
        headers = kwargs['headers'] or {}
        headers_str = quote(json.dumps(headers))
        return requests.get(proxy_get_url.format(quote(url), headers_str))
    else:
        return requests.get(url, kwargs)


def post(url, **kwargs):
    if str(url).startswith("https://ancho.re"):
        headers = kwargs['headers'] or {}
        post_data = kwargs['data'] or {}
        headers_str = quote(json.dumps(headers))
        return requests.post(proxy_post_url.format(quote(url), headers_str), data=post_data)
    else:
        return requests.post(url, kwargs)
