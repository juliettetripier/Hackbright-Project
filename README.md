# Eggsplorer

## Table of Contents

* [Overview](#overview)
* [Tech Stack](#tech-stack)
* [Features](#features)
* [Setup](#setup)
* [About the Dev](#about-me)

## <a name="overview"></a>Overview
**Eggsplorer** is a full-stack, Python-based Flask application that rewards users for documenting their epicurean adventures. 

Eggsplorer allows users to discover their new favorite local restaurants while building out a personalized profile and earning achievements. Users can search for restaurants by keyword and location, record their restaurant visits, add them to customized lists, and assign tags to them. Users earn achievements as they use Eggsplorer's site features, affecting both the user's standing in the achievement leaderboards and the hats a user can unlock for the site mascot.

<a href="https://www.youtube.com/watch?v=rhc7XCFqZMY">Click here</a> to view the demo video.

## <a name="tech-stack"></a>Tech Stack
__Front End:__ HTML, Jinja2, JavaScript (AJAX, JSON), CSS, Bootstrap, Flexbox </br>
__Back End:__ Python, Flask, PostgreSQL, SQLAlchemy </br>
__APIs:__ Yelp Fusion </br>

## <a name="features"></a>Features
(wip)

## <a name="setup"></a>Setup

#### Requirements:

- Python 3.9.18
- PostgreSQL

#### Step-by-step Setup

For each step, type the specified command into the command line in your terminal.

Clone the repository from GitHub:
```
$ git clone https://github.com/juliettetripier/Hackbright-Project.git
```

Create your virtual environment:
```
$ virtualenv env
```

Activate your virtual environment:
```
$ source env/bin/activate
```

Install dependencies:
```
$ pip3 install -r requirements.txt
```

Set up your secret key:
- Create a secrets.sh file in the project directory.
```
$ touch secrets.sh
```
- Add your secret key to your secrets.sh file.
```
export SECRET_KEY='[add your secret key here]'
```
- Access your environmental variables. You will need to do this each time you reactivate your virtual environment.
```
$ source secrets.sh
```

Create your 'seed' database:
```
$ createdb seed
```

Set up the tables in the database:
```
$ python3 seed_database.py
```

Run the app:
```
$ python3 server.py
```

You can now visit Eggsplorer by going to localhost:5000 on your browser.

## <a name="about-me"></a>About the Dev
Juliette Tripier (they/she) is a programmer with a background in both cognitive neuroscience and administrative/HR work. They have two great loves: working through delicate, complex logic puzzles and drawing cute, silly cartoons. Building a Flask application with a friendly egg mascot has proven to be the perfect marriage of these two things.

Learn more about the developer here: www.linkedin.com/in/juliette-tripier/