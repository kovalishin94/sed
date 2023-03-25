from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import UpdateView, ListView, CreateView
from .models import *
from .forms import *


class ListOutbox(LoginRequiredMixin, ListView):
    model = Doc
    template_name = 'docs/base_listdoc.html'
    context_object_name = 'content'

    def get_queryset(self):
        try:
            queryset = Doc.objects.filter(user_id=self.request.user.per.pk)
        except:
            raise Http404
        return queryset

class ListAgree(LoginRequiredMixin, ListView):
    model = Doc
    template_name = 'docs/base_listdoc.html'
    context_object_name = 'content'

    def get_queryset(self):
        try:
            queryset = Doc.objects.filter(status='C', agreementer=self.request.user.per)
        except:
            raise Http404
        return queryset

class CreateOutbox(LoginRequiredMixin, CreateView):
    form_class = NewOutboxForm
    template_name = 'docs/outbox_create.html'
    success_url = reverse_lazy('outbox')

    def form_valid(self, form):
        form.instance.status = 'C'
        form.instance.user = self.request.user.per
        return super().form_valid(form)


class UpdateOutbox(UpdateView):
    model = Doc
    form_class = NewOutboxForm
    template_name = 'docs/outbox_create.html'
    success_url = reverse_lazy('outbox')


def index(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('outbox')

        else:
            messages.add_message(request, messages.ERROR,
                                 'Неверный логин или пароль')
            return render(request, 'docs/auth.html')
    else:
        if request.user.is_authenticated:
            return redirect('outbox')
        else:
            return render(request, 'docs/auth.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect('auth')

@login_required
def del_doc(request, pk): 
    try:
        doc = Doc.objects.get(pk=pk)
    except:
        raise Http404
    if doc.user == request.user.per and doc.status in 'PDC':
        doc.delete()
    else:
        raise Http404
    return redirect('outbox')

@login_required
def agree(request, pk):
    try:
        doc = Doc.objects.get(pk=pk)
    except:
        raise Http404
    if doc.agreementer == request.user.per and doc.status in 'PDC':
        doc.status = 'S'
        doc.save()
    else:
        raise Http404
    return redirect('outbox')

@login_required
def revision(request, pk):
    try:
        doc = Doc.objects.get(pk=pk)
    except:
        raise Http404
    if doc.agreementer == request.user.per and doc.status in 'PC':
        doc.status = 'D'
        doc.save()
    else:
        raise Http404
    return redirect('outbox')

def ajax(request):
    person = list(Person.objects.values())
    return JsonResponse(person, safe=False)