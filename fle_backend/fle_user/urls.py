from django.urls import path
from .import views


urlpatterns = [


     path('register/',views.RegisterView.as_view(),name='register'),

     path('login/',views.LoginView.as_view(),name='login'),

     path('Googlelogin/',views.GoogleLoginView.as_view(),name='Googlelogin'),

     path('check_auth/',views.CheckAuthView.as_view(),name="check_auth"),

     path('user/view/',views.UserHomeView.as_view(),name='user-view'),

     path('user/edit-profile/',views.UserHomeView.as_view(),name='user-edit-profile'),

     path('verify-email/<str:token>/',views.RegisterView.as_view(),name='verify-email'),

    #  path('logout/', views.LogoutView.as_view(), name='logout'),

]