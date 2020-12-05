import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.template import loader
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import FormView
from django.contrib import messages

from .forms import LoginForm, AtracacaoForm
from .models import Atracacao, Solicitacao, Navio,  Berco

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
    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    if request.method == "POST":
        navio = request.POST['navio']
        if not navio.replace(' ', '').isalnum():
            messages.error(request, "Identificação do navio inválida!")
            return HttpResponseRedirect(reverse_lazy('insercao'))
        nome_navio = navio.upper()
        try:
            navio = Navio.objects.get(nome=nome_navio)
        except Navio.DoesNotExist:    
            navio = Navio.objects.create(nome=nome_navio)
            navio.save()   
        solicitacao = Solicitacao.objects.create(usuario=request.user, navio=navio)
        solicitacao.save()
        messages.success(request, "Solicitação criada!")
        messages.success(request, "Você será notificado quando ela for atendida.")
    


    return render(request, "core/insercao.html", {})

def editar(request, atrid):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    obj = get_object_or_404(Atracacao, solicitacao__usuario=request.user, pk=atrid)
    form = AtracacaoForm(instance=obj)
    #form = AtracacaoForm2()

    return render(request, "core/editar.html", {'form': form})

def visualizar(request):    
    context = {}
    if request.user.is_authenticated:
        context['base_template'] = 'base_autenticado.html'
    else:
        context['base_template'] = 'base.html'
        
    bercos = Berco.objects.all()
    solitacoes = [Solicitacao.objects.filter(berco=i,  status=1).order_by('data') for i in list(bercos)]
    context['solicitacoes'] = solitacoes

    return render(request, "core/visualizar.html", context)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Deslogado')
    
    return HttpResponseRedirect(reverse_lazy('index'))

    
def solicitacoes(request):
    context = {}
    if request.user.is_authenticated:
        context['base_template'] = 'base_autenticado.html'
    else:
        context['base_template'] = 'base.html'

    if not request.user.is_authenticated or request.user.user_type not in (1, 3):
        return HttpResponseForbidden()
    result = Solicitacao.objects.filter(status=0).order_by('data')
    context['solicitacoes'] = result
    return render(request, "core/solicitacoes.html", context)

    
def solicitacao(request, pk=None):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    context = {}
    obj = get_object_or_404(Solicitacao, pk=pk)
    if obj.usuario == request.user:
        context = {
            'owner': True,
        }
    context['user_type'] = request.user.user_type
    context['obj'] = obj

    return render(request, "core/solicitacao.html", context)

