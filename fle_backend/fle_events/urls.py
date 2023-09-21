from django.urls import path
from .import views


urlpatterns = [
     path('create_event/',views.create_event.as_view(),name='create_event'),
     path('eventlist/',views.UserViewEventManage.as_view(),name='eventlist'),
     path('eventlist/detail/<str:event_id>/',views.UserViewEvenDetail.as_view(),name='detailss'),
     path('contributon/',views.ContributonView.as_view(),name='contributon'),
     path('verifySignature/',views.VerifySignatureView.as_view(),name='verifySignature'),
     path('join_to_event/',views.EventJoinView.as_view(),name='join_to_event'),
     path('delete_join_to_event/<str:event_id>/',views.EventJoinView.as_view(),name='delete_join_to_event'),
     path('edit_event/<str:event_id>/',views.create_event.as_view(),name='edit_event'),
]