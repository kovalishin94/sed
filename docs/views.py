from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import *


def index(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main')
        
        else:
            messages.add_message(request, messages.ERROR, 'Неверный логин или пароль')
            return render(request, 'docs/auth.html')
    else:
        if request.user.is_authenticated:
            return redirect('main')
        else:
            return render(request, 'docs/auth.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('auth')

@login_required
def main(request):
    content = Doc.objects.filter(user=Person.objects.get(name_id=request.user.pk))
    return render(request, 'docs/main.html', {'content': content})

@login_required
def newoutbox(request):
    if request.method == 'POST':
        form = NewOutboxForm(request.POST, request.FILES)
        if form.is_valid():
            doc = Doc.objects.create(**form.cleaned_data)
            doc.status = 'C'
            doc.user = Person.objects.get(name_id=request.user.pk)
            doc.save()
    else:
        form = NewOutboxForm()
    return render(request, 'docs/outbox_create.html', {'form': form})    