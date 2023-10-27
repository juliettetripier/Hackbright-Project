from model import db, connect_to_db, User, Restaurant, RestaurantVisit, Achievement, UserAchievement, Tag, UserTag, Wishlist, ListItem
from sqlalchemy import desc

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
    

def add_list_item(user_id, restaurant_id, list_id):
    """Create and return an instance of a user adding a restaurant to a list."""

    list_item = ListItem(user_id=user_id, restaurant_id=restaurant_id, list_id=list_id)

    return list_item


def create_user_tag(user_id, restaurant_id, tag_id):
    """Create and return an instance of a user adding a tag to a restaurant."""

    user_tag = UserTag(user_id=user_id, restaurant_id=restaurant_id, tag_id=tag_id)

    return user_tag




def get_user_by_id(user_id):
    """Take a user id and return the user object with that user id."""

    return User.query.get(user_id)


def get_user_by_email(email):
    """Take an email address and return the user object with that email address."""

    return User.query.filter(email == User.email).first()


def get_all_users():
    """Return all users in the database."""

    return User.query.all()


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


def get_all_visits(user_id):
    """Returns all visits from the specified user."""

    return RestaurantVisit.query.filter_by(user_id=user_id).all()


def get_list_by_list_id(list_id):
    """Return a wishlist object with the given list id."""

    return Wishlist.query.get(list_id)


def get_lists_by_user(user_id):
    """Return all lists created by the specified user."""

    return Wishlist.query.filter_by(user_id=user_id).all()


def get_list_items(list_id):
    """Return all items in a wishlist with the specified list id."""

    return ListItem.query.filter_by(list_id=list_id).all()


def get_list_item(list_id, restaurant_id):
    """Return one list item from the specified list corresponding to the specified restaurant."""

    return ListItem.query.filter_by(list_id=list_id, restaurant_id=restaurant_id).first()


def get_all_list_items_by_user(user_id):
    """Return all list items added by the specified user, across all their lists."""

    return ListItem.query.filter_by(user_id=user_id).all()


def get_all_tags():
    """Return all tags in the database."""

    return Tag.query.all()


def get_tag_by_tag_id(tag_id):
    """Return the tag with the specified tag ID."""

    return Tag.query.get(tag_id)


def get_user_tags(user_id):
    """Return all tags assigned by the specified user."""

    return UserTag.query.filter_by(user_id=user_id).all()


def get_user_tags_by_restaurant_and_user(user_id, restaurant_id):
    """Return all user tags for a given restaurant by a given user."""

    return UserTag.query.filter_by(user_id=user_id, restaurant_id=restaurant_id).all()


def get_user_tag_by_restaurant_and_tag_id(tag_id, restaurant_id, user_id):
    """Return the instance of a tag being added to the specified restaurant, with the specified user tag id."""

    return UserTag.query.filter_by(tag_id=tag_id, restaurant_id=restaurant_id, user_id=user_id).first()


def add_achievement(user, achievement):
    """Add an achievement to a user."""

    user.achievements.append(achievement)
    user.num_achievements += 1
    user.total_points += achievement.points


def get_all_user_achievements(user_id):
    """Return all achievements earned by the specified user."""

    return UserAchievement.query.filter_by(user_id=user_id).all()


def get_user_achievement_by_achievement(user_id, achievement_id):
    """Return the instance of the specified user earning the specified achievement."""

    return UserAchievement.query.filter_by(user_id=user_id, achievement_id=achievement_id).first()


def get_achievement_by_name(name):
    """Return the achievement object with the specified name."""

    return Achievement.query.filter_by(name=name).first()


def get_num_achievements_by_user_id(user_id):
    """Return the number of achievements earned by the user with the specified ID."""

    achievement_list = UserAchievement.query.filter_by(user_id=user_id).all()
    return len(achievement_list)


def get_achievement_points_by_user_id(user_id):
    """Return the number of achievement points earned by the user with the specified ID."""

    num_points = 0
    user = get_user_by_id(user_id)
    for achievement in user.achievements:
        num_points += achievement.points
    return num_points


def update_achievement_info_by_user_id(user_id, point_change, num_achievments_changed):
    """Update total achievement points and # of achievements for a user with the specified ID."""

    user = get_user_by_id(user_id)
    user.total_points += point_change
    user.num_achievements += num_achievments_changed


def get_users_sorted_by_points():
    """Return all users, sorted by achievement points in descending order."""

    return User.query.order_by(desc(User.total_points)).all()
