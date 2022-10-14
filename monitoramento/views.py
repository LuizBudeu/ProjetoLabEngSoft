from django.shortcuts import render, redirect

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
            return redirect(f"home")
        else:
            context['error_msg'] = 'Usuário ou senha errados.'

    return render(request, 'login.html', context)


def home(request, permission='None'):
    context = {'permission': permission}
    return render(request, 'home.html', context)


def crud(request, permission='all'):
    context = {'permission': permission}
    return render(request, 'crud.html', context)

def crudcreate(request):
    context = {}
    return render(request, 'crud-create.html', context)

def crudread(request):
    context = {}
    return render(request, 'crud-read.html', context)

def crudupdate(request):
    context = {}
    return render(request, 'crud-update.html', context)

def cruddelete(request):
    context = {}
    return render(request, 'crud-delete.html', context)

def monitoramento(request):
    context = {}
    return render(request, 'monitoramento.html', context)


def relatorio(request):
    context = {}
    return render(request, 'relatorio.html', context)

def estado(request):
    context = {}
    return render(request, 'estado.html', context)

def mostrarelatorio(request):
    context = {}
    return render(request, 'mostrarelatorio.html', context)