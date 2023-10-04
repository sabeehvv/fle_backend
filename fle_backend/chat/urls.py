from django.urls import path
from .import views


urlpatterns = [
    path('event/<str:event_id>/',views.ChatMessageApiView.as_view(),name='messages')
]