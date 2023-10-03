import os
# import json

# import crud
import model
import server

os.system("dropdb seed")
os.system("createdb seed")

model.connect_to_db(server.app)
model.db.create_all()

# Test seed







model.db.session.commit()
