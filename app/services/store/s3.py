from app.services.store import Store
# todo we can use Factory , and Dependency injection also


class S3(Store):
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
