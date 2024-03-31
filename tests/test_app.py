

from app.models import User
from app.forms.form import RegistrationForm
import pytest
from app import db as _db
from app import create_app



@pytest.fixture(scope='session')
def app():
    """Create and configure a new app instance for each test session."""
    app = create_app()
    app.config.from_object("config.Testing")
    with app.app_context():
        yield app
        _db.drop_all()


@pytest.fixture
def client(app, db):
    """Create a test client for the app."""
    with app.test_client() as client:
        with app.app_context():
            yield client



@pytest.fixture(scope='session')
def db(app):
    """Initialize and clean up the database."""
    _db.app = app
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.remove()
        _db.drop_all()




def test_registration_form_validation(client):
    # Test form validation with invalid data
    with client:
        with client.session_transaction() as sess:
            sess['csrf_token'] = 'test_csrf_token'  # Mock CSRF token for testing
        form = RegistrationForm(
            username='a',  # Invalid username length
            email='invalid_email',  # Invalid email format
            password='password',
            confirm_password='password'
        )
        assert not form.validate()