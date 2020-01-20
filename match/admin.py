from django.contrib import admin

# Register your models here.
from match.models import Category, Player, Team, Group,MatchHistory

models = [Category,Player,Team,Group,MatchHistory]

for i in models:
    admin.site.register(i)
