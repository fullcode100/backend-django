from rest_framework import serializers
from match.models import MatchHistory

from match.serializer import team_serializer,group_serializer


class MatchHistorySerializer(serializers.ModelSerializer):
    team_a = team_serializer.TeamNameSerializer(many=False,read_only=True)
    team_b = team_serializer.TeamNameSerializer(many=False,read_only=True)
    match_date = serializers.DateField(format="%d/%m/%Y")
    group = group_serializer.GroupDataNameSerializer(many=False,read_only=True)

    class Meta:
        model = MatchHistory
        fields = ['id', 'team_a', 'team_b', 'is_game', 'team_a_goal', 'team_b_goal', 'stage', 'is_a_win', 'is_b_win','match_date','group']
