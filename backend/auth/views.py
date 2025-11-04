from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm

# Inscription
def register_view(request):
    if request.user.is_authenticated:
        return redirect("tasks:list")  # redirige vers la page principale si déjà connecté

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Compte créé avec succès ! Vous pouvez maintenant vous connecter.")
            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "auth/register.html", {"form": form})


# Connexion
def login_view(request):
    if request.user.is_authenticated:
        return redirect("tasks:list")

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Bienvenue {user.username} 👋")
            return redirect("tasks:list")
    else:
        form = LoginForm()

    return render(request, "auth/login.html", {"form": form})


# 🔹 Déconnexion
@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté.")
    return redirect("atuh:login")
