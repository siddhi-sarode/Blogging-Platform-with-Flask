import unittest
from datetime import datetime, timezone
import unittest
from app import create_app, db
from app.models import User, Post
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='siddhi')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_user_creation(self):
        u = User(username='john')
        db.session.add(u)
        db.session.commit()
        self.assertEqual(User.query.count(), 1)

if __name__ == '__main__':
    unittest.main(verbosity=2)
    