import datetime
from django.shortcuts import render, redirect
from .models import Voos, Partidas, Chegadas
from .filters import VoosFilter


def first(request):
    return render(request, 'FIRST.html')

def login(request):
    context = {}
    logins = {
        'felipe' : {
            'password': 'felipe',
            'permission': 'relatorio'
        },
        'gabriel' : {
            'password': 'gabriel',
            'permission': 'monitoramento'
        },
        'luiz' : {
            'password': 'luiz',
            'permission': 'crud'
        },
        'admin': {
            'password': 'admin',
            'permission': 'all'
        }
    }

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username in logins and password == logins[username]['password']:
            request.session['permission'] = logins[username]['permission']
            return redirect(f"home")
        else:
            context['error_msg'] = 'Usuário ou senha errados.'

    return render(request, 'login.html', context)


def home(request):
    context = {'permission': request.session.get('permission')}
    return render(request, 'home.html', context)


def crud(request):
    # now = datetime.now().replace(tzinfo=timezone.utc)
    # voo = {
    #     'companhia_aerea': 'Azul',
    #     'codigo': 'XX1111',
    #     'origem': 'São Paulo',
    #     'destino': 'Rio de Janeiro',
    #     'partida_prevista': now,
    #     'chegada_prevista': now,
    # }
    # print(request.POST)
    
    # Voos.objects.create(**voo)

    context = {}
    return render(request, 'crud.html', context)


def crudcreate(request):  
    obj = None
    created = False
    
    if request.method == 'POST':
        created = False
        chegada_prevista = datetime.datetime.strptime(request.POST['chegada_prevista'], '%Y-%m-%d %H:%M:%S')
        partida_prevista = datetime.datetime.strptime(request.POST['partida_prevista'], '%Y-%m-%d %H:%M:%S') # TODO pegar de jeito certo, com calendar widget
        
        # TODO parsear codigo
        
        voo = {
            'companhia_aerea': request.POST['companhia'],
            'codigo': request.POST['codigo'],
            'origem': request.POST['origem'],
            'destino': request.POST['destino'],
            'partida_prevista': partida_prevista,
            'chegada_prevista': chegada_prevista,
        }
        print(request.POST)
        
        obj = Voos.objects.create(**voo)

    context = {
        'obj': '' if obj is None and not created else obj,
    }
    return render(request, 'crud-create.html', context)


def crudread(request):
    voos_qs = Voos.objects.all()
    voos_filter = VoosFilter(request.GET, queryset=voos_qs)
    voos_qs = voos_filter.qs
    
    print(voos_qs)

    context = {
        'voos_filter': voos_filter,
        'voos_qs': voos_qs,
    }
    return render(request, 'crud-read.html', context)


def crudupdate(request):
    context = {}
    return render(request, 'crud-update.html', context)


def cruddelete(request):
    context = {}
    return render(request, 'crud-delete.html', context)


def monitoramento(request):
    voos_qs = Voos.objects.all()
    voos_filter = VoosFilter(request.GET, queryset=voos_qs)
    voos_qs = voos_filter.qs
    context = {
        'voos_filter': voos_filter,
         'voos_qs': voos_qs,
    }
    return render(request, 'monitoramento.html', context)


def relatorio(request):
    context = {}

    if request.method == "POST":
        initial_date = request.POST["data-inicio"]
        end_date = request.POST["data-fim"]
        voos = Voos.objects.all()
        voos_filter = VoosFilter(request.GET, voos)
    return render(request, 'relatorio.html', context)


def estado(request):
    
    context = {}
    
    return render(request, 'estado.html', context)


def mostrarelatorio(request):
    context = {}
    return render(request, 'mostrarelatorio.html', context)