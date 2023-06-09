from rest_framework import serializers

from match.models import Team


class TeamDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'win', 'lose', 'draw', 'goal_masuk', 'goal_kebobolan', 'points', 'selisih_goal',
                  'banyak_match', 'team_logo']


class TeamNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name']


class TeamMinimizeDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'team_logo']


from match.serializer import player_serializer, category_serializer


class TeamDetailSerializer(serializers.ModelSerializer):
    team_players = player_serializer.PlayerSerializer(many=True, read_only=True)
    category = category_serializer.CategoryDataSerializer(read_only=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'win', 'lose', 'draw', 'goal_masuk', 'goal_kebobolan', 'points', 'selisih_goal',
                  'banyak_match', 'team_players', 'category', 'manager', 'team_logo']


class TeamPlayersSerializer(serializers.ModelSerializer):
    team_players = player_serializer.PlayerSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'team_players']
