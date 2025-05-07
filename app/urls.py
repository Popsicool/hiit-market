from django.urls import path
from app.views import *

urlpatterns = [
    path('', home, name='home'),
    path('signup', signup, name='signup'),
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
]