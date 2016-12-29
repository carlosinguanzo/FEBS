from django.db import models

# Create your models here.

# !/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
import datetime
from decimal import Decimal
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator

PHONE_VALIDATOR = RegexValidator(
    regex=r'^(0414|0412|0424|0416|0426)\d{7}$',
    message="Formato inválido.",
)

NAME_VALIDATOR = RegexValidator(
    regex='^[\'\-A-Za-záéíóúñÑÁÉÍÓÚäëïöüÄËÏÖÜ][\'\-A-Za-záéíóúñÑÁÉÍÓÚäëïöüÄËÏÖÜ ]*$',
    message='El nombre no puede iniciar con espacio en blanco ni contener números ni caracteres desconocidos.',
)

ID_VALIDATOR = RegexValidator(
    regex='^[0-9]+$',
    message='La cédula solo puede contener caracteres numéricos.',
)

APORTE = 10


# Direcciones
class Estado(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Ciudad(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Municipio(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Direccion(models.Model):
    estado = models.ForeignKey(Estado)
    ciudad = models.ForeignKey(Ciudad)
    municipio = models.ForeignKey(Municipio)
    calle = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return "Calle " + self.calle + ", Mcpo. " + self.municipio.name + ". " \
               + self.ciudad.name + ", Edo. " + self.estado.name + ", Venezuela."


# User models.


class Rol(models.Model):
    # Users roles
    name = models.CharField('Nombre del rol', max_length=50)

    def __str__(self):
        return self.name


class UserAttributes(models.Model):
    user = models.OneToOneField(User)
    cedula = models.CharField('Número de cedula', max_length=12, validators=[ID_VALIDATOR])
    User_Rol = models.ForeignKey(Rol, null=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " " + self.User_Rol


class PuntosDolorTypes(models.Model):
    nombre = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return "%i, %s" % (self.pk, self.nombre)


class PuntosDolor(models.Model):
    punto_dolor = models.ForeignKey(PuntosDolorTypes)
    check = models.BooleanField(default=True)


class Ruta(models.Model):
    nombre = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.nombre


class Tendero(models.Model):
    AMIGO = 0
    INSTAGRAM = 1
    WEB = 2

    LLEGO_CHOICES = (
        (AMIGO, 'Amigo'),
        (INSTAGRAM, 'Instagram'),
        (WEB, 'Web'),
    )

    TIENDA = 3
    PUESTO_CARRETA = 4
    RESTAURANTE = 5
    OTRO = 6

    TIPO_CHOICES = (
        (TIENDA, 'Tienda'),
        (PUESTO_CARRETA, 'Puesto/Carreta'),
        (RESTAURANTE, 'Restaurante'),
        (OTRO, 'Otro'),
    )

    YES = 7
    NO = 8
    MAYBE = 9

    INTERES_CHOICES = (
        (YES, 'Si'),
        (NO, 'No'),
        (MAYBE, 'Tal Vez'),
    )

    user = models.OneToOneField(User)
    barrio = models.CharField(max_length=50, blank=False)
    nombre_tienda = models.CharField(max_length=200)
    fecha_ingreso = models.DateField("Fecha de ingreso", default=datetime.date.today)
    # puntos_dolor = models.OneToOneField(Puntos_Dolor)
    como_llego = models.IntegerField("¿Cómo llegó a la empresa?", choices=LLEGO_CHOICES,
                                     default=WEB, validators=[MinValueValidator(0),
                                                              MaxValueValidator(2)])
    ruta = models.ForeignKey(Ruta, default="1")
    tipo = models.IntegerField("Tipo de local:", choices=TIPO_CHOICES,
                               default=WEB, validators=[MinValueValidator(3),
                                                        MaxValueValidator(6)])
    interes = models.IntegerField("¿Está interesado en Agruppa?", choices=INTERES_CHOICES,
                                  default=WEB, validators=[MinValueValidator(7),
                                                           MaxValueValidator(9)])
    direccion = models.ForeignKey(Direccion, null=True)
    usuario_registrador = models.ForeignKey(User, related_name='%(class)s_usuario_registrador', null=True)
    smartphone = models.BooleanField("¿Tiene un teléfono inteligente?", default=True)
    comentarios = models.TextField("Agregue algún comentario", max_length=200, default="")

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " Nombre de barrio: " + self.barrio


class Transportador(models.Model):
    user = models.OneToOneField(User)
    ruta = models.ForeignKey(Ruta, default="1")

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " " + self.ruta.nombre


class JefeBodega(models.Model):
    user = models.OneToOneField(User)
    bodega = models.CharField("Nombre de bodega", max_length=100, blank=False)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " " + self.bodega


class Administrador(models.Model):
    user = models.OneToOneField(User)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class TeleVentas(models.Model):
    user = models.OneToOneField(User)
    puesto = models.CharField(max_length=50)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " " + self.puesto
