from abc import ABC, abstractmethod


class Lrequest(ABC):
    def __init__(self):
        self.headers = {}
        self.cookies = {}
        self.agent = {}

    # todo implement
    def set_headers(self, headers):
        self.headers = headers

    # todo implement
    def set_cookies(self, cookies):
        self.cookies = cookies

    def get_headers(self):
        return self.headers

    def get_cookies(self):
        return self.cookies

    @abstractmethod
    def send_request(self, **kwargs):
        pass
