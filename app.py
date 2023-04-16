import os
import requests

from flask import Flask, render_template, request, flash, redirect, session, g, abort
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError



from forms import UserAddForm, LoginForm, GameListForm
from models import db, connect_db, Game, User, Image, Video, Review, Game_Gamelist, GameList



API_BASE_URL = "https://api.boardgameatlas.com/api"
key = "TAAifFP590,OIXt3DmJU0"
client_id = "Ctqu3FqFnC"

CURR_USER_KEY = "curr_user"

app = Flask(__name__)
app.app_context().push()


# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///boardgame'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

##############################################################################
# User signup/login/logout


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session: 
        g.user = User.query.get(session[CURR_USER_KEY])
    else: 
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id

def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                image_url=form.image_url.data
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('users/signup.html', form=form)
    


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    flash ("You have been logout!")
    do_logout()
    return redirect ("/")

##############################################################################

@app.route('/')
def homepage():
    
    # """if user is verified, show their dashboard, if not, let them sign-up"""

    if g.user: 
        # print("g.user is not None:", g.user)
        return render_template ("home.html")
    
    else:

        return render_template ("home-anon.html")

##############################################################################
# API FUNCTIONS

def get_names(name):
    """get boardgame names based on searchquery"""

    
    res = requests.get(f"{API_BASE_URL}/search", 
                       params = {'name': name, 'client_id': client_id })

    data = res.json()

    name1 = data["games"][0]["name"]
    name2 = data["games"][1]["name"]
    name3 = data["games"][2]["name"]
    name4 = data["games"][3]["name"]

    id1 = data["games"][0]["id"]
    id2 = data["games"][1]["id"]
    id3 = data["games"][2]["id"]
    id4 = data["games"][3]["id"]

    # names = {"name1": name1, "name2": name2, "name3": name3, "name4": name4}
    name_and_id = {"name1": name1, 
                        "name2": name2, 
                        "name3": name3, 
                        "name4": name4, 
                        "id1": id1,
                        "id2": id2,
                        "id3": id3, 
                        "id4": id4
                        }
    return name_and_id


def get_boardgame_details(name):
    """Retrieve game details based on game_id, e.g., using an API call or from a database"""

    res = requests.get(f"{API_BASE_URL}/search", 
                       params = {'name': name, 'client_id': client_id })

    data = res.json()

    name = data["games"][0]["name"]
    description = data["games"][0]["description"]
    lowest_price = data["games"][0]["price"]
    year_published = data["games"][0]["year_published"]
    MSRP = data["games"][0]["msrp"]
    players =data["games"][0]["players"]
    mechanics = data["games"][0]["mechanics"][0]["url"]
    artist = data["games"][0]["artists"][0]


    game_details = {"name": name, "description": description, "lowest_price": lowest_price, 
                    "year_published": year_published, "MSRP": MSRP, "players": players,
                    "mechanics": mechanics, "artist": artist}
    
    return game_details

##############################################################################
# BOARD GAME ROUTE


@app.route('/boardgamelist')
def get_boardgamelist():
    name = request.args["name"]
    API_BASE_URL = "https://api.boardgameatlas.com/api"
    client_id = "Ctqu3FqFnC"
    
    name_and_id = get_names(name)


    return render_template("home.html", name_and_id = name_and_id)

    # import pdb; pdb.set_trace()


@app.route("/boardgame/<int:game_id>")
def show_boardgame_details():
    
   

##############################################################################

# USER PROFILE ROUTE


@app.route('/user/<int:user_id>')
def check_user_profile(user_id):
    """Show user profile"""

    

    if not g.user:
       flash ("You are not authorized to view this!", "danger")
       return redirect("/")
       
    user = User.query.get_or_404(user_id)
    return render_template("users/userprofile.html", user = user)



@app.route('/user/<int:user_id>/games')
def show_games(user_id):
    """Show list of games from the user"""

    if not g.user: 
       flash ("You are not authorized to view this!", "danger")
       return redirect("/")
       
    user = User.query.get_or_404(user_id)
    return render_template("users/games.html", user = user)



# @app.route('/user/add-game', methods = ["GET", "POST"])
# def add_user_games():
#     """adds gameslist to user's profile"""

    
#     form = GameListForm()

#     if form.validate_on_submit():
#         name = form.name.data
#         description = form.description.data

#         game = Game(name = name, description = description)

#         db.session.add(game)
#         db.session.commit()

#         return redirect("/user/<int:user_id>/gamelist")
    
#     else: 

#         return render_template("users/add_game.html", form = form)
