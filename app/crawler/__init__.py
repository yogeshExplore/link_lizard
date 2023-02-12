from abc import ABC, abstractmethod


# todo create abstractmethod, would make sense only if knows other crawler requirements

class Crawler(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def run(self, **kwargs):
        pass
