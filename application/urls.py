from django.urls import path
from . import views

urlpatterns = [
    # FIXME result page
    path('songs/', views.songs, name='songs'),
    path('result/', views.result, name='result'),
    path('test/', views.test, name='test'),
    path('', views.homepage, name='home'),
    path('predictMood/', views.predictMood, name='predictMood'),
    path('journal/', views.journal, name='journal'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    
]