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
        if request.POST['username'] == 'luiz':
            return redirect('first')

    context = {}

    return render(request, 'login.html', context)


def home(request):
    context = {}
    return render(request, 'home.html', context)
