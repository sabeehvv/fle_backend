from django.urls import path
from .import views


urlpatterns = [
    path('fcmToken/',views.FCMTokenView.as_view(),name='fcmToken')
]