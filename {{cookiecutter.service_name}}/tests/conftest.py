import pytest

from {{cookiecutter.service_name}} import create_app
from {{cookiecutter.service_name}}.models import db, User


@pytest.fixture()
def testapp(request):
    app = create_app('{{cookiecutter.service_name}}.settings.TestConfig')
    client = app.test_client()

    db.app = app
    db.create_all()

    if getattr(request.module, "create_user", True):
        admin = User('admin', 'supersafepassword')
        db.session.add(admin)
        db.session.commit()

    def teardown():
        db.session.remove()
        db.drop_all()

    request.addfinalizer(teardown)

    return client