from django.urls import path
from .views import process_word, connectpuzzle

urlpatterns = [
    path('process-word/', process_word, name='process_word'),
    path('connect-puzzle/', connectpuzzle, name='connect-puzzle'),
]
