from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import FormView
from django.contrib import messages

from .forms import LoginForm

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        return redirect('visualizar')
    else:
        return redirect('login')

    

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data['email'], password=data['password'])
            if user is not None:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, 'Usuário autenticado')
                return HttpResponseRedirect(reverse_lazy('visualizar'))
            else:
                messages.add_message(request, messages.ERROR, 'Dados incorretos')
                return HttpResponseRedirect(reverse_lazy('login'))
    else:
        if request.user.is_authenticated:
            messages.add_message(request, messages.SUCCESS, 'Usuário autenticado')
            return HttpResponseRedirect(reverse_lazy('visualizar'))
        form = LoginForm()
        return render(request, "core/login.html", {'form': form})

def insercao(request):
    return HttpResponse("insercao")

def editar(request):
    return HttpResponse("editar_insercao")

def visualizar(request):
    logout(request)
    return HttpResponse("visualizacao")

    


