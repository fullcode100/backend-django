from django.contrib import admin

# Register your models here.
from match.models import Category, Player, Team, Group

models = [Category,Player,Team,Group]

for i in models:
    admin.site.register(i)
