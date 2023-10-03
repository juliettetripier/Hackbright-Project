from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# TO DO:
# create all tables - done
# create all relationships between tables
    # set up relationships specifically when you want to pull info together
    # every time
    # users / achievements, users / tags?
# write __repr__ functions
# write connect to db function
# make seed file
    # test by adding info to one table at a time, running psql queries


class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    email = db.Column(db.String, unique=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    lists = db.relationship("List", secondary="list_items", back_populates="user")
    achievements = db.relationship("Achievement", secondary="user_achievements", back_populates="users")
    tags = db.relationship("Tag", secondary="user_tags", back_populates="users")

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email} username={self.username}>'


class Restaurant(db.Model):
    """A restaurant."""

    __tablename__ = "restaurants"

    restaurant_id = db.Column(db.Integer,
                              autoincrement=True,
                              primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    def __repr__(self):
        return f'<Restaurant restaurant_id={self.restaurant_id} name={self.name}>'


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


class Achievement(db.Model):
    """An achievement a user can earn."""

    __tablename__ = "achievements"

    achievement_id = db.Column(db.Integer,
                               autoincrement=True,
                               primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    points = db.Column(db.Integer)

    users = db.relationship("User", secondary="user_achievements", back_populates="achievements")

    def __repr__(self):
        return f'<Achievement achievement_id={self.achievement_id} name={self.name}>'


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


class Tag(db.Model):
    """A tag a user can assign to a restaurant."""

    __tablename__ = "tags"

    tag_id = db.Column(db.Integer,
                       autoincrement=True,
                       primary_key=True)
    name = db.Column(db.String)

    users = db.relationship("User", secondary="user_tags", back_populates="tags")

    def __repr__(self):
        return f'<Tag tag_id={self.tag_id} name={self.name}>'


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

    def __repr__(self):
        return f'<List list_id={self.list_id} user_id={self.user_id} name={self.name}>'


class ListItem(db.Model):
    """An instance of a restaurant being added to a list by a user."""

    __tablename__ = "list_items"

    list_item_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    list_id = db.Column(db.Integer,
                        db.ForeignKey('lists.list_id'))
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'))
    restaurant_id = db.Column(db.Integer,
                        db.ForeignKey('restaurants.restaurant_id'))

    