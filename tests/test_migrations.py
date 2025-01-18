import os
import pytest
from pytest_alembic.tests import (
    test_single_head_revision,  # noqa
    test_up_down_consistency,  # noqa
    test_upgrade,  # noqa
)


@pytest.fixture(autouse=True)
def set_testing_environment():
    """Set the TESTING environment variable for all tests."""
    os.environ["TESTING"] = "1"
    yield
    del os.environ["TESTING"]
