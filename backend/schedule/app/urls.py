from django.urls import path
from .views import TrainerAPIView, RecordAPIView, UserAPIView

app_name = 'app'

urlpatterns = [
    path('trainers/', TrainerAPIView.as_view(), name='trainers'),
    path('users/', UserAPIView.as_view(), name='users'),
    path('records/', RecordAPIView.as_view(), name='records'),
]


# /api/v1/trainers/ get
# /api/v1/users/ get
# /api/v1/records/ post
