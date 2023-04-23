"""SQLAlchemy models for Warbler."""

from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class Game(db.Model):
    """Games table"""

    __tablename__ = "games"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    game_sku_id = db.Column (db.Text, nullable = True)
    name = db.Column(db.Text, nullable = False )
    description = db.Column(db.Text, nullable = True )
    lowest_price = db.Column(db.Float, nullable = True )
    MSRP = db.Column(db.Float, nullable = True )
    image_url = db.Column(db.Text, nullable = True )
    min_play = db.Column(db.Integer, nullable = True )
    max_play = db.Column(db.Integer, nullable = True )
    mechanics = db.Column(db.Text, nullable = True )
    artists= db.Column(db.Text, nullable = True )

    # gamelists = db.relationship("GameList", secondary = "game_gamelists", backref = "games")

class GameList(db.Model):

    __tablename__ = "gamelists"

    id = db.Column (db.Integer, primary_key = True, autoincrement = True)
    title = db.Column (db.Text, nullable = False) 
    name = db.Column (db.Text, nullable = False)
    description = db.Column (db.Text, nullable = False)
    user_id = db.Column (db.Integer, db.ForeignKey("users.id"),nullable = False)


class Game_Gamelist (db.Model):

    __tablename__ = "game_gamelists"

    id = db.Column (db.Integer, primary_key = True, autoincrement = True)
    game_id = db.Column (db.Integer, db.ForeignKey("games.id"), nullable = False)
    
    # This is incorrect
    user_id = db.Column (db.Integer, db.ForeignKey("users.id"), nullable = False)
    
    # This is what Raymon recommended
    # gamelist_id = db.Column (db.Integer, db.ForeignKey("gamelists.id"), nullable = False)


class Video(db.Model):

    __tablename__= "videos"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    url = db.Column (db.Text, nullable = False)
    games_id = db.Column(db.Integer, db.ForeignKey("games.id"), nullable = False )

class Image(db.Model):

    __tablename__= "images"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    url = db.Column (db.Text, nullable = False)
    games_id = db.Column(db.Integer, db.ForeignKey("games.id"), nullable = False )

class Review(db.Model):

    __tablename__= "reviews"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False )
    gamelist_id = db.Column(db.Integer, db.ForeignKey("gamelists.id"), nullable = False )
    rating = db.Column (db.Integer, nullable = False)
    feedback = db.Column (db.Text, nullable = False)

class User(db.Model):

    __tablename__ = "users"

    id = db.Column (db.Integer, primary_key = True, autoincrement = True)
    username = db.Column (db.Text, nullable = False)
    password = db.Column (db.Text, nullable = False)
    image_url = db.Column (db.Text, nullable = True)
    email = db.Column(db.Text, nullable = False)

    @classmethod
    def signup(cls, username, email, password, image_url):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            image_url=image_url,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False
    

def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)
