from django.urls import path
from .views import process_and_connect_game, validate_word_associations_view

urlpatterns = [
    path('process-and-connect-game/', process_and_connect_game, name='process_and_connect_game'),
    path('validate-word-association/',validate_word_associations_view, name='validate_word_associations_view')
]
