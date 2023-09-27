from django.urls import path
from .import views


urlpatterns = [
    path('landing-page-View/',views.landingpageView.as_view(),name='landing-page-View'),
    path('EventHighlight-View/',views.EventHighlightView.as_view(),name='EventHighlight-View'),
    path('Volunteers-View/',views.VolunteersView.as_view(),name='Volunteers-View'),
]