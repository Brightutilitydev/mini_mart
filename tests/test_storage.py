#!/usr/bin/env python3
"""Test the creation and storage of models"""

from models import *

user1 = User(first_name="Blalock", last_name="Taussig", username="Blalock1", email="blalock@gmail.com", password="communityfilia")
user1.save()
storage.save()
print(user1)

retrieved = storage.get(User, user1.id)
print("---retrieved---")
print(retrieved)

retrieved.username = "Bossbaby"
retrieved.save()
storage.save()

print("")
for entry in storage.all():
    print(entry)
