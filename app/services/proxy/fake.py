from app.services.proxy import Proxy


class Fake(Proxy):
    def __init__(self):
        super().__init__()

    def get_proxy(self):
        return {}
