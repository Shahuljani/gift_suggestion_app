from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('suggestion/generate/', views.generate_suggestions, name='generate_suggestions'),
]