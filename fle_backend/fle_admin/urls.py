from django.urls import path
from .import views


urlpatterns = [
     path('userlist/',views.AdminViewUserManage.as_view(),name='user-manage'),
     path('status-user/<int:pk>/',views.AdminViewUserManage.as_view(),name='status-user'),
     path('eventlist/',views.AdminViewEventManage.as_view(),name='event-manage'),
     path('status-event/<str:id>/',views.AdminViewEventManage.as_view(),name='status-event'),
     path('landing-page-update/',views.LandingPageUpdateView.as_view(),name='landing-page-update'),
     path('landing-page-View/',views.LandingPageView.as_view(),name='landing-page-View'),
     path('EventHighlight/',views.AdminEventHighlight.as_view(),name='EventHighlight'),
     path('EventHighlight-create/',views.EventHighlightCreateView.as_view(),name='EventHighlight-create'),
     path('EventHighlight-delete/<int:pk>/',views.EventHighlightDeleteView.as_view(),name='EventHighlight-delete'),
     path('dashboardData/',views.UserDataAPIView.as_view(),name='dashboardData'),
]