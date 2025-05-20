from django.urls import path
from .views import process_and_connect_game

urlpatterns = [
    path('process-and-connect-game/', process_and_connect_game, name='process_and_connect_game'),
]
