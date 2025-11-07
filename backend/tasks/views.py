from django.views.generic.edit import FormMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Task
from .forms import TaskForm
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone


class TaskListView(LoginRequiredMixin, FormMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'tasks/list.html'
    # Formulaire utilisé pour la création depuis la page liste
    form_class = TaskForm

    # Intercepte le POST du formulaire de création 
    # Valide le formulaire et redirige, sinon ré-affiche la page avec les erreurs
    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    # Construit l'URL de redirection après création
    # 1) Si un champ hidden 'next' est présent, on y retourne (préserve l'URL/filtre)
    # 2) Sinon, on retourne vers la liste en conservant le filtre courant si différent de 'all'
    def get_success_url(self):
        next_url = self.request.POST.get('next')
        if next_url:
            return next_url  # Permet de revenir exactement sur l'URL courante (avec filtre)
        base = reverse_lazy('tasks:list')
        current_filter = self.request.GET.get('filter')
        if current_filter and current_filter != 'all':
            return str(base) + '?filter=' + current_filter
        return str(base)
    
    # Associe la tâche à l'utilisateur courant et enregistre
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return redirect(self.get_success_url())

    # Ré-affiche la page avec le formulaire en erreurs
    def form_invalid(self, form):
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)

    # Retourne les tâches de l'utilisateur en appliquant le filtre (all/active/completed)
    # Tâches triées des plus récentes aux plus anciennes
    def get_queryset(self):
        base_qs = Task.objects.filter(user=self.request.user).order_by('-created_at')
        current_filter = self.request.GET.get('filter', 'all')
        if current_filter == 'active':
            return base_qs.filter(is_active=True)
        if current_filter == 'completed':
            return base_qs.filter(is_active=False)
        return base_qs

    # Ajoute les statistiques, le filtre courant et le formulaire au contexte
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
        context['form'] = self.get_form()
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/detail.html'


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/form.html'
    success_url = reverse_lazy('tasks:list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/form.html'
    success_url = reverse_lazy('tasks:list')

    def test_func(self):
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
