from django.http import Http404
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
    try:
        person = Person.objects.get(name_id=request.user.pk)
        content = Doc.objects.filter(user_id=person.pk)
    except:
        content=''
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
            return redirect('main')
    else:
        form = NewOutboxForm()
    return render(request, 'docs/outbox_create.html', {'form': form})

@login_required
def del_doc(request, pk):
    try:
        Doc.objects.get(pk=pk).delete()
    except:
        raise Http404
    return redirect('main')