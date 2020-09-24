from django.http import JsonResponse
from django.middleware.csrf import get_token, get_random_string
from rest_framework import generics, status
from rest_framework.response import Response
from gameperak.models import Player, GameSchedule
from gameperak.serializers import PlayerSerializer
from rest_framework.permissions import AllowAny
from datetime import datetime
import pytz


def test(request):
  csrf = get_token(request)
  return JsonResponse({"csrf_token": csrf})

def get_current_schedule():
  utc=pytz.UTC
  now = utc.localize(datetime.utcnow())
  schedules = GameSchedule.objects.all().order_by('phase')
  # the checks are in UTC (+0) even though input in UTC+7
  for s in schedules:
    if (s.start <= now) and (s.end > now): 
      return s
  return None

class GameStart(generics.GenericAPIView):
  permission_classes = (AllowAny,)
  queryset = Player.objects.all()
  serializer_class = PlayerSerializer

  def get(self, request):
    return Response({"token": get_random_string(101)})

  def post(self, request):
    try:
      schedule = get_current_schedule()
      if schedule != None:
        kontak = request.data['kontak']
        player = Player.objects.get_or_create(kontak=kontak.lower())[0]
        if float(getattr(player, 'game_{}'.format(schedule.phase))) != 0:
          return Response({'message': 'Anda sudah Bermain hari ini'}, status=status.HTTP_403_FORBIDDEN)
        if player.token == None:
          player.token = get_random_string(101)
          player.save()
        response = {"player": player.kontak, "token": player.token, "phase": schedule.phase, "maxTime": schedule.max_time}
        return Response(response)
      return Response({'message': 'Periode Game masih belum dimulai'}, status=status.HTTP_403_FORBIDDEN)
    except KeyError:
      return Response({"token": get_random_string(101)})

class SendResult(generics.GenericAPIView):
  permission_classes = (AllowAny,)
  queryset = Player.objects.all()
  serializer_class = PlayerSerializer

  def get(self, request):
    return Response(get_random_string(101))

  def post(self, request):
    try :
      schedule = get_current_schedule()
      if schedule != None:
        token = request.data['token']
        waktu = request.data['time']
        benar = request.data['benar']
        kontak = request.data['kontak']
        player = Player.objects.get(token=token, kontak=kontak.lower())
        if float(getattr(player, 'game_{}'.format(schedule.phase))) != 0:
          return Response({'message': 'Anda sudah Bermain hari ini'}, status=status.HTTP_403_FORBIDDEN)
        setattr(player, 'game_{}'.format(schedule.phase), float(waktu))
        setattr(player, 'benar_{}'.format(schedule.phase), int(benar))
        player.count_total()
        player.remove_token()
        player.save()
        return Response({'message': 'OK'})
      return Response({'message': 'Periode Game masih belum dimulai'}, status=status.HTTP_403_FORBIDDEN)
    except KeyError:
      return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
    except Player.DoesNotExist:
        return Response({'message': 'OKEEEEEEEE'})
