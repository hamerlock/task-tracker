from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Task
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'tasks/list.html'

    def get_queryset(self):
        base_qs = Task.objects.filter(user=self.request.user).order_by('-created_at')
        current_filter = self.request.GET.get('filter', 'all')
        if current_filter == 'active':
            return base_qs.filter(is_active=True)
        if current_filter == 'completed':
            return base_qs.filter(is_active=False)
        return base_qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_tasks = Task.objects.filter(user=self.request.user)
        context.update({
            'stats': {
                'total': user_tasks.count(),
                'active': user_tasks.filter(is_active=True).count(),
                'completed': user_tasks.filter(is_active=False).count(),
            },
            'current_filter': self.request.GET.get('filter', 'all'),
        })
        return context
    
class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/detail.html'

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'tasks/form.html'
    success_url = reverse_lazy('tasks:list')

    def form_valid(self, form):
        # Associe automatiquement la tâche à  l'utilisateur connecté
        form.instance.user = self.request.user
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    template_name = 'tasks/form.html'
    success_url = reverse_lazy('tasks:list')

    def test_func(self):
        # Vérifie que l'utilisateur qui modifie est bien le propriétaire de la tâche
        return self.get_object().user == self.request.user

class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'tasks/confirm_delete.html'
    success_url = reverse_lazy('tasks:list')

    def test_func(self):
        return self.get_object().user == self.request.user
    
class TaskFinishView(LoginRequiredMixin, UserPassesTestMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk, user=request.user)
        if task.is_active:
            task.is_active = False
            if not task.end_date:
                task.end_date = timezone.now()
            task.save(update_fields=["is_active", "end_date"])
        return redirect('tasks:list')

    def test_func(self):
        try:
            obj = Task.objects.get(pk=self.kwargs.get('pk'))
        except Task.DoesNotExist:
            return False
        return obj.user == self.request.user
