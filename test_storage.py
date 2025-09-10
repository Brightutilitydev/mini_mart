#!/usr/bin/env python3
"""Test the creation and storage of models"""

from models import *

user1 = User(first_name="Blalock", last_name="Taussig", username="Blalock1", email="blalock@gmail.com", password="communityfilia")

print(user1)

stored_user = storage.add(user1)

retrive = storage.get(User, user1.id)
print("---retrieved---")
print(retrive)

retrive.username = "Bossbaby"

print(storage.update(retrive))
print("")
for entry in storage.all():
    print(entry)
