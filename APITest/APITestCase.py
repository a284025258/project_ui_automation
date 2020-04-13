import requests


class APITestCase:

    def __init__(self, obj, ):
        self.req = obj.method, obj.url, obj.headers,

    def run_case(self):
        requests.request()
    #
    # def init
