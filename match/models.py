from datetime import time, date

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="match_groups", blank=True, null=True)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=100)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="group_teams", null=True, blank=True)
    win = models.PositiveIntegerField(default=0)
    lose = models.PositiveIntegerField(default=0)
    draw = models.PositiveIntegerField(default=0)
    position = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    points = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_teams", null=True,
                                 blank=True)
    goal_masuk = models.PositiveIntegerField(default=0)
    goal_kebobolan = models.PositiveIntegerField(default=0)
    selisih_goal = models.PositiveIntegerField(default=0)
    banyak_match = models.PositiveIntegerField(default=0)
    team_logo = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ['position']
        unique_together = [('position', 'group')]

    def __str__(self):
        return self.name


class Player(models.Model):
    name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True, related_name="team_players")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True,
                                 related_name="category_players")
    profile_picture = models.URLField(blank=True, null=True)
    captain = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.name


class PostThread(models.Model):
    image = models.ImageField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_posts", null=True,
                                 blank=True)
    caption = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_posts")
    title = models.CharField(max_length=100)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class MatchHistory(models.Model):
    team_a = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team_a_history")
    team_b = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team_b_history")
    match_date = models.DateField()
    is_game = models.BooleanField(default=False)
    team_a_goal = models.PositiveIntegerField(default=0)
    team_b_goal = models.PositiveIntegerField(default=0)
    stage = models.CharField(max_length=100)
    is_a_win = models.BooleanField(default=False)
    is_b_win = models.BooleanField(default=False)

    class Meta:
        ordering = ['match_date']

    def __str__(self):
        return "Match {} vs {} tanggal {}".format(self.team_a.name,self.team_b.name,self.match_date.strftime())

