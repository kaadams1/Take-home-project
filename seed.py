"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import model
import server

os.system("dropdb reservations")
os.system("createdb reservations")

model.connect_to_db(server.app)
model.db.create_all()

#need to create and fill reservation_data

# reservations_in_db = []
# for reservation in reservation_data:
#     reservation_time = (reservation["reservation_time"])

#     db_reservation = model.Reservation.create(reservation_time)
#     reservations_in_db.append(db_reservation)

# model.db.session.add_all(reservations_in_db)
# model.db.session.commit()

# Create 10 users
for n in range(10):
    email = f"user{n}@test.com"

    user = model.User.create(email)
    model.db.session.add(user)

model.db.session.commit()