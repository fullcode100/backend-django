from rest_framework import serializers

from match.serializer import player_serializer, group_serializer
from match.models import Category


class CategoryGroupSerializer(serializers.ModelSerializer):
    match_groups = group_serializer.GroupDataNameSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'match_groups']


class CategoryDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class CategoryPlayerSerializer(serializers.ModelSerializer):
    category_players = player_serializer.PlayerSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'category_players']
