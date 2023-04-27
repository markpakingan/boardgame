""" Test user model"""

# run these tests like:
#
#    python3 -m unittest test_user_model.py

import os, requests
from unittest import TestCase
from sqlalchemy import exc

from models import db, Game, GameList, Game_Gamelist, Video, Image, Review, User

os.environ['DATABASE_URL'] = "postgresql:///boardgame-test"

from app import app

db.create_all()


class UserModelTestCase(TestCase):

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        self.uid = 94566
        u = User.signup("testing", "testing@test.com", "password", None)
        u.id = self.uid
        db.session.commit()

        self.u = User.query.get(self.uid)

        self.client = app.test_client()


    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res
    


# class APITestCase(TestCase):
    
#     def test_get_request(self):
#         """check if api is pulling"""
#         response = requests.get("https://api.boardgameatlas.com/api/search?name=Catan&pretty=true&client_id=Ctqu3FqFnC")
        
#         self.assertEqual(response.status_code, 200)
        
    

    def test_user_signup(self):
        """Checks if the user is created on the database"""

        username = "testuser"
        email = "test@gmail.com"
        password = "p@ssword"
        image_url = "https://images.pexels.com/photos/1716861/pexels-photo-1716861.jpeg?auto=compress&cs=tinysrgb&w=1600"


        user = User.signup(username, email ,password, image_url)

        self.assertEqual(user.username, username)
        self.assertEqual(user.email, email)

    
    def test_user_authenticate(self):
        """Authenticates the user from the database"""

        username = "testuser"
        password = "p@ssword"

        user = User.authenticate(username, password)

        self.assertIsNotNone(user)
        self.assertFalse(User.authenticate("testuser", "wrongpassword"))
        self.assertFalse(User.authenticate("invalidtestuser", "p@ssword"))


    def test_add_user(self):
        """Checks if the user will be added on the database"""

        id = "1"
        username = "testuser"
        email = "test@gmail.com"
        password = "p@ssword"
        image_url = "https://images.pexels.com/photos/1716861/pexels-photo-1716861.jpeg?auto=compress&cs=tinysrgb&w=1600"

        user = User(id=id, username=username, email=email, 
                    password=password, image_url=image_url)
        
        db.session.add(user)
        db.session.commit()

        self.assertIn(user, db.session)
