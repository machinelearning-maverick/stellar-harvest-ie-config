import pytest
from .logging_config import setup_logging


@pytest.fixture(scope="session", autouse=True)
def configure_logging():
    """
    This fixture runs once per test session, before any tests execute,
    and configures the root logger according to our logging_config.
    """
    setup_logging()
