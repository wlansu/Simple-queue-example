import pytest
from django.test import Client as TestClient


@pytest.fixture
def client():
    client = TestClient()
    yield client
