from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.db.models import fields
from .models import TaskModel

from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin


class UserLoginView(LoginView):
    template_name = "base/login.html"
    fields = '__all__'
    redirect_authenticated_user = True
    def get_success_url(self) -> str:
        return reverse_lazy('task-list')


class SignUpView(FormView):
    template_name = 'base/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('task-list')
    
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('task-list')
        return super().get(*args, **kwargs)



# Create your views here.
class TaskListView(LoginRequiredMixin, ListView):
    model = TaskModel
    context_object_name = "task_list"  # default will be object_list
    # By default every data will be returned by context to filter out only required data or add additional fields we have to override get_context_data method
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task_list"] = context["task_list"].filter(user=self.request.user) # only show task belong to the logged in user's task
        context["count"] = context["task_list"].filter(complete=False).count()
        search_value = self.request.GET.get('search_text') or ''
        if search_value:
            context["task_list"] = context["task_list"].filter(title__icontains=search_value)
            context["search_text"] = search_value
        return context
    
        


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = TaskModel
    context_object_name = "task"  # default will be object


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = TaskModel
    fields = ["title","description","complete"]  # django's build in forms will contains these fields if specified as list, if '__all__' is provided all filed must be included
    success_url = reverse_lazy("task-list")
    def form_valid(self, form):
        form.instance.user = self.request.user # specifying the user who is going to be the creator/editor
        return super().form_valid(form)

    


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = TaskModel
    fields = fields = ["title","description","complete"]
    success_url = reverse_lazy("task-list")

    


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = TaskModel
    context_object_name = 'task'
    success_url = reverse_lazy("task-list")
