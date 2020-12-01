from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.

def index(request):
    context = {}
    return render(request, 'index.html', context)

def login(request):
    context = {}
    return render(request, "core/login.html", context)

def insercao(request):
    return HttpResponse("insercao")

def editar(request):
    return HttpResponse("editar_insercao")

def visualizar(request):
    return HttpResponse("visualizacao")

