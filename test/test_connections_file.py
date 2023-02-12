from app.setting import Setting
from app.connections import file
from os import path
from test import tc

FILE_NAME = "test_connection"
FILE_MODE = 'w'


# todo fixures
# todo argument passing
# todo tear down implementations
def test_file_set_connection_parameter_s1(tc):
    f = file.File()
    f.set_connection_parameter(file_name=FILE_NAME, mode=FILE_MODE)
    assert f._connection_parameter['file_name'] == str(path.join(Setting.OUTPUT_DIR, f"{Setting.FILE_PREFIX}_{FILE_NAME}"))
    assert f._connection_parameter['mode'] == FILE_MODE


def test_file_get_connection_parameter_s1(tc):
    f = file.File()
    f.set_connection_parameter(file_name=FILE_NAME, mode=FILE_MODE)
    conn_params = f.get_connection_parameter()
    assert conn_params['file_name'] == str(path.join(Setting.OUTPUT_DIR, f"{Setting.FILE_PREFIX}_{FILE_NAME}"))
    assert conn_params['mode'] == FILE_MODE


def test_file_set_connection_s1(tc):
    f = file.File()
    f.set_connection_parameter(file_name=FILE_NAME, mode=FILE_MODE)
    f.set_connection()
    assert f._connection.name == str(path.join(Setting.OUTPUT_DIR, f"{Setting.FILE_PREFIX}_{FILE_NAME}"))
    assert f._connection.mode == FILE_MODE
    assert f._connection.closed is False
