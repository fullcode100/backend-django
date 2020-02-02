from django.contrib import admin
from match import forms
# Register your models here.
from match.models import Category, Player, Team, Group, MatchHistory, PostThread
from match.proxy_model import CSGOMatchHistory, DotaMatchHistory, FutsalMatchHistory
from match import proxy_model
from match.admin_actions import team

models = [PostThread]

for i in models:
    admin.site.register(i)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        teams = Team.objects.filter(category=obj)
        for team in teams:
            team.calibrate_score()
            team.save()


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'category'
    ]


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['name', 'team', 'category']


from match.model_admin import match_history_model_admin,team_model_admin