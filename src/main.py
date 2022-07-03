import base64
import json
import random
from mitmproxy import http


class Proxy:
    def __init__(self):
        with open('config.json') as f:
            self.config = json.load(f)

    def request(self, flow: http.HTTPFlow):
        method = flow.request.method
        headers_base64 = base64.b64encode(json.dumps(dict(flow.request.headers.items())).encode()).decode()
        subdomain = random.choice(list(self.config['workers'].keys()))
        worker = random.choice(self.config['workers'][subdomain])

        if method == "GET":
            flow.request = flow.request.make(
                method="POST",
                url="https://{}.{}".format(worker, subdomain),
                content=json.dumps({"method": method, "url": flow.request.url, "headers": headers_base64}),
                headers={"Host": "{}.{}".format(worker, subdomain), "Content-Type": "application/json"},
            )
        elif method == "POST":
            body = flow.request.text
            body_base64 = base64.b64encode(body.encode()).decode()
            flow.request = flow.request.make(
                method="POST",
                url="https://{}.{}".format(worker, subdomain),
                content=json.dumps({"method": method, "url": flow.request.url, "headers": headers_base64, "body": body_base64}),
                headers={"Host": "{}.{}".format(worker, subdomain), "Content-Type": "application/json"},
            )


addons = [Proxy()]
