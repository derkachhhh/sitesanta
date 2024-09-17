from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('secret_santa/', views.secret_santa, name='secret_santa'),
]
