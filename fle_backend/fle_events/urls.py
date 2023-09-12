from django.urls import path
from .import views


urlpatterns = [
     path('create_event/',views.create_event.as_view(),name='create_event'),
     path('eventlist/',views.UserViewEventManage.as_view(),name='eventlist'),
     path('eventlist/detail/<str:event_id>/',views.UserViewEvenDetail.as_view(),name='detailss'),
     path('contributon/',views.ContributonView.as_view(),name='contributon'),
     path('verifySignature/',views.VerifySignatureView.as_view(),name='verifySignature'),
]