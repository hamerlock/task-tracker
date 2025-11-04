from django.db import models
from django.conf import settings
from django.utils import timezone

class Task(models.Model):
    # --- Conseil n°1 : Utiliser des choix pour les catégories ---
    # Plutôt qu'un champ de texte libre, utiliser des choix (Choices)
    # garantit la cohérence des données et évite les fautes de frappe.
    class Category(models.TextChoices):
        WORK = 'WORK', 'Travail'
        PERSONAL = 'PERSO', 'Personnel'
        HOME = 'HOME', 'Maison'
        OTHER = 'OTHER', 'Autre'

    # --- Vos attributs, avec des noms de champs en anglais (convention Django) ---
    description = models.TextField(verbose_name="Description")
    category = models.CharField(
        max_length=10,
        choices=Category.choices,
        default=Category.OTHER,
        verbose_name="Catégorie"
    )
    start_date = models.DateTimeField(verbose_name="Date de début", null=True, blank=True)
    end_date = models.DateTimeField(verbose_name="Date de fin", null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Actif")

    # --- Conseil n°2 : Utiliser AUTH_USER_MODEL pour la liaison utilisateur ---
    # C'est la meilleure pratique pour lier un modèle à votre modèle utilisateur,
    # qu'il soit celui par défaut de Django ou un modèle personnalisé.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tasks")

    # --- Conseil n°3 : Ajouter des horodatages automatiques ---
    # C'est très utile pour savoir quand une tâche a été créée ou modifiée.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.description[:50]}... ({self.user.username})"