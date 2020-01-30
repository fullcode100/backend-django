from match.models import MatchHistory, Team


class FutsalMatchHistory(MatchHistory):
    class Meta:
        proxy = True


class DotaMatchHistory(MatchHistory):
    class Meta:
        proxy = True


class CSGOMatchHistory(MatchHistory):
    class Meta:
        proxy = True


class FutsalTeam(Team):
    class Meta:
        proxy = True


class DotaTeam(Team):
    class Meta:
        proxy = True


class CSGOTeam(Team):
    class Meta:
        proxy = True
