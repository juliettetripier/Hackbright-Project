import os
# import json

# import crud
import model
import server

with server.app.app_context():

    os.system("dropdb seed")
    os.system("createdb seed")

    model.connect_to_db(server.app)
    model.db.create_all()

    # Test seed
    user1 = model.User(email="test@test.com", username="user1", password="password2")
    model.db.session.add(user1)

    user2 = model.User(email="juliette@juliette.com", username="juliette", password="juliette")
    model.db.session.add(user2)

    restaurant1 = model.Restaurant(name="Starbucks", address="123 Street Road")
    model.db.session.add(restaurant1)

    achievement1 = model.Achievement(name="Restaurant Explorer 1", description="Visited your first restaurant", points=5)
    model.db.session.add(achievement1)
    achievement2 = model.Achievement(name="Restaurant Explorer 2", description="Visited five restaurants", points=10)
    model.db.session.add(achievement2)
    achievement3 = model.Achievement(name="List Maker 1", description="Created your first list", points=5)
    model.db.session.add(achievement3)
    achievement4 = model.Achievement(name="Dreamer 1", description="Added a restaurant to a list", points=5)
    model.db.session.add(achievement4)
    achievement5 = model.Achievement(name="Tagger 1", description="Assigned your first tag", points=5)
    model.db.session.add(achievement5)
    achievement6 = model.Achievement(name="Tagger 2", description="Assigned a tag to a restaurant five times", points=10)
    model.db.session.add(achievement6)

    tag1 = model.Tag(name="Vegetarian")
    model.db.session.add(tag1)
    tag2 = model.Tag(name="Vegan")
    model.db.session.add(tag2)
    tag3 = model.Tag(name="Gluten-free")
    model.db.session.add(tag3)
    tag4 = model.Tag(name="Halal")
    model.db.session.add(tag4)
    tag5 = model.Tag(name="Kosher")
    model.db.session.add(tag5)
    tag6 = model.Tag(name="Family-friendly")
    model.db.session.add(tag6)
    tag7 = model.Tag(name="Cheap Eats")
    model.db.session.add(tag7)
    tag8 = model.Tag(name="Woman-owned")
    model.db.session.add(tag8)
    tag9 = model.Tag(name="Black-owned")
    model.db.session.add(tag9)
    tag10 = model.Tag(name="Dog-friendly")
    model.db.session.add(tag10)

    user1.achievements.append(achievement1)

    list1 = model.Wishlist(user_id=1, name="Wishlist", description="user1's wishlist")
    model.db.session.add(list1)

    model.db.session.commit()

    listitem = model.ListItem(list_id=1, user_id=1, restaurant_id=1)
    model.db.session.add(listitem)
    model.db.session.commit()

    restaurant2 = model.Restaurant(name="Food", address="Food store")
    model.db.session.add(restaurant2)
    model.db.session.commit()

    listitem2 = model.ListItem(list_id=1, user_id=1, restaurant_id=2)
    model.db.session.add(listitem2)
    model.db.session.commit()

    usertag = model.UserTag(user_id=1, tag_id=1, restaurant_id=2)
    model.db.session.add(usertag)
    model.db.session.commit()

    user1.visits.append(restaurant1)

    model.db.session.commit()
