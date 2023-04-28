""" Test Review model"""

# run these tests like:
#
#    python3 -m unittest test_api.py

import os, requests
from unittest import TestCase
from sqlalchemy import exc

from models import db, Game, GameList, Game_Gamelist, Video, Image, Review, User

os.environ['DATABASE_URL'] = "postgresql:///boardgame-test"

from app import app

db.create_all()


class APITestCase(TestCase):
    
    def test_get_request(self):
        """check if api is pulling"""
        response = requests.get("https://api.boardgameatlas.com/api/search?name=Catan&pretty=true&client_id=Ctqu3FqFnC")
        
        self.assertEqual(response.status_code, 200)


    

    def test_get_names(self):
        """Check if the API is pulling the data based on the user's search query"""

        