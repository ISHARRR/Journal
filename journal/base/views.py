from django.shortcuts import render, redirect
from django.template.context_processors import request
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Imports for Reordering Feature
from django.views import View
from django.shortcuts import redirect
from django.db import transaction

from .models import Task, Contact, Stack
from .forms import PositionForm


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['task_recent'] = context['tasks'].filter(user=self.request.user).order_by('-updated_at')[:3]
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__contains=search_input)

        context['search_input'] = search_input

        return context


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'stack', 'contact', 'complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'stack', 'contact', 'complete']
    success_url = reverse_lazy('tasks')


class DeleteTaskView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')

    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)


class TaskReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                self.request.user.set_task_order(positionList)

        return redirect(reverse_lazy('tasks'))


# contacts
class ContactList(LoginRequiredMixin, ListView):
    model = Contact
    context_object_name = 'contacts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contacts'] = context['contacts'].filter(user=self.request.user)

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['contacts'] = context['contacts'].filter(
                first_name__contains=search_input)

        context['search_input'] = search_input

        return context


class ContactCreate(LoginRequiredMixin, CreateView):
    model = Contact
    fields = ['first_name', 'last_name', 'phone']
    success_url = reverse_lazy('contacts')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ContactCreate, self).form_valid(form)


class ContactUpdate(LoginRequiredMixin, UpdateView):
    model = Contact
    fields = ['first_name', 'last_name', 'phone']
    success_url = reverse_lazy('contacts')


class DeleteContactView(LoginRequiredMixin, DeleteView):
    model = Contact
    context_object_name = 'Contact'
    success_url = reverse_lazy('contacts')


# stack
class StackList(LoginRequiredMixin, ListView):
    model = Stack
    context_object_name = 'stacks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stacks'] = context['stacks'].filter(user=self.request.user)

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['stacks'] = context['stacks'].filter(
                language__contains=search_input)

        context['search_input'] = search_input

        return context


class StackCreate(LoginRequiredMixin, CreateView):
    model = Stack
    fields = ['language', 'description']
    success_url = reverse_lazy('stacks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(StackCreate, self).form_valid(form)


class StackUpdate(LoginRequiredMixin, UpdateView):
    model = Stack
    fields = ['language', 'description']
    success_url = reverse_lazy('stacks')


class DeleteStackView(LoginRequiredMixin, DeleteView):
    model = Stack
    context_object_name = 'Stack'
    success_url = reverse_lazy('stacks')


