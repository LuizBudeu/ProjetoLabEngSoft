from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from .models import Voos, Partidas, Chegadas
from .filters import VoosFilter, PartidasFilter, ChegadasFilter, VoosFilterRead
from .extras import *
import pytz


tries = 0

def first(request):
    return render(request, 'FIRST.html')

def login(request):
    global tries
    context = {}
    logins = {
        'gerente' : {
            'password': 'gerente',
            'permission': 'relatorio'
        },
        'funcionario' : {
            'password': 'funcionario',
            'permission': 'monitoramento'
        },
        'operadorvoo' : {
            'password': 'operadorvoo',
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
        if username in logins and password == logins[username]['password'] and 2-tries >= 0:
            request.session['permission'] = logins[username]['permission']
            return redirect(f"home")
        elif 2-tries > 0: 
            tries += 1
            context['error_msg'] = f'Usuário ou senha errados. Tentativas restantes: {3-tries}'
        else:
            tries += 1
            context['error_msg'] = 'Tentativas esgotadas.'

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
    excs = []
    
    if request.method == 'POST':
        if request.POST['origem'] == "São Paulo" or request.POST['destino'] == "São Paulo":
            if request.POST['chegada_prevista'] and request.POST['partida_prevista']:
                chegada_prevista = datetime.strptime(request.POST['chegada_prevista'], '%Y-%m-%dT%H:%M')
                partida_prevista = datetime.strptime(request.POST['partida_prevista'], '%Y-%m-%dT%H:%M')
                partida_chegada_result = check_chegada_partida(chegada_prevista, partida_prevista, excs)
            else:
                excs.append(Exception('Partida prevista e chegada prevista têm que estar preenchidas.'))

            codigo_result = parse_code(request.POST['codigo'], excs)

            if codigo_result and partida_chegada_result:
                chegada_prevista, partida_prevista = partida_chegada_result
                codigo = codigo_result
                origem = request.POST['origem']
                destino = request.POST['destino']
                status = 'em voo'
                companhia_aerea = request.POST['companhia_aerea']
                if request.POST['destino'] == "São Paulo":
                    try:    
                        chegada = {
                            'companhia_aerea': companhia_aerea,
                            'codigo': codigo,
                            'status': status,
                            'origem': origem,
                            'chegada_prevista': chegada_prevista,
                        }
                        obj = Chegadas.objects.create(**chegada)
                        voo = {
                            'companhia_aerea': companhia_aerea,
                            'codigo': codigo,
                            'origem': origem,
                            'status': status,
                            'destino': destino,
                            'partida_prevista': partida_prevista,
                            'chegada_prevista': chegada_prevista,
                        }
                    except Exception as e:
                        error = e
                        print(error) 
                else:
                    try:
                        partida = {
                            'companhia_aerea': companhia_aerea,
                            'codigo': codigo,
                            'destino': destino,
                            'partida_prevista': partida_prevista,
                        }
                        obj = Partidas.objects.create(**partida)
                        voo = {
                            'companhia_aerea': companhia_aerea,
                            'codigo': codigo,
                            'origem': origem,
                            'destino': destino,
                            'partida_prevista': partida_prevista,
                            'chegada_prevista': chegada_prevista,
                        }
                    except Exception as e:
                        error = e
                obj = Voos.objects.create(**voo)
        else:
                excs.append(Exception('Preencha com um voo que pertence a esse aeroporto.'))
    
    context = {
        'obj': '' if obj is None else obj,
        'error': '' if error is None else error,
        'excs': excs,
    }
    return render(request, 'crud-create.html', context)


def crudread(request):
    voos_qs = Voos.objects.all()
    voos_filter = VoosFilterRead(request.GET, queryset=voos_qs)
    voos_qs = voos_filter.qs
    error = False

    if len(voos_qs) == 0:
        error = True

    context = {
        'voos_filter': voos_filter,
        'voos_qs': voos_qs,
        'error': error,
        'codigo': request.GET.get('codigo')
    }
    return render(request, 'crud-read.html', context)


def crudupdate(request):
    voos_qs = Voos.objects.all()
    voos_filter = VoosFilter(request.GET, queryset=voos_qs)
    voos_qs = voos_filter.qs
    obj = None
    error = None
    error_id = False
    excs = []
    # print(len(voos_qs), request.GET.get('codigo'))

    if len(voos_qs) == 0 and request.GET.get('id'):
        error_id = True
    
    voos_fields = [key.name for key in Voos._meta.fields]
    fields = {}

    if request.method == 'POST':
        for key in request.POST:
            if request.POST[key] == '':
                continue
            if key in voos_fields:
                fields[key] = request.POST[key]

        if fields.get('partida_prevista'):
            partida_prevista = pytz.UTC.localize(datetime.strptime(fields.get('partida_prevista'), '%Y-%m-%dT%H:%M'))
        else:
            partida_prevista = Voos.objects.get(id=request.GET['id']).partida_prevista

        if fields.get('chegada_prevista'):
            chegada_prevista = pytz.UTC.localize(datetime.strptime(fields.get('chegada_prevista'), '%Y-%m-%dT%H:%M'))
        else:
            chegada_prevista = Voos.objects.get(id=request.GET['id']).chegada_prevista

        chegada_partida_result = check_chegada_partida(chegada_prevista, partida_prevista, excs)
            
        if len(excs) == 0:
            chegada_prevista, partida_prevista = chegada_partida_result
            fields['chegada_prevista'] = chegada_prevista
            fields['partida_prevista'] = partida_prevista
            obj = Voos.objects.filter(id=request.GET['id']).update(**fields)
                    
    context = {
        'voos_filter': voos_filter,
        'voos_qs': voos_qs,
        'obj': obj,
        'error': '' if error is None else error,
        'excs': excs,
        'error_id': error_id,
        'id': request.GET.get('id')
    }
    return render(request, 'crud-update.html', context)


def cruddelete(request):
    voos_qs = Voos.objects.all()
    voos_filter = VoosFilter(request.GET, queryset=voos_qs) 
    voos_qs = voos_filter.qs
    id = None
    obj = None
    deleted = False
    codigo = None
    error_id = False
    
    id = request.GET.get('id')
    
    if len(voos_qs) == 0 and request.GET.get('id'):
        error_id = True

    if request.method == 'POST':
        deleted = True
        obj = Voos.objects.filter(id=id).delete()
    
    context = {
        'voos_filter': voos_filter,
        'voos_qs': voos_qs,
        'error_id': error_id,
        'codigo': codigo,
        'obj': obj,
        'id': request.GET.get('id'),
        'error': True if deleted and not obj[1] else False,
    }
    return render(request, 'crud-delete.html', context)


def monitoramento(request):
    chegadas_qs = Chegadas.objects.all()
    chegadas_filter = ChegadasFilter(request.GET, queryset=chegadas_qs)
    chegadas_qs = chegadas_filter.qs
    partidas_qs = Partidas.objects.all()
    partidas_filter = PartidasFilter(request.GET, queryset=partidas_qs)
    partidas_qs = partidas_filter.qs
    context = {
        'chegadas_filter': chegadas_filter,
        'chegadas_qs': chegadas_qs,
        'partidas_filter': partidas_filter,
        'partidas_qs': partidas_qs,
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
    error = None
    context = {
        'voos_filter': voos_filter,
        'voos_qs': voos_qs,
        'obj': obj,
        'error': '' if error is None else error,
    }
    voos_fields = [key.name for key in Voos._meta.fields]
    a = {}
    if request.method == 'POST':
        voo = voos_qs.get()
        if request.POST.get("chegada_real") is not None and voo.destino == "São Paulo":
            utc=pytz.UTC
            if voo.chegada_prevista >  utc.localize(datetime.strptime(request.POST["chegada_real"], "%Y-%m-%dT%H:%M")):  # Erro de datas
                context["error_msg"] = "Insira uma data válida."
                return render(request, 'estado.html', context)
            obj = Chegadas.objects.filter(codigo=voo.codigo).update(chegada_real = datetime.strptime(request.POST["chegada_real"], "%Y-%m-%dT%H:%M"))
        elif request.POST.get("partida_real") is not None and voo.origem == "São Paulo":
            utc=pytz.UTC
            if voo.partida_prevista > utc.localize(datetime.strptime(request.POST["partida_real"], "%Y-%m-%dT%H:%M")):  # Erro de datas
                context["error_msg"] = "Insira uma data válida."
                return render(request, 'estado.html', context)
            obj = Partidas.objects.filter(codigo=voo.codigo).update(partida_real = datetime.strptime(request.POST["partida_real"], "%Y-%m-%dT%H:%M"))
        else:
            if request.POST.get("status") != "aterrisando":
                    obj = Partidas.objects.filter(codigo=voo.codigo).update(status= request.POST.get("status"))
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
    voos_prontos = voos_filtered.filter(status="pronto")
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
        'hoje': datetime.now().date().strftime("%d/%m/%Y")
    }
    return render(request, 'mostrarelatoriodia.html', context)

def mostrarelatoriogeral(request):
    initial_date = datetime.strptime(request.session.get("initial-date"), "%Y-%m-%d")
    end_date = datetime.strptime(request.session.get("end-date"), "%Y-%m-%d")

    voos_filtered = Voos.objects.filter(partida_prevista__gte=initial_date, partida_prevista__lte=end_date)
    n_partidas = len(Partidas.objects.filter(partida_real__gte=initial_date, partida_real__lte=end_date))
    n_chegadas = len(Chegadas.objects.filter(chegada_real__gte=initial_date, chegada_real__lte=end_date))

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
    cia_mais_finalizados = max(cia_finalizados_dict if len(cia_finalizados_dict) > 0 else {"":0}, key=cia_finalizados_dict.get) or "(Nenhuma)"
    cia_finalizados = cia_finalizados_dict.get(cia_mais_finalizados) or "0"

    cia_cancelados_dict = {}
    for voo in voos_cancelados:
        if voo.companhia_aerea not in cia_cancelados_dict:
            cia_cancelados_dict[voo.companhia_aerea] = 1
        else:
            cia_cancelados_dict[voo.companhia_aerea] += 1
    cia_mais_cancelados = max(cia_cancelados_dict if len(cia_cancelados_dict) > 0 else {"":0}, key=cia_cancelados_dict.get) or "(Nenhuma)"
    cia_cancelados = cia_cancelados_dict.get(cia_mais_cancelados) or "0"

    context = {
        'finalizados' : n_finalizados,
        'cancelados' : n_cancelados,
        'atrasados' : voos_atrasados,
        'nao_atrasados' : voos_nao_atrasados,
        'companhia_mais_cancelados' : cia_mais_cancelados,
        'companhia_mais_finalizados' : cia_mais_finalizados,
        'mais_finalizados' : cia_finalizados,
        'mais_cancelados' : cia_cancelados,
        'data_inicio' : initial_date.strftime("%d/%m/%Y"),
        'data_fim' : end_date.strftime("%d/%m/%Y"),
        'partidas' : n_partidas,
        'chegadas' : n_chegadas
    }

    return render(request, 'mostrarelatoriogeral.html', context)