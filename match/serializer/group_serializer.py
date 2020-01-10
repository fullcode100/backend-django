from rest_framework import serializers

from match.models import Group
from match.serializer import team_serializer


class GroupDataNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


from match.serializer import category_serializer


class GroupCategoryDataSerializer(serializers.ModelSerializer):
    category = category_serializer.CategoryDataSerializer(many=False, read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'category']


class GroupTeamsDataSerializer(serializers.ModelSerializer):
    teams = team_serializer.TeamDataSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'teams']
