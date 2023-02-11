import os
from app import logger
from app import Setting
from time import time


class File:
    def __init__(self) -> None:
        self._connection_parameter = None
        self._connection = None

    def set_connection_parameter(self, **kwargs):
        self._connection_parameter = {
            "file_name": os.path.join(Setting.OUTPUT_DIR, f"{Setting.FILE_PREFIX}_{int(time())}")
            if not kwargs.get('file_name')
            else os.path.join(Setting.OUTPUT_DIR, f"{Setting.FILE_PREFIX}_{kwargs.get('file_name')}"),
            "mode": 'w'
        }

    def get_connection_parameter(self):
        return self._connection_parameter

    def set_connection(self):
        if self._connection_parameter is None:
            self.set_connection_parameter()
        try:
            logger.info(f"Opening file {self._connection_parameter['file_name']}")
            conn = open(self._connection_parameter['file_name'], self._connection_parameter['mode'])
            self._connection = conn

        except Exception as ce:
            logger.error(f"[FILE] Error in opening file {self._connection_parameter['file_name']} ,error={ce}")
            raise Exception(f"[FILE] Error in opening file {self._connection_parameter['file_name']}")

    @property
    def connection(self):
        if self._connection is None or not self._connection.closed:
            self.set_connection()
        return self._connection

    def close_connection(self):
        if self._connection is not None:
            try:
                self._connection.close()
            except Exception as e:
                logger.error(f'[FILE] Unable to close file, file might be already closed. Error : {e}')
            finally:
                self._connection = None
                self._connection_parameter = None
        return self._connection
