from rest_framework import serializers

from match.models import Group


class GroupDataNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


from match.serializer import category_serializer,team_serializer


class GroupDetailsDataSerializer(serializers.ModelSerializer):
    category = category_serializer.CategoryDataSerializer(many=False, read_only=True)
    group_teams = team_serializer.TeamDataSerializer(read_only=True,many=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'category','group_teams']


class GroupTeamsDataSerializer(serializers.ModelSerializer):
    group_teams = team_serializer.TeamDataSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'group_teams']
