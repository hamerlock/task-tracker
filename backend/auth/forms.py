from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password

# Formulaire d'inscription
class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput,
        validators=[validate_password]
    )
    password_confirm = forms.CharField(
        label="Confirmer le mot de passe",
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["username"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Bootstrap styling
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': "Nom d'utilisateur"})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Mot de passe'})
        self.fields['password_confirm'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirmer le mot de passe'})
        # Messages d'erreur en français
        self.fields['username'].error_messages.update({'required': "Le nom d'utilisateur est requis."})
        self.fields['password'].error_messages.update({'required': "Le mot de passe est requis."})
        self.fields['password_confirm'].error_messages.update({'required': "La confirmation du mot de passe est requise."})

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if username and User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Ce nom d'utilisateur est déjà pris.")
        return username

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return password_confirm

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


# Formulaire de connexion (basé sur celui de Django)
class LoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': "Identifiants invalides. Vérifiez le nom d'utilisateur et le mot de passe.",
        'inactive': "Ce compte est inactif.",
    }

    username = forms.CharField(label="Nom d'utilisateur")
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Bootstrap styling
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': "Nom d'utilisateur"})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Mot de passe'})
        # Messages d'erreur en français
        self.fields['username'].error_messages.update({'required': "Le nom d'utilisateur est requis."})
        self.fields['password'].error_messages.update({'required': "Le mot de passe est requis."})
