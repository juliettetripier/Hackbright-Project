from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
from model import connect_to_db, db
import crud
import datetime
import os
import math
import requests

app = Flask(__name__)
app.secret_key = "REPLACE ME LATER"

YELP_API_KEY = os.environ['YELP_KEY']
# MAPS_API_KEY = os.environ['MAPS_KEY']

# Helper functions
def get_restaurant_info(yelp_id):
    url = f'https://api.yelp.com/v3/businesses/{yelp_id}'
    payload = {
        'id': yelp_id
    }
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {YELP_API_KEY}',
    }

    response = requests.get(url, params=payload, headers=headers)
    data = response.json()

    restaurant_dict = {'address': " ".join(data['location']['display_address']), 'res_name':data['name'],
                       'yelp_id': yelp_id}

    return restaurant_dict



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
        data = response.json()
        print(data)
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

    # convert hours from military time to standard time
    for hours in data['hours'][0]['open']:
        for item in hours:
            if item == 'start' or item == 'end':
                military_hour = hours[item]
                hour = datetime.datetime.strptime(military_hour, '%H%M').strftime('%I:%M %p')
                hours[item] = hour
    
    # check if user has visited restaurant
    user_id = session.get('user')
    user = crud.get_user_by_id(user_id)
    restaurant = crud.get_restaurant_by_yelp_id(data['id'])
    restaurant_id = restaurant.restaurant_id
    visit = crud.get_visit(user_id, restaurant_id)

    return render_template('restaurant-details.html',
                           data=data,
                           visit=visit,
                           user=user)


@app.route('/addvisit', methods=['POST'])
def add_visit():
    """Add restaurant to a user's visited restaurants."""

    yelp_restaurant_id = request.json.get('restaurantid')
    restaurant = crud.get_restaurant_by_yelp_id(yelp_restaurant_id)
    user = crud.get_user_by_id(session.get('user'))
    
    if restaurant:
        new_visit = crud.add_visit(user.user_id, restaurant.restaurant_id)
    else:
        restaurant_info = get_restaurant_info(yelp_restaurant_id)
        new_restaurant = crud.create_restaurant(name=restaurant_info['res_name'], address=restaurant_info['address'],
                                                yelp_id=restaurant_info['yelp_id'])
        db.session.add(new_restaurant)
        db.session.commit()

        new_visit = crud.add_visit(user.user_id, new_restaurant.restaurant_id)

    db.session.add(new_visit)
    db.session.commit()
    print(new_visit)

    return jsonify({'code': 'Visit registered!'})


@app.route('/removevisit', methods=['POST'])
def remove_visit():
    """Remove visit from user's visited restaurants."""

    yelp_restaurant_id = request.json.get('restaurantid')
    restaurant = crud.get_restaurant_by_yelp_id(yelp_restaurant_id)
    user = crud.get_user_by_id(session.get('user'))
    
    visit = crud.get_visit(user.user_id, restaurant.restaurant_id)

    db.session.delete(visit)
    db.session.commit()

    return jsonify({'code': 'Visit deleted!'})


@app.route('/newlist')
def show_new_list_form():
    """Show the form to create a new list."""

    user = crud.get_user_by_id(session.get('user'))
    if user:
        return render_template('list-form.html')
    else:
        flash('Please log in before making a list.')
        return redirect('/')
    

@app.route('/newlist/go')
def create_new_list():
    """Create new list."""

    user = crud.get_user_by_id(session.get('user'))
    list_name = request.args.get('listname')
    description = request.args.get('description')

    new_list = crud.create_list(user.user_id, list_name, description)

    db.session.add(new_list)
    db.session.commit()
    flash('List created successfully!')

    return redirect('/profile')


@app.route('/list/<id>')
def show_list(id):
    """Show the contents of a user's list."""

    user = crud.get_user_by_id(session.get('user'))
    wishlist = crud.get_list_by_list_id(id)
    list_items = crud.get_list_items(id)

    restaurants = []
    if list_items:
        for item in list_items:
            restaurant = crud.get_restaurant_by_internal_id(item.restaurant_id)
            restaurants.append(restaurant)


    return render_template('/list-details.html',
                           user=user,
                           list=wishlist,
                           restaurants=restaurants)


@app.route('/addtolist', methods=['POST'])
def add_to_list():
    """Add a restaurant to a user's list."""

    user = crud.get_user_by_id(session.get('user'))
    list_id = request.json.get('listid')
    yelp_id = request.json.get('restaurantid')
    restaurant = crud.get_restaurant_by_yelp_id(yelp_id)

    new_list_item = crud.add_list_item(user.user_id, restaurant.restaurant_id, list_id)

    db.session.add(new_list_item)
    db.session.commit()

    return jsonify({'code': 'Restaurant successfully added to list!'})


@app.route('/delete-list-item')
def delete_list_item():
    """Delete a restaurant from a user's list."""

    user = crud.get_user_by_id(session.get('user'))
    restaurant_id = request.args.get('item-dropdown')
    list_id = request.args.get('list-id')

    list_item = crud.get_list_item(list_id, restaurant_id)

    db.session.delete(list_item)
    db.session.commit()
    
    flash('Item deleted!')
    return redirect(f'/list/{list_id}')


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)