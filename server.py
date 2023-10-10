from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
import crud
import os
import math
import requests

app = Flask(__name__)
app.secret_key = "REPLACE ME LATER"

YELP_API_KEY = os.environ['YELP_KEY']
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
    """Add search results to db if not already in db."""

    keywords = request.args.get('keywords')
    location = request.args.get('location')
    radius = request.args.get('radius')
    unit = request.args.get('unit')

    # Convert radius to meters for Yelp API
    if radius != "":
        radius = float(radius)
        if unit == "miles":
            radius = radius * 1609.34
        elif unit == "kilometers":
            radius = radius * 1000
        radius = math.ceil(radius)
        
    url = 'https://api.yelp.com/v3/businesses/search'
    payload = {
            'term': keywords,
            'location': location,
            'radius': radius,
            'limit': 50,
            }
    headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {YELP_API_KEY}',
        }

    response = requests.get(url, params=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        restaurants = data['businesses']
        for restaurant in restaurants:
            restaurant_in_db = crud.get_restaurant_by_yelp_id(restaurant['id'])
            if not restaurant_in_db:
                new_restaurant = crud.create_restaurant(name=restaurant['name'], address=restaurant['location']['display_address'],
                                       yelp_id=restaurant['id'])
                db.session.add(new_restaurant)
        db.session.commit()           
    elif response.status_code == 400:
        restaurants = []

    return render_template('search-results.html',
                           data=data,
                           restaurants=restaurants)


@app.route('/restaurant/<id>')
def show_restaurant_page(id):
    """Show details for a particular restaurant."""

    url = f'https://api.yelp.com/v3/businesses/{id}'
    payload = {
        'id': id
    }
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {YELP_API_KEY}',
    }

    response = requests.get(url, params=payload, headers=headers)
    data = response.json()

    return render_template('restaurant-details.html',
                           data=data)




if __name__ == "__main__":
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)