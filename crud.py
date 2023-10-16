from model import db, connect_to_db, User, Restaurant, RestaurantVisit, Achievement, UserAchievement, Tag, UserTag, Wishlist, ListItem


if __name__ == '__main__':
    from server import app
    with app.app_context():
        connect_to_db(app) 


def create_user(email, username, password):
    """Create and return a new user."""

    user = User(email=email, username=username, password=password)

    return user


def create_restaurant(name, address, yelp_id):
    """Create and return a new restaurant."""

    restaurant = Restaurant(name=name, address=address, yelp_id=yelp_id)

    return restaurant


def create_list(user_id, name, description):
    """Create and return a new list belonging to a user."""

    list = Wishlist(user_id=user_id, name=name, description=description)

    return list


def add_visit(user_id, restaurant_id):
    """Create and return an instance of a user visiting a restaurant."""

    visit = RestaurantVisit(user_id=user_id, restaurant_id=restaurant_id)

    return visit
    

# def add_tag()
    

def add_list_item(user_id, restaurant_id, list_id):
    """Create and return an instance of a user adding a restaurant to a list."""

    list_item = ListItem(user_id=user_id, restaurant_id=restaurant_id, list_id=list_id)

    return list_item



def add_achievement(user, achievement):
    """Add an achievement to a user."""

    user.achievements.append(achievement)


def get_user_by_id(user_id):
    """Take a user id and return the user object with that user id."""

    return User.query.get(user_id)

def get_user_by_email(email):
    """Take an email address and return the user object with that email address."""

    return User.query.filter(email == User.email).first()

def get_user_by_username(username):
    """Take a username and return the user object with that username."""

    return User.query.filter(username == User.username).first()

def get_restaurant_by_yelp_id(yelp_id):
    """Return a restaurant object with the given Yelp ID."""

    return Restaurant.query.filter(yelp_id == Restaurant.yelp_id).first()

def get_restaurant_by_internal_id(restaurant_id):
    """Return a restaurant object with the given internal ID."""

    return Restaurant.query.get(restaurant_id)

def get_visit(user_id, restaurant_id):
    """Takes in a user id and restaurant id and returns the corresponding restaurant visit object."""

    return RestaurantVisit.query.filter_by(user_id=user_id, restaurant_id=restaurant_id).first()

def get_list_by_list_id(list_id):
    """Return a wishlist object with the given list id."""

    return Wishlist.query.get(list_id)

def get_list_items(list_id):
    """Return all items in a wishlist with the specified list id."""

    return ListItem.query.filter_by(list_id=list_id).all()


