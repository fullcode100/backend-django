from django.core.paginator import Paginator
from rest_framework import viewsets
# Create your views here.
from rest_framework.decorators import action
from rest_framework.response import Response

from match import models
from match.serializer.team_serializer import TeamDataSerializer
from match.serializer import group_serializer, category_serializer, team_serializer, match_history_serializer
from match.paginator import MatchHistoryPaginator


class TeamViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Team.objects.all()
    serializer_class = TeamDataSerializer

    @action(methods=['get'], detail=True, url_path="players")
    def get_players(self, request, pk=None):
        team = self.get_object()
        serializer = team_serializer.TeamPlayersSerializer(team, read_only=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        team = self.get_object()
        serializer = team_serializer.TeamDetailSerializer(team, read_only=True)
        return Response(serializer.data)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Group.objects.all()
    serializer_class = group_serializer.GroupDataNameSerializer

    @action(methods=['get'], detail=True, url_path="teams")
    def get_teams(self, request, pk=None):
        group = self.get_object()
        serializer = group_serializer.GroupTeamsDataSerializer(group, read_only=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        group = self.get_object()
        serializer = group_serializer.GroupDetailsDataSerializer(group, read_only=True)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = category_serializer.CategoryDataSerializer

    @action(methods=['get'], detail=True, url_path="players")
    def get_players(self, request, pk=None):
        category = self.get_object()
        serializer = category_serializer.CategoryPlayerSerializer(category, read_only=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True, url_path="groups")
    def get_groups(self, request, pk=None):
        category = self.get_object()
        serializer = category_serializer.CategoryGroupSerializer(category, read_only=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True, url_path="teams")
    def get_teams(self, request, pk=None):
        category = self.get_object()
        serializer = category_serializer.CategoryTeamSerializer(category, read_only=True)
        return Response(serializer.data)


class MatchHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.MatchHistory.objects.all()
    serializer_class = match_history_serializer.MatchHistorySerializer
    pagination_class = MatchHistoryPaginator

    def retrieve(self, request, pk=None, *args, **kwargs):
        category = models.Category.objects.get(name=pk)
        query = models.MatchHistory.objects.filter(category=category)
        if 'size' in request.GET:
            page = self.paginate_queryset(query)
            serializer = self.get_serializer(page,many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(query,many=True)
        return Response(serializer.data)