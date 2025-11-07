from django.apps import AppConfig


class AuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auth'
    # Pour résoudre le conflit car Django verra maintenant deux applications distinctes :
    # auth (l'application intégrée de Django)
    # custom_auth (votre application)
    label = 'custom_auth'  # Ajoutez cette ligne
