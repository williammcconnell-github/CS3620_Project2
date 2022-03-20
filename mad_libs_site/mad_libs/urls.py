from . import views
from django.urls import path

app_name = 'mad_libs'
urlpatterns = [
    path('', views.home, name='home'),
]
