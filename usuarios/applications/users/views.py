from django.shortcuts import render
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import CreateView, View
from django.views.generic.edit import FormView


from .forms import (
    UserRegisterForm,
    LoginForm,
    UpdatePasswordForm,
    VerificarForms
)
from .models import User
from .functions import generar_codigo

# Create your views here.

class UserCreateView(FormView):
    template_name = "user/crear_usuario.html"
    form_class = UserRegisterForm
    success_url = '/'

    def form_valid(self, form):

        codigo = generar_codigo()
        usuario = User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            nombres = form.cleaned_data['nombres'],
            apellidos = form.cleaned_data['apellidos'],
            genero = form.cleaned_data['genero'],
            codregistro = codigo
        )
        #Enviar codigo al email
        #Definicion de variables
        asunto='Confirmacion de email'
        mensaje = 'Codigo de verificacion: ' + codigo
        email_remitente = 'cristian.garcia.rua@gmail.com'
        #Logica del send mail
        send_mail(asunto,mensaje,email_remitente, [form.cleaned_data['email'],])
        #Redirigir a pantalla de validacion
        return HttpResponseRedirect(
            reverse(
                'users_app:validacion',
                kwargs={'pk':usuario.id}
            )
        )

        #return super(UserCreateView,self).form_valid(form)

class Login(FormView):
    template_name = "user/login.html"
    form_class = LoginForm
    success_url = reverse_lazy('home_app:panel')

    def form_valid(self, form):
        user = authenticate(
            username = form.cleaned_data['username'],
            password = form.cleaned_data['password']
        )
        login(self.request, user)
        return super(Login,self).form_valid(form)

class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        
        return HttpResponseRedirect(
            reverse(
                'users_app:login'
            )
        )

class ActualizarContrasena(LoginRequiredMixin,FormView):
    template_name = "user/updatep.html"
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('users_app:login')
    login_url = reverse_lazy('users_app:login')

    def form_valid(self, form):
        usuario = self.request.user
        user = authenticate(
            username = usuario.username,
            password = form.cleaned_data['password1']
        )
        if user:
            new_password = form.cleaned_data['password2']
            usuario.set_password(new_password)
            usuario.save()

        logout(self.request)
        return super(ActualizarContrasena,self).form_valid(form)

class ValidarUser(FormView):
    template_name = "user/validacion.html"
    form_class = VerificarForms
    success_url = reverse_lazy('users_app:login')

    def get_form_kwargs(self):
        kwargs = super(ValidarUser,self).get_form_kwargs()
        kwargs.update({
            'pk':self.kwargs['pk'],
        })
        return kwargs

    def form_valid(self, form):
        User.objects.filter(
            id = self.kwargs['pk']
        ).update(
            is_active = True
        )
        return super(ValidarUser,self).form_valid(form)