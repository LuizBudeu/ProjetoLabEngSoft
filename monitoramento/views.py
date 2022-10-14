from django.shortcuts import render, redirect

def first(request):
    return render(request, 'FIRST.html')

def login(request):
    logins = {
        'felipe' : {
            'password': 'felipe',
        },
        'gabriel' : {
            'password': 'gabriel',
        },
        'luiz' : {
            'password': 'luiz',
        }
    }

    if request.method == 'POST':
        print(request.POST.keys())
        print(request.POST['username'])
        username = request.POST['username']
        password = request.POST['password']
        if username in logins and password == logins[username]['password']:
            return redirect('home')

    context = {}

    return render(request, 'login.html', context)


def home(request):
    context = {}
    return render(request, 'home.html', context)
