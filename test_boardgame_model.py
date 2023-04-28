""" Test user model"""

# run these tests like:
#
#    python3 -m unittest test_boardgame_model.py

import os, requests
from unittest import TestCase
from sqlalchemy import exc

from models import db, Game, GameList, Game_Gamelist, Video, Image, Review, User

os.environ['DATABASE_URL'] = "postgresql:///boardgame-test"

from app import app

db.create_all()


class BoardgameTestCase(TestCase):

    API_BASE_URL = 'https://api.boardgameatlas.com/api'
    game_official_id = '12345'
    client_id = 'Ctqu3FqFnC'
    name = 'Mario Monopoly'


    def test_get_gameinfo(self):
        """Check if API is pulling for the method get_game_info"""
        
        res = requests.get(f"{self.API_BASE_URL}/search", 
                       params = {'ids': self.game_official_id, 'client_id': self.client_id })
            
        self.assertEqual(res.status_code, 200)

    def test_get_names(self):
        """Test if the data is pulling from the API"""

        res = requests.get(f"{self.API_BASE_URL}/search", 
                       params = {'name': self.name, 'client_id': self.client_id })
        
        self.assertEqual(res.status_code, 200)


    
