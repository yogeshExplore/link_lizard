from app import Config, logger
from app.services.store import Store
from app.connections.mongo_db import MongoDb as MongoDbConnection
from time import time


# todo we can use Factory , and Dependency injection also


class MongoDb(Store):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._client = MongoDbConnection().connection
        self.db = self._client[Config.MONGODB['database']]
        self.coll_name = str(int(time()))
        self.coll = self.db[self.coll_name]

    def client(self):
        self._client = MongoDbConnection().connection
        return self._client

    def write(self, output_chunk: list):
        output_chunk_list_dict = []
        for items in output_chunk:
            output_chunk_list_dict.append({'origin_url': items[0], 'target_url': items[1]})
        if output_chunk_list_dict:
            logger.info(f"[MONDODB] Writing {len(output_chunk_list_dict)} rows")
            self.coll.insert_many(output_chunk_list_dict)

    def read(self):
        pass

    def delete(self):
        pass
