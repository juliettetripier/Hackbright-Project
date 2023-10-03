from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# TO DO:
# create all tables - done
# create all relationships between tables
# write __repr__ functions
# write connect to db function


class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    email = db.Column(db.String, unique=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    lists = db.relationship("List", back_populates="user")


class Restaurant(db.Model):
    """A restaurant."""

    __tablename__ = "restaurants"

    restaurant_id = db.Column(db.Integer,
                              autoincrement=True,
                              primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)


class RestaurantVisit(db.Model):
    """An instance of a user visiting a restaurant."""

    __tablename__ = "restaurant_visits"

    visit_id = db.Column(db.Integer,
                              autoincrement=True,
                              primary_key=True)
    restaurant_id = db.Column(db.Integer,
                              db.ForeignKey('restaurants.restaurant_id'))
    user_id = db.Column(db.Integer,
                              db.ForeignKey('users.user_id'))
    
    user = db.relationship("User", back_populates="restaurant_visits")
    restaurant = db.relationship("Restaurant", back_populates="restaurant_visits")


class Achievement(db.Model):
    """An achievement a user can earn."""

    __tablename__ = "achievements"

    achievement_id = db.Column(db.Integer,
                               autoincrement=True,
                               primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    points = db.Column(db.Integer)


class UserAchievement(db.Model):
    """An instance of a user earning an achievement."""

    __tablename__ = "user_achievements"

    user_achievement_id = db.Column(db.Integer,
                       autoincrement=True,
                       primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'))
    achievement_id = db.Column(db.Integer,
                        db.ForeignKey('achievements.achievement_id'))
    
    user = db.relationship("User", back_populates="user_achievements")
    achievement = db.relationship("Achievement", back_populates="user_achievements")


class Tag(db.Model):
    """A tag a user can assign to a restaurant."""

    __tablename__ = "tags"

    tag_id = db.Column(db.Integer,
                       autoincrement=True,
                       primary_key=True)
    name = db.Column(db.String)


class UserTags(db.Model):
    """An instance of a user assigning a tag."""

    __tablename__ = "user_tags"

    usertag_id = db.Column(db.Integer,
                       autoincrement=True,
                       primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'))
    tag_id = db.Column(db.Integer,
                       db.ForeignKey('tags.tag_id'))
    restaurant_id = db.Column(db.Integer,
                              db.ForeignKey('restaurants.restaurant_id'))
    
    user = db.relationship("User", back_populates="user_tags")
    tag = db.relationship("Tag", back_populates="user_tags")
    restaurant = db.relationship("Restaurant", back_populates="user_tags")
    

class List(db.Model):
    """A list belonging to a user."""

    __tablename__ = "lists"

    list_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'))
    name = db.Column(db.String)
    description = db.Column(db.String)
    
    user = db.relationship("User", back_populates="lists")


class ListItem(db.Model):
    """An instance of a restaurant being added to a list by a user."""

    __tablename__ = "list_items"

    list_item_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    list_id = db.Column(db.Integer,
                        db.ForeignKey('lists.list_id'))
    restaurant_id = db.Column(db.Integer,
                        db.ForeignKey('restaurants.restaurant_id'))
    
    user_list = db.Relationship("List", back_populates="list_items")
    restaurant = db.relationship("Restaurant", back_populates="list_items")

    