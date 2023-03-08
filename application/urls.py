from django.urls import path
from . import views

urlpatterns = [
    path('songs/', views.index, name='songs'),
    path('result/', views.result, name='result'),
    path('test/', views.test, name='test'),
    path('',views.homepage,name='home'),
    path('journal',views.predict,name='journal'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.custom_login,name='login'),
    path('logout/',views.custom_logout,name='logout'),
    
]
