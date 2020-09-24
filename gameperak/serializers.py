from rest_framework import serializers

from gameperak.models import Player

class PlayerSerializer(serializers.HyperlinkedRelatedField):
  # player_token = PlayerTokenSerializer(view_name='player-token',read_only=True)

  class Meta:
      model = Player
      fields = [
        'kontak',
        'token',
      ]