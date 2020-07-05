import pytest
from src.simulator import get_new_worker_id


def test_get_new_worker_id():
    assert get_new_worker_id(2) == 3
