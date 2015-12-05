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

import mandrill

from decimal import Decimal

def index(request):
    titulo = "Inicio"
    if 'cliente' in request.session and request.session['cliente'] is not None:
        logeado=True
        cliente = request.session['cliente']
        nombre = cliente["nombres"]
    else:
        logeado=False

    return render_to_response('cliente/inicio.html', locals(), context_instance=RequestContext(request))


class Logear(TemplateView):
    def post(self, request, *args, **kwargs):
        logeado=False
        email = request.POST['user-email']
        password = request.POST['user-password']
        webService = suds.client.Client(servicio.URL_CLIENTE_WS)

        respuesta = webService.service.logear(email, password)
        
        if respuesta!='null':
            data=json.loads(respuesta)
            request.session['cliente'] = data
            logeado=True
        response = json.dumps({'logeado':logeado})
        return HttpResponse(response, content_type="application/json")

def Salir(request):
    del request.session['cliente']
    return HttpResponseRedirect('/')
        
    

class RegistrarCliente(TemplateView):
    def post(self, request, *args, **kwargs):
        logeado=False
        
        dni = request.POST['user-dni']
        nombres= request.POST['user-nombres']
        apellidoPaterno= request.POST['user-apellidoPaterno']
        apellidoMaterno= request.POST['user-apellidoMaterno']
        celular= request.POST['user-celular']
        email = request.POST['user-email']
        password = request.POST['user-password']
        
        cliente = {"dni":dni, "nombres":nombres, "apellidoPaterno":apellidoPaterno, 
        "apellidoMaterno":apellidoMaterno, "celular":celular, "email":email, "password":password  }
        
        webService = suds.client.Client(servicio.URL_CLIENTE_WS)

        data = json.dumps(cliente)

        respuesta = webService.service.registrar(data)
        
        if respuesta is not None and int(respuesta)>0:
            data=json.loads(respuesta)
            request.session['cliente'] = cliente
            logeado=True
        response = json.dumps({'logeado':logeado})
        return HttpResponse(response, content_type="application/json")
        

def Cartelera(request):
    titulo = "Cartelera"
    if 'cliente' in request.session and request.session['cliente'] is not None:
        logeado=True
        cliente = request.session['cliente']
        nombre = cliente["nombres"]
    else:
        logeado=False
        
    webService = suds.client.Client(servicio.URL_CIUDAD_WS)
    ciudades=json.loads(webService.service.listar())

    

    return render_to_response('cliente/cartelera.html', locals(), context_instance=RequestContext(request))
    
def ComplejosPorCiudad(request):
    idCiudad= request.GET['idCiudad']
    fecha = request.GET['fecha']
    
    webService = suds.client.Client(servicio.URL_COMPLEJO_WS)

    respuesta = str(webService.service.listarPorCiudad(idCiudad))
    print respuesta
    print type(respuesta)
    
    repuesta = respuesta.replace("idComplejo","key")
    repuesta = respuesta.replace("nombre","value")
    print respuesta
    complejos=json.loads(respuesta)
        
    response = json.dumps({'complejos':complejos})
    return HttpResponse(response, content_type="application/json")