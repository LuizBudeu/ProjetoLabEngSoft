from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from .models import Voos, Partidas, Chegadas
from .filters import VoosFilter
import re
import pytz


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
                'companhia_aerea': request.POST['companhia_aerea'],
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
    
    voos_fields = [key.name for key in Voos._meta.fields]
    print(voos_fields)
    a = {}

    if request.method == 'POST':
        for key in request.POST:
            if request.POST[key] == '':
                continue
            if key in voos_fields:
                print(key)
                a[key] = request.POST[key]
        
        print(a)
        obj = Voos.objects.filter(codigo=request.GET['codigo']).update(**a)
                
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
    deleted = False
    
    if request.method == 'POST':
        deleted = True
        codigo = request.POST['codigo'] 
        obj = Voos.objects.filter(codigo=codigo).delete() 
    
    context = {
        'voos_filter': voos_filter,
        'voos_qs': voos_qs,
        'codigo': codigo,
        'obj': obj,
        'error': True if deleted and codigo else False,
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
        if initial_date == "" or end_date == "" or datetime.strptime(initial_date, "%Y-%m-%d") > datetime.strptime(end_date, "%Y-%m-%d"):  # Erro de datas
            context["error_msg"] = "Insira datas válidas."
            return render(request, 'relatorio.html', context)
        request.session["initial-date"] = initial_date
        request.session["end-date"] = end_date
        return redirect(f"mostrarelatoriogeral")

    # Relatório do dia
    initial_date = datetime.now().date()
    end_date = initial_date + timedelta(days=1)
    request.session["initial-date"] = initial_date.strftime("%Y-%m-%d")
    request.session["end-date"] = end_date.strftime("%Y-%m-%d")
    return redirect(f"mostrarelatoriodia")


def estado(request):
    voos_qs = Voos.objects.all()
    voos_filter = VoosFilter(request.GET, queryset=voos_qs)
    voos_qs = voos_filter.qs
    obj = None
     
    voos_fields = [key.name for key in Voos._meta.fields]
    print(voos_fields)
    a = {}
    context = {
        'voos_filter': voos_filter,
        'voos_qs': voos_qs,
        'obj': obj,
    }
    if request.method == 'POST':
        voo = voos_qs.get()
        if request.POST.get("chegada_real") is not None:
            utc=pytz.UTC
            if voo.chegada_prevista >  utc.localize(datetime.strptime(request.POST["chegada_real"], "%Y-%m-%dT%H:%M")):  # Erro de datas
                context["error_msg"] = "Insira datas válidas."
                return render(request, 'estado.html', context)
        if request.POST.get("partida_real") is not None:
            utc=pytz.UTC
            if voo.partida_prevista > utc.localize(datetime.strptime(request.POST["partida_real"], "%Y-%m-%dT%H:%M")):  # Erro de datas
                context["error_msg"] = "Insira datas válidas."
                return render(request, 'estado.html', context)
        for key in request.POST:
            if request.POST[key] == '':
                continue
            if key in voos_fields:
                print(key)
                a[key] = request.POST[key]
        
        print(a)
        obj = Voos.objects.filter(codigo=request.GET['codigo']).update(**a)
    return render(request, 'estado.html', context)


def mostrarelatoriodia(request):
    initial_date = datetime.strptime(request.session.get("initial-date"), "%Y-%m-%d")
    end_date = datetime.strptime(request.session.get("end-date"), "%Y-%m-%d")

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
    initial_date = datetime.strptime(request.session.get("initial-date"), "%Y-%m-%d")
    end_date = datetime.strptime(request.session.get("end-date"), "%Y-%m-%d")

    voos_filtered = Voos.objects.filter(partida_prevista__gte=initial_date, partida_prevista__lte=end_date)

    voos_cancelados = voos_filtered.filter(status="cancelado")
    n_cancelados = len(voos_cancelados)
    voos_finalizados = voos_filtered.filter(status="aterrissado")
    n_finalizados = len(voos_finalizados)

    voos_atrasados = len([voo for voo in voos_filtered.exclude(partida_real__isnull=True) if voo.partida_real > voo.partida_prevista])
    voos_nao_atrasados = len(voos_filtered) - voos_atrasados

    cia_finalizados_dict = {}
    for voo in voos_finalizados:
        if voo.companhia_aerea not in cia_finalizados_dict:
            cia_finalizados_dict[voo.companhia_aerea] = 1
        else:
            cia_finalizados_dict[voo.companhia_aerea] += 1
    cia_mais_finalizados = max(cia_finalizados_dict if len(cia_finalizados_dict) > 0 else {"":0}, key=cia_finalizados_dict.get) or ""
    cia_finalizados = cia_finalizados_dict[cia_mais_finalizados]

    cia_cancelados_dict = {}
    for voo in voos_cancelados:
        if voo.companhia_aerea not in cia_cancelados_dict:
            cia_cancelados_dict[voo.companhia_aerea] = 1
        else:
            cia_cancelados_dict[voo.companhia_aerea] += 1
    cia_mais_cancelados = max(cia_cancelados_dict if len(cia_cancelados_dict) > 0 else {"":0}, key=cia_cancelados_dict.get) or ""
    cia_cancelados = cia_cancelados_dict[cia_mais_cancelados]

    context = {
        'finalizados' : n_finalizados,
        'cancelados' : n_cancelados,
        'atrasados' : voos_atrasados,
        'nao_atrasados' : voos_nao_atrasados,
        'companhia_mais_cancelados' : cia_mais_cancelados,
        'companhia_mais_finalizados' : cia_mais_finalizados,
        'mais_finalizados' : cia_finalizados,
        'mais_cancelados' : cia_cancelados
    }

    return render(request, 'mostrarelatoriogeral.html', context)