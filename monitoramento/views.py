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
            return redirect(f"home/{logins[username]['permission']}")
        else:
            context['error_msg'] = 'Usuário ou senha errados.'

    return render(request, 'login.html', context)


def home(request, permission='None'):
    context = {'permission': permission}
    return render(request, 'home.html', context)


def crud(request, permission='all'):
    context = {'permission': permission}
    return render(request, 'crud.html', context)


def monitoramento(request, permission='all'):
    context = {'permission': permission}
    return render(request, 'monitoramento.html', context)


def relatorio(request, permission='all'):
    context = {'permission': permission}
    return render(request, 'relatorio.html', context)