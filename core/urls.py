from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path("login/submit", views.submit_login),
    path('insercao/', views.insercao, name='insercao'),
    path('editar/<int:atrid>', views.editar, name='editar'),
    path('visualizar/', views.visualizar, name='visualizar'),
    path('logout/', views.logout_view, name='logout'),
    path('solicitacoes/', views.solicitacoes, name='solicitacoes'),
    path('solicitacao/<int:pk>', views.solicitacao, name='solicitacao'),
]