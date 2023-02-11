from app.services.store import Store


class Postgresql(Store):
    def __init__(self):
        super().__init__()
        return

    def client(self):
        pass

    def write(self, output_chunk: list):
        pass

    def read(self):
        pass

    def delete(self):
        pass
