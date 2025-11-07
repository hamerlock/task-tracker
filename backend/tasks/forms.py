from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['description', 'category', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_date'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['end_date'].input_formats = ('%Y-%m-%dT%H:%M',)
        # Required fields
        self.fields['description'].required = True
        self.fields['category'].required = True
        # Bootstrap styling 
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Description de la tâche', 'rows': '2', 'required': 'required'})
        self.fields['category'].widget.attrs.update({'class': 'form-select', 'required': 'required'})
        self.fields['start_date'].widget.attrs.update({'class': 'form-control'})
        self.fields['end_date'].widget.attrs.update({'class': 'form-control'})
        #self.fields['is_active'].widget.attrs.update({'class': 'form-check-input'})

