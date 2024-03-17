from django.urls import path
from .views import SendMessageView

urlpatterns = [
    path('', SendMessageView.as_view(), name='send_mesage'),
]