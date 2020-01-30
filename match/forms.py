from django import forms
from match import models


class MatchHistoryForm(forms.ModelForm):
    class Meta:
        model = models.MatchHistory
        exclude = ['category', 'group']

    def clean(self):
        cleaned_data = super().clean()
        team_a = cleaned_data.get("team_a")
        team_b = cleaned_data.get("team_b")
        is_a_win = cleaned_data.get("is_a_win")
        is_b_win = cleaned_data.get("is_b_win")

        if team_b == team_a:
            raise forms.ValidationError(
                'Team A and B is same'
            )
        if not is_b_win and not is_a_win:
            raise forms.ValidationError(
                'Both team cannot lose'
            )


class TeamForm(forms.ModelForm):
    class Meta:
        model = models.Team
        exclude = ['category']


class FutsalMatchHistoryForm(MatchHistoryForm):
    team_a = forms.ModelChoiceField(queryset=models.Team.objects.filter(category__name="futsal"))
    team_b = forms.ModelChoiceField(queryset=models.Team.objects.filter(category__name="futsal"))

    class Meta(MatchHistoryForm.Meta):
        pass


class CSGOMatchHistoryForm(MatchHistoryForm):
    team_a = forms.ModelChoiceField(queryset=models.Team.objects.filter(category__name="csgo"))
    team_b = forms.ModelChoiceField(queryset=models.Team.objects.filter(category__name="csgo"))

    class Meta(MatchHistoryForm.Meta):
        pass


class DotaMatchHistoryForm(MatchHistoryForm):
    team_a = forms.ModelChoiceField(queryset=models.Team.objects.filter(category__name="dota"))
    team_b = forms.ModelChoiceField(queryset=models.Team.objects.filter(category__name="dota"))

    class Meta(MatchHistoryForm.Meta):
        pass


class DotaTeamForm(TeamForm):
    group = forms.ModelChoiceField(queryset=models.Group.objects.filter(category__name="dota"))

    class Meta(TeamForm.Meta):
        pass


class CSGOTeamForm(TeamForm):
    group = forms.ModelChoiceField(queryset=models.Group.objects.filter(category__name="csgo"))

    class Meta(TeamForm.Meta):
        pass


class FutsalTeamForm(TeamForm):
    group = forms.ModelChoiceField(queryset=models.Group.objects.filter(category__name="futsal"))

    class Meta(TeamForm.Meta):
        pass
