from rest_framework import serializers

from match.models import Team
from match.serializer import player_serializer


class TeamDetailSerializer(serializers.ModelSerializer):
    team_players = player_serializer.PlayerSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'win', 'lose', 'draw', 'goal', 'team_players','category']


class TeamPlayersSerializer(serializers.ModelSerializer):
    team_players = player_serializer.PlayerSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'team_players']


class TeamDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'win', 'lose', 'draw', 'goal']

