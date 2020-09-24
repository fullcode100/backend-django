from django.contrib import admin
from .models import Player, GameSchedule
from .views import get_current_schedule


class PlayerAdmin(admin.ModelAdmin):
  ordering = ['total_time']
  actions = ['auto_fill']
  actions_selection_counter=False
  def auto_fill(self, request, queryset):
    schedule = get_current_schedule()
    phase = int(schedule.phase)
    for player in Player.objects.all():
      for i in range(1, phase):
        if float(getattr(player, 'game_{}'.format(i))) == 0:
          setattr(player, 'game_{}'.format(i), float(schedule.max_time))
      player.count_total()
      player.save()

admin.site.register(Player, PlayerAdmin)
admin.site.register(GameSchedule)

