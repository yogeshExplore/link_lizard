from abc import ABC, abstractmethod

# todo use session, use proxy if get special kind of error like


class Proxy(ABC):
    def __init__(self):
        self.proxy_count = 0

    @abstractmethod
    def get_proxy(self):
        pass
