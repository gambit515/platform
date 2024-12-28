from django.urls import path
from . import views

urlpatterns = [
    path('', views.video_page, name='video_page'),
    path('mathanal', views.math_anal, name='math_anal'),
]