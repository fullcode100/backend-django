from django.contrib import admin

from match import proxy_model, forms
from match.admin_actions import team
from match.models import Team


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
                       'points',
                       'manager',
                       'team_logo',
                       'group',
                       'name']
    actions = [team.reset_statistic, team.calibrate_score,]

    def get_readonly_fields(self, request, obj=None):
        read_only_fields = super(TeamAdmin, self).get_readonly_fields(request, obj)
        if request.user.groups.filter(name="Publisher").exists():
            return read_only_fields
        else:
            return read_only_fields[:0]

    def get_queryset(self, request):
        qs = super(TeamAdmin, self).get_queryset(request)
        if hasattr(self, "category"):
            return qs.filter(category__name=self.category)
        return qs

    def save_model(self, request, obj, form, change):
        if obj.group is not None:
            obj.category = obj.group.category
        if request.user.groups.filter(name="Publisher").exists():
            obj.calibrate_score()
        super().save_model(request, obj, form, change)


@admin.register(proxy_model.FutsalTeam)
class FutsalTeamAdmin(TeamAdmin):
    form = forms.FutsalTeamForm

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.category = "futsal"


@admin.register(proxy_model.CSGOTeam)
class CSGOTeamAdmin(TeamAdmin):
    form = forms.CSGOTeamForm

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.category = "csgo"


@admin.register(proxy_model.DotaTeam)
class DotaTeamAdmin(TeamAdmin):
    form = forms.DotaTeamForm

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.category = "dota"
