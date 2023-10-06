from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
import crud
import os
import requests

app = Flask(__name__)
app.secret_key = "REPLACE ME LATER"

# YELP_API_KEY = os.environ['YELP_KEY']
# MAPS_API_KEY = os.environ['MAPS_KEY']


@app.route('/')
def homepage():
    return render_template('homepage.html')


@app.route('/newuser', methods=["POST"])
def register_user():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)

    if user:
        flash('A user with that email already exists. Please try again.')
    else:
        db.session.add(crud.create_user(email, username, password))
        db.session.commit()
        flash('Account successfully created!')

    return redirect('/')


@app.route('/login', methods=["POST"])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = crud.get_user_by_username(username)

    if user:
        if password == user.password:
            session['user'] = user.user_id
            return redirect('/profile')
        else: 
            flash('Your login credentials are incorrect. Please try again.')
            return redirect('/')
    else:
        flash('Your login credentials are incorrect. Please try again.')
        return redirect('/')
    

@app.route('/profile')
def show_profile():
    """Show user profile."""

    user = crud.get_user_by_id(session.get('user'))
    if user:
        return render_template('profile.html', user=user)
    else:
        flash('Please log in to view your profile page.')
        return redirect('/')


@app.route('/search')
def show_search_form():
    """Display restaurant search form."""

    user = crud.get_user_by_id(session.get('user'))
    if user:
        return render_template('search-form.html')
    else:
        flash('Please log in to search for restaurants.')
        return redirect('/')


@app.route('/search/go')
def get_search_results():
    """Search for restaurants on Yelp."""

    keywords = request.args.get('keywords')
    location = request.args.get('location')
    radius = request.args.get('radius')
    







if __name__ == "__main__":
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)