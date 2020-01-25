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


def check_category(dict):
    for key in dict.keys():
        try:
            dict[key] = models.Category.objects.get(name=key)
            print("{} category object found".format(key.title()))
        except models.Category.DoesNotExist:
            print("{} category object not found".format(key.title()))
            dict[key] = models.Category(name=key)
            dict[key].save()
            print("Done creating {} category".format(key))


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
        check_category(category)
        data = {
            'futsal_teams': [],
            'dota_teams': [],
            'csgo_teams': []
        }
        json.dump(data, file)
else:
    print("Migration data found")
    with open(migration_path, 'r') as file:
        check_category(category)
        print("Import data.....")
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
            team_name = team.split("-")[0]
            print("Get data from team {}".format(team_name))
            team_document = collection[key].document(team)
            team_document_object = team_document.get().to_dict()
            team_data = {
                'details': team_document_object,
                'logo': bucket.blob(team_document_object['teamLogo']) if "teamLogo" in team_document_object else None,
                'players': team_document.collection("player"),
            }
            if team_data['logo']:
                team_data['logo'].make_public()
                team_object = models.Team(name=team_name, category=category[key],
                                          team_logo=team_data['logo'].public_url,manager=team_data['details'].get('namaLengkap_manager',""))
            else:
                team_object = models.Team(name=team_name, category=category[key])
            team_object.save()
            if key != "futsal":
                captain = models.Player(name=team_document_object['namaLengkap_kapten'], category=category[key],
                                        team=team_object, captain=True)
                captain.save()
                print("Captain {} saved".format(captain))
            for player in team_data['players'].stream():
                player_data = player.to_dict()
                player_picture = bucket.blob(player_data['foto']) if "foto" in player_data else None
                if player_picture:
                    player_picture.make_public()
                    player_object = models.Player(name=player_data['namaLengkap'], team=team_object,
                                                  category=category[key], profile_picture=player_picture.public_url)
                else:
                    player_object = models.Player(name=player_data['namaLengkap'], team=team_object,
                                                  category=category[key])
                player_object.save()
                print("Player {} saved".format(player_object))
            print("Team {} saved".format(team_object))
if change:
    print("Exporting data...")
    with open(migration_path, 'w') as file:
        json.dump(db_data, file)
else:
    print("No Change")
