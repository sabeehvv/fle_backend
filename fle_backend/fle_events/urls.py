from django.urls import path
from .import views


urlpatterns = [
     path('create_event/',views.EventCreateAPIView.as_view(),name='create_event'),
     path('eventlist/',views.EventListView.as_view(),name='eventlist'),
     path('eventlist/detail/<str:event_id>/',views.EventDetailView.as_view(),name='detailss'),
     path('contributon/',views.ContributonView.as_view(),name='contributon'),
     path('verifySignature/',views.VerifySignatureView.as_view(),name='verifySignature'),
     path('join_to_event/',views.EventJoinView.as_view(),name='join_to_event'),
     path('delete_join_to_event/<str:event_id>/',views.DeleteJoinView.as_view(),name='delete_join_to_event'),
     path('edit_event/<uuid:pk>/',views.EventUpdateAPIView.as_view(),name='edit_event'),
     path('Contributors/',views.ContributorsView.as_view(),name='Contributors'),
]