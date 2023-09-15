from django.urls import path
from .import views


urlpatterns = [
     path('userlist/',views.AdminViewUserManage.as_view(),name='user-manage'),
     path('status-user/<int:pk>/',views.AdminViewUserManage.as_view(),name='status-user'),
     path('eventlist/',views.AdminViewEventManage.as_view(),name='event-manage'),
     path('status-event/<str:id>/',views.AdminViewEventManage.as_view(),name='status-event'),
     path('landing-page-update/',views.LandingPageUpdate.as_view(),name='landing-page-update'),
     path('EventHighlight/',views.AdminEventHighlight.as_view(),name='EventHighlight'),
     path('EventHighlight-create/',views.AdminEventHighlight.as_view(),name='EventHighlight-create'),
     path('EventHighlight-delete/<int:pk>/',views.AdminEventHighlight.as_view(),name='EventHighlight-delete'),  
]