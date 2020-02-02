from django.contrib import admin

from match import forms
from match.models import MatchHistory, Team
from match.proxy_model import FutsalMatchHistory, DotaMatchHistory, CSGOMatchHistory


@admin.register(MatchHistory)
class MatchHistoryAdmin(admin.ModelAdmin):
    exclude = ['group', 'category', 'is_game']
    list_display = admin.ModelAdmin.list_display + ('category',)

    @staticmethod
    def reset_team_data(team_a, team_b, obj):

        team_a.reduce_goal(obj.team_a_goal, obj.team_b_goal)
        team_b.reduce_goal(obj.team_b_goal, obj.team_a_goal)

        if obj.is_a_win and obj.is_b_win:
            team_a.reduce_match_stat("draw")
            team_b.reduce_match_stat("draw")
        elif obj.is_a_win:
            team_a.reduce_match_stat("win")
            team_b.reduce_match_stat("lose")
        elif obj.is_b_win:
            team_a.reduce_match_stat("lose")
            team_b.reduce_match_stat("win")

    def delete_model(self, request, obj):
        if obj.is_group_stage:
            team_a = obj.team_a
            team_b = obj.team_b
            MatchHistoryAdmin.reset_team_data(team_a, team_b, obj)
            team_a.save()
            team_b.save()
        super().delete_model(request, obj)

    def get_queryset(self, request):
        qs = super(MatchHistoryAdmin, self).get_queryset(request)
        if hasattr(self, "category"):
            return qs.filter(category__name=self.category)
        return qs

    def save_model(self, request, obj, form, change):
        if change and not obj.is_group_stage:
            match_history_before = MatchHistory.objects.get(pk=obj.id)
            team_a_before = match_history_before.team_a
            team_b_before = match_history_before.team_b
            if match_history_before.is_group_stage:
                MatchHistoryAdmin.reset_team_data(team_a_before, team_b_before, match_history_before)
                team_a_before.save()
                team_b_before.save()

        if obj.is_group_stage:
            if change:
                match_history_before = MatchHistory.objects.get(pk=obj.id)
                team_a_before = match_history_before.team_a
                team_b_before = match_history_before.team_b
                if match_history_before.is_group_stage:
                    MatchHistoryAdmin.reset_team_data(team_a_before, team_b_before, match_history_before)
                    team_a_before.save()
                    team_b_before.save()

            team_a = Team.objects.get(pk=obj.team_a.id)
            team_b = Team.objects.get(pk=obj.team_b.id)

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
    form = forms.FutsalMatchHistoryForm

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.category = "futsal"


@admin.register(DotaMatchHistory)
class MatchHistoryDotaAdmin(MatchHistoryAdmin):
    form = forms.DotaMatchHistoryForm

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.category = "dota"


@admin.register(CSGOMatchHistory)
class MatchHistoryCSGOAdmin(MatchHistoryAdmin):
    form = forms.CSGOMatchHistoryForm

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.category = "csgo"
