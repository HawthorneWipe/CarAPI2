import pytest
import dj_database_url


@pytest.fixture(scope="session")
def django_db_setup():
    DATABASES = {}
    DATABASES["default"] = dj_database_url.config()
