import json
import sys

sys.dont_write_bytecode = True

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "perak.settings")
import django

django.setup()

from firebase_utils.db_storage import db, bucket

from match import models

migration_path = os.path.join("firebase_utils", "migration.json")

collection = {
    'futsal': db.collection(u'futsal-team'),
    'dota': db.collection(u'dota'),
    'csgo': db.collection(u'csgo')
}

teams = {
    'dota': [],
    'csgo': [],
    'futsal': []
}

category = {
    'dota': None,
    'csgo': None,
    'futsal': None
}

if not os.path.exists(migration_path):
    print('Initial migrate')
    with open(migration_path, 'w') as file:
        for key in category.keys():
            category[key] = models.Category(name=key)
            category[key].save()
        data = {
            'futsal_teams': [],
            'dota_teams': [],
            'csgo_teams': []
        }
        json.dump(data, file)
        print("Done creating category")
else:
    print("Migration data found")
    with open(migration_path, 'r') as file:
        print("Import data.....")
        for key in category.keys():
            category[key] = models.Category.objects.get(name=key)
        data = json.load(file)
        for key in teams.keys():
            teams[key] = data['{}_teams'.format(key)]

print("Get data from firebase....")
db_data = {'{}_teams'.format(key): [doc.id for doc in collection[key].stream()] for key in teams.keys()}

print("Checking data....")
change = False
for key in teams.keys():
    difference = set(db_data['{}_teams'.format(key)]) - set(teams[key])
    if len(difference) != 0:
        print("Update data in {} category".format(key))
        change = True
        for team in difference:
            print("Get data from team {}".format(team.split("-")[0]))
            print(collection[key].document(team).get().to_dict())

# for doc in futsal_team.stream():
#     print(doc.to_dict())
