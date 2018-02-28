import json
import logging
import sys
from urllib.parse import unquote

import requests
from flask import Flask
from flask import Response
from flask import request


def init_logger():
    log_level = logging.INFO
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    new_logger = logging.getLogger(__name__)
    new_logger.setLevel(log_level)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(log_level)
    ch.setFormatter(formatter)
    new_logger.addHandler(ch)
    return new_logger


logger = init_logger()
app = Flask(__name__)


class ProxyRequest:
    def __init__(self, is_post=False):
        self.is_post = is_post
        self.target_url = unquote(request.args.get('target'))
        try:
            if request.args.get('headers'):
                self.headers = json.loads(unquote(request.args.get('headers')))
            else:
                self.headers = {}
        except Exception:
            raise Exception("Invalid headers param")
        if is_post:
            self.post_data = self.get_post_data()

    def make_request(self):
        if self.is_post:
            response = requests.post(url=self.target_url, headers=self.headers, data=self.post_data)
        else:
            response = requests.get(url=self.target_url, headers=self.headers)

        if response.status_code == 200:
            content_type = response.headers.get('Content-Type')
            return Response(response.content, content_type=content_type, mimetype=content_type, status=200)
        else:
            return Response("ERROR: request returned status of {}".format(response.status_code), status=400)

    @staticmethod
    def get_post_data():
        if request.form:
            return request.form
        elif request.data:
            return request.data
        else:
            return ""


@app.route('/get')
def proxy_get():
    try:
        req = ProxyRequest()
        return req.make_request()
    except Exception:
        return Response("ERROR: badly formatted request", status=400)


@app.route('/post', methods=['POST'])
def proxy_post():
    try:
        req = ProxyRequest(is_post=True)
        return req.make_request()
    except Exception:
        return Response("ERROR: badly formatted request", status=400)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
