from app import logger
from app.services.store import Store
from app.connections.file import File as FileConnection


class File(Store):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._client = FileConnection().connection

    def client(self):
        self._client = FileConnection().connection
        return self._client

    def write(self, output_chunk: list):
        logger.info(f"[FILE] Writing {len(output_chunk)} rows")
        output_chunk_str = '\n'.join(f"{element[0]}->{element[1]}" for element in output_chunk)
        self._client.write(output_chunk_str)
        self._client.flush()

    def read(self):
        pass

    def delete(self):
        pass
