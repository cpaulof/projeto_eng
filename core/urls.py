from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('insercao/', views.insercao, name='insercao'),
    path('editar/', views.editar, name='editar'),
    path('visualizar/', views.visualizar, name='visualizar')
]