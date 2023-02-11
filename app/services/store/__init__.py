from abc import ABC, abstractmethod


class Store(ABC):
    def __init__(self, **kwargs):
        self._client = None

    @property
    @abstractmethod
    def client(self):
        pass

    @abstractmethod
    def write(self, output_chunk: list):
        pass

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    def close(self):
        self._client.close()
