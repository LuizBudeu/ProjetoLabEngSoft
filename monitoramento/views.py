from django.shortcuts import render

def first(request):
    return render(request, 'FIRST.html')

def login(request):
    return render(request, 'login.html')
