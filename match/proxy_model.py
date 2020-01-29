from match.models import MatchHistory


class FutsalMatchHistory(MatchHistory):
    class Meta:
        app_label = "match_history"
        proxy = True


class DotaMatchHistory(MatchHistory):
    class Meta:
        app_label = "match_history"
        proxy = True


class CSGOMatchHistory(MatchHistory):
    class Meta:
        app_label = "match_history"
        proxy = True
