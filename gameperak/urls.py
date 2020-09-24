from django.urls import path
from .views import test, GameStart, SendResult

urlpatterns = [
    path('', test),
    path('start/', GameStart.as_view()),
    path('finish/', SendResult.as_view()),
]