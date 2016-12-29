#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, validate_email
from Plan_Amigo.models import *

# Longitudes de campos
MAX_NAME = 25
MIN_PASSWORD = 6
MAX_PASSWORD = 10
MAX_ID = 10
MAX_PHONE = 12
MAX_EMAIL = 255
MAX_NUMBER = 9999

#   validators  #
NAME_VALIDATOR = RegexValidator(
    regex='^[\'\-A-Za-záéíóúñÑÁÉÍÓÚäëïöüÄËÏÖÜ][\'\-A-Za-záéíóúñÑÁÉÍÓÚäëïöüÄËÏÖÜ ]*$',
    message='El nombre no puede iniciar con espacio en blanco ni contener números ni caracteres desconocidos.',
)

ID_VALIDATOR = RegexValidator(
    regex='^[0-9]+$',
    message='La cédula solo puede contener caracteres numéricos.',
)

PHONE_VALIDATOR = RegexValidator(
    regex=r'^(0414|0412|0424|0416|0426)\d{7}$',
    message="Formato inválido.",
)


class UserForm(forms.ModelForm):
    username = forms.CharField(
        label="Celular",
        validators=[PHONE_VALIDATOR]
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput()
    )

    first_name = forms.CharField(
        label="Nombre",
        validators=[NAME_VALIDATOR]
    )
    last_name = forms.CharField(
        label="Apellido",
        validators=[NAME_VALIDATOR]
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        ##placeholder
        self.fields['first_name'].widget.attrs['placeholder'] = 'Sólo se admiten letras'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Sólo se admiten letras'
        self.fields['password'].widget.attrs['placeholder'] = 'Sólo caracteres alfanuméricos'
        self.fields['username'].widget.attrs['placeholder'] = 'Sólo caracteres numéricos'
        self.fields['email'].widget.attrs['placeholder'] = 'Ej: nombre@example.com'

        for key in self.fields:
            self.fields[key].required = True
            self.fields[key].widget.attrs['required'] = 'True'
            self.fields[key].widget.attrs['class'] = 'form-control inputs-unete'
            self.fields[key].widget.attrs['aria-describedby'] = "basic-addon1"


class UserAttributesForm(forms.ModelForm):
    class Meta:
        model = UserAttributes
        fields = ('cedula', 'User_Rol')

    def __init__(self, *args, **kwargs):
        super(UserAttributesForm, self).__init__(*args, **kwargs)

        self.fields['cedula'].widget.attrs['placeholder'] = 'Ej: 00000000000'
        self.fields['User_Rol'].widget.attrs['id'] = 'Rol'

        for key in self.fields:
            self.fields[key].widget.attrs['class'] = 'form-control'
            self.fields[key].required = True
            self.fields[key].widget.attrs['required'] = 'True'
            self.fields[key].widget.attrs['class'] = 'form-control inputs-unete'
            self.fields[key].widget.attrs['aria-describedby'] = "basic-addon1"


class TenderoForm(forms.ModelForm):
    class Meta:
        model = Tendero
        fields = ('barrio', 'nombre_tienda', 'fecha_ingreso', 'como_llego',
                  'ruta', 'tipo', 'interes', 'direccion', 'smartphone', 'comentarios')

    def __init__(self, *args, **kwargs):
        super(TenderoForm, self).__init__(*args, **kwargs)

        ##placeholder
        self.fields['barrio'].widget.attrs['placeholder'] = 'Sólo caracteres alfanuméricos'
        self.fields['nombre_tienda'].widget.attrs['placeholder'] = 'Sólo caracteres alfanuméricos'
        self.fields['comentarios'].widget.attrs['placeholder'] = 'Sólo caracteres alfanuméricos'

        for key in self.fields:
            self.fields[key].required = True
            self.fields[key].widget.attrs['required'] = 'True'
            self.fields[key].widget.attrs['class'] = 'form-control inputs-unete'
            self.fields[key].widget.attrs['aria-describedby'] = "basic-addon1"


class TransportadorForm(forms.ModelForm):
    class Meta:
        model = Transportador
        fields = ('ruta',)

    def __init__(self, *args, **kwargs):
        super(TransportadorForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = True
            self.fields[key].widget.attrs['required'] = 'True'
            self.fields[key].widget.attrs['class'] = 'form-control inputs-unete'
            self.fields[key].widget.attrs['aria-describedby'] = "basic-addon1"


class JefeBodegaForm(forms.ModelForm):
    class Meta:
        model = JefeBodega
        fields = ('bodega',)

    def __init__(self, *args, **kwargs):
        super(JefeBodegaForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = True
            self.fields[key].widget.attrs['required'] = 'True'
            self.fields[key].widget.attrs['class'] = 'form-control inputs-unete'
            self.fields[key].widget.attrs['aria-describedby'] = "basic-addon1"


class TeleVentasForm(forms.ModelForm):
    class Meta:
        model = TeleVentas
        fields = ('puesto',)

    def __init__(self, *args, **kwargs):
        super(TeleVentasForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = True
            self.fields[key].widget.attrs['required'] = 'True'
            self.fields[key].widget.attrs['class'] = 'form-control inputs-unete'
            self.fields[key].widget.attrs['aria-describedby'] = "basic-addon1"


class DireccionForm(forms.ModelForm):
    class Meta:
        model = Direccion
        exclude = []
        widgets = {
            'calle': forms.TextInput(
                attrs={'placeholder': 'Ej: Av. Ej, Edif. Ej, Piso 3, Apto. 3A'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(DireccionForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs['required'] = 'True'
            self.fields[key].widget.attrs['class'] = 'form-control inputs-unete'
            self.fields[key].widget.attrs['aria-describedby'] = "basic-addon1"


'''
class CelularForm(forms.ModelForm):
    class Meta:
        model = UserAttributes
        fields = ('tlf_celular',)
        widgets = {
            'tlf_celular': forms.TextInput(
                attrs={
                    'placeholder': 'Ej: 00000000000',
                    'class': 'form-control inputs-unete',
                    'aria-describedby': 'basic-addon1'
                })
        }


'''


class LoginForm(forms.Form):
    username = forms.CharField(max_length=60, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    # remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput())

    labels = {
        'username': 'Número Celular',
    }
