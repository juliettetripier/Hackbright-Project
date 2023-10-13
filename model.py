from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    email = db.Column(db.String, unique=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    lists = db.relationship("Wishlist", secondary="list_items", back_populates="user")
    achievements = db.relationship("Achievement", secondary="user_achievements", back_populates="users")
    tags = db.relationship("Tag", secondary="user_tags", back_populates="users")
    visits = db.relationship("Restaurant", secondary="restaurant_visits", back_populates="visitors")

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email} username={self.username}>'


class Restaurant(db.Model):
    """A restaurant."""

    __tablename__ = "restaurants"

    restaurant_id = db.Column(db.Integer,
                              autoincrement=True,
                              primary_key=True)
    yelp_id = db.Column(db.String)
    name = db.Column(db.String)
    address = db.Column(db.String)

    visitors = db.relationship("User", secondary="restaurant_visits", back_populates="visits")
    tags = db.relationship("Tag", secondary="user_tags", back_populates="restaurants")

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
    
    def __repr__(self):
        return f'<RestaurantVisit visit_id={self.visit_id} user_id={self.user_id} restaurant_id={self.restaurant_id}>'


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
    
    def __repr__(self):
        return f'user_id {self.user_id} has earned achievement {self.achievement_id}'


class Tag(db.Model):
    """A tag a user can assign to a restaurant."""

    __tablename__ = "tags"

    tag_id = db.Column(db.Integer,
                       autoincrement=True,
                       primary_key=True)
    name = db.Column(db.String)

    users = db.relationship("User", secondary="user_tags", back_populates="tags")
    restaurants = db.relationship("Restaurant", secondary="user_tags", back_populates="tags")

    def __repr__(self):
        return f'<Tag tag_id={self.tag_id} name={self.name}>'


class UserTag(db.Model):
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
    
    
class Wishlist(db.Model):
    """A list."""

    __tablename__ = "lists"

    list_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'))
    name = db.Column(db.String)
    description = db.Column(db.String)
    
    user = db.relationship("User", back_populates="lists")
    listitems = db.relationship("ListItem", back_populates="wishlist")

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
    
    wishlist = db.relationship("Wishlist", back_populates="listitems")

    
def connect_to_db(flask_app, db_uri="postgresql:///seed", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app
    with app.app_context():
        connect_to_db(app)