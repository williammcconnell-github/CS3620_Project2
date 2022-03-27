from . import views
from django.urls import path

app_name = 'mad_libs'
urlpatterns = [
    path('', views.home, name='home'),
    path('madlibs', views.mad_libs, name='mad_libs'),
    path('madlibs/<int:mad_lib_id>', views.mad_lib_detail, name='mad_lib_detail'),
    path('madlibs/create', views.create_mad_lib, name='create_mad_lib'),
    path('madlibs/<int:mad_lib_id>/update', views.update_mad_lib, name='update_mad_lib'),
    path('madlibs/<int:mad_lib_id>/delete', views.delete_mad_lib, name='delete_mad_lib'),
    path('wordlist/create', views.create_word_list, name='create_word_list'),
]
