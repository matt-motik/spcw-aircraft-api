from src.path import get_data_dir
from src.path import get_log_path
from src.path import get_root_dir


def test_get_root_dir():
    path = get_root_dir()
    assert isinstance(path, str)
    assert len(path) > 0


def test_get_log_path():
    path = get_log_path()
    assert isinstance(path, str)
    assert "logs" in path


def test_get_data_dir():
    path = get_data_dir()
    assert isinstance(path, str)
    assert "data" in path
