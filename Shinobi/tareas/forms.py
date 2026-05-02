from django import forms
from .models import Actividad
from django.contrib.auth.models import User


class CreatForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = ['titulo', 'descripcion', 'importante']

        widgets = {'titulo': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Write a título' }), 'descripcion': forms.Textarea(attrs={  'class': 'form-control', 'placeholder': 'Write a descripción'  }), 'importante': forms.CheckboxInput(attrs={   'class': 'form-check-input m-auto' }),}


class RegistroForm(forms.Form):
    username = forms.CharField( max_length=150,  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario'})  )

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo'}) )

    password1 = forms.CharField(  widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}) )

    password2 = forms.CharField( widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar contraseña'}) )

    numero = forms.CharField( widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Celular'}) )

    documento = forms.CharField( widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Documento'}) )

    plan = forms.ChoiceField(
        choices=[
            ('basico', 'Básico'),
            ('premium', 'Premium'),
            ('vip', 'VIP'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def clean(self):
        cleaned = super().clean()

        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")

        if p1 != p2:
            raise forms.ValidationError("Las contraseñas no coinciden")

        return cleaned