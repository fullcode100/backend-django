from rest_framework import serializers

from match.models import Category


class CategoryDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


from match.serializer import player_serializer, group_serializer, team_serializer


class CategoryGroupSerializer(serializers.ModelSerializer):
    match_groups = group_serializer.GroupDataNameSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'match_groups']


class CategoryPlayerSerializer(serializers.ModelSerializer):
    category_players = player_serializer.PlayerSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'category_players']


class CategoryTeamSerializer(serializers.ModelSerializer):
    category_teams = team_serializer.TeamDataSerializer(many=True,read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'category_teams']
