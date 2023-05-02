import os
import requests

from flask import Flask, render_template, request, flash, redirect, session, g, abort
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError



from forms import UserAddForm, LoginForm, GameListForm, DeleteForm, ReviewForm, SingleGameForm, NewGameForGamelistForm
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
# USER SIGNUP, LOGIN, LOGOUT


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
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


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

    flash ("You have been logout!", "danger")
    do_logout()
    return redirect ("/")

##############################################################################
# HOMEPAGE

@app.route('/')
def homepage():
    
    """if user is verified, show their dashboard, if not, let them sign-up"""

    if g.user: 
        # print("g.user is not None:", g.user)
        return render_template ("home.html")
    
    else:

        return render_template ("home-anon.html")
    
##############################################################################
#ACCOUNT ROUTE

@app.route('/account/user/<int:user_id>')
def show_user_account(user_id):
    """shows the user's account information"""

    user = User.query.get_or_404(user_id)

    if g.user.id != user_id:
       flash ("You are not authorized to view this!", "danger")
       return redirect("/")
    
    

    return render_template("users/account.html", user=user)

@app.route('/account/user/<int:user_id>/edit', methods = ["GET", "POST"])
def edit_user_account(user_id):
    """Edits the user's account information"""

    user = User.query.get_or_404(user_id)
    form = UserAddForm(obj=user)

    if g.user.id != user_id:
        flash ("You are not authorized to view this!", "danger")
        return redirect("/")
    

    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        flash('User account updated!', 'success')
        return redirect("/")

    return render_template('users/edit_user.html', form=form, 
                           user=user)

##############################################################################
#GAME ROUTE

@app.route('/user/<int:user_id>/games')
def show_all_games(user_id):
    """Show all user's games"""

    if g.user.id != user_id:
        flash("You are not authorized to view this!", "danger")
        return redirect("/")  
    
    games = Game.query.filter_by(user_id=user_id).all()

    return render_template("users/all_games.html", games=games)


@app.route('/user/<int:user_id>/games/<int:game_id>')
def show_game_info(user_id, game_id):
    """Shows which playlst is this game under"""

    if g.user.id != user_id:
        flash("You are not authorized to view this!", "danger")
        return redirect("/")  
    
    game = Game.query.get_or_404(game_id)

    # for testing
    gamelists = [gamelist for gamelist in game.gamelists]
    
    return render_template("users/game.html", game=game, gamelists=gamelists)

@app.route('/user/<int:user_id>/games/add', methods = ["GET", "POST"])
def add_single_game(user_id):
    """Manually adds a game"""

    if g.user.id != user_id:
        flash("You are not authorized to view this!", "danger")
        return redirect("/")  
    
    form = SingleGameForm()

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data

        game = Game(name=name, 
                    description=description, user_id=user_id)
        
        db.session.add(game)
        db.session.commit()

        return redirect(f'/user/{g.user.id}/games')

    else: 
        return render_template("boardgames/add_single_game.html", form=form)
    
@app.route('/user/<int:user_id>/games/edit', methods = ["GET", "POST"])
def edit_single_game(user_id):
    """Edit single game from the user"""

    games = Game.query.filter_by(user_id=user_id).all()

    if g.user.id != user_id:
        flash("You are not authorized to view this!", "danger")
        return redirect("/")
    
    form = SingleGameForm(obj=games)

    if form.validate_on_submit():
        form.populate_obj(games)
        db.session.commit()
        flash('Game Has Been Updated!', 'success')
        return redirect(f'/user/{g.user.id}/games')
    
    return render_template('boardgames/edit_game.html', form=form, 
                           games=games)

##############################################################################
#GAMELIST ROUTE


@app.route('/user/<int:user_id>/gamelist')
def show_all_gamelists(user_id):
    """Show user's gamelist"""
    
    if g.user.id != user_id:
        flash("You are not authorized to view this!", "danger")
        return redirect("/")    
    
    users = User.query.get_or_404(user_id)
    gamelists = GameList.query.filter_by(user_id = user_id).all()

 
    return render_template("users/all_gamelists.html", users=users,
                            gamelists = gamelists)

    

@app.route('/user/<int:user_id>/gamelist/<int:gamelist_id>')
def show_gamelist_info(user_id, gamelist_id):
    """show gamelist info"""
    
    gamelist = GameList.query.get_or_404(gamelist_id)

    # filters only results for a specific user & gamelist
    games = Game.query.join(Game_Gamelist).filter(Game_Gamelist.gamelist_id == gamelist.id, Game.user_id == g.user.id).all()

    if g.user.id != user_id:
        flash("You are not authorized to view this!", "danger")
        return redirect("/")

    return render_template("users/gamelist.html", gamelist=gamelist, games=games)




@app.route('/user/<int:user_id>/gamelist/add', methods = ["GET", "POST"])
def add_user_games(user_id):
    """creates new gameslist for a user"""

    if g.user.id != user_id:
        flash("You are not authorized to view this!", "danger")
        return redirect("/")   
    

    form = GameListForm()

    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data

        gamelist = GameList(description = description,
                        title = title, user_id = user_id)

        db.session.add(gamelist)
        db.session.commit()

        
        return redirect(f"/user/{g.user.id}/gamelist")
    
    else: 

        return render_template("boardgames/add_gamelist.html", form = form)


@app.route('/user/<int:user_id>/gamelist/<int:gamelist_id>/edit', methods=['GET', 'POST'])
def edit_gamelist(user_id, gamelist_id):
    """Edits a gamelist"""

    gamelist = GameList.query.get_or_404(gamelist_id)

    if g.user.id != user_id:
        flash("You are not authorized to view this!", "danger")
        return redirect("/")   
    
    
    form = GameListForm(obj=gamelist)


    if form.validate_on_submit():
        form.populate_obj(gamelist)
        db.session.commit()
        flash('Gamelist updated!', 'success')
        return redirect(f"/user/{g.user.id}/gamelist")

    return render_template('boardgames/edit.html', form=form, 
                           gamelist=gamelist)



@app.route('/user/<int:user_id>/gamelist/<int:gamelist_id>/delete', methods=['POST'])
def delete_gamelist(user_id, gamelist_id):
    """Deletes a single boardgame"""

    
    gamelist = GameList.query.get_or_404(gamelist_id)
    # user_id = gamelist.user_id


    if g.user.id != user_id:
        flash("You are not authorized to view this!", "danger")
        return redirect("/")   
    
    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(gamelist)
        db.session.commit()

    return redirect(f"/user/{g.user.id}/gamelist")



@app.route('/user/<int:user_id>/gamelist/<int:gamelist_id>/add-game', methods = ["GET", "POST"])
def add_game_to_gamelist(user_id, gamelist_id):
    """Add a game to a specific gamelist"""

    gamelist = GameList.query.get_or_404(gamelist_id)
    form = NewGameForGamelistForm()

    if g.user.id != user_id:
        flash("You are not authorized to view this!", "danger")
        return redirect("/")

    form.game.choices = [(game.id, game.name) for game in Game.query.all()]
    
    if form.validate_on_submit():
        game = Game.query.get(form.game.data)
        game_gamelist = Game_Gamelist(game_id=game.id, gamelist_id=gamelist.id)
        db.session.add(game_gamelist)
        db.session.commit()
        flash(f'{game.name} added to {gamelist.title} collection!', 'success')
        return redirect(f'/user/{g.user.id}/gamelist')

    return render_template('users/add_game_to_gamelist.html', form=form, 
                           gamelist=gamelist)


##############################################################################
# SINGLE GAME ROUTE

@app.route('/boardgamelist')
def get_boardgamelist():
    """Show 4 boardgame names"""

    name = request.args["name"]
    
    name_and_id = get_names(name)
    return render_template("home.html", name_and_id = name_and_id)


@app.route('/game/<game_official_id>')
def show_selected_game(game_official_id):
    """show details for a chosen boardgame"""

    game_details = get_gameinfo(game_official_id)

    return render_template ('boardgames/game_description.html',
                           game_details = game_details, 
                           game_official_id=game_official_id
                           )

@app.route('/game/<game_official_id>/add', methods = ["GET", "POST"])
def add_selected_game(game_official_id):


    #get the data form API
    game_details = get_gameinfo(game_official_id)

    user_id = g.user.id
    
    # if g.user.id != user_id:
    #     flash("You are not authorized to view this!", "danger")
    #     return redirect("/")

    
    form = SingleGameForm(name=game_details["name"])

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data

        game = Game(name=name, description=description, user_id=user_id)

        db.session.add(game)
        db.session.commit()

        return redirect("/")

    else:
        return render_template("boardgames/add_single_game.html", form=form,
                               game_details = game_details["name"])


##############################################################################
# REVIEW ROUTE

@app.route('/gamelist/<int:gamelist_id>/review')
def show_review(gamelist_id):
    """Shows the review of a game"""

    username = g.user.username
    gamelist = GameList.query.get_or_404(gamelist_id)
    review = Review.query.filter_by(gamelist_id=gamelist_id).first()
  
    return render_template("review/show_review.html", gamelist=gamelist, 
                           review=review, username=username)


@app.route('/gamelist/<int:gamelist_id>/review/add', methods = ["GET", "POST"])
def add_singlegame_review(gamelist_id):
    """adds a review to a single game"""

    form = ReviewForm()


    gamelist = GameList.query.get_or_404(gamelist_id)
    review = Review.query.filter_by(gamelist_id=gamelist_id,
                                    user_id=g.user.id).first()
    
    # check if review is already existing
    if review:
        flash("You already added a review for this game!", "danger")
        return redirect(f"/gamelist/{gamelist_id}/review")


    if form.validate_on_submit():
        rating = form.rating.data
        feedback = form.feedback.data

        review = Review(rating=rating, feedback=feedback,
                        user_id = g.user.id, gamelist_id=gamelist_id)
        
        db.session.add(review)
        db.session.commit()
        flash("You added a review!")
        return redirect("/")

    else:

        return render_template("review/add_review.html", form = form, 
                               gamelist=gamelist)


@app.route('/gamelist/<int:gamelist_id>/review/edit', methods=['GET', 'POST'])
def edit_reviewlist(gamelist_id):
    """Edits the review of a single boardgame"""

    review = Review.query.filter_by(gamelist_id=gamelist_id).first()
    gamelist = GameList.query.get_or_404(gamelist_id)
    form = ReviewForm(obj=review)

    if form.validate_on_submit():
        form.populate_obj(review)
        db.session.commit()
        flash('Your review has been updated!', 'success')
        return redirect(f"/gamelist/{gamelist_id}/review")

    return render_template('review/edit_review.html', form=form, 
                           review=review, gamelist=gamelist)



@app.route('/gamelist/<int:gamelist_id>/review/delete', methods=['POST'])
def delete_review(gamelist_id):
    """Deletes the review of a boardgame"""

    if not g.user:
        flash ("You are not authorized to view this!", "danger")
        return redirect("/")
    

    review = Review.query.filter_by(gamelist_id=gamelist_id).first()
    
    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(review)
        db.session.commit()

    return redirect(f"/gamelist/{gamelist_id}/review")

##############################################################################
# API FUNCTIONS

def get_names(name):
    """get 4 boardgame names based on searchquery"""

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


def get_gameinfo(game_official_id):
    """gets all the game information form the API"""


    res = requests.get(f"{API_BASE_URL}/search", 
                       params = {'ids': game_official_id, 'client_id': client_id })
    
    # import pdb; pdb.set_trace()
    data = res.json()

    name = data["games"][0]["name"]
    description = data["games"][0]["description"]
    lowest_price = data["games"][0]["price"]
    year_published = data["games"][0]["year_published"]
    MSRP = data["games"][0]["msrp"]
    min_players =data["games"][0]["min_players"]
    max_players =data["games"][0]["max_players"]
    mechanics = data["games"][0].get("mechanics",None)
    thumb_url = data["games"][0]["thumb_url"]

    game_details = {"name": name, "description": description, "lowest_price": lowest_price, 
                    "year_published": year_published, "MSRP": MSRP, "min_players": min_players,
                    "max_players": max_players,
                    "mechanics": mechanics, 
                    "thumb_url": thumb_url
                    }
    
    return game_details