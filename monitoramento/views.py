from datetime import datetime, timedelta
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
        
        obj = Voos.objects.create(**voo)

    context = {
        'obj': '' if obj is None and not created else obj,
    }
    return render(request, 'crud-create.html', context)


def crudread(request):
    voos_qs = Voos.objects.all()
    voos_filter = VoosFilter(request.GET, queryset=voos_qs)
    voos_qs = voos_filter.qs

    context = {
        'voos_filter': voos_filter,
        'voos_qs': voos_qs,
    }
    return render(request, 'crud-read.html', context)


def crudupdate(request):
    context = {}
    return render(request, 'crud-update.html', context)


def cruddelete(request):
    voos_qs = Voos.objects.all()
    voos_filter = VoosFilter(request.GET, queryset=voos_qs)
    voos_qs = voos_filter.qs
    
    if request.method =='GET': 
        codigo = request.GET.get('codigo')  # TODO codigo unico?
        obj = Voos.objects.filter(codigo=codigo).delete()  # TODO tela de confirmação de delete
    
    context = {
        'voos_filter': voos_filter,
        'voos_qs': voos_qs,
        'codigo': codigo,
        'obj': obj,
    }
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
    if request.method == "GET":
        return render(request, 'relatorio.html', context)

    if request.method == "POST":  # Relatório de período específico
        initial_date = request.POST["data-inicio"]
        end_date = request.POST["data-fim"]
        request.session["initial-date"] = initial_date
        request.session["end-date"] = end_date

    elif request.method == "PATCH":  # Relatório do dia
        initial_date = datetime.now().date()
        end_date = initial_date + timedelta(days=1)
        request.session["initial-date"] = initial_date.strftime("%Y-%m-%dT%H:%M")
        request.session["end-date"] = end_date.strftime("%Y-%m-%dT%H:%M")
    
    return redirect(f"mostrarelatorio")


def estado(request):
    
    context = {}
    
    return render(request, 'estado.html', context)


def mostrarelatorio(request):
    initial_date = datetime.strptime(request.session.get("initial-date"), "%Y-%m-%dT%H:%M")
    end_date = datetime.strptime(request.session.get("end-date"), "%Y-%m-%dT%H:%M")

    voos_filter = Voos.objects.filter(partida_prevista__gte=initial_date, partida_prevista__lte=end_date)
    voos_qs = Voos.objects.all()
    context = {
        'voos_filter': voos_filter,
        'voos_qs': voos_qs,
    }
    return render(request, 'mostrarelatorio.html', context)