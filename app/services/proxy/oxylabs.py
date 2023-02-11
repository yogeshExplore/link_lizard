from app.services.proxy import Proxy


# Todo access Free Proxy available online


class Oxylabs(Proxy):
    def __init__(self):
        super().__init__()

    # todo implement
    def get_proxy(self):
        self.proxy_count += 1
        return {}
