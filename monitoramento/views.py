from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from .models import Voos, Partidas, Chegadas
from .filters import VoosFilter
import re


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
    error = None
    
    if request.method == 'POST':
        try:
            chegada_prevista = datetime.strptime(request.POST['chegada_prevista'], '%Y-%m-%dT%H:%M')
            partida_prevista = datetime.strptime(request.POST['partida_prevista'], '%Y-%m-%dT%H:%M')
            
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
        except Exception as e:
            error = e

    context = {
        'obj': '' if obj is None else obj,
        'error': '' if error is None else error,
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
    voos_qs = Voos.objects.all()
    voos_filter = VoosFilter(request.GET, queryset=voos_qs)
    voos_qs = voos_filter.qs
    obj = None

    if request.method == 'POST':  # TODO debugar isso
        for key in request.POST:
            if key in Voos._meta.fields:
                codigo = request.GET['codigo']
                obj = Voos.objects.get(codigo=codigo).update(key=request.POST[key.name])
                print(obj)

    context = {
        'voos_filter': voos_filter,
        'voos_qs': voos_qs,
        'obj': obj,
    }
    return render(request, 'crud-update.html', context)


def cruddelete(request):
    voos_qs = Voos.objects.all()
    voos_filter = VoosFilter(request.GET, queryset=voos_qs)
    voos_qs = voos_filter.qs
    codigo = None
    obj = None
    
    if request.method == 'POST':
        codigo = request.POST['codigo']  # TODO ver error message
        obj = Voos.objects.filter(codigo=codigo).delete() 
    
    context = {
        'voos_filter': voos_filter,
        'voos_qs': voos_qs,
        'codigo': codigo,
        'obj': obj,
        'error': True if obj is None and codigo else False,
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

    if request.POST.get("data-inicio") is not None:  # Relatório de período específico
        initial_date = request.POST["data-inicio"]
        end_date = request.POST["data-fim"]
        request.session["initial-date"] = initial_date
        request.session["end-date"] = end_date
        return redirect(f"mostrarelatoriogeral")

    # Relatório do dia
    initial_date = datetime.now().date()
    end_date = initial_date + timedelta(days=1)
    request.session["initial-date"] = initial_date.strftime("%Y-%m-%dT%H:%M")
    request.session["end-date"] = end_date.strftime("%Y-%m-%dT%H:%M")
    return redirect(f"mostrarelatoriodia")


def estado(request):
    voos_qs = Voos.objects.all()
    voos_filter = VoosFilter(request.GET, queryset=voos_qs)
    voos_qs = voos_filter.qs
    context = {
        'voos_filter': voos_filter,
         'voos_qs': voos_qs,
    }
    return render(request, 'estado.html', context)


def mostrarelatoriodia(request):
    initial_date = datetime.strptime(request.session.get("initial-date"), "%Y-%m-%dT%H:%M")
    end_date = datetime.strptime(request.session.get("end-date"), "%Y-%m-%dT%H:%M")

    voos_filtered = Voos.objects.filter(partida_prevista__gte=initial_date, partida_prevista__lte=end_date)

    voos_cancelados = voos_filtered.filter(status="cancelado")
    voos_embarcando = voos_filtered.filter(status="embarcando")
    voos_programados = voos_filtered.filter(status="programado")
    voos_autorizados = voos_filtered.filter(status="autorizado")
    voos_taxiando = voos_filtered.filter(status="taxiando")
    voos_prontos = voos_filtered.filter(status="prontos")
    voos_em_andamento = voos_filtered.filter(status="em voo")
    voos_finalizados = voos_filtered.filter(status="aterrissado")

    context = {
        'voos_cancelados': voos_cancelados,
        'voos_embarcando': voos_embarcando,
        'voos_programados': voos_programados,
        'voos_autorizados': voos_autorizados,
        'voos_taxiando': voos_taxiando,
        'voos_prontos': voos_prontos,
        'voos_em_andamento': voos_em_andamento,
        'voos_finalizados': voos_finalizados,
    }
    return render(request, 'mostrarelatoriodia.html', context)

def mostrarelatoriogeral(request):
    context = {}
    return render(request, 'mostrarelatoriogeral.html', context)