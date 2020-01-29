from django.contrib import admin
from match import forms
# Register your models here.
from match.models import Category, Player, Team, Group, MatchHistory, PostThread
from match.proxy_model import CSGOMatchHistory, DotaMatchHistory, FutsalMatchHistory

models = [Category, PostThread]

for i in models:
    admin.site.register(i)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'category'
    ]


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['name', 'team', 'category']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    exclude = ['category']
    list_display = ['name', 'group', 'category']
    readonly_fields = ['goal_masuk',
                       'goal_kebobolan',
                       'selisih_goal',
                       'banyak_match',
                       'draw',
                       'lose',
                       'win',
                       'points']

    def save_model(self, request, obj, form, change):
        obj.category = obj.group.category
        super().save_model(request, obj, form, change)


@admin.register(MatchHistory)
class MatchHistoryAdmin(admin.ModelAdmin):
    exclude = ['group', 'category', 'is_game']

    def save_model(self, request, obj, form, change):
        team_a = obj.team_a
        team_b = obj.team_b

        if change:
            match_history_before = MatchHistory.objects.get(pk=obj.id)
            team_a.reduce_goal(match_history_before.team_a_goal, match_history_before.team_b_goal)
            team_b.reduce_goal(match_history_before.team_b_goal, match_history_before.team_a_goal)

            if match_history_before.is_a_win and match_history_before.is_b_win:
                team_a.reduce_match_stat("draw")
                team_b.reduce_match_stat("draw")
            elif match_history_before.is_a_win:
                team_a.reduce_match_stat("win")
                team_b.reduce_match_stat("lose")
            elif match_history_before.is_b_win:
                team_a.reduce_match_stat("lose")
                team_b.reduce_match_stat("win")

        team_a.add_goal(obj.team_a_goal, obj.team_b_goal)
        team_b.add_goal(obj.team_b_goal, obj.team_a_goal)

        if obj.is_a_win and obj.is_b_win:
            team_a.add_match_stat("draw")
            team_b.add_match_stat("draw")
        elif obj.is_a_win:
            team_a.add_match_stat("win")
            team_b.add_match_stat("lose")
        elif obj.is_b_win:
            team_a.add_match_stat("lose")
            team_b.add_match_stat("win")

        team_a.save()
        team_b.save()

        obj.group = team_a.group
        obj.category = team_a.category

        if team_a.category.name != "futsal":
            obj.is_game = True
        else:
            obj.is_game = False

        super().save_model(request, obj, form, change)


@admin.register(FutsalMatchHistory)
class MatchHistoryFutsalAdmin(MatchHistoryAdmin):
    form = forms.FutsalForm

    def get_queryset(self, request):
        qs = super(MatchHistoryFutsalAdmin, self).get_queryset(request)
        futsal = Category.objects.get(name="futsal")
        return qs.filter(category=futsal)


@admin.register(DotaMatchHistory)
class MatchHistoryDotaAdmin(MatchHistoryAdmin):
    form = forms.DotaForm

    def get_queryset(self, request):
        qs = super(MatchHistoryDotaAdmin, self).get_queryset(request)
        dota = Category.objects.get(name="dota")
        return qs.filter(category=dota)


@admin.register(CSGOMatchHistory)
class MatchHistoryCSGOAdmin(MatchHistoryAdmin):
    form = forms.CSGOForm

    def get_queryset(self, request):
        qs = super(MatchHistoryCSGOAdmin, self).get_queryset(request)
        csgo = Category.objects.get(name="csgo")
        return qs.filter(category=csgo)
