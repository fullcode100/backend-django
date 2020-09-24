from django.test import TestCase, Client
from gameperak.models import GameSchedule, Player
from datetime import datetime
import pytz

''' TEST DISINI '''
class GamePerakTest(TestCase):
  def setUp(self):
    self.client = Client()
    self.start_url = '/game/start/'
    self.finish_url = '/game/finish/'

  def setSchedule(self):
    # setup schedule with phase 1
    utc=pytz.UTC
    now = utc.localize(datetime.utcnow())
    later = utc.localize(datetime(now.year, now.month, now.day+1))
    GameSchedule.objects.create(start=now, end=later, phase=1)


class GameStartTest(TestCase):
  def setUp(self):
    self.client = Client()
    self.url = '/game/start/'

  def setSchedule(self):
    # setup schedule
    utc=pytz.UTC
    now = utc.localize(datetime.utcnow())
    later = utc.localize(datetime(now.year, now.month, now.day+1))
    GameSchedule.objects.create(start=now, end=later, phase=1)

  def assert_fake(self, response):
    # assert there is token but no player (fake token)
    self.assertContains(response, 'token')
    self.assertNotContains(response, 'player')

  def assert_right(self, response):
    # assert there is both token and player
    self.assertContains(response, 'token')
    self.assertContains(response, 'player')

  def assert_same_token(self, response, player):
    # assert same token from player and response
    self.assertEqual(player.token, response.data['token'])

  def assert_status_code(self, response, status_code=200):
    # assert status code 
    self.assertEqual(response.status_code, status_code)


  ''' get to this api will return fake token but no player created '''
  def test_cant_get(self):
    response = self.client.get(self.url)
    self.assert_status_code(response)
    self.assert_fake(response)

  ''' post will return token and player if there is a gameSchedule active '''
  def test_post_new_player(self):
    response = self.client.post(self.url, {'kontak': 'player1'})
    self.assert_status_code(response, 403)
    self.assertEqual(response.data['message'], 'Periode Game masih belum dimulai')

    # Creating Game Schedule
    self.setSchedule()

    response = self.client.post(self.url, {'kontak': 'player1'})
    self.assert_right(response)
    self.assert_same_token(response, Player.objects.get(kontak='player1'))

  ''' test with no post data return fake token '''
  def test_with_no_data(self):
    self.setSchedule()
    response = self.client.post(self.url, {})
    self.assert_status_code(response)
    self.assert_fake(response)

  ''' post with exsisting player will always return same token while not used '''
  def test_existing_player(self):
    self.setSchedule()

    response_1 = self.client.post(self.url, {'kontak': 'player1'})
    token = Player.objects.all()[0].token
    self.assertEqual(Player.objects.all()[0].kontak, 'player1')

    response = self.client.post(self.url, {'kontak': 'player1'})
    self.assert_right(response)
    self.assertEqual(token, response.data['token'])
    self.assertEqual(token, response_1.data['token'])
    self.assertEqual(response_1.data['token'], response.data['token'])
    self.assert_status_code(response)
    self.assert_status_code(response_1)

  ''' already play player cant get token '''
  def test_already_play_player(self):
    self.setSchedule()
    Player.objects.create(kontak="kontak", game_1=70)
    response = self.client.post(self.url, {'kontak': 'kontak'})
    self.assert_status_code(response, 403)
    self.assertEqual(response.data['message'], 'Anda sudah Bermain hari ini')


class GameFinishTest(TestCase):
  def setUp(self):
    self.client = Client()
    self.url = '/game/finish/'
    Player.objects.create(token="haha", kontak="player1")

  def setSchedule(self):
    # setup schedule
    utc=pytz.UTC
    now = utc.localize(datetime.utcnow())
    later = utc.localize(datetime(now.year, now.month, now.day+1))
    GameSchedule.objects.create(start=now, end=later, phase=1)

  def assert_right(self, response):
    self.assertEqual(response.data['message'], 'OK')

  def assert_fake(self, response):
    self.assertEqual(response.data['message'], 'OKEEEEEEEE')

  def assert_status_code(self, response, status_code=200):
    # assert status code 
    self.assertEqual(response.status_code, status_code)

  def test_bad_request(self):
    self.setSchedule()
    body = {}
    res = self.client.post(self.url, body)
    self.assert_status_code(res, 400)
    self.assertEqual(res.data['message'], 'Bad Request')

    body['kontak'] = 'player1'
    res = self.client.post(self.url, body)
    self.assert_status_code(res, 400)
    self.assertEqual(res.data['message'], 'Bad Request')

    body['token'] = 'haha'
    res = self.client.post(self.url, body)
    self.assert_status_code(res, 400)
    self.assertEqual(res.data['message'], 'Bad Request')

    body['time'] = 100
    res = self.client.post(self.url, body)
    self.assert_status_code(res, 400)
    self.assertEqual(res.data['message'], 'Bad Request')

    body['benar'] = 3
    res = self.client.post(self.url, body)
    self.assert_status_code(res, 200)
    self.assert_right(res)


  def test_post_no_schedule(self):
    res = self.client.post(self.url, {'kontak': 'player1', 'token': 'haha', 'benar': 3, 'time': 100})
    self.assert_status_code(res, 403)
    self.assertEqual(res.data['message'], 'Periode Game masih belum dimulai')

    self.setSchedule()
    res = self.client.post(self.url, {'kontak': 'player1', 'token': 'haha', 'benar': 3, 'time': 100})
    self.assert_status_code(res, 200)
    self.assert_right(res)

  def test_post_wrong_token(self):
    self.setSchedule()
    res = self.client.post(self.url, {'kontak': 'player1', 'token': 'hahasalah', 'benar': 3, 'time': 100})
    self.assert_status_code(res, 200)
    self.assert_fake(res)

  def test_cant_post_twice(self):
    self.setSchedule()
    self.client.post(self.url, {'kontak': 'player1', 'token': 'haha', 'benar': 3, 'time': 100})
    res = self.client.post(self.url, {'kontak': 'player1', 'token': 'haha', 'benar': 3, 'time': 100})
    self.assert_fake(res)

    player = Player.objects.get(kontak='player1')
    self.assertEqual(player.token, None)
    player.token = 'test'
    player.save()
    res = self.client.post(self.url, {'kontak': 'player1', 'token': 'test', 'benar': 3, 'time': 100})
    self.assertEqual(res.data['message'], 'Anda sudah Bermain hari ini')
    self.assert_status_code(res, 403)

  def test_right_amount_of_time(self):
    self.setSchedule()
    time = 40
    res = self.client.post(self.url, {'kontak': 'player1', 'token': 'haha', 'benar': 3, 'time': time})
    player = Player.objects.get(kontak='player1')
    self.assertEqual(player.total_time, time)
    self.assertEqual(player.game_1, time)
    
    schedule = GameSchedule.objects.all()[0]
    schedule.phase = 2
    schedule.save()

    player = Player.objects.get(kontak='player1')
    player.token = 'hari2'
    player.save()

    time2 = 60
    res = self.client.post(self.url, {'kontak': 'player1', 'token': 'hari2', 'benar': 3, 'time': time2})
    self.assert_right(res)
    player = Player.objects.get(kontak='player1')
    self.assertEqual(player.game_1, time)
    self.assertEqual(player.game_2, time2)
    self.assertEqual(player.total_time, time+time2)