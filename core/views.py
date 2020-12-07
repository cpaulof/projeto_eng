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

def submit_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email)
        print(password)

        user = authenticate(username=email, password=password)

        if user is not None:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, 'Usuário autenticado')
                return HttpResponseRedirect(reverse_lazy('visualizar'))
        else:
            messages.error(request, 'Dados incorretos!')
        return render(request, "core/login.html", {})


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse_lazy('visualizar'))
    return render(request, 'core/login.html')
#    if request.method == 'POST':
#        form = LoginForm(request.POST)
#
#        if form.is_valid():
#            data = form.cleaned_data
#            user = authenticate(username=data['email'], password=data['password'])
#            if user is not None:
#                login(request, user)
#                messages.add_message(request, messages.SUCCESS, 'Usuário autenticado')
#                return HttpResponseRedirect(reverse_lazy('visualizar'))
#            else:
#                messages.add_message(request, messages.ERROR, 'Dados incorretos')
#                return HttpResponseRedirect(reverse_lazy('login'))
#    else:
#        if request.user.is_authenticated:
#            messages.add_message(request, messages.SUCCESS, 'Usuário autenticado')
#            return HttpResponseRedirect(reverse_lazy('visualizar'))
#        form = LoginForm()
#        return render(request, "core/login.html", {'form': form})

def insercao(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    context = {}
    context['base_template'] =  _get_base_template(request)
    
    if request.method == "POST":
        navio = request.POST['navio']
        navio = _get_navio_or_create(request, navio)
        if navio is None:
            return HttpResponseRedirect(reverse_lazy('insercao'))
        try:
            berco = int(request.POST['berco'])
            berco = get_object_or_404(Berco, pk=berco)
        except ValueError:
            messages.error(request, "Informação de berço incorreta!")
            return HttpResponseRedirect(reverse_lazy('insercao'))
        solicitacao = Solicitacao.objects.create(usuario=request.user, navio=navio, berco=berco)
        solicitacao.save()
        messages.success(request, "Solicitação criada!")
        messages.success(request, "Você será notificado quando ela for atendida.")

    context['bercos'] = list(Berco.objects.all())
    return render(request, "core/insercao.html", context)

def editar(request, atrid):
    context = {}
    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    context['base_template'] = 'base_autenticado.html'
    if request.user.user_type in (1, 3):
        obj = get_object_or_404(Solicitacao, pk=atrid)
    else:
        obj = get_object_or_404(Solicitacao, usuario=request.user, pk=atrid)
    
    if request.method == "POST":
        try:
            berco = int(request.POST['berco'])
            berco = obj.berco = get_object_or_404(Berco, pk=berco)
        except ValueError:
            messages.error(request, "Informação de berço incorreta!")
            return HttpResponseRedirect(reverse_lazy('editar', kwargs={"atrid": atrid}))
        navio = request.POST['navio']
        navio = _get_navio_or_create(request, navio)
        if navio is None:
            return HttpResponseRedirect(reverse_lazy('editar', kwargs={"atrid": atrid}))
        obj.berco = berco
        obj.navio = navio
        obj.save()
        messages.success(request, "Solicitação editada")
        return HttpResponseRedirect(reverse_lazy('solicitacoes'))

    context['obj'] = obj
    context['bercos'] = list(Berco.objects.all())
    return render(request, "core/editar.html", context)


def visualizar(request):    
    context = {}
    context['base_template'] =  _get_base_template(request)
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
    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    context['base_template'] = 'base_autenticado.html'
    if request.user.user_type in (1, 3):
        result = Solicitacao.objects.filter(status=0).order_by('data')
    else:
        result = Solicitacao.objects.filter(status=0, usuario=request.user).order_by('data')
    context['solicitacoes'] = result
    return render(request, "core/solicitacoes.html", context)

    
def solicitacao(request, pk=None):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    context = {}
    user_type = request.user.user_type
    context['base_template'] =  _get_base_template(request)
    if user_type in (1, 3):
        obj = get_object_or_404(Solicitacao, pk=pk)
    else:
        obj = get_object_or_404(Solicitacao, pk=pk, usuario=request.user)

    context['user_type'] = user_type
    context['obj'] = obj

    return render(request, "core/solicitacao.html", context)


def confirmar_solicitacao(request, pk):
    if not request.user.is_authenticated and request.user.user_type not in (1, 3):
        return HttpResponseForbidden()
    obj = get_object_or_404(Solicitacao, pk=pk)
    obj.status = 1
    obj.save()
    return HttpResponse("CONFIRMAR" + str(pk))

def excluir_solicitacao(request, pk):
    return HttpResponse("EXCLUIR")

def _get_base_template(request):
    if request.user.is_authenticated:
        return 'base_autenticado.html'
    return 'base.html'

def _get_navio_or_create(request, navio):
    if not navio.replace(' ', '').isalnum():
        messages.error(request, "Identificação do navio inválida!")
        return None
    nome_navio = navio.upper()
    try:
        navio = Navio.objects.get(nome=nome_navio)
    except Navio.DoesNotExist:    
        navio = Navio.objects.create(nome=nome_navio)
        navio.save() 
    return navio

