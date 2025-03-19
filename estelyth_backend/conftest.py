import pytest

from estelyth_backend.agents.models import Company
from estelyth_backend.agents.models import Seller
from estelyth_backend.agents.tests.factories import CompanyFactory
from estelyth_backend.agents.tests.factories import SellerFactory
from estelyth_backend.locations.models import Address
from estelyth_backend.locations.tests.factories import AddressFactory
from estelyth_backend.users.models import User
from estelyth_backend.users.tests.factories import AdminUserFactory
from estelyth_backend.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def _media_storage(settings, tmpdir) -> None:
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user(db) -> User:
    return UserFactory()


@pytest.fixture
def another_user(db) -> User:
    return UserFactory()


@pytest.fixture
def admin(db) -> User:
    return AdminUserFactory()


@pytest.fixture
def address(db) -> Address:
    return AddressFactory()


@pytest.fixture
def company(db) -> Company:
    return CompanyFactory()


@pytest.fixture
def seller(db) -> Seller:
    return SellerFactory()
