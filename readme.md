
Title: 
Board Game Bazooka

Link: 
https://github.com/markpakingan/boardgame.git

Description of the project:
- This website will help customers get information about a boardgame. It allows a user to search for a specific boardgame, get basic information (e.g. mechanics, description, players) and create a gamelist. 
- The gamelist can help a user to categorize games based on the user's preference. 
  
Wireframes:
[Wireframe Idea] (https://docs.google.com/presentation/d/1Lr3XvMNEcujM5e0siS6AKrZNIuaePIyYi1z1AzQG9IQ/edit?usp=sharing)



User Stories
* "My friends and I love playing boardagames all the time, In fact, I always buy atleast 2 boardgames per month. I need an app that allows me to search for a specific boardgame and check if they are even worth buying. In addition, I'd like to find a way to organize all my games virtually. This will help me manage and share my list of games to my other friends."



Setup
In order to run on the server, please follow these steps:

- Step 1: Download the code and run the terminal
- Step 2: Download the necessary scripts. 
  You can find the list of scripts in "requirements.txt"
- Step 3: Start the server
  Use the command "flask run" to start the server. 
- Step 4: Copy the route to your browser. 
  You can run the program by pasting this url to the browser: http://127.0.0.1:5000/

Technologies Used:
- Python 3
- Flask
- SQLAlchemy
- HTML
- CSS
- Bootstrap
- Git
- Pip

This project uses mainly Python 3 as the main programming language and the Flask framework
for building the web application. SQLAlchemy is used for database access and management. 

HTML, CSS are used for the front-end UI, with some bootstrap styling. Git is used for version control and Pip is used as the package manager for installing dependencies.


Models:
* User
    The user model represenents a registered user of the system

    - id: the unique identifier for the product (integer)
    - username: the name of the user (charfield)
    - password: the hidden pin of the user (charfield)
    - image_url: the chosen image of the user (charfield)
    - email: the chosen image of the user (charfield)

* Game
    The game model represents the general information about a game

    - id: the unique identified for the product
    - game_official id: the unique identifier of a game derived from the API (Charfield)
    - name: the name of the game (Charfield)
    - user_id: the unique identifier for the product derived form the USER table (integer)
  


* Gamelist
    The gamelist model represents a collection of games based on a user's personal criteria

    - id: the unique identifier for the product (integer)
    - title: the name of the gamelist (Charfield)
    - description: provides info of what the gamelist is all about (Charfield)
    - user_id: the unique identifier for the product derived form the USER table (integer)


* Game_gamelist
    The game_gamelist model represents the connection between the game & the gamelist.

    - id: the unique identifier for the product (integer)
    - game_id: the unique identifier for the product derived from the table GAME (integer)
    - gamelist_id: the unique identifier for the product derived from the table GAME (integer)


  
Server routes table(Method, Route or URL, Description as columns):
![Alt text](/images/Boardgame%20table%20route.png)


Demo (Screenshots or GIFs of the application)
![Alt text](/images/Demo%201.png)
![Alt text](/images/Demo%202.png)
![Alt text](/images/Demo%203.png)
![Alt text](/images/Demo%204.png)


Project Link:
https://github.com/markpakingan/boardgame.git


Future Work:

There are serveral potential areas for future work in this project: 

* Show and add user reviews for specific games
* Allow users to connect with other users and show their games
* Additional testing and more smoother UI


Resources:
 [API Documentation](https://www.boardgameatlas.com/api/docs)


Team members:
Mark Pakingan - Developer, Designer, Tester