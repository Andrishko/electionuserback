from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('counter/', views.counter, name='count'),
    path('check/', views.check, name='check'),
    path('get_key/', views.get_key, name='key'),
]
