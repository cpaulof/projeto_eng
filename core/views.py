import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import FormView
from django.contrib import messages

from .forms import LoginForm, AtracacaoForm, ToDoForm, ToDoForm2, AtracacaoForm2
from .models import Atracacao

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
    obj = get_object_or_404(Atracacao, solicitacao__usuario=request.user, pk=1)
    form = AtracacaoForm(instance=obj)

    #form = ToDoForm()

    return render(request, "core/test.html", {'form': form})

def editar(request, atrid):
    obj = get_object_or_404(Atracacao, solicitacao__usuario=request.user, pk=atrid)
    form = AtracacaoForm(instance=obj)
    #form = AtracacaoForm2()

    return render(request, "core/editar.html", {'form': form})

def visualizar(request):
    objs = Atracacao.objects.filter(status=0)
    
    context = {'objs':objs}
    if request.user.is_authenticated:
        context['nome_usuario'] = request.user.name
        context['logado'] = True
    return render(request, "core/visualizar.html", context)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Deslogado')
    
    return HttpResponseRedirect(reverse_lazy('index'))

    


