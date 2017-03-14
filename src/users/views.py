from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View

from users.forms import LoginForm


class LoginView(View):

    def get(self, request):
        """
        Presenta el formulario de login a un usuario
        :param request: HttpRequest
        :return: HttpResponse
        """

        context = {
            'form': LoginForm()
        }

        return render(request, 'login.html', context)

    def post(self, request):
        """
        Hace login de un usuario
        :param request: HttpRequest
        :return: HttpResponse
        """

        form = LoginForm(request.POST)
        context = dict()
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                # Usuario autenticado
                request.session["default-language"] = "es"
                django_login(request, user)
                url = request.GET.get('next', 'posts_list') #Permite redirigir a la url desde donde venga el usuario al hacer login
                return redirect(url)
            else:
                # Usuario no autenticadopero
                context["error"] = "Wrong username or password"
        context['form'] = form
        return render(request, 'login.html', context)


class SignupView(View):

    def get(self, request):
        """
        Presenta el formulario de registro a un usuario
        :param request: HttpRequest
        :return: HttpResponse
        """

        context = {
            'form': UserCreationForm()
        }

        return render(request, 'signup.html', context)

    def post(self, request):
        """
        Hace el registro de un usuario
        :param request: HttpRequest
        :return: HttpResponse
        """

        form = UserCreationForm(request.POST)
        print(form.errors)
        context = dict()
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            email = form.data.get("email")
            first_name = form.data.get("first_name")
            last_name = form.data.get("last_name")
            f = form.save(commit=False)
            f.email = email
            f.first_name = first_name
            f.last_name = last_name
            f.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                # Usuario autenticado
                request.session["default-language"] = "es"
                django_login(request, user)
                return HttpResponseRedirect('/')
        else:
            # Usuario no autenticadopero
            context["error"] = "El formulario no es válido"
        context['form'] = form
        return render(request, 'signup.html', context)


def logout(request):
    """
    Hace logout de un usuario
    :param request:
    :return:
    """
    django_logout(request)
    return redirect('login')