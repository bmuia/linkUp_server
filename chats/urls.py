from django.urls import path
from .views import ChatHistoryView

urlpatterns = [
    path('v1/history/', ChatHistoryView.as_view(), name='chat-history'),
    
]