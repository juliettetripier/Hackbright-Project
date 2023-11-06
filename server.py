from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
from model import connect_to_db, db
from collections import Counter
import crud
import datetime
import os
import math
import requests

app = Flask(__name__)
app.secret_key = "REPLACE ME LATER"

YELP_API_KEY = os.environ['YELP_KEY']

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
            return redirect(f'/profile/{user.user_id}')
        else: 
            flash('Your login credentials are incorrect. Please try again.')
            return redirect('/')
    else:
        flash('Your login credentials are incorrect. Please try again.')
        return redirect('/')
    

@app.route('/logout')
def logout():
    session.pop('user', default=None)

    flash('Logged out!')
    return redirect('/')
    

@app.route('/profile/<id>')
def show_profile(id):
    """Show user profile."""

    user = crud.get_user_by_id(session.get('user'))
    profile_owner = crud.get_user_by_id(id)
    if user:
        return render_template('profile.html', 
                               user=user,
                               profile_owner=profile_owner)
    else:
        flash('Please log in to view profile pages.')
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
    sort_by = request.args.get('sort_by')

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
            'sort_by': sort_by,
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

    # make dictionary to hold the restaurant's hours
    hours_dict = {'Monday': {'when_open': "", 'is_closed_today': True},
                'Tuesday': {'when_open': "", 'is_closed_today': True},
                'Wednesday': {'when_open': "", 'is_closed_today': True},
                'Thursday': {'when_open': "", 'is_closed_today': True},
                'Friday': {'when_open': "", 'is_closed_today': True},
                'Saturday': {'when_open': "", 'is_closed_today': True},
                'Sunday': {'when_open': "", 'is_closed_today': True}}

    def set_hours(day):
        if hours_dict[day]['when_open'] == "":
            hours_dict[day]['when_open'] += f"{hours_info['start']} - {hours_info['end']}"
        else:
            hours_dict[day]['when_open'] += f", {hours_info['start']} - {hours_info['end']}"
        hours_dict[day]['is_closed_today'] = False

    for hours_info in data['hours'][0]['open']:
        if hours_info['day'] == 0:
            set_hours('Monday')
        elif hours_info['day'] == 1:
            set_hours('Tuesday')
        elif hours_info['day'] == 2:
            set_hours('Wednesday')
        elif hours_info['day'] == 3:
            set_hours('Thursday')
        elif hours_info['day'] == 4:
            set_hours('Friday')
        elif hours_info['day'] == 5:
            set_hours('Saturday')
        elif hours_info['day'] == 6:
            set_hours('Sunday')
    
    # check if user has visited restaurant
    user_id = session.get('user')
    user = crud.get_user_by_id(user_id)
    restaurant = crud.get_restaurant_by_yelp_id(data['id'])
    restaurant_id = restaurant.restaurant_id
    visit = crud.get_visit(user_id, restaurant_id)

    # get all tags from DB
    tags = crud.get_all_tags()

    # get the user's tags for this restaurant, if any
    user_tags_for_restaurant = crud.get_user_tags_by_restaurant_and_user(user_id, restaurant_id)

    # get most common tags for restaurant, if any
    all_tags_for_restaurant = crud.get_user_tags_by_restaurant(restaurant_id)
    tag_count = Counter(all_tags_for_restaurant)
    most_popular_tags = tag_count.most_common(3)
    most_popular_tag_names = []
    for tag in most_popular_tags:
        tag_object = tag[0]
        grabbed_tag = crud.get_tag_name_by_user_tag(tag_object)
        most_popular_tag_names.append(grabbed_tag)
    most_popular_tags_string = ", ".join(most_popular_tag_names)
        
    return render_template('restaurant-details.html',
                           data=data,
                           hours=hours_dict,
                           visit=visit,
                           user=user,
                           tags=tags,
                           user_tags=user_tags_for_restaurant,
                           most_popular_tags=most_popular_tags_string)


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
    
    # check user's previous visits to determine achievement eligibility
    previous_visits = crud.get_all_visits(user.user_id)
    if not previous_visits:
        new_achievement = crud.get_achievement_by_name('Restaurant Explorer 1')
        crud.add_achievement(user, new_achievement)
        flash(f'New achievement earned: {new_achievement.name}')
    elif len(previous_visits) == 4:
        new_achievement = crud.get_achievement_by_name('Restaurant Explorer 2')
        crud.add_achievement(user, new_achievement)
        flash(f'New achievement earned: {new_achievement.name}')

    db.session.add(new_visit)
    db.session.commit()

    return jsonify({'code': 'Visit registered!'})


@app.route('/removevisit', methods=['POST'])
def remove_visit():
    """Remove visit from user's visited restaurants."""

    yelp_restaurant_id = request.json.get('restaurantid')
    restaurant = crud.get_restaurant_by_yelp_id(yelp_restaurant_id)
    user = crud.get_user_by_id(session.get('user'))
    
    visit = crud.get_visit(user.user_id, restaurant.restaurant_id)

    # check user's previous visits to determine if an achievement should be removed
    previous_visits = crud.get_all_visits(user.user_id)
    if len(previous_visits) == 1:
        achievement = crud.get_achievement_by_name('Restaurant Explorer 1')
        achievement_to_delete = crud.get_user_achievement_by_achievement(user.user_id, achievement.achievement_id)
        db.session.delete(achievement_to_delete)
        crud.update_achievement_info_by_user_id(user.user_id, -(achievement.points), -1)
    elif len(previous_visits) == 5:
        achievement = crud.get_achievement_by_name('Restaurant Explorer 2')
        achievement_to_delete = crud.get_user_achievement_by_achievement(user.user_id, achievement.achievement_id)
        db.session.delete(achievement_to_delete)
        crud.update_achievement_info_by_user_id(user.user_id, -(achievement.points), -1)

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

    # check how many lists this user has to determine achievement eligibility
    previous_lists = crud.get_lists_by_user(user.user_id)
    if not previous_lists:
        new_achievement = crud.get_achievement_by_name('List Maker 1')
        crud.add_achievement(user, new_achievement)
        flash(f'New achievement earned: {new_achievement.name}')


    db.session.add(new_list)
    db.session.commit()
    flash('List created successfully!')

    return redirect(f'/profile/{user.user_id}')


@app.route('/list/<id>')
def show_list(id):
    """Show the contents of a user's list."""

    user = crud.get_user_by_id(session.get('user'))
    wishlist = crud.get_list_by_list_id(id)
    list_items = crud.get_list_items(id)
    list_owner = crud.get_user_by_list(id)

    restaurants = []
    if list_items:
        for item in list_items:
            restaurant = crud.get_restaurant_by_internal_id(item.restaurant_id)
            restaurants.append(restaurant)

    return render_template('/list-details.html',
                           user=user,
                           list_owner=list_owner,
                           list=wishlist,
                           restaurants=restaurants)


@app.route('/addtolist', methods=['POST'])
def add_to_list():
    """Add a restaurant to a user's list."""

    user = crud.get_user_by_id(session.get('user'))
    print(user)
    list_id = request.json.get('listid')
    print(list_id)
    yelp_id = request.json.get('restaurantid')
    print(yelp_id)
    restaurant = crud.get_restaurant_by_yelp_id(yelp_id)
    print(restaurant)

    new_list_item = crud.add_list_item(user.user_id, restaurant.restaurant_id, list_id)
    print(new_list_item)

    # check user's previous list items to determine eligibility for achievements
    previous_list_items = crud.get_all_list_items_by_user(user.user_id)
    if not previous_list_items:
        new_achievement = crud.get_achievement_by_name('Dreamer 1')
        print(new_achievement)
        crud.add_achievement(user, new_achievement)
        flash(f'New achievement earned: {new_achievement.name}')

    db.session.add(new_list_item)
    db.session.commit()

    return jsonify({'code': 'Restaurant successfully added to list!'})


@app.route('/delete-list-item')
def delete_list_item():
    """Delete a restaurant from a user's list."""

    user_id = session.get('user')
    restaurant_id = request.args.get('item-dropdown')
    list_id = request.args.get('list-id')

    # check user's list items to determine if an achievement should be removed
    previous_list_items = crud.get_all_list_items_by_user(user_id)
    if len(previous_list_items) == 1:
        achievement = crud.get_achievement_by_name('Dreamer 1')
        achievement_to_delete = crud.get_user_achievement_by_achievement(user_id, achievement.achievement_id)
        db.session.delete(achievement_to_delete)
        crud.update_achievement_info_by_user_id(user_id, -(achievement.points), -1)

    list_item = crud.get_list_item(list_id, restaurant_id)
    db.session.delete(list_item)
    db.session.commit()
    
    flash('Item deleted!')
    return redirect(f'/list/{list_id}')


@app.route('/delete-list')
def delete_list():
    """Delete a user's list."""

    list_id = request.args.get('list-id')
    print(list_id)
    user_id = session.get('user')

    list_to_delete = crud.get_list_by_list_id(list_id)
    items_to_delete = crud.get_list_items(list_id)

    # check user's lists to determine if an achievement should be removed
    previous_lists = crud.get_lists_by_user(user_id)
    if len(previous_lists) == 1:
        achievement = crud.get_achievement_by_name('List Maker 1')
        achievement_to_delete = crud.get_user_achievement_by_achievement(user_id, achievement.achievement_id)
        db.session.delete(achievement_to_delete)
        crud.update_achievement_info_by_user_id(user_id, -(achievement.points), -1)

    db.session.delete(list_to_delete)

    # check user's list items to determine if an achievement should be removed
    if items_to_delete:
        num_items_deleted = len(items_to_delete)
        all_list_items = crud.get_all_list_items_by_user(user_id)
        list_items_remaining = len(all_list_items) - num_items_deleted
        if list_items_remaining == 0:
            achievement = crud.get_achievement_by_name('Dreamer 1')
            achievement_to_delete = crud.get_user_achievement_by_achievement(user_id, achievement.achievement_id)
            db.session.delete(achievement_to_delete)
            crud.update_achievement_info_by_user_id(user_id, -(achievement.points), -1)
        for item in items_to_delete:
            db.session.delete(item)

    db.session.commit()

    flash('List deleted!')
    return redirect(f'/profile/{user_id}')


@app.route('/addtag', methods=['POST'])
def add_tag():
    """Add an instance of a user assigning a tag to a restaurant."""

    user_id = session.get('user')
    user = crud.get_user_by_id(user_id)
    yelp_id = request.json.get('restaurantid')
    restaurant = crud.get_restaurant_by_yelp_id(yelp_id)
    tag_id = request.json.get('tagid')
    tag = crud.get_tag_by_tag_id(tag_id)

    # check user's previous tags to determine achievement eligibility
    previous_tags = crud.get_user_tags(user_id)
    if not previous_tags:
        new_achievement = crud.get_achievement_by_name('Tagger 1')
        crud.add_achievement(user, new_achievement)
        flash(f'New achievement earned: {new_achievement.name}')
    elif len(previous_tags) == 4:
        new_achievement = crud.get_achievement_by_name('Tagger 2')
        crud.add_achievement(user, new_achievement)
        flash(f'New achievement earned: {new_achievement.name}')

    # check that user hasn't already tagged restaurant with this tag
    already_tagged = crud.get_user_tag_by_restaurant_and_tag_id(tag_id, restaurant.restaurant_id, user_id)
    if already_tagged:
        code = 'Error: tag already added'
    else:
        user_tag = crud.create_user_tag(user_id, restaurant.restaurant_id, tag_id)
        code = 'Tag successfully added!'
        db.session.add(user_tag)
        db.session.commit()

    return jsonify({'code': code, 'tag_id': tag_id, 'tag_name': tag.name})


@app.route('/deletetag', methods=['POST'])
def delete_tag():
    """Remove an instance of a user assigning a tag to a restaurant."""

    user_id = session.get('user')
    tags_to_delete = request.form.getlist('tag_id')
    yelp_id = request.form.get('restaurant_yelp_id')
    restaurant = crud.get_restaurant_by_yelp_id(yelp_id)

    for tag in tags_to_delete:
        tag_to_delete = crud.get_user_tag_by_restaurant_and_tag_id(tag, restaurant.restaurant_id, user_id)
        db.session.delete(tag_to_delete)
    db.session.commit()
    flash('Tag(s) successfully deleted!')

    # check how many tags the user now has, to determine if an achievement should be removed
    user_tags = crud.get_user_tags(user_id)
    if len(user_tags) == 0:
            achievement2 = crud.get_achievement_by_name('Tagger 1')
            user_achievement2 = crud.get_user_achievement_by_achievement(user_id, achievement2.achievement_id)
            db.session.delete(user_achievement2)
            crud.update_achievement_info_by_user_id(user_id, -(achievement2.points), -1)
    if len(user_tags) < 5:
        achievement = crud.get_achievement_by_name('Tagger 2')
        user_achievement = crud.get_user_achievement_by_achievement(user_id, achievement.achievement_id)
        if user_achievement:
            db.session.delete(user_achievement)
            crud.update_achievement_info_by_user_id(user_id, -(achievement.points), -1)

    db.session.commit()

    return redirect(f'/restaurant/{yelp_id}')


@app.route('/leaderboard')
def show_leaderboard():
    """Display the achievement leaderboard."""

    user = crud.get_user_by_id(session.get('user'))

    if user:
        users_by_points = crud.get_users_sorted_by_points()
        top_ten = users_by_points[:10]
        user_in_top_ten = False
        if user in top_ten:
            user_in_top_ten = True
        user_rank = (users_by_points.index(user)) + 1
        return render_template('leaderboard.html',
                            user=user,
                            top_ten=top_ten,
                            user_in_top_ten=user_in_top_ten,
                            user_rank=user_rank,
                            enumerate=enumerate)
    else:
        flash('Please log in to view the leaderboard.')
        return redirect('/')
    

@app.route('/search-user')
def get_user_search_results():
    """Search for a user with the requested username."""
    requested_username = request.args.get('requested_user')
    requested_user = crud.get_user_by_username(requested_username)
    user = session.get('user')

    if user:
        return render_template('user-search-results.html',
                            requested_username=requested_username,
                           requested_user=requested_user)
    else:
        flash('You must be logged in to search for users!')
        return redirect('/')



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)