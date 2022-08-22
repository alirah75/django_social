from django.urls import path
from .views import RegisterUser


app_name = 'account'
urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),

]
