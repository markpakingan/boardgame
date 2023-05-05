""" Test Review model"""

# run these tests like:
#
#    python3 -m unittest test_review_model.py

import os, requests
from unittest import TestCase
from sqlalchemy import exc

from models import db, Game, GameList, Game_Gamelist, Video, Image, Review, User

os.environ['DATABASE_URL'] = "postgresql:///boardgame-test"

from app import app

db.create_all()


# class ReviewModelTestCase(TestCase):

#     def setUp(self):
#         """Set up the test database with review data"""

        

#         user_id = "1"
#         gamelist_id = "1"
#         rating = "5"
#         feedback = "This is awesome!"

#         review = Review(user_id=user_id, gamelist_id=gamelist_id, 
#                         rating=rating, feedback=feedback)
        
#         db.session.add(review)
#         db.session.commit()


#     def test_review_form(self):
#         """Check if review form is working"""
#         with app.test_client() as client:
#             res = client.get(f'/gamelist/1/review/add')
#             html = res.get.data(as_text=True)

#             self.assertEqual(res.status_code, 200)
#             self.assertIn('<h1>Game Review for', html)

class ReviewModelTestCase(TestCase):
    
    def setUp(self):
        """Set up the test database with review data"""

        # Create a test client
        self.client = app.test_client()

        # Add a test user
        user = User(id = "1", username='testuser', email='testuser@example.com',
                    password ='p@ssword')
        # user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()

        # Log in the test user
        self.client.post('/login', data=dict(
            username='testuser',
            password='testpassword'
        ), follow_redirects=True)

        # Add a test game
        game = Game(name='Test Game', description='This is a test game.')
        db.session.add(game)
        db.session.commit()

        # Add the test game to a test gamelist
        gamelist = GameList(name='Test Gamelist', description='This is a test gamelist.',
                            title="Test Title Name", user_id='1')
        db.session.add(gamelist)
        db.session.commit()


        # game_gamelist = Game_Gamelist(game_id=game.id, gamelist_id=gamelist.id)
        # db.session.add(game_gamelist)
        # db.session.commit()

        # Add a test review
        review = Review(rating=5, feedback='This is an awesome game!', user_id=user.id, gamelist_id=gamelist.id)
        db.session.add(review)
        db.session.commit()

    def test_review_form(self):
        """Check if review form is working"""
        with app.test_client() as client:
            res = client.get(f'/gamelist/1/review/add')
            html = res.get.data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Game Review for', html)    