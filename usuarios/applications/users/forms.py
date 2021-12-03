from typing_extensions import Required
from django import forms
from usuarios.settings import base
from django.contrib.auth import authenticate

from .models import User

class UserRegisterForm(forms.ModelForm):

    password1 = forms.CharField(
        label= 'Contrasena',
        required=True,
        widget= forms.PasswordInput(
            attrs={
                'placeholder':'Contrasena'
            }
        )
    )
    password2 = forms.CharField(
        label= 'Contrasena',
        required=True,
        widget= forms.PasswordInput(
            attrs={
                'placeholder':'Repetir contrasena'
            }
        )
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'nombres',
            'apellidos',
            'genero',
            #'username',
        )

    def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            self.add_error('password2', 'Las contrasenas no coinciden')

class LoginForm(forms.Form):
    username = forms.CharField(
        label= 'username',
        required=True,
        widget= forms.TextInput(
            attrs={
                'placeholder':'username',
                'style':'{margin:10px}',
            }
        )
    )
    password = forms.CharField(
        label= 'Contrasena',
        required=True,
        widget= forms.PasswordInput(
            attrs={
                'placeholder':'Contrasena'
            }
        )
    )

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if not authenticate(username=username,password=password):
            raise forms.ValidationError('Los datos de usuario no son validos')

        return self.cleaned_data

class UpdatePasswordForm(forms.Form):
    password1 = forms.CharField(
        label= 'Contrasena',
        required=True,
        widget= forms.PasswordInput(
            attrs={
                'placeholder':'Contrasena actual'
            }
        )
    )

    password2 = forms.CharField(
        label= 'Contrasena',
        required=True,
        widget= forms.PasswordInput(
            attrs={
                'placeholder':'Contrasena nueva'
            }
        )
    )

class VerificarForms(forms.Form):
    codregistro = forms.CharField(required = True)

    def __init__(self, pk, *args, **kwargs):
        self.id_user = pk
        super(VerificarForms,self).__init__(*args, **kwargs)

    def clean_codregistro(self):
        codigo = self.cleaned_data['codregistro']

        if len(codigo) == 6:
            #Verificamos si el codigo y el id de usuario son validos
            activo = User.objects.cod_validation(
                self.id_user,
                codigo
            )
            if not activo:
                raise forms.ValidationError('Codigo incorrecto')
        else:
            raise forms.ValidationError('Codigo incorrecto')