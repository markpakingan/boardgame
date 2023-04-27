""" Test user model"""

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


class ReviewModelTestCase(TestCase):
    # def test_add_review(self):
    #     """added review on a specific game"""

    #     user_id = "1"
    #     gamelist_id = "1"
    #     rating = "5"
    #     feedback = "This is awesome"

    #     review = Review(user_id=user_id, gamelist_id=gamelist_id, 
    #                     rating=rating, feedback=feedback)
        
    #     db.session.add(review)
    #     db.session.commit()

    #     self.assertIn(review, db.session)

    
