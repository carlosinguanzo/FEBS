from django.shortcuts import render
from django.views.generic import TemplateView
from Plan_Amigo.forms import UserForm, UserAttributesForm, TenderoForm, TransportadorForm, JefeBodegaForm, \
    TeleVentasForm, LoginForm


class HomeView(TemplateView):
    template_name = 'home.html'

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import hashlib
import datetime
from django.contrib.auth import authenticate, login, REDIRECT_FIELD_NAME
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, Context
from django.views.generic import TemplateView
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.core.mail import send_mail, EmailMessage
from django.utils import timezone


# Create your views here.
class UserRegistration(TemplateView):
    template_name = 'signup.html'

    def get_context_data(self, **kwargs):
        context = super(UserRegistration, self).get_context_data(**kwargs)
        context['formulario1'] = UserForm()
        context['formulario2'] = UserAttributesForm()
        context['formulario3'] = TenderoForm()
        context['formulario4'] = TransportadorForm()
        context['formulario5'] = JefeBodegaForm()
        context['formulario6'] = TeleVentasForm()

        return context

    def post(self, request, *args, **kwargs):

        post_values = request.POST.copy()
        userForm = UserForm(post_values)
        userattrForm = UserAttributesForm(post_values)
        #tenderoForm = TenderoForm(post_values)
        #direcForm = DireccionForm(post_values)

        if userForm.is_valid()  and userattrForm.is_valid():
            # User
            new_user = userForm.save()
            new_user.set_password(post_values['password'])
            new_user.save()


            # Direction
            #direction = direcForm.save()

            # User Attributes
            userattr = userattrForm.save(commit=False)
            userattr.user = new_user
            userattr.save()
            #userattr.direccion = direction

            #User Rol
            if userattr.User_Rol.name == "Tendero":
                tenderoForm = TenderoForm(post_values)
                tenForm = tenderoForm.save(commit=False)
                tenForm.user = new_user
                tenForm.save()
            elif userattr.User_Rol.name == "Transportador":
                transporForm = TransportadorForm(post_values)
                transForm = transporForm.save(commit=False)
                transForm.user = new_user
                transForm.save()
            elif userattr.User_Rol.name == "Jefe de bodega":
                jefeForm = JefeBodegaForm(post_values)
                jefeForm = jefeForm.save(commit=False)
                jefeForm.user = new_user
                jefeForm.save()
            elif userattr.User_Rol.name == "Televentas":
                teleForm = TeleVentasForm(post_values)
                teleForm = teleForm.save(commit=False)
                teleForm.user = new_user
                teleForm.save()



            return HttpResponseRedirect(reverse_lazy('login'))
        else:
            context = {
                        'formulario1':userForm,
                        'formulario2': userattrForm,
                        'formulario3': TenderoForm(),
                        'formulario4': TransportadorForm(),
                        'formulario5': JefeBodegaForm(),
                        'formulario6': TeleVentasForm(),

                        #'formulario2': direcForm
                      }
            return render_to_response('signup.html', context,
                                      context_instance=RequestContext(request))


def authenticate_user(username=None, password=None):
    """ Authenticate a user based on email address as the user name. """
    try:
        user = User.objects.get(email=username)
        if user is not None:
            return user
    except User.DoesNotExist:
        try:
            user = User.objects.get(username=username)
            if user is not None:
                return user
        except User.DoesNotExist:
            return None


def login_request(request,redirect_field_name=REDIRECT_FIELD_NAME):
    redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, '../../../?msg=1'))
    context = {'next':redirect_to}
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse_lazy('home'))

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user_auth = authenticate_user(username, password)
            if user_auth is not None:
                user = authenticate(username=user_auth.username,
                                    password=password)
            else:
                form.add_error(None, "La combinación celular contraseña es incorrecta")
                user = None
                context = {'error': "La combinación celular contraseña es incorrecta"}
                return render_to_response('login.html', context,
                                          context_instance=RequestContext(request))
            if (user is not None) and user.is_active:
                login(request, user)
                return HttpResponseRedirect(redirect_to)
            else:
                context = {'error': "La combinación celular contraseña es incorrecta"}
                return render_to_response('login.html', context,
                                          context_instance=RequestContext(request))
    else:
        form = LoginForm()
    context['form']=form
    return render_to_response('login.html', context,
                              context_instance=RequestContext(request))