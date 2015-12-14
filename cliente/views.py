# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from django.views.generic import TemplateView
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

import servicio

from django.core import serializers
from django.http import HttpResponse
import suds
import json
import time
import datetime
from util import *

import mandrill

from decimal import Decimal


def PaginaInicio(request):
    titulo = "Inicio"
    if 'cliente' in request.session and request.session['cliente'] is not None:
        logeado = True
        cliente = request.session['cliente']
        nombre = cliente["nombres"]
    else:
        logeado = False

    return render_to_response('cliente/inicio.html', locals(), context_instance=RequestContext(request))


class Logear(TemplateView):
    def post(self, request, *args, **kwargs):
        logeado = False
        email = request.POST['user-email']
        password = request.POST['user-password']
        webService = suds.client.Client(servicio.URL_CLIENTE_WS)

        respuesta = webService.service.logear(email, password)

        if respuesta != 'null':
            data = json.loads(respuesta)
            request.session['cliente'] = data
            logeado = True
        response = json.dumps({'logeado': logeado})
        return HttpResponse(response, content_type="application/json")


def Salir(request):
    del request.session['cliente']
    return HttpResponseRedirect('/')


class RegistrarCliente(TemplateView):
    def post(self, request, *args, **kwargs):
        logeado = False

        dni = request.POST['user-dni']
        nombres = request.POST['user-nombres']
        apellidoPaterno = request.POST['user-apellidoPaterno']
        apellidoMaterno = request.POST['user-apellidoMaterno']
        celular = request.POST['user-celular']
        email = request.POST['user-email']
        password = request.POST['user-password']

        cliente = {"dni": dni, "nombres": nombres, "apellidoPaterno": apellidoPaterno,
                   "apellidoMaterno": apellidoMaterno, "celular": celular, "email": email, "password": password}

        webService = suds.client.Client(servicio.URL_CLIENTE_WS)

        data = json.dumps(cliente)

        respuesta = webService.service.registrar(data)

        if respuesta is not None and int(respuesta) > 0:
            data = json.loads(respuesta)
            request.session['cliente'] = cliente
            logeado = True
        response = json.dumps({'logeado': logeado})

        try:
            send_mail('Sistemas Distribuidos - Registro Nuevo Cliente', [cliente["email"]],
                      context={'nombre': cliente["nombres"]})
        except:
            print 'falló envio de correo'
            raise

        return HttpResponse(response, content_type="application/json")


class ActualizarCliente(TemplateView):
    def post(self, request, *args, **kwargs):

        webService = suds.client.Client(servicio.URL_CLIENTE_WS)
        cliente = request.session['cliente']
        respuesta = webService.service.buscar(cliente["dni"])
        cliente = json.loads(respuesta)

        dni = request.POST['user-dni']
        nombres = request.POST['user-nombres']
        apellidoPaterno = request.POST['user-apellidoPaterno']
        apellidoMaterno = request.POST['user-apellidoMaterno']
        celular = request.POST['user-celular']
        email = request.POST['user-email']
        password = request.POST['user-password']

        if len(password) > 0:
            cliente = {"idCliente": cliente["idCliente"], "dni": dni, "nombres": nombres,
                       "apellidoPaterno": apellidoPaterno,
                       "apellidoMaterno": apellidoMaterno, "celular": celular, "email": email, "password": password}
        else:
            cliente = {"idCliente": cliente["idCliente"], "dni": dni, "nombres": nombres,
                       "apellidoPaterno": apellidoPaterno,
                       "apellidoMaterno": apellidoMaterno, "celular": celular, "email": email, "password": "1234"}

        webService = suds.client.Client(servicio.URL_CLIENTE_WS)
        respuesta = webService.service.actualizar(json.dumps(cliente))

        if respuesta is not None and int(respuesta) > 0:
            data = json.loads(respuesta)
            request.session['cliente'] = cliente
        response = json.dumps({'resultado': data})
        return HttpResponse(response, content_type="application/json")


def PaginaCartelera(request, idCiudad, idComplejo, fecha):
    titulo = "Cartelera"
    if 'cliente' in request.session and request.session['cliente'] is not None:
        logeado = True
        cliente = request.session['cliente']
        nombre = cliente["nombres"]
    else:
        logeado = False

    # Ciudades
    webService = suds.client.Client(servicio.URL_CIUDAD_WS)
    ciudades = json.loads(webService.service.listar())

    if int(idCiudad) == 0:
        idCiudad = str(ciudades[0]["idCiudad"])

    request.session['idCiudad'] = idCiudad

    # Complejos de la primera ciudad
    complejos = Complejos(idCiudad)

    if int(idComplejo) == 0:
        idComplejo = complejos[0]["idComplejo"]

    if fecha != "01/01/2000":
        f = time.strptime(fecha, "%d/%m/%Y")
        fechaServicio = fechaServicio = str(f[0]) + "-" + str(f[1]) + "-" + str(f[2])
    else:
        fecha = time.strftime("%d/%m/%Y")
        fechaServicio = time.strftime("%y-%m-%d")

    # Cartelera por defecto
    cartelera = Cartelera(idComplejo, fechaServicio)
    print cartelera
    return render_to_response('cliente/cartelera.html', locals(), context_instance=RequestContext(request))


def ComplejosPorCiudad(request):
    idCiudad = request.GET['idCiudad']
    complejos = Complejos(idCiudad)
    response = json.dumps({'complejos': complejos})

    return HttpResponse(response, content_type="application/json")


def PaginaButacas(request, fecha, idSala, hora, idCartelera):
    titulo = "Butacas"
    if 'cliente' in request.session and request.session['cliente'] is not None:
        logeado = True
        cliente = request.session['cliente']
        nombre = cliente["nombres"]
    else:
        logeado = False
    request.session['fechaNormal'] = fecha
    fecha = time.strptime(fecha, "%d/%m/%Y")

    fecha = str(fecha[0]) + '-' + str(fecha[1]) + '-' + str(fecha[2])
    request.session['fechaBD'] = fecha
    idSala = int(idSala)

    request.session['idCartelera'] = idCartelera

    request.session['hora'] = hora

    ocupados = ButacasOcupadas(fecha, idSala, hora)

    ListaA = tuple('A' + str(i) for i in range(2, 18))

    ListaB = tuple('B' + str(i) for i in range(1, 19))
    ListaC = tuple('C' + str(i) for i in range(1, 19))
    ListaD = tuple('D' + str(i) for i in range(1, 19))
    ListaE = tuple('E' + str(i) for i in range(1, 19))
    ListaF = tuple('F' + str(i) for i in range(1, 19))
    ListaG = tuple('G' + str(i) for i in range(1, 19))

    ListaI = tuple('I' + str(i) for i in range(3, 17))

    ListaJ = tuple('J' + str(i) for i in range(5, 15))
    ListaK = tuple('K' + str(i) for i in range(5, 15))

    ListaL = tuple('L' + str(i) for i in range(6, 14))

    return render_to_response('cliente/butacas.html', locals(), context_instance=RequestContext(request))


def PaginaReservacion(request, butacas, tickets, total):
    titulo = "Reservacion"
    if 'cliente' in request.session and request.session['cliente'] is not None:
        logeado = True
        cliente = request.session['cliente']
        nombre = cliente["nombres"]
    else:
        logeado = False

    asientos = json.loads(butacas)

    request.session['tickets'] = tickets
    request.session['total'] = total

    return render_to_response('cliente/reservacion.html', locals(), context_instance=RequestContext(request))


def PaginaConfirmacion(request, butacas, email):
    titulo = "Confirmación"
    if 'cliente' in request.session and request.session['cliente'] is not None:
        logeado = True
        cliente = request.session['cliente']
        nombre = cliente["nombres"]
    else:
        logeado = False
    idCartelera = request.session['idCartelera']
    idCliente = str(cliente['idCliente'])
    fecha = request.session['fechaBD']
    asientos = json.loads(butacas)

    butacas = '"reservabutacas":' + butacas
    cadena = '{"idCartelera":' + idCartelera + ',"fechaReserva":"' + fecha + '","idCliente":' + \
             idCliente + ',"estado":"Vigente",' + butacas + '}'

    reserva = ReservarButacas(cadena)

    fecha = request.session['fechaNormal']

    idCartelera = request.session['idCartelera']
    idCiudad = request.session['idCiudad']

    hora = request.session['hora']

    tickets = request.session['tickets']
    total = request.session['total']

    cartelera = BuscarCartelera(idCartelera)
    sala = cartelera["sala"]
    # ciudad=BuscarCiudad(idCiudad)
    complejo = sala["complejo"]
    pelicula = cartelera["pelicula"]

    try:
        cad=''
        for a in asientos:
            cad+=a["butaca"]+"/"

        send_mail('Sistemas Distribuidos - Registro Reserva',
                  [cliente["email"]],
                  context={'nombre': cliente["nombres"],
                           'pelicula': pelicula["nombre"],
                           #'ciudad': ciudad.nombre,
                           'ciudad': 'ciudad',
                           'complejo': complejo["nombre"],
                           'fecha': fecha,
                           'hora': hora,
                           'sala': sala["idSala"],
                           'butacas': cad,
                           'numero': reserva["numeroTicket"]})
    except:
        print 'falló envio correo de reserva'
        raise

    del request.session['idCartelera']
    del request.session['idCiudad']
    del request.session['fechaNormal']
    del request.session['fechaBD']
    del request.session['hora']
    del request.session['tickets']
    del request.session['total']

    return render_to_response('cliente/confirmacion.html', locals(), context_instance=RequestContext(request))


def PaginaProfile(request):
    titulo = "Perfil"
    if 'cliente' in request.session and request.session['cliente'] is not None:
        logeado = True
        cliente = request.session['cliente']
        nombre = cliente["nombres"]
        return render_to_response('cliente/profile.html', locals(), context_instance=RequestContext(request))
    else:
        logeado = False
        return PaginaInicio(request)


def PaginaHistorial(request):
    titulo = "Historial"
    if 'cliente' in request.session and request.session['cliente'] is not None:
        logeado = True
        cliente = request.session['cliente']
        nombre = cliente["nombres"]

        historial = HisorialReservas(cliente["idCliente"])
        reservaciones=[]
        for h in historial:
            reserva=BuscarReserva(h["idReserva"])

            total=0
            for b in reserva["reservabutacas"]:
                total+=int(b["precio"])
            reserva["total"]=total
            reservaciones.append(reserva)

        return render_to_response('cliente/historial.html', locals(), context_instance=RequestContext(request))
    else:
        logeado = False
        return PaginaInicio(request)