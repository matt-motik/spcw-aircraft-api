import logging

from src.logger_creator import create_logger


def test_create_logger():
    logger = create_logger("test_logger")
    assert logger.name == "test_logger"
    assert logger.level == logging.DEBUG


def test_create_logger_creates_dir(tmp_path, monkeypatch):
    monkeypatch.setattr("src.logger_creator.get_log_path", lambda: str(tmp_path / "new_logs"))
    logger = create_logger("test")
    assert logger.name == "test"
    assert (tmp_path / "new_logs").exists()
