from app import logger
import os
from pymongo import MongoClient


class MongoDb:
    def __init__(self) -> None:
        self._connection_parameter = None
        self._connection = None

    def set_connection_parameter(self, **kwargs):
        self._connection_parameter = {
            "user": os.environ.get('MONGODB_USER') if not kwargs.get('user') else kwargs.get('user'),
            "password": os.environ.get('MONGODB_PASSWORD') if not kwargs.get('password') else kwargs.get('password'),
            "host": os.environ.get('MONGODB_HOST') if not kwargs.get('host') else kwargs.get('host'),
            "port": int(os.environ.get('MONGODB_PORT')) if not kwargs.get('port') else kwargs.get('port'),
            "database": os.environ.get('MONGODB_DATABASE') if not kwargs.get('database') else kwargs.get('database')
        }

    def get_connection_parameter(self):
        return self._connection_parameter

    def set_connection(self):
        logger.info("Setting MongoDB connection")
        if self._connection_parameter is None:
            self.set_connection_parameter()

        try:
            conn = MongoClient(
                username=self._connection_parameter['user'],
                password=self._connection_parameter['password'],
                host=self._connection_parameter['host'],
                port=self._connection_parameter['port'],
                tz_aware=True,
                connect=True,
                serverSelectionTimeoutMS=10
            )
            self._connection = conn
            self._connection.server_info()

        except Exception as ce:
            logger.error(f'''[MONGODB] Error in making mongodb connection with
                host {self._connection_parameter['host']} ,
                port {self._connection_parameter['port']} ,
                user {self._connection_parameter['user']} ,
                database {self._connection_parameter['database']} ,
                error={ce}''')
            raise Exception(f"[MONGODB] Connection Error with MongoDb connection {str(self._connection)}")

    @property
    def connection(self):
        logger.info('Getting MongoDB connection')
        if self._connection is None or not hasattr(self._connection, 'is_primary'):
            self.set_connection()
        return self._connection

    def close_connection(self):
        if self._connection is not None:
            try:
                self._connection.close()
            except Exception as e:
                logger.error(f'[MONGODB] Unable to close mongodb connection. '
                             f'Connection might be already closed. Error : {e}')
            finally:
                self._connection = None
                self._connection_parameter = None
        return self._connection
