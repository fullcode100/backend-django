from django.db import models

class Player(models.Model):
  kontak = models.CharField(max_length=50, unique=True)
  token = models.TextField(unique=True, blank=True, null=True)
  total_time = models.FloatField(null=True, blank=True)
  game_1 = models.FloatField(default=0)
  game_2 = models.FloatField(default=0)
  game_3 = models.FloatField(default=0)
  game_4 = models.FloatField(default=0)
  benar_1 = models.IntegerField(default=-1)
  benar_2 = models.IntegerField(default=-1)
  benar_3 = models.IntegerField(default=-1)
  benar_4 = models.IntegerField(default=-1)

  def remove_token(self):
    self.token = None

  def count_total(self):
    self.total_time = float(self.game_1) + float(self.game_2) + float(self.game_3) + float(self.game_4)

  def __str__(self):
    return '{} - {}'.format(self.kontak, self.total_time)


class GameSchedule(models.Model):
  start = models.DateTimeField()
  end = models.DateTimeField()
  phase = models.IntegerField(default=0)
  max_time = models.IntegerField(default=300)

  def __str__(self):
    return "{} || {} - {}".format(self.phase, self.start, self.end)


