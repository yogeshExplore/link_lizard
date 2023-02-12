# todo all services
class Service:
    def __init__(self):
        self._store = None
        self._request = None
        self._proxies = None

    def set_store_service(self, service_name, **kwargs):
        if service_name == 'file':
            from app.services.store import file
            self._store = file.File(**kwargs)
        if service_name == 'mongodb':
            from app.services.store import mongo_db
            self._store = mongo_db.MongoDb(**kwargs)

    def get_store_service(self):
        return self._store
