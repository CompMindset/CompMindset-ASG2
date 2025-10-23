import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User
from App.controllers import (
    create_user,
    get_all_users_json,
    login,
    get_user,
    get_user_by_username,
    update_user
)


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User("Bob Smith", "bob@email.com", "bob", "bobpass", "STAFF")
        assert user.username == "bob"

    # pure function no side effects or integrations called
    def test_get_json(self):
        user = User("Bob Smith", "bob@email.com", "bob", "bobpass", "STAFF")
        user_json = user.get_json()
        self.assertDictEqual(user_json, {"id":None, "username":"bob", "full_name":"Bob Smith", "email":"bob@email.com", "role":"STAFF"})
    
    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='pbkdf2:sha256')
        user = User("Bob Smith", "bob@email.com", "bob", password, "STAFF")
        assert user.password_hash != password

    def test_check_password(self):
        password = "mypass"
        user = User("Bob Smith", "bob@email.com", "bob", password, "STAFF")
        assert user.check_password(password)

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


def test_authenticate():
    user = create_user("STAFF", "Bob Smith", "bob@email.com", "bob", "bobpass")
    assert login("bob", "bobpass") != None

class UsersIntegrationTests(unittest.TestCase):

    def test_create_user(self):
        user = create_user("STAFF", "Rick Jones", "rick@email.com", "rick", "bobpass")
        assert user.username == "rick"

    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        # Check that we have the expected users
        assert len(users_json) >= 2
        usernames = [user['username'] for user in users_json]
        assert 'bob' in usernames
        assert 'rick' in usernames

    # Tests data changes in the database
    def test_update_user(self):
        update_user(1, username="ronnie")
        user = get_user(1)
        assert user.username == "ronnie"
        

