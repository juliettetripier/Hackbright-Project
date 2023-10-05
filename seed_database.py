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

    restaurant1 = model.Restaurant(name="Starbucks", address="123 Street Road")
    model.db.session.add(restaurant1)

    achievement1 = model.Achievement(name="You did it", description="wow congrats", points=5)
    model.db.session.add(achievement1)

    tag1 = model.Tag(name="Vegan")
    model.db.session.add(tag1)

    user1.achievements.append(achievement1)

    list1 = model.List(user_id=1, name="Wishlist", description="user1's wishlist")
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
